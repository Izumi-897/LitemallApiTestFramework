import pytest
import json
import time
import random
from api.login import LoginApi


def get_register_data():
    """
    加载用户注册模块测试数据集 (DDT)
    :return: list, 包含注册参数与预期结果的列表
    """
    with open("data/register_data.json", "r", encoding="utf-8") as f:
        return json.load(f)


class TestRegister:
    """
    用户注册模块业务逻辑测试套件
    验证新用户创建流程及账号唯一性约束校验
    """

    def setup_class(self):
        """测试环境预置：初始化认证模块对象"""
        self.login_api = LoginApi()

    @pytest.mark.parametrize("username, password, mobile, code, expected_errno, desc", get_register_data())
    def test_register(self, username, password, mobile, code, expected_errno, desc):
        """
        验证用户注册接口在不同输入组合下的业务行为
        校验点：1. 动态凭证生成的合法性；2. 业务状态码 (errno) 契约校验
        """

        # Step 1: 动态构造唯一性测试数据，规避数据库唯一键冲突
        if mobile == "NEW_MOBILE":
            unique_suffix = str(int(time.time()))[-6:]
            mobile = f"138{unique_suffix}{random.randint(10, 99)}"
            username = f"user_{unique_suffix}"

        # Step 2: 提交注册请求并获取业务响应
        res = self.login_api.register(username, password, mobile)
        res_json = res.json()

        print(f"\n[TestCase: {desc}] Response: {res_json}")

        # Step 3: 执行业务状态码断言
        assert res_json["errno"] == expected_errno, f"用例【{desc}】业务校验失败，实际返回: {res_json}"