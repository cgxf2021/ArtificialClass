import json
import os

class User:

    """
    用户类
    """
    
    def __init__(self, username = None, password = None) -> None:
        """
        构造方法
        """
        self.username = username
        self.password = password


    def __eq__(self, other) -> bool:
        
        if self.username == other.username:
            return True
        else:
            return False

    def __hash__(self) -> int:
        
        return hash(self.username)



class UserService:

    """
    用户服务类
    """

    def __init__(self) -> None:
        pass
    

    def read_user(self, path: str) -> list:
        
        """
        description: 读取文件中user数据
        param: path 路径
        Returns: users_list 用户列表
        """

        if os.path.exists(path) == False or os.path.getsize(path) == 0:
            return list()
        else:
            users_list = list()
            file = open(path, "r", encoding = "UTF-8")
            users_dict = json.loads(file.read())
            file.close()
            for item in users_dict:
                user = User(username = item["username"], password = item["password"])
                users_list.append(user)
            return users_list


    def userlist_to_userdict(self, users_list) -> list:

        """
        description: 用户列表转化为字典数据列表
        param: users_list 用户列表
        Returns: users_dict
        """

        users_dict = list()
        for item in users_list:
            user_dict = {
                "username": item.username,
                "password": item.password
            }
            users_dict.append(user_dict)
        
        return users_dict


    def save_user(self, user: User, path: str):
        """
        保存用户到user.json数据中
        """

        user_dict = {
            "username": user.username, 
            "password": user.password
        }

        if user.username != "" and user.password != "":
            if os.path.exists(path) == False or os.path.getsize(path) == 0:
                file = open(path, "w", encoding = "UTF-8")
                file.write(json.dumps([user_dict], indent = 2, ensure_ascii = False))
                file.close()
            else:
                file = open(path, "r", encoding = "UTF-8")
                users_list = json.loads(file.read())
                users_list.append(user_dict)
                file.close()
                users_set = set()
                for item in users_list:
                    user = User(username = item["username"], password = item["password"])
                    users_set.add(user)
                file = open(path, "w", encoding = "UTF-8")
                users_list = self.userlist_to_userdict(users_set)
                file.write(json.dumps(users_list, indent = 2, ensure_ascii = False))
                file.close()