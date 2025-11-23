import datetime

class FileControlBlock:
    def __init__(self,name,owner):
        self.name = name    
        self.owner = owner
        self.data = "" # 文件内容
        self.size = 0 # 文件大小
        current_time = datetime.datetime.now()
        self.create_time = current_time # 创建时间
        self.modify_time = current_time # 修改时间
        self.attributes = {}
        self.permission = "rwx"

    def read(self,current_user_name):
        if current_user_name == self.owner.name and 'r' in self.permission:
            print(f"文件: {self.name}:\n{self.data}")
        else:
            print(f"拒绝访问：用户 {current_user_name} 没有读取 '{self.name}' 的权限")

    def write(self,content,current_user):
        if current_user == self.owner.name and 'w' in self.permission:
            self.data += content
            self.size = len(self.data)
            current_time = datetime.datetime.now()
            self.modify_time = current_time
        else:
            print(f"拒绝访问：用户 {current_user} 没有写入 '{self.name}' 的权限")
