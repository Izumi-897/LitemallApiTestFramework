import pytest
import os

if __name__ == '__main__':
    # 运行 scripts 目录下所有用例，并生成 allure 原始数据
    pytest.main(['-s', '-v', 'scripts/', '--alluredir', './report/allure-results'])

    os.system("allure generate ./report/allure-results -o ./report/html --clean")