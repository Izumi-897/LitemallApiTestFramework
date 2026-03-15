import requests

class GoodsApi:
    """
    商品模块接口对象
    提供商品检索、分类详情查询以及分类下商品列表获取功能
    """
    def __init__(self):
        self.base_url = "http://127.0.0.1:8080/wx/goods"
        self.list_url = f"{self.base_url}/list"
        self.category_url = f"{self.base_url}/category"

    def search(self, keyword):
        """
        根据关键字搜索商品
        :param keyword: str, 搜索关键词
        :return: requests.Response, 返回包含商品列表的分页数据
        """
        params = {
            "keyword": keyword,
            "page": 1,
            "limit": 10
        }
        return requests.get(self.list_url, params=params)

    def get_category(self, category_id):
        """
        获取指定分类的详情信息
        :param category_id: int/str, 商品类目ID
        :return: requests.Response
        """
        params = {"id": category_id}
        return requests.get(self.category_url, params=params)

    def get_goods_by_category(self, category_id):
        """
        按分类筛选商品列表
        :param category_id: int/str, 商品类目ID
        :return: requests.Response, 返回该分类下的分页商品数据
        """
        params = {
            "categoryId": category_id,
            "page": 1,
            "limit": 10
        }
        return requests.get(self.list_url, params=params)