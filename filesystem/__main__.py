# filesystem/__main__.py
"""
当使用 `python -m filesystem` 启动时，会执行这里的代码。
我们直接复用项目根目录的 main.main()，保持入口唯一。
"""

import os
import sys

# 把项目根目录加入 sys.path，确保可以导入 main.py
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from main import main  # 导入根目录 main.py 中的 main() 函数


if __name__ == "__main__":
    main()
