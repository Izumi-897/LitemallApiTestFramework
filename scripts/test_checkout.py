import pytest
import json
from api.checkout import CheckoutApi
from api.cart import CartApi
from api.login import LoginApi

def get_checkout_data():
    """
    加载订单结算模块测试数据集
    :return: list, 测试参数化数据
    """
    with open("data/checkout_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

class TestCheckout:
    """
    订单结算模块业务逻辑测试套件
    重点验证下单链路中的金额核算逻辑，包括运费分摊、实付金额计算的准确性
    """
    def setup_class(self):
        """测试环境预置：初始化 API 实例并获取 Session 鉴权凭证"""
        self.checkout_api = CheckoutApi()
        self.cart_api = CartApi()
        self.login_api = LoginApi()
        res = self.login_api.login("user123", "user123")
        self.token = res.json()["data"]["token"]

    @pytest.mark.parametrize("goodsId, number, productId, exp_errno, exp_freight, exp_actual, desc",
                             get_checkout_data())
    def test_checkout_price_logic(self, goodsId, number, productId, exp_errno, exp_freight, exp_actual, desc):
        """
        验证结算页面的金额计算逻辑
        校验点：1. 接口连通性；2. 运费策略触发；3. 应付总额核算一致性
        """
        # Step 1: 环境净化，清除购物车存量数据以确保测试环境隔离
        self.cart_api.clear_cart(self.token)

        # Step 2: 构造业务场景，添加指定商品至购物车
        self.cart_api.add_cart(goodsId, number, productId, self.token)

        # Step 3: 调用结算确认接口获取核算详情
        res = self.checkout_api.checkout(self.token)
        res_json = res.json()

        # Step 4: 基础契约断言 (Business errno)
        assert res_json["errno"] == exp_errno, f"【{desc}】接口业务响应异常: {res_json}"

        # Step 5: 金额计算逻辑一致性校验
        if exp_errno == 0:
            data = res_json.get("data", {})
            actual_price = data.get("actualPrice")
            freight_price = data.get("freightPrice")

            print(f"\n[TestCase: {desc}] Expected Actual: {exp_actual} | Server Actual: {actual_price}")

            # 验证系统运费计算是否符合业务预期
            assert float(freight_price) == float(exp_freight), f"【{desc}】运费核算不匹配"

            # 验证实付总额（商品总价 + 运费 - 优惠）是否与预期基线一致
            assert float(actual_price) == float(exp_actual), f"【{desc}】实付金额核算异常，请核对商品单价基线"