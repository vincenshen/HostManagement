import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.path.join(BASE_DIR)

from HostManage.core import main


if __name__ == '__main__':
    main.interactive()