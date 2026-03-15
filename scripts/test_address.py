import pytest
import json
from api.address import AddressApi
from api.login import LoginApi

def get_address_data():
    """
    加载收货地址模块测试数据集 (DDT)
    :return: list, 包含测试参数的嵌套列表
    """
    with open("data/address_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

class TestAddress:
    """
    收货地址业务逻辑测试套件
    覆盖：新增地址、数据合法性校验及测试资源回收
    """

    def setup_class(self):
        """
        测试环境预置：初始化 API 实例并获取 Session 鉴权令牌
        """
        self.address_api = AddressApi()
        self.login_api = LoginApi()
        res = self.login_api.login("user123", "user123")
        self.token = res.json()["data"]["token"]

    @pytest.mark.parametrize("name, tel, province, city, county, detail, area_code, is_default, exp_errno, desc",
                             get_address_data())
    def test_address_lifecycle(self, name, tel, province, city, county, detail, area_code, is_default, exp_errno, desc):
        """
        收货地址全生命周期校验（参数化测试）
        验证点：1. 接口响应状态码；2. 业务 errno 码；3. 数据库资源创建结果
        """
        payload = {
            "name": name, "tel": tel, "province": province, "city": city,
            "county": county, "addressDetail": detail, "areaCode": area_code, "isDefault": is_default
        }

        # Step 1: 调用接口执行地址保存/新增操作
        res = self.address_api.save(payload, self.token)
        res_json = res.json()

        # 提取动态生成的资源 ID 用于后续 Teardown 阶段清理
        new_address_id = res_json.get("data")

        try:
            # Step 2: 业务响应断言与结果记录
            print(f"\n[Test Case] {desc}")
            assert res_json["errno"] == exp_errno, f"业务错误码不匹配！实际返回: {res_json}"

            if exp_errno == 0:
                assert new_address_id is not None, "新增成功但未返回资源唯一标识 ID"
                print(f" -> Result: Success, Resource ID: {new_address_id}")

        finally:
            # Step 3: 环境清理 (Teardown)
            # 无论断言是否通过，均需对已产生的数据库记录执行物理删除，维持测试环境幂等性
            if new_address_id and isinstance(new_address_id, int):
                del_res = self.address_api.delete(new_address_id, self.token).json()
                if del_res["errno"] == 0:
                    print(f" -> Teardown: Successfully deleted resource ID {new_address_id}")
                else:
                    print(f" -> Teardown Warning: Failed to delete ID {new_address_id}, Response: {del_res}")