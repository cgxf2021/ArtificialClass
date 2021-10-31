import os

# class Course:

#     """
#     课程类
#     """

#     def __init__(self, courseName) -> None:

#         """
#         description: 构造方法
#         param: courseName
#         Returns: None
#         """
        
#         self.courseName = courseName


#     def __eq__(self, other) -> bool:
        
#         if self.courseName == other.courseName:
#             return True
#         else:
#             return False
        
    
#     def __hash__(self) -> int:
        
#         return hash(self.courseName)



class CourseService:

    """
    课程服务类
    """

    def __init__(self) -> None:
        pass

    
    def read_course(self, path: str) -> list:

        """
        description: 读取txt文件
        param: path 路径
        Returns: class_list 用户列表
        """

        if os.path.exists(path) == False and os.path.getsize(path) == 0:
            return list()
        else:
            courses_list = list()
            file = open(path, "r", encoding = "UTF-8")
            line = file.readline()
            courses_list.append(line[0:-1])
            while line:
                line = file.readline()
                if len(line) > 0:
                    courses_list.append(line[0:-1])
            file.close()
            return courses_list

    
    def save_course(self, courseName: str, path: str) -> None:

        """
        description: 保存课程数据
        param: path 路径
        Returns: None
        """

        if courseName != "":
            if os.path.exists(path) == False and os.path.getsize(path) == 0:
                file = open(path, "w", encoding = "UTF-8")
                file.write(courseName)
                file.close()
            else:
                courses_list = self.read_course(path = path)
                if courseName not in courses_list:
                    file = open(path, "a", encoding = "UTF-8")
                    file.write(courseName)
                    file.write("\n")
                    file.close()
                else:
                    pass
