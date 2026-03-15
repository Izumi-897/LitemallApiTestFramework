import requests

class CheckoutApi:
    """
    订单结算模块接口
    用于获取下单前的核算信息，包括商品总额、运费计算、优惠券抵扣及最终实付金额。
    """

    def __init__(self):
        self.url = "http://127.0.0.1:8080/wx/cart/checkout"

    def checkout(self, token, cartId=0, addressId=0, couponId=0, userCouponId=0):
        """
        获取下单确认信息
        :param token: str, 用户授权凭证
        :param cartId: int, 购物车ID (默认为0，表示结算当前所有勾选商品)
        :param addressId: int, 收货地址ID (默认为0，表示系统自动选择默认地址)
        :param couponId: int, 优惠券ID
        :param userCouponId: int, 用户优惠券关联ID
        :return: requests.Response
        """
        headers = {"X-Litemall-Token": token}
        params = {
            "cartId": cartId,
            "addressId": addressId,
            "couponId": couponId,
            "userCouponId": userCouponId
        }
        return requests.get(self.url, params=params, headers=headers)