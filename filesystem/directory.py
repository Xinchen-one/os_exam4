class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.files = {}  # filename -> FCB
        self.sub_dirs = {}  # dirname -> Directory

    def add_file(self, fcb):
        # 添加文件
        name = getattr(fcb, "name", None)
        if name is None:
            raise ValueError("文件名不能为空~")
        if name in self.files or name in self.sub_dirs:
            raise FileExistsError(f"文件 '{name}' 已经存在 '{self.name}'")

        self.files[name] = fcb
        if hasattr(fcb, "parent"):
            fcb.parent = self
        return fcb
    
    def remove_file(self, name):
        # 移除文件
        if name is None:
            raise ValueError("文件名不能为空~")
        if name not in self.files and name not in self.sub_dirs:
            raise FileNotFoundError(f"文件 '{name}' 不存在")
        
        if name in self.files:
            self.files.pop(name)
            print(f"文件 {name} 删除成功~")
        else:
            raise PermissionError(f"'{name}' 是目录, 请使用remove_dir来删除")
        
    def add_sub_dirs(self, directory):
        # 添加文件夹
        name = getattr(directory, "name", None)
        if name is None:
            raise ValueError("文件夹名不能为空~")
        if name in self.files or name in self.sub_dirs:
            raise FileExistsError(f"文件 '{name}' 已经存在 '{self.name}'")
        self.sub_dirs[name] = directory
        if hasattr(directory, "parent"):
            directory.parent = self
        return directory
        
    def remove_dir(self, name):
        # 删除文件夹
        if name is None:
            raise ValueError("文件名不能为空~")
        if name not in self.files and name not in self.sub_dirs:
            raise FileNotFoundError(f"文件 '{name}' 不存在")
        if name in self.files:
            raise PermissionError(f"'{name}' 是目录, 请使用remove_file来删除")
        dir_remove = self.sub_dirs[name]
        if dir_remove.files or dir_remove.sub_dirs:
            raise FileExistsError(f"文件夹 '{name}' 不为空，请清空后重试~")
        
        self.sub_dirs.pop(name)
        dir_remove.parent = None
        print(f"文件夹 {name} 成功删除~")
            
    def get_path(self):
        # 获取当前目录下的路径
        current = self
        path_components = []
        while current is not None:
            path_components.insert(0, current.name)
            current = current.parent
        if len(path_components) == 1 and path_components[0] == '/':
            return '/'
        return '/' + '/'.join(path_components[1:])

