import pytest
from api.login import LoginApi
from common.utils import read_json_data

class TestLogin:
    """
    用户身份认证模块测试套件
    覆盖：合法/非法账户登录校验、业务错误码一致性验证
    """

    def setup_class(self):
        """测试环境预置：初始化认证模块接口对象"""
        self.login_api = LoginApi()

    @pytest.mark.parametrize("username, password, expect_errno, desc", read_json_data("login_data.json"))
    def test_login(self, username, password, expect_errno, desc):
        """
        用户登录接口参数化测试 (DDT)
        校验点：1. HTTP 响应状态码；2. 业务逻辑错误码 (errno)
        """
        print(f"\n[TestCase] 执行场景: {desc}")

        # Step 1: 构造认证载荷并提交登录请求
        response = self.login_api.login(username, password)
        res_json = response.json()

        # Step 2: 响应结果多维校验
        # 验证接口契约（HTTP 200 OK）
        assert response.status_code == 200, f"HTTP状态码契约校验失败，实际返回: {response.status_code}"
        # 验证业务逻辑错误码是否符合预期基线
        assert res_json["errno"] == expect_errno, f"业务逻辑校验失败，预期: {expect_errno}, 实际: {res_json['errno']}"