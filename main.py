import os
import sys
from PyQt5 import  QtCore,QtGui,QtWidgets
from BuildDialog import BuildDialog
import logging

logger = logging.getLogger('mainModule')
logger.setLevel(logging.INFO)  # 定义该handler级别
handler = logging.FileHandler('log.txt')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # 定义该handler格式
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(console)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    contents = BuildDialog()
    contents.show()
    logger.info('启动UI')
    sys.exit(app.exec_())


