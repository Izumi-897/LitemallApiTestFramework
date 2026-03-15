import requests

class CartApi:
    """
    购物车模块接口封装
    包含：添加购物车、获取列表、批量删除及清空操作
    """

    def __init__(self):
        self.url_add = "http://127.0.0.1:8080/wx/cart/add"
        self.url_index = "http://127.0.0.1:8080/wx/cart/index"

    def add_cart(self, goodsId, number, productId, token):
        """
        向购物车添加商品
        :param goodsId: 商品SPU ID
        :param number: 购买数量
        :param productId: 规格SKU ID
        :param token: 用户授权Token
        :return: requests.Response
        """
        headers = {"X-Litemall-Token": token}
        payload = {
            "goodsId": goodsId,
            "number": number,
            "productId": productId
        }
        return requests.post(self.url_add, json=payload, headers=headers)

    def get_cart_index(self, token):
        """
        获取当前购物车索引列表详情
        :param token: 用户授权Token
        :return: requests.Response
        """
        headers = {"X-Litemall-Token": token}
        return requests.get(self.url_index, headers=headers)

    def delete(self, productIds, token):
        """
        批量删除购物车中的指定商品
        :param productIds: list, 产品规格ID数组
        :param token: 用户授权Token
        :return: requests.Response
        """
        headers = {"X-Litemall-Token": token}
        payload = {"productIds": productIds}
        return requests.post("http://127.0.0.1:8080/wx/cart/delete", json=payload, headers=headers)

    def clear_cart(self, token):
        """
        清理类前置/后置操作：清空当前用户购物车
        步骤：
        1. 获取当前购物车全量数据
        2. 提取数据中所有商品的 productId
        3. 调用批量删除接口实现物理清空
        """
        res = self.get_cart_index(token).json()
        if res["errno"] == 0 and res["data"]:
            cart_list = res["data"]["cartList"]
            if cart_list:
                # 批量提取待删除的产品ID集合
                p_ids = [item["productId"] for item in cart_list]
                self.delete(p_ids, token)