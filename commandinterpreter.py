# command_interpreter.py
"""
命令解释器：
负责解析用户输入的命令字符串，并调用 Filesystem 中对应的方法。
"""

from filesystem.file_system import Filesystem


class CommandInterpreter:
    def __init__(self, fs: Filesystem):
        self.fs = fs

    def run(self):
        """
        主循环：显示提示符 -> 读命令 -> 分析并执行
        """
        print("----- 欢迎进入模拟文件系统 Shell -----")
        print("提示：输入 'help' 查看命令列表，输入 'exit' 或 'quit' 退出。")

        while True:
            # 构造提示符：[用户名@当前路径] $
            user_name = self.fs.current_user.name if self.fs.current_user else "guest"
            if hasattr(self.fs.current_dir, "get_path"):
                current_path = self.fs.current_dir.get_path()
            else:
                current_path = "/"

            prompt = f"[{user_name}@{current_path}] $ "

            try:
                line = input(prompt).strip()
            except KeyboardInterrupt:
                print("\n再见！")
                break

            if not line:
                continue

            should_exit = self.handle_command(line)
            if should_exit:
                break

    # ------------------ 命令分发核心 ------------------ #
    def handle_command(self, line: str) -> bool:
        """
        解析并执行一行命令。
        返回值：
            True  -> 退出程序
            False -> 继续运行
        """
        parts = line.split()
        cmd = parts[0]
        args = parts[1:]

        try:
            # ===== 系统命令 =====
            if cmd in ("exit", "quit"):
                print("退出系统。")
                return True

            elif cmd == "help":
                self.print_help()

            # ===== 用户管理 =====
            elif cmd == "useradd":
                # useradd <username>
                if len(args) < 1:
                    print("用法: useradd <username>")
                else:
                    self.fs.create_user(args[0])

            elif cmd == "login":
                # login <username>
                if len(args) < 1:
                    print("用法: login <username>")
                else:
                    self.fs.login(args[0])

            elif cmd == "logout":
                self.fs.logout()
                print("已退出登录")

            # ===== 目录操作 =====
            elif cmd == "ls":
                # 列出当前目录内容
                self.fs.list_directory()

            elif cmd == "mkdir":
                # mkdir <dirname>
                if len(args) < 1:
                    print("用法: mkdir <dirname>")
                else:
                    self.fs.make_directory(args[0])

            elif cmd == "rmdir":
                # rmdir <dirname>
                if len(args) < 1:
                    print("用法: rmdir <dirname>")
                else:
                    self.fs.remove_directory(args[0])

            elif cmd == "cd":
                # cd <path>   支持 . 和 ..
                if len(args) < 1:
                    print("用法: cd <path> (支持 . 和 ..)")
                else:
                    self.fs.change_directory(args[0])

            elif cmd == "pwd":
                # 显示当前路径
                if hasattr(self.fs.current_dir, "get_path"):
                    print(self.fs.current_dir.get_path())
                else:
                    print("/")

            # ===== 文件操作 =====

            # 创建文件：两种命令名都支持
            elif cmd in ("touch", "create"):
                # touch <filename>
                if len(args) < 1:
                    print("用法: touch <filename>")
                else:
                    self.fs.create_file(args[0])

            # 删除文件：支持 delete 和 rm
            elif cmd in ("delete", "rm"):
                # rm <filename>
                if len(args) < 1:
                    print("用法: rm <filename>")
                else:
                    self.fs.delete_file(args[0])

            elif cmd == "open":
                # open <filename>
                if len(args) < 1:
                    print("用法: open <filename>")
                else:
                    self.fs.open_file(args[0])
                    print(f"文件 {args[0]} 已打开 (使用 'write' 写入, 'read' 读取, 'close' 关闭)")

            elif cmd == "close":
                # 注意：Filesystem 中方法名是 close_flie（原代码拼写如此）
                self.fs.close_flie()
                print("文件已关闭")

            # 读文件内容：支持 read 和 cat（都是读取当前已打开文件）
            elif cmd in ("read", "cat"):
                self.fs.read_file()

            elif cmd == "write":
                # write <content...>
                if len(args) < 1:
                    print("用法: write <content...>")
                else:
                    content = " ".join(args)
                    # 自动加一个换行，便于多次写入时换行显示
                    self.fs.write_file(content + "\n")
                    print("写入成功")

            # ===== 其他操作：重命名 =====
            elif cmd in ("rename", "mv"):
                # rename <oldname> <newname>
                if len(args) < 2:
                    print("用法: rename <oldname> <newname>")
                else:
                    old_name, new_name = args[0], args[1]
                    self.fs.rename_file(old_name, new_name)
                    print(f"文件 {old_name} 已重命名为 {new_name}")

            else:
                print(f"未知的命令: {cmd}")

        except Exception as e:
            # 捕获 Filesystem 抛出的各种错误信息（权限、找不到文件等）
            print(f"错误: {e}")

        return False

    # ------------------ 帮助信息 ------------------ #
    @staticmethod
    def print_help():
        print(
            """
可用命令列表：
-------------------------
[系统]
  help           : 显示本帮助
  exit, quit     : 退出程序

[用户]
  useradd <name> : 创建用户
  login <name>   : 登录
  logout         : 登出

[目录]
  pwd            : 显示当前路径
  ls             : 列出当前目录内容
  mkdir <name>   : 创建目录
  rmdir <name>   : 删除目录
  cd <path>      : 切换目录 (支持 . 和 ..)

[文件]
  touch <name>   : 创建文件（别名: create）
  rm <name>      : 删除文件（别名: delete）
  open <name>    : 打开文件
  close          : 关闭当前打开的文件
  read           : 读取当前打开文件内容（别名: cat）
  write <text>   : 向当前打开的文件写入一行内容

[其他]
  rename <old> <new> : 重命名文件（别名: mv）
-------------------------
"""
        )
