import pytest
import requests
from api.login import LoginApi
from common.db_util import DBUtil


@pytest.fixture(scope="session")
def login_token():
    """
    Session级全域认证Fixture
    执行全局登录并提取 Token，供后续业务模块调用
    :return: str, 授权令牌
    """
    login_api = LoginApi()
    res = login_api.login("user123", "user123")
    token = res.json().get("data", {}).get("token")

    # 异常分支处理：若鉴权失败则阻断后续测试链路
    if not token:
        pytest.fail("Session 鉴权异常：无法获取有效授权 Token")
    return token


@pytest.fixture
def clean_cart():
    """
    购物车模块数据清洗（Post-test Cleanup）
    用于测试结束后的数据回滚，确保测试环境的幂等性
    """
    yield
    db = DBUtil()
    # 业务逻辑：根据 user123 对应的固定 UID (1) 物理删除购物车存量数据
    db.execute("DELETE FROM litemall_cart WHERE user_id = 1")
    db.close()


@pytest.fixture
def clean_address():
    """
    地址库模块数据清洗（Post-test Cleanup）
    通过匹配测试特征值，批量清理自动化测试产生的冗余地址记录
    """
    yield
    db = DBUtil()
    # 业务逻辑：清理以 "测" 为前缀的所有模拟收货地址
    db.execute("DELETE FROM litemall_address WHERE name LIKE '测%'")
    db.close()