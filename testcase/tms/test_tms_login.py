import pytest
from pages.index import loginPage
from selenium import webdriver
import allure


class TestLogin():

    def setup_class(self):
        '''用例执行前，启动浏览器，创建chrome实例'''
        driver=webdriver.Chrome()
        self.login_page=loginPage.LoginPage(driver)


    def teardown_class(self):
        '''用例执行完毕，关闭浏览器'''
        self.login_page.quit()


    def test_login_001(self):
        self.login_page.crm_login()


    def test_login_002(self):
        self.login_page.crm_login(username="200",password="123456")

if __name__ == '__main__':
    pytest.main(['-s','test_login.py'])

    