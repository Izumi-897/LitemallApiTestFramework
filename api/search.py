import requests
from config import BASE_URL

class SearchApi:
    """
    商品检索模块接口对象
    封装商品搜索相关的 API 调用逻辑
    """

    def __init__(self):
        self.url = f"{BASE_URL}/goods/list"

    def search(self, keyword):
        """
        根据指定的关键词执行商品检索
        :param keyword: str, 搜索关键字
        :return: requests.Response
        """
        params = {"keyword": keyword}
        return requests.get(self.url, params=params)