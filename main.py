# main.py

from filesystem.file_system import Filesystem
from commandinterpreter import CommandInterpreter


def main():
    # 1. 创建文件系统核心对象
    fs = Filesystem()

    # 2. 创建命令解释器，并把文件系统对象传进去
    interpreter = CommandInterpreter(fs)

    # 3. 启动交互式 Shell
    interpreter.run()


if __name__ == "__main__":
    main()
