'''
    统一登陆界面

'''
from common import basePage
from selenium import webdriver


class LoginPage(basePage.BasePage):

    '''统一登录网址'''
    url="http://192.168.23.153/"

    '''
        crm系统相关元素
    '''
    crm_button=('xpath','/html/body/div[10]/div[2]/div[3]/ul/li[1]')
    crm_username=('id',"username")
    crm_password=('id','password')
    crm_login_button=('xpath','//*[@id="login-zhanghao"]/div[6]/button')

    '''
        crm系统相关组件
    '''
    def crm_login(self,username="1000000",password="dj123456"):
        '''登陆CRM系统，账号：1000000，密码：dj123456'''
        self.get(self.url)
        self.click(self.crm_button)
        self.sendKeys(self.crm_username,text=username)
        self.sendKeys(self.crm_password,text=password)
        self.click(self.crm_login_button)



if __name__ == '__main__':

    driver=webdriver.Chrome()
    login_page=LoginPage(driver)
    login_page.crm_login()


