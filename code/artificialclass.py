import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from bs4 import BeautifulSoup
from user import User
from PIL import Image

class ArtificialBrowser:

    """
    虚拟浏览器
    """

    def __init__(self, selected: int, url: str) -> None:

        """
        构造方法
        """

        self.selected = selected
        self.url = url

    
    def initilize_browser(self):

        """
        description: 初始化浏览器(Chrome/Firefox/Edge) 
        param: None
        Returns: None
        """

        # chrome
        if self.selected == 1:
            service = ChromeService(executable_path = ".//driver//chromedriver.exe")
            options = ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.browser = webdriver.Chrome(service = service, options = options)
        # firefox
        elif self.selected == 2:
            service = FirefoxService(executable_path = ".//driver//geckodriver.exe")
            self.browser = webdriver.Firefox(service = service)
        # edge
        else:
            service = EdgeService(executable_path = ".//driver//msedgedriver.exe")
            options = EdgeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.browser = webdriver.Edge(service = service, options = options)
        
        # 设置浏览器窗口大小
        self.browser.set_window_size(width = 1200, height = 800)

    
    def get_html(self):

        """
        description: 获取url指定网页
        param: None
        Returns: None
        """

        self.browser.get(self.url)
        time.sleep(3)
        
        # 截图
        self.browser.save_screenshot(".//image//login.png")
        # 定位验证码
        numVerCode = self.browser.find_element(By.XPATH, "//*[@id=\"numVerCode\"]")
        # 验证码位置、宽高
        num_location = numVerCode.location
        num_size = numVerCode.size
        # 验证码定位
        num_coordinate = (int(num_location['x']), int(num_location['y']), int(num_location['x'] + num_size['width']), int(num_location['y'] + num_size['height']))
        # 图片缩放
        screenshot = Image.open(".//image//login.png").resize((1184, 668), Image.ANTIALIAS)
        os.remove(".//image//login.png")
        numVerCode = screenshot.crop(box = num_coordinate)
        # 保存为jpg
        # numVerCode = numVerCode.convert('RGB')
        numVerCode.save(".//image//numVerCode.png")


    def login_study(self, user: User, numVerCode: str) -> bool:

        """
        description: 登录
        param: user 用户
        Returns: state
        """

        # 输入username
        self.browser.find_element(by = By.ID, value = "unameId").send_keys(user.username)
        time.sleep(1)
        # 输入密码
        self.browser.find_element(by = By.ID, value = "passwordId").send_keys(user.password)
        # 输入验证码
        self.browser.find_element(by = By.ID, value = "numcode").send_keys(numVerCode)
        # 登录按钮
        self.browser.find_element(by = By.XPATH, value = "//*[@id=\"form\"]/table/tbody/tr[7]/td[2]/label/input").click()
        time.sleep(3)
        # 查看show_error
        try:
            show_error = self.browser.find_element(by = By.ID, value = "show_error")
            error_text = show_error.text
            print(error_text)
            return False
        except:
            return True
        
    
    def choose_class(self, class_name):

        """
        description: 选择课程
        param: class_name 课程名
        Returns: None
        """

        try:
            iframe = self.browser.find_element(by = By.XPATH, value = '//*[@id="frame_content"]')
            self.browser.switch_to.frame(iframe)
            self.browser.find_element(by = By.XPATH, value = '//span[@title="%s"]/parent::a[@class="color1"]'%class_name).click()
            # 切换到新的窗口
            self.browser.switch_to.window(self.browser.window_handles[1])
            time.sleep(3)
        except:
            pass

    
    def list_of_class(self, start_node: str) -> list:

        """
        description: 搜索未刷完的课 
        param: start_node 初始节点
        Returns: list of class
        """

        div_html = self.browser.find_element(By.XPATH, "/html/body/div[5]/div[1]/div[2]/div[3]").get_attribute('innerHTML')
        # 找出所有课程节点
        soup = BeautifulSoup(div_html, 'html.parser')
        class_list = list()
        for item in soup.select(".units .leveltwo .clearfix .chapterNumber"):
            class_list.append(item.get_text())
        # 遍历找出start_note之后的节点
        for i in range(len(class_list)):
            if start_node == class_list[i]:
                break
        # 返回课程节点
        return class_list[i: :]
        

    def watch_video(self, class_node: str) -> bool:

        """
        description: 点击该节点视频
        param: class_node 课程节点
        Returns: None
        """

        self.browser.find_element(by = By.XPATH, value = '//span[contains(text(), "%s")]/parent::a'%class_node).click()
        time.sleep(3)

        # 找到视频选项框
        try:
            self.browser.find_element(by = By.XPATH, value = '//span[@title="视频"]').click()
        except NoSuchElementException:
            print("No video")
        time.sleep(2)

        # 切换frame
        try:
            self.browser.switch_to.frame(self.browser.find_element(by = By.XPATH, value = '//*[@id="iframe"]'))
            self.browser.switch_to.frame(self.browser.find_element(by = By.XPATH, value = '//iframe'))
        except NoSuchElementException:
            print("No frame")
        time.sleep(1)

        # 点击播放按钮
        try:
            self.browser.find_element(by = By.CLASS_NAME, value = "vjs-big-play-button").click()
            return True
        except NoSuchElementException:
            print("No button")
            return False

    
    def get_progress_bar(self, time_interval: float) -> float:

        """
        description: 获取进度条
        param: time_interval 时间间隔
        Returns: progress bar
        """

        time.sleep(time_interval)
        progress_bar = self.browser.find_element(by = By.XPATH, value = '//div[@aria-label="进度小节"]').get_attribute("aria-valuenow")
        return float(progress_bar)
    
    
    def set_answer(self):
        """
        description: 答题 
        param: flag 标志
        Returns: None
        """

        submit = self.browser.find_element(by = By.XPATH, value = '//div[@class="ans-videoquiz-submit"]')
        input_a = self.browser.find_element(by = By.XPATH, value = '//input[@value="true"]')
        input_b = self.browser.find_element(by = By.XPATH, value = '//input[@value="false"]')

        # test code
        # submit = self.browser.find_element(by = By.XPATH, value = '/html/body/input[3]')
        # input_a = self.browser.find_element(by = By.XPATH, value = '/html/body/input[1]')
        # input_b = self.browser.find_element(by = By.XPATH, value = '/html/body/input[2]')

        input_a.click()
        submit.click()
        try:
            alert = self.browser.switch_to.alert
            print(alert.text)
            alert.accept()
            input_b.click()
            submit.click()
            print("Choose B")
        except NoAlertPresentException:
            print("choose A")


    def back_to_page(self):

        """
        description: 返回选课页面 
        param: None
        Returns: None
        """

        # 切回父frame
        self.browser.switch_to.parent_frame()
        self.browser.switch_to.parent_frame()
        # 返回按钮
        self.browser.find_element(by = By.XPATH, value = '//a[contains(text(), "回到课程")]').click()
        time.sleep(3)

    
    def refresh_browser(self):
        
        """
        description: 刷新浏览器
        param: None
        Returns: None
        """
        
        self.browser.refresh()


    def close_browser(self):

        """
        description: 关闭浏览器
        param: None
        Returns: None
        """

        self.browser.quit()