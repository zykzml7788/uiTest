# pytest+selenium+allure2框架

## 技术选型及版本
- pytest:3.6.0
- selenium:3.141.0
- pytest-allure-adaptor:1.7.10
- pytest-rerunfailures:5.0

## allure常用函数

- allure.severity("优先级")
- allure.feature("模块名")
- allure.story("功能名")
- allure.step("步骤")
- allure.attach("用例参数")

## yaml配置文件
- logging.yaml  配置日志输出格式
- project.yaml  配置项目绝对路径
- testcase.yaml 配置用例相关（需执行用例文件，重跑次数）

## allure.bat配置环境变量
- allure-2.7.0/bin

## 待实现功能
- 告罄功能
- 邮件功能
- 数据库校验
- 数据驱动（参数化）
