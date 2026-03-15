import requests

class AddressApi:
    """
    收货地址模块接口对象
    封装地址的新增、修改、查询与删除接口
    """

    def __init__(self):
        self.base_url = "http://127.0.0.1:8080/wx/address"

    def save(self, data, token):
        """
        添加或更新收货地址
        :param data: dict, 地址信息详情
        :param token: str, 用户授权凭证
        :return: requests.Response
        """
        headers = {"X-Litemall-Token": token}
        return requests.post(f"{self.base_url}/save", json=data, headers=headers)

    def get_list(self, token):
        """
        获取当前用户的收货地址列表
        :param token: str, 用户授权凭证
        :return: requests.Response
        """
        headers = {"X-Litemall-Token": token}
        return requests.get(f"{self.base_url}/list", headers=headers)

    def delete(self, address_id, token):
        """
        根据地址ID删除指定收货地址
        :param address_id: int/str, 地址唯一标识
        :param token: str, 用户授权凭证
        :return: requests.Response
        """
        headers = {"X-Litemall-Token": token}
        payload = {"id": address_id}
        return requests.post(f"{self.base_url}/delete", json=payload, headers=headers)