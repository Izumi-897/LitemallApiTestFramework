import pytest
import json
import os
from api.goods import GoodsApi

def get_goods_data():
    """
    加载商品模块测试数据集
    采用绝对路径定位数据文件，以确保自动化任务在不同执行环境下路径的兼容性
    :return: list, 包含分类ID及预期结果的参数列表
    """
    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file_path))
    file_path = os.path.join(project_root, "data", "goods_data.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

class TestGoods:
    """
    商品模块业务逻辑测试套件
    覆盖：商品分类检索、类目详情数据准确性验证
    """
    def setup_class(self):
        """测试环境预置：初始化商品接口对象"""
        self.goods_api = GoodsApi()

    @pytest.mark.parametrize("category_id, exp_errno, exp_name, desc", get_goods_data())
    def test_get_category_details(self, category_id, exp_errno, exp_name, desc):
        """
        验证商品分类详情接口的数据一致性
        验证点：1. 业务响应状态码 (errno)；2. 分类主体名称 (Category Name)
        """
        # Step 1: 调用分类详情检索接口
        res = self.goods_api.get_category(category_id)
        res_json = res.json()

        # Step 2: 响应契约校验 - 验证业务状态码
        assert res_json["errno"] == exp_errno, f"【{desc}】业务状态码校验失败"

        # Step 3: 业务数据校验 - 验证分类名称的一致性
        if exp_errno == 0:
            # 提取返回数据集中当前分类的名称字段
            actual_name = res_json.get("data", {}).get("currentCategory", {}).get("name", "")
            print(f"\n[TestCase: {desc}] Expected: {exp_name} | Actual: {actual_name}")

            # 执行数据一致性断言
            assert actual_name == exp_name, f"【{desc}】分类名称匹配失败"