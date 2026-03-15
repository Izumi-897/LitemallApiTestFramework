import pytest
import json
from api.goods import GoodsApi

def get_search_data():
    """
    加载搜索模块测试数据集 (DDT)
    :return: list, 包含关键词、预期业务码及预期结果类型的参数化数据
    """
    with open("data/search_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

class TestSearch:
    """
    商品检索业务逻辑测试套件
    覆盖：关键词精准检索、模糊匹配召回及空结果响应校验
    """
    def setup_class(self):
        """测试环境预置：初始化商品接口对象"""
        self.goods_api = GoodsApi()

    @pytest.mark.parametrize("keyword, expected_errno, expected_type, desc", get_search_data())
    def test_search_logic(self, keyword, expected_errno, expected_type, desc):
        """
        验证搜索接口的检索逻辑与数据一致性
        验证点：1. 接口协议契约；2. 业务响应码；3. 检索结果相关性（召回率）
        """
        # Step 1: 调用搜索接口并解析响应报文
        res = self.goods_api.search(keyword)
        res_json = res.json()

        # Step 2: 响应契率校验 (Protocol & Business layer)
        assert res.status_code == 200, "HTTP 状态码契约校验失败"
        assert res_json["errno"] == expected_errno, f"【{desc}】业务逻辑错误码不匹配"

        # Step 3: 数据检索一致性与召回质量校验
        data = res_json.get("data", {})
        total = data.get("total", 0)
        goods_list = data.get("list", [])

        if expected_type == "has_data":
            # 校验检索命中场景：确保总数统计与列表数据的一致性
            assert total > 0, f"【{desc}】数据召回异常：预期有结果但 total 为 0"
            assert len(goods_list) > 0, f"【{desc}】结果集异常：商品列表为空"

            # 校验搜索结果相关性 (Fuzzy Match Relevancy)
            if "毛巾" in keyword:
                first_name = goods_list[0].get("name", "")
                assert "毛巾" in first_name, f"检索相关性校验失败：首位商品名称 {first_name} 未命中核心关键词"

        elif expected_type == "no_data":
            # 校验零结果检索场景：确保响应数据为空
            assert total == 0, f"【{desc}】逻辑异常：预期无结果但返回总数为 {total}"
            assert len(goods_list) == 0