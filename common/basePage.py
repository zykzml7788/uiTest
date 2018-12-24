from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from common import logger
from allure import MASTER_HELPER
from allure.constants import *
import platform
import time
from common import readYaml


'''
定义基类
'''
class BasePage():

    '''基于原生的selenium做二次封装'''



    def __init__(self, driver):
        '''获取操作系统信息'''
        platform1=platform.platform()  # 获取操作系统名称及版本号，'Windows-7-6.1.7601-SP1'
        version=platform.version()  # 获取操作系统版本号，'6.1.7601'
        architecture=platform.architecture()  # 获取操作系统的位数，('32bit', 'WindowsPE')
        machine=platform.machine()  # 计算机类型，'x86'
        node=platform.node()  # 计算机的网络名称，'hongjie-PC'
        processor=platform.processor()  # 计算机处理器信息，'x86 Family 16 Model 6 Stepping 3, AuthenticAMD'
        uname=platform.uname()  # 包含上面所有的信息汇总，uname_result(system='Windows', node='hongjie-PC',
        MASTER_HELPER.environment(platform=platform1,version=version,architecture=architecture,machine=machine,node=node,processor=processor,uname=uname)

        '''设置轮循时间及超时时间'''
        self.logger = logger.Logger().getLogger()
        self.driver = driver
        self.timeout = 10
        self.t = 0.5

    def get(self,url=''):
        '''访问网址'''
        self.driver.get(url)
        self.logger.info("访问网址："+url)

    def quit(self):
        '''关闭浏览器'''
        self.driver.quit()
        self.logger.info("退出浏览器")

    def get_title(self):
        '''获取网页title'''
        self.logger.info("获取网页title："+self.driver.title)
        return self.driver.title

    def get_current_url(self):
        '''获取当前url'''
        self.logger.info("获取当前url:"+self.driver.current_url)
        return self.driver.current_url

    def findElement(self, locator):
        '''定位到元素，返回元素对象，没定位到，Timeout异常'''
        if not isinstance(locator, tuple):
            print('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        else:
            try:
                self.logger.info("正在定位元素信息：定位方式->%s, value值->%s" % (locator[0], locator[1]))
                ele = WebDriverWait(self.driver, self.timeout, self.t).until(EC.presence_of_element_located(locator))
                return ele
            except Exception as e:
                self.get_screen()
                raise Exception("定位元素超时，未定位到该元素")


    def findElements(self, locator):
        if not isinstance(locator, tuple):
            print('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        else:
            try:
                self.logger.info("正在定位元素信息：定位方式->%s, value值->%s"%(locator[0], locator[1]))
                eles = WebDriverWait(self.driver, self.timeout, self.t).until(EC.presence_of_all_elements_located(locator))
                return eles
            except Exception as e:
                self.get_screen()
                raise Exception("定位元素超时，未定位到该类元素")

    def sendKeys(self, locator, text=''):
        try:
            ele = self.findElement(locator)
            ele.send_keys(text)
            self.logger.info("元素:{},输入文本：{}".format(locator,text))
        except Exception as e:
            self.get_screen()
            raise Exception("元素：{}，输入异常！！".format(locator,text))

    def click(self, locator):
        try:
            ele = self.findElement(locator)
            ele.click()
            self.logger.info("点击元素:"+str(locator))
        except Exception:
            self.get_screen()
            raise Exception("点击元素{}失败".format(locator))

    def clear(self, locator):
        try:
            ele = self.findElement(locator)
            ele.clear()
        except Exception:
            self.get_screen()
            raise Exception("清除元素{}失败".format(locator))

    def isSelected(self, locator):
        """判断元素是否被选中，返回bool值"""
        ele = self.findElement(locator)
        r = ele.is_selected()
        return r

    def isElementExist(self, locator):
        self.logger.info("判断元素{}是否存在".format(locator))
        try:
            self.findElement(locator)
            self.logger.info("元素{}存在".format(locator))
            return True
        except:
            self.get_screen()
            self.logger.error("元素{}不存在".format(locator))
            return False

    def is_title(self, _title=''):
        '''返回bool值'''
        self.logger.info("判断标题是否为："+_title)
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_is(_title))
            self.logger.info("标题为："+_title)
            return result
        except:
            self.get_screen()
            self.logger.error("标题不是："+_title)
            return False

    def is_title_contains(self, _title=''):
        '''返回bool值'''
        self.logger.info("判断标题是否包含文本："+_title)
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_contains(_title))
            self.logger.info("标题包含："+_title)
            return result
        except:
            self.get_screen()
            self.logger.info("标题不包含："+_title)
            return False

    def is_text_in_element(self, locator, _text=''):
        '''返回bool值'''
        self.logger.info("判断元素文本是否为："+_text)
        if not isinstance(locator, tuple):
            print('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.text_to_be_present_in_element(locator, _text))
            self.logger.info("元素文本为："+_text)
            return result
        except:
            self.get_screen()
            self.logger.error("元素文本不为："+_text)
            return False

    def is_value_in_element(self, locator, _value=''):
        '''返回bool值, value为空字符串，返回Fasle'''
        self.logger.info("判断元素value值是否为："+_value)
        if not isinstance(locator, tuple):
            print('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        try:
            result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.text_to_be_present_in_element_value(locator, _value))
            self.logger.info("元素value值为："+_value)
            return result
        except:
            self.get_screen()
            self.logger.error("元素value值不为："+_value)
            return False

    def is_alert(self, timeout=3):
        '''判断alert,存在返回alert实例，不存在，返回false'''
        self.logger.info("判断是否存在alert，并返回alert实例")
        try:
            result = WebDriverWait(self.driver, timeout, self.t).until(EC.alert_is_present())
            self.logger.info("存在alert，返回实例："+result)
            return result
        except:
            self.get_screen()
            self.logger.error("不存在alert")
            return False

    def get_title(self):
        '''获取title'''
        return self.driver.title

    def get_text(self, locator):
        '''获取文本'''
        self.logger.info("元素：{}，获取文本".format(locator))
        try:
            t = self.findElement(locator).text
            self.logger.info("获取到文本："+t)
            return t
        except:
            self.get_screen()
            self.logger.error("获取text失败，返回空字符串 ")
            return ""

    def get_attribute(self, locator, name):
        '''获取属性'''
        self.logger.info("元素：{}，获取属性：{}" % locator,name)
        try:
            element = self.findElement(locator)
            atr=element.get_attribute(name)
            self.logger.info("获取到元素属性："+atr)
            return atr
        except:
            self.get_screen()
            self.logger.error("获取%s属性失败，返回'' "%name)
            return ""

    def js_focus_element(self, locator):
        '''聚焦元素'''
        self.logger.info("聚焦元素："+str(locator))
        try:
            target = self.findElement(locator)
            self.driver.execute_script("arguments[0].scrollIntoView();", target)
        except Exception:
            self.get_screen()
            raise Exception("聚焦元素{}失败".format(locator))

    def js_scroll_top(self):
        '''滚动到顶部'''
        self.logger.info("调用Js滚动到顶部")
        try:
            js = "window.scrollTo(0,0)"
            self.driver.execute_script(js)
            self.logger.info("滚动成功")
        except Exception:
            self.get_screen()
            raise Exception("滚动失败")

    def js_scroll_end(self,x=0):
        '''滚动到底部'''
        self.logger.info("调用Js滚动到底部")
        try:
            js = "window.scrollTo(%s,document.body.scrollHeight)"%x
            self.driver.execute_script(js)
            self.logger.info("滚动成功")
        except:
            self.get_screen()
            raise Exception("滚动失败")

    def select_by_index(self, locator, index=0):
        self.logger.info("根据下标：{},查找下拉选".format(index))
        '''通过索引,index是索引第几个，从0开始，默认选第一个'''
        try:
            element = self.findElement(locator)  # 定位select这一栏
            Select(element).select_by_index(index)
            self.logger.info("成功定位到select")
        except Exception:
            self.get_screen()
            raise Exception("定位select失败")

    def select_by_value(self, locator, value):
        '''通过value属性'''
        self.logger.info("根据属性：{},查找下拉选".format(value))
        try:
            element = self.findElement(locator)
            Select(element).select_by_value(value)
            self.logger.info("成功定位到select")
        except Exception:
            self.get_screen()
            raise Exception("定位select失败")

    def select_by_text(self, locator, text):
        '''通过文本值定位'''
        self.logger.info("根据本文：{},查找下拉选".format(text))
        try:
            element = self.findElement(locator)
            Select(element).select_by_visible_text(text)
        except Exception:
            self.get_screen()
            raise Exception("定位select失败")

    def switch_iframe(self, id_index_locator):
        '''切换iframe'''
        try:
            if isinstance(id_index_locator, int):
                self.logger.info("根据id：{}，切换iframe".format(id_index_locator))
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, str):
                self.logger.info("根据index：{}，切换iframe".format(id_index_locator))
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, tuple):
                self.logger.info("根据iframe实例：{}，切换iframe".format(id_index_locator))
                ele = self.findElement(id_index_locator)
                self.driver.switch_to.frame(ele)
            self.logger.info("切换iframe成功！！")
        except Exception:
            self.get_screen()
            raise Exception("iframe切换异常!!")

    def switch_handle(self, window_name):
        self.logger.info("切换handler")
        self.driver.switch_to.window(window_name)

    def switch_alert(self):
        self.logger.info("切换alert")
        r = self.is_alert()
        if not r:
            self.logger.error("alert不存在")
            self.get_screen()
        else:
            self.logger.info("alert存在")
            return r

    def move_to_element(self, locator):
        '''鼠标悬停操作'''
        self.logger.info("鼠标悬停在元素："+str(locator))
        try:
            ele = self.findElement(locator)
            ActionChains(self.driver).move_to_element(ele).perform()
        except:
            raise Exception("悬停元素失败")

    def get_screen(self,file_name=time.strftime('%Y-%m-%d_%H-%S-%M',time.localtime(time.time()))):
        '''截图'''
        self.logger.info("在此时进行截图！！")
        try:
            dit=readYaml.read("project.yaml")
            file_name=r"{}\screen\{}.png".format(dit['project']['path'],file_name)
            self.driver.get_screenshot_as_file(file_name)
            with open(file_name, 'rb') as file:
                f = file.read()
                MASTER_HELPER.attach("截图", f, type=AttachmentType.PNG)
            self.logger.info("已成功生成截图，请确认！")
        except:
            raise Exception("截图失败!")


if __name__ == "__main__":

    driver=webdriver.Chrome()
    base=BasePage(driver)
    base.get("https://www.baidu.com")
    print(base.get_screen())





