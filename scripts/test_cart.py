import pytest
import json
from api.cart import CartApi
from api.login import LoginApi

def get_cart_data():
    """
    数据驱动：加载购物车模块测试数据集
    :return: list, 包含商品ID、数量、规格ID及预期结果的参数列表
    """
    with open("data/cart_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

class TestCart:
    """
    购物车模块业务逻辑测试套件
    覆盖：添加购物车接口幂等性、商品数量累加逻辑验证
    """

    def setup_class(self):
        """
        测试环境初始化：实例化 API 对象并获取 Session 级别授权令牌
        """
        self.cart_api = CartApi()
        self.login_api = LoginApi()

        # 执行前置登录以获取后续接口所需的鉴权凭证
        login_res = self.login_api.login("user123", "user123")
        login_data = login_res.json()

        if login_data["errno"] == 0:
            self.token = login_data["data"]["token"]
        else:
            pytest.fail(f"前置登录失败，阻断测试链路。账号信息: user123, 响应详情: {login_data}")

    @pytest.mark.parametrize("goodsId, number, productId, expected_errno, desc", get_cart_data())
    def test_add_cart(self, goodsId, number, productId, expected_errno, desc):
        """
        验证添加购物车接口的业务逻辑一致性
        验证点：1. 接口响应状态码；2. 成功加购后购物车内商品数量的数学累加关系
        """

        # Step 1: 获取加购前的商品基线数量 (仅针对预期成功的用例)
        old_total_number = 0
        if expected_errno == 0:
            index_res = self.cart_api.get_cart_index(self.token).json()
            cart_list = index_res.get("data", {}).get("cartList", [])
            if cart_list:
                for item in cart_list:
                    if item["productId"] == productId:
                        old_total_number = item["number"]
                        break

        # Step 2: 提交加购请求
        res = self.cart_api.add_cart(goodsId, number, productId, self.token)
        res_json = res.json()
        print(f"\n[TestCase] {desc} | Response: {res_json}")

        # Step 3: 响应状态码 (errno) 契约校验
        assert res_json["errno"] == expected_errno, f"用例【{desc}】errno 校验失败！"

        # Step 4: 业务数据一致性验证 (验证商品数量累加逻辑)
        if expected_errno == 0:
            # 重新查询购物车列表并检索目标 SKU 数量
            new_index_res = self.cart_api.get_cart_index(self.token).json()
            new_cart_list = new_index_res.get("data", {}).get("cartList", [])

            new_total_number = 0
            if new_cart_list:
                for item in new_cart_list:
                    if item["productId"] == productId:
                        new_total_number = item["number"]
                        break

            # 验证加购后的总数是否严格等于预期（基线数量 + 新增数量）
            assert new_total_number == old_total_number + number, \
                f"【{desc}】数据一致性校验失败！预期总数: {old_total_number + number}, 实际总数: {new_total_number}"