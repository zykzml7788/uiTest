import pytest
from pages.index import loginPage
from selenium import webdriver
from allure import MASTER_HELPER




@MASTER_HELPER.feature("CRM登陆")
class TestLogin():

    @MASTER_HELPER.step("初始化启动浏览器")
    def setup_class(self):
        '''用例执行前，启动浏览器，创建chrome实例'''
        driver=webdriver.Chrome()
        self.login_page=loginPage.LoginPage(driver)

    @MASTER_HELPER.step("关闭浏览器")
    def teardown_class(self):
        '''用例执行完毕，关闭浏览器'''
        self.login_page.quit()

    @MASTER_HELPER.testcase("用例名：登陆CRM——正常场景")
    def test_login_001(self):
        with MASTER_HELPER.step("登陆CRM"):
            self.login_page.crm_login()



    @MASTER_HELPER.testcase("用例名：登陆CRM——账号错误")
    def test_login_002(self):
        self.login_page.crm_login(username="200",password="123456")
        self.login_page.get_screen()

if __name__ == '__main__':
    pytest.main(['-s','test_login.py'])

    