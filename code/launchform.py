import threading
import tkinter as tk
import tkinter.font
import tkinter.messagebox
from tkinter import ttk
from artificialclass import ArtificialBrowser
from course import CourseService
from user import User
from user import UserService

class LaunchForm:

    """
    启动界面类
    """

    def __init__(self) -> None:
        pass


    def create_from(self):

        """
        description: 创建可视化界面
        param: None
        Returns: None
        """

        # 浏览器
        global browser_cgxf, passwordShown

        # 用户服务
        user_service = UserService()

        # 课程服务
        course_service = CourseService()

        # 显示密码
        passwordShown = False

        # 主窗口
        self.win = tk.Tk()
        self.win.title(string = "The Class Script")
        title_icon = tk.PhotoImage(file = ".//image//huaji.png")
        self.win.iconphoto(False, title_icon)
        self.win.resizable(False, False)

        # 浏览器标签
        self.browser_label = ttk.Label(self.win, text = "浏览器", compound = "center")
        self.browser_label.grid(column = 0, row = 0, padx = 25, pady = 10)

        # 浏览器单选框
        self.browser_frame = ttk.Frame(self.win)
        self.browser_frame.grid(column = 1, row = 0)
        self.radio_var = tk.IntVar()
        self.chrome_radio = tk.Radiobutton(self.browser_frame, text = "Chrome", variable = self.radio_var, value = 1)
        self.chrome_radio.grid(column = 0, row = 0, sticky = tk.W)
        self.Firefox_radio = tk.Radiobutton(self.browser_frame, text = "Firefox", variable = self.radio_var, value = 2)
        self.Firefox_radio.grid(column = 1, row = 0, sticky = tk.W)
        self.Edge_radio = tk.Radiobutton(self.browser_frame, text = "Edge", variable = self.radio_var, value = 3)
        self.Edge_radio.grid(column = 2, row = 0, sticky = tk.W)


        def click_commit_button():
        
            """
            description: 点击commit按钮效果
            param: None
            Returns: None
            """

            global browser_cgxf

            radio_value = self.radio_var.get()
            if radio_value != 0:
                browser_cgxf = ArtificialBrowser(radio_value, "https://passport2.chaoxing.com/login")
                browser_cgxf.initilize_browser()
                browser_cgxf.get_html()
                self.numVerCode_photo = tk.PhotoImage(file = ".//image//numVerCode.png")
                self.numVerCode_image.configure(image = self.numVerCode_photo)

        
        # 确定按钮
        self.commit_button = ttk.Button(self.win, text = "确定", command = click_commit_button)
        self.commit_button.grid(column = 2, row = 0, padx = 8, pady = 10)
        
        # 用户名
        self.username_label = ttk.Label(self.win, text = "用户名", compound = "center")
        self.username_label.grid(column = 0, row = 1, padx = 25, pady = 8)

        # 用户名文本
        self.username_value = tk.StringVar()
        self.username_text = ttk.Combobox(self.win, width = 20, textvariable = self.username_value)
        # 读取用户名
        self.users_list = user_service.read_user(path = ".//data//user.json")
        users_name_list = list()
        for item in self.users_list:
            users_name_list.append(item.username)
        self.username_text['values'] = users_name_list
        self.username_text.grid(column = 1, row = 1, padx = 10, pady = 10, sticky = tk.W)

        # 密码
        self.password_label = ttk.Label(self.win, text = "密  码", compound = "center")
        self.password_label.grid(column = 0, row = 2, padx = 25, pady = 8)

        # 密码文本
        self.password_value = tk.StringVar()
        self.password_text = ttk.Entry(self.win, width = 20, show = "*", textvariable = self.password_value)
        self.password_text.grid(column = 1, row = 2, padx = 10, pady = 8, sticky = tk.W)


        def change_password(*args):

            """
            description: 改变密码
            param: *args 不知道为什么要加
            Returns: None
            """

            for item in self.users_list:
                if item.username == self.username_value.get():
                    self.password_value.set(item.password)
                    break


        # 自动补全密码
        self.username_text.bind("<<ComboboxSelected>>", func = change_password)


        def show_password():

            """
            description: 是否显示密码
            param: 
            Returns: 
            """

            global passwordShown

            if passwordShown == True:
                # 显示状态
                passwordShown = False
                self.password_text.configure(show = "*")
                self.password_show.configure(text = "显示")
            else:
                # 隐藏状态
                passwordShown = True
                self.password_text.configure(show = "")
                self.password_show.configure(text = "隐藏")

            

        # 密码显示隐藏
        self.password_show = ttk.Button(self.win, text = "显示", width = 6, command = show_password)
        self.password_show.grid(column = 2, row = 2, pady = 8, sticky = tk.W)

        # 验证码
        self.numVerCode_label = ttk.Label(self.win, text = "验证码", compound = "center")
        self.numVerCode_label.grid(column = 0, row = 3, padx = 10, pady = 8)

        # 验证码文本
        self.numVerCode_value = tk.StringVar()
        self.numVerCode_text = ttk.Entry(self.win, width = 20, textvariable = self.numVerCode_value)
        self.numVerCode_text.grid(column = 1, row = 3, padx = 10, pady = 8, sticky = tk.W)
        
        # 验证码图片
        self.numVerCode_photo = tk.PhotoImage(file = ".//image//huaji.png")
        self.numVerCode_image = ttk.Label(self.win, image = self.numVerCode_photo)
        self.numVerCode_image.grid(column = 2, row = 3, padx = 8, sticky = tk.W)


        def click_login_button():
            
            """
            description: 点击登录按钮效果
            param: None
            Returns: None
            """
            
            global browser_cgxf

            try:
                user = User(username = self.username_value.get(), password = self.password_value.get())
                numVerCode = self.numVerCode_value.get()
                state = browser_cgxf.login_study(user = user, numVerCode = numVerCode)
                user_service.save_user(user = user, path = ".//data//user.json")
                if state == False:
                    browser_cgxf.get_html()
                    self.numVerCode_photo = tk.PhotoImage(file = ".//image//numVerCode.png")
                    self.numVerCode_image.configure(image = self.numVerCode_photo)
            except:
                pass


        # 登录按钮
        self.login_button = ttk.Button(self.win, text = "登录", command = click_login_button)
        self.login_button.grid(column = 1, row = 4, pady = 8, sticky = tk.E)


        def click_reset_button():

            """
            description: 点击重置按钮效果
            param: None
            Returns: None
            """

            self.radio_var.set(0)
            self.username_value.set("")
            self.password_value.set("")
            self.numVerCode_value.set("")
            

        # 重置按钮
        self.reset_button = ttk.Button(self.win, text = "重置", command = click_reset_button)
        self.reset_button.grid(column = 2, row = 4, pady = 8)

        # 课程名称
        self.className_label = ttk.Label(self.win, text = "课程名", compound = "center")
        self.className_label.grid(column = 0, row = 5, padx = 10, pady = 8)

        # 课程名称文本
        self.className_value = tk.StringVar()
        self.className_text = ttk.Combobox(self.win, width = 20, textvariable = self.className_value)

        # 本地读取课程名
        course_list = course_service.read_course(path = ".//data//course.txt")
        self.className_text["values"] = course_list
        self.className_text.grid(column = 1, row = 5, padx = 10, pady = 8, sticky = tk.W)

        # 课程开始节点
        self.classNode_label = ttk.Label(self.win, text = "节点", compound = "center")
        self.classNode_label.grid(column = 0, row = 6, padx = 10, pady = 8)

        # 课程名开始节点文本
        self.classNode_value = tk.StringVar()
        self.classNode_text = ttk.Combobox(self.win, width = 6, textvariable = self.classNode_value)
        self.classNode_text["values"] = ("1.1", "2.1", "3.1", "4.1", "5.1", "6.1")
        self.classNode_text.grid(column = 1, row = 6, padx = 10, pady = 8, sticky = tk.W)


        def click_start_button():

            """
            description: 点击开始按钮
            param: None
            Returns: None
            """
        
            global browser_cgxf

            try:
                # 保存课程名
                course_service.save_course(self.className_value.get(), path = ".//data//course.txt")
                browser_cgxf.choose_class(class_name = self.className_value.get())
                class_list = browser_cgxf.list_of_class(start_node = self.classNode_value.get())
                print("课程节点: ", class_list)
                print("============开始============")
                for class_node in class_list:
                    print("==========该节点开始==========")
                    flag = browser_cgxf.watch_video(class_node = class_node)
                    if flag == False:
                        browser_cgxf.back_to_page()
                        continue
                    progress_bar, moment = 0.0, 0.0
                    while progress_bar < 99.50:
                        progress_bar = browser_cgxf.get_progress_bar(10)
                        print(progress_bar)
                        if moment < 99.5 and moment == progress_bar:
                            browser_cgxf.set_answer()
                        else:
                            moment = progress_bar
                    print("==========该节点结束==========")
                    browser_cgxf.back_to_page()
            except:
                print("课程选择错误哦！")
                browser_cgxf.refresh_browser()
                pass
        

        def watch_video_thread(func):

            """
            description: 自定义线程(解决单线程按钮任务未执行完，界面未响应问题)
            param: 函数
            Returns: None
            """

            # 创建线程
            video_thread = threading.Thread(target = func)
            # 守护线程
            video_thread.setDaemon(True)
            # 启动线程
            video_thread.start()
            
        
        def click_end_button():

            """
            description: 点击结束按钮
            param: None
            Returns: None
            """

            global browser_cgxf

            try:
                browser_cgxf.close_browser()
                print("========浏览器关闭========")
            except:
                browser_cgxf.refresh_browser()
                pass
            

        # 开始按钮
        self.start_button = ttk.Button(self.win, text = "开始", command = lambda: watch_video_thread(click_start_button))
        self.start_button.grid(column = 1, row = 7, pady = 8, sticky = tk.E)

        # 结束按钮
        self.end_button = ttk.Button(self.win, text = "结束", command = click_end_button)
        self.end_button.grid(column = 2, row = 7, pady = 8)


        def version_message():

            """
            description: 显示版本信息
            param: None
            Returns: None
            """

            message = "Version 2.0 By CGXF\nSupport for Chrome, Firefox and Edge"
            tkinter.messagebox.showinfo(title = "关于", message = message)
            
        
        def keyboard_message():

            """
            description: 打印私货
            param: None
            Returns: None
            """

            message = "诶，没有快捷键，不是我不会写！"
            tkinter.messagebox.showinfo(title = "快捷键", message = message)
            

        def introduction_message():

            """
            description: 发行说明
            param: None
            Returns: None
            """
            
            message = "学习通网站的网课学习辅助工具"
            tkinter.messagebox.showinfo(title = "发行说明", message = message)


        def coffee_message():

            """
            description: 夹带私货
            param: None
            Returns: None
            """

            message = "Buy the author a cup of coffee"
            tkinter.messagebox.showinfo(title = "coffee", message = message)        


        # 菜单栏
        self.menu_bar = tk.Menu(self.win)

        self.operation = tk.Menu(self.menu_bar, tearoff = False)
        self.operation.add_command(label = "重置", command = click_reset_button)  
        self.operation.add_command(label = "Coffee", command = coffee_message)
        self.operation.add_command(label = "Exit", command = self.win.quit)

        self.introduction = tk.Menu(self.menu_bar, tearoff = False)
        self.introduction.add_command(label = "关于", command = version_message)
        self.introduction.add_command(label = "快捷键", command = keyboard_message)
        self.introduction.add_command(label = "说明", command = introduction_message)

        self.menu_bar.add_cascade(label = "操作", menu = self.operation)
        self.menu_bar.add_cascade(label = "帮助", menu = self.introduction)
        self.win.config(menu = self.menu_bar)

        self.win.mainloop()