import json
import os

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys  # 键盘导入类
import time

# 设置用户名、密码
username = "123456"
password = "*******"
# option = webdriver.ChromeOptions()
# option.add_argument('--user-data-dir=/Users/deanls/Library/Application Support/Google/Chrome/Default')
# 谷歌浏览器驱动
browser = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")


def login():
    if os.path.exists("./cookies.txt"):
        browser.delete_all_cookies()
        with open('./cookies.txt', 'r') as cookie_file:
            # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
            cookies_list = json.load(cookie_file)

            # 方法1 将expiry类型变为int
            for cookie in cookies_list:
                # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
                if isinstance(cookie.get('expiry'), float):
                    cookie['expiry'] = int(cookie['expiry'])
                browser.add_cookie(cookie)
        time.sleep(3)
        browser.get('https://m.weibo.cn/')

    else:
        # 填写登录信息：用户名、密码
        browser.find_element_by_id("loginName").send_keys(username)
        browser.find_element_by_id("loginPassword").send_keys(password)
        time.sleep(1)

        # 点击登录
        browser.find_element_by_id("loginAction").click()
        time.sleep(5)

        # 使用其他方式
        browser.find_element_by_xpath("//*[@id='vdVerify']/div[1]/div/div/div[4]/span/a").click()
        time.sleep(1)
        # 使用私信接收验证码
        browser.find_element_by_xpath("//*[@id='vdVerify']/div[3]/div[2]/div[1]/div/div/div/a").click()
        time.sleep(1)
        # 输入验证码
        code = input("input验证码:")
        time.sleep(3)
        browser.find_element_by_xpath(
            "//*[@id='verifyCode']/div[1]/div/div/div[2]/div/div/div/span[1]/input").send_keys(code)
        browser.find_element_by_xpath("//*[text()='确认']").click()
        time.sleep(60)
        with open('./cookies.txt', 'w') as cookie_f:
            # 将cookies保存为json格式
            cookie_f.write(json.dumps(browser.get_cookies()))


# 打开微博登录页
browser.get('https://passport.weibo.cn/signin/login')
browser.implicitly_wait(5)
time.sleep(1)
login()

# 点击我的
browser.find_element_by_xpath("//*[@id='app']/div[1]/div[1]/div[1]/div[1]").click()
time.sleep(1)
# 点击关注
browser.find_element_by_xpath("//*[text()='关注']").click()
time.sleep(1)
# 点击超话
browser.find_element_by_xpath("//*[text()='超话']").click()
time.sleep(1)
# 点击所有
browser.find_element_by_xpath("//*[text()='查看全部']").click()
time.sleep(1)
# 签到
qd_data = browser.find_elements_by_xpath("//*[text()='签到']")
print("please login first!")
print(len(qd_data))
if len(qd_data) != 0:
    for i in range(0, len(qd_data)):
        data = browser.find_element_by_xpath("//*[text()='签到']")
        while 1:
            try:
                data.click()
                time.sleep(2)
                browser.find_element_by_xpath("//*[text()='返回']").click()
                time.sleep(2)
                break
            except  Exception as e:
                print(e)
                ActionChains(browser).key_down(Keys.DOWN).perform()
                time.sleep(2)
                print(i)
                continue
