from .directory import Directory
from .user import User
from .fcb import FileControlBlock

class Filesystem:
    def __init__(self):
        self.user = {} # 用户名 -> User
        self.current_user = None
        self.root = Directory("/")
        self.current_dir = self.root
    
    # 用户管理类
    def create_user(self,name):
        # 创建新用户
        if name in self.user:
            raise FileExistsError(f"用户 {name} 已存在")
        
        user = User(name)
        self.user[name] = user
        print(f"用户 '{name}' 创建成功")
    
    def login(self,name):
        # 用户登录
        if self.current_user is not None:
            raise FileExistsError(f"当前已有用户在登录中~")
        if name not in self.user:
            raise FileNotFoundError(f"用户 '{name}' 不存在")
        self.current_user = self.user[name]
        print(f"用户 '{name}' 登录成功")

    def logout(self):
        # 用户退出
        if self.current_user is None:
            raise FileNotFoundError(f"当前未有用户登录~")
        self.current_user = None

    #目录类操作
    def list_directory(self):
        # 显示当前路径和文件夹内容
        full_path = self.current_dir.get_path()
        print(f"当前路径为： {full_path}")
        if not self.current_dir.files and not self.current_dir.sub_dirs:
            return
        else:
            print("--- 子目录 ---")
            for dir_key in self.current_dir.sub_dirs.keys():
                print(f"- {dir_key}")
            print("--- 文件 ---")
            for file_key in self.current_dir.files.keys():
                print(f"{file_key}")
    
    def make_directory(self,dir_name):
        # 创建新目录
        dir = Directory(dir_name,self.current_dir)
        self.current_dir.add_sub_dirs(dir) 

    def remove_directory(self,dir_name):
        #移除目录
        self.current_dir.remove_dir(dir_name)

    def change_directory(self,path):
        # 改变当前目录进入上一级或者下一级目录
        if path == '..':
            if self.current_dir.parent is not None:
                self.current_dir = self.current_dir.parent
            else:
                print("已经是根目录，无法继续向上。")
        elif path == '.':
            pass
        else:
            if path not in self.current_dir.sub_dirs:
                raise FileNotFoundError(f"目录 {path} 不存在~")
            self.current_dir = self.current_dir.sub_dirs[path]

    # 文件类操作
    def create_file(self,file_name): # 创建新文件
        # 创建新文件
        if self.current_user == None:
            raise FileNotFoundError("当前未有用户，请登录~")
        if file_name is None or file_name.strip() == "":
            raise ValueError("文件名不能为空！")
        
        file_fcb = FileControlBlock(file_name,self.current_user)
        self.current_dir.add_file(file_fcb)

    def delete_file(self,file_name): # 删除文件
        if self.current_user == None:
            raise FileNotFoundError("当前未有用户，请登录~")
        self.current_dir.remove_file(file_name)


    def open_file(self,file_name):
        # 打开文件
        if self.current_user == None:
            raise FileNotFoundError("当前未有用户，请登录~")
        if self.current_user.opened_file is not None:
            raise FileExistsError(f"当前用户已打开文件 {self.current_user.opened_file} ，请关闭后重试~")
        
        fcb = self.current_dir.files[file_name]
        self.current_user.opened_file = fcb

    def close_flie(self):
        # 关闭文件
        if self.current_user.opened_file == None:
            raise FileNotFoundError(f"当前用户未打开文件~")
        self.current_user.opened_file = None

    # 位于 Filesystem 类中

    def read_file(self):
        # 读取文件
        if self.current_user is None:
            raise FileNotFoundError("当前未有用户登录，无法执行文件操作。请登录~")
        fcb = self.current_user.opened_file 
        if fcb is None:
            raise FileNotFoundError(f"用户 '{self.current_user.name}' 未打开任何文件。")
        
        fcb.read(self.current_user.name)

    def write_file(self,content):
        if self.current_user is None:
            raise FileNotFoundError("当前未有用户登录，无法执行文件操作。请登录~")
        fcb = self.current_user.opened_file 
        if fcb is None:
            raise FileNotFoundError(f"用户 '{self.current_user.name}' 未打开任何文件。")
        
        fcb.write(content,self.current_user.name)