import requests

class LoginApi:
    """
    身份认证模块接口对象
    负责处理用户注册、登录授权等核心认证流程
    """
    def __init__(self):
        self.base_url = "http://127.0.0.1:8080/wx/auth"
        self.login_url = f"{self.base_url}/login"
        self.register_url = f"{self.base_url}/register"

    def register(self, username, password, mobile):
        """
        新用户注册接口
        :param username: 注册用户名
        :param password: 注册密码
        :param mobile: 绑定手机号
        :return: requests.Response
        """
        # 封装注册业务载荷，code 为 Mock 或固定环境验证码
        payload = {
            "username": username,
            "password": password,
            "mobile": mobile,
            "code": "123456"
        }
        return requests.post(self.register_url, json=payload)

    def login(self, username, password):
        """
        用户登录验证接口
        :param username: 用户名
        :param password: 密码
        :return: requests.Response (包含返回的 X-Litemall-Token)
        """
        payload = {
            "username": username,
            "password": password
        }
        return requests.post(self.login_url, json=payload)

# 导出 Login 别名以维持框架调用兼容性
Login = LoginApi