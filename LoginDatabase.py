from ui_LoginDatabase import Ui_Dialog
from PyQt5.QtCore import QObject,pyqtSignal,pyqtSlot
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import psycopg2
import os
import Recover
import BuildDialog
import logging
import codecs
from PyQt5.QtWidgets import QMessageBox
module_logger = logging.getLogger("mainModule.sub")
import threading,time
from PyQt5.QtCore import QObject,pyqtSignal,pyqtSlot
import configparser
import sys

class LoginDatabase(QtWidgets.QDialog,Ui_Dialog):
    Signal_buildFinished = pyqtSignal([str, str])
    def __init__(self):
        self.logger = logging.getLogger('mainModule.sub.module')
        super(LoginDatabase, self).__init__()
        self.setupUi(self)

        self.resize(530,281)
        self.setFixedSize(530,281)

        self.setModal(True)
        self.user =''
        self.password = ''
        self.host = ''
        self.port = ''
        self.databaseName = ''
        self.sqlList =[]
        self.strBackupType = ''
        self.strBranch = ''
        self.strVersion = ''

        self.Signal_buildFinished[str, str].connect(self.Slot_buildFinished)

        self.buildReady = True
    def SetBackuPath(self,path):
        self.databasePath = path

    def SetNeedExcuteSqlFile(self,sqlList):
        self.sqlList = sqlList

    def ReadInitInfo(self,strVersion,strBranch,strBackupType):
        #如果有配置文件则从配置中读取参数显示
        if True == os.path.isfile("userconfig.ini"):
            config = configparser.ConfigParser()
            config.sections()
            config.read("userconfig.ini")
            config.sections()

            if "Home" in config:
                self.user = config["Home"]["user"]
                self.password = config["Home"]["password"]
                self.host = config["Home"]["host"]
                self.port = config["Home"]["port"]

            self.userLineEdit.setText(self.user)
            self.passwordLineEdit.setText(self.password)
            self.portLineEdit.setText(self.port)
            self.hostLineEdit.setText(self.host)

        #默认新建数据库名称为选中的sql的version
        self.strVersion = strVersion
        strDatabaseName = strVersion.replace('.','')
        self.databaseLineEdit.setText(strDatabaseName.lower())
        self.strBackupType = strBackupType
        self.strBranch = strBranch

        if self.userLineEdit.text() == "":
            self.userLineEdit.setPlaceholderText("请输入账户如:postgres")
        if self.passwordLineEdit.text() == "":
            self.passwordLineEdit.setPlaceholderText("请输入密码")
        if self.portLineEdit.text() == "":
            self.portLineEdit.setPlaceholderText("请输入端口号")
        if self.hostLineEdit.text() == "":
            self.hostLineEdit.setPlaceholderText("主机名如:localhost/127.0.0.1")

    def WriteInitInfo(self):
        #如果有配置文件则从配置中读取参数显示
        if True == os.path.isfile("userconfig.ini"):
            os.remove("userconfig.ini")

        config = configparser.ConfigParser()
        config["Home"] = {}
        config["Home"]["user"] = self.userLineEdit.text()
        config["Home"]["password"] = self.passwordLineEdit.text()
        config["Home"]["Host"] = self.hostLineEdit.text()
        config["Home"]["port"] = self.portLineEdit.text()

        with open('userconfig.ini', 'w') as configfile:
            config.write(configfile)



    def Slot_buildFinished(self, strType,strTips):
        if strTips != None:
            self.logger.info(strTips)
        if strType == '0':
            QMessageBox.information(self, "提示", strTips)
            if strTips == '恢复成功.已保存到应用程序同级目录下' or strTips == '不需要执行sql脚本' or strTips == "备份已存在且不需要执行sql脚本":
                self.accept()
        else:
            self.statusLabel.setText(strTips)
        pass


    @pyqtSlot()
    def on_ConnectDatabaseBtn_clicked(self):
        if self.buildReady == False:
            return
        self.buildReady = False
        self.user = self.userLineEdit.text()
        self.password = self.passwordLineEdit.text()
        self.host = self.hostLineEdit.text()
        self.databaseName = self.databaseLineEdit.text()
        self.port = self.portLineEdit.text()

        self.databaseName = self.databaseName.lower()
        self.databaseLineEdit.setText(self.databaseName)

        if self.user == "" or self.password == "" or self.host == "" or self.port == "" or self.databaseName == "":
            QMessageBox.information(self, '提示', '有信息未填完整，请检查')
            self.buildReady = True
            return
        try:
            buildThread = threading.Thread(target=self.RecoverPro)
            buildThread.start()
        except (Exception)  as e:
            self.logger.info(e)
            #print(e)
            QMessageBox.information(self, '提示', '执行恢复线程异常')
            self.buildReady = True
            return

        pass


    def PsqlExcuteCmd(self,cmd):
        strCmd = u"psql.exe --host=" + self.host + " --username=" + "\"" + self.user+ "\""+ " --no-password=" + "\""+self.password+ "\""+ " --command="+ "\""+cmd+ "\""
        return Recover.ExecteCmd(strCmd)

    def PgrestoreExcuteCmd(self):
        strcmd = u"pg_restore.exe --host "+ self.host+" --port " + self.port+" --username "+"\"" + self.user+"\""+" --dbname "+"\""+self.databaseName+"\" --no-password  --verbose \""+ self.databasePath+"\""
        return Recover.ExecteCmd(strcmd)

    def PgdumpExcuteCmd(self,backupname,databasename):
        strcmd = u"pg_dump.exe --host "+self.host+" --port "+self.port+" --username "+"\"" +self.user+"\""+" --no-password  --format custom --blobs --verbose --file \"./" + backupname + "\" \"" + databasename + "\""
        return Recover.ExecteCmd(strcmd)

    #TODO:封装等待框UI线程类去做
    def RecoverPro(self):
        # 先检查数据库名是否已存在--需要先连上默认的系统数据库
        self.Signal_buildFinished.emit('1', '开始连接postgres数据库')
        try:
            conn = psycopg2.connect(database='postgres', user=self.user, host=self.host, port=self.port)
        except(Exception) as e:
            conn = None

        if conn is None:
            self.Signal_buildFinished.emit('0','连接系统数据库postgres失败')
            self.buildReady = True
            return

        cur = conn.cursor()
        self.Signal_buildFinished.emit('1', '检查新建数据库是否存在')
        strSql = "SELECT u.datname  FROM pg_catalog.pg_database u where u.datname=" + "\'" + self.databaseName + "\'" + ";"
        try:
            cur.execute(strSql)
        except(Exception) as e:
            self.Signal_buildFinished.emit('0','查询数据库失败')
            self.buildReady = True
            return

        rows = cur.fetchall()

        rowDatabaseName = ""
        for item in rows:
            rowDatabaseName = item[0]
        conn.commit()
        cur.close()
        conn.close()
        if rowDatabaseName == self.databaseName:
            self.Signal_buildFinished.emit('0','已存在数据库，请修改数据库名称')
            self.buildReady = True
            return

        if self.sqlList.__len__() <= 0 and False == self.checkBox.isChecked():
            self.Signal_buildFinished.emit('0','备份已存在且不需要执行sql脚本')
            self.WriteInitInfo()
            self.buildReady = True
            return

        # 创建数据库
        self.Signal_buildFinished.emit('1', '开始创建数据库')
        cmd = u"create database " +self.databaseName + ";"
        if self.PsqlExcuteCmd(cmd) != 0:
            self.logger.info('创建数据库' + self.databaseName + '失败')
            self.Signal_buildFinished.emit('0','创建数据库失败')
            self.buildReady = True
            return

        # 如果创建成功则恢复备份
        self.Signal_buildFinished.emit('1', '开始恢复数据库备份,可能耗时比较长请稍后...')
        if self.PgrestoreExcuteCmd() != 0:
            self.logger.info('恢复数据库备份失败')
            strcmd = u"drop database " + self.databaseName + ";"
            self.Signal_buildFinished.emit('1', '删除新建数据库...')
            if self.PsqlExcuteCmd(strcmd) != 0:
                self.Signal_buildFinished.emit('0', '删除数据库失败.')

            self.Signal_buildFinished.emit('0','恢复数据库备份失败')
            self.buildReady = True
            return

        # 如果恢复成功则建立连接执行sql
        self.Signal_buildFinished.emit('1', '与新建的数据库建立连接')
        if self.sqlList.__len__() <= 0:
            self.Signal_buildFinished.emit('0','不需要执行sql脚本')
            self.WriteInitInfo()
            self.buildReady = True
            return
        try:
            conn = psycopg2.connect(database=self.databaseName, user=self.user, host=self.host, port=self.port)
        except(Exception) as e:
            #print(e)
            self.logger.info(e)
            conn = None

        if conn is None:
            self.Signal_buildFinished.emit('0','连接新建数据库' + self.databaseName + "失败")
            self.buildReady = True
            return

        cur = conn.cursor()

        allsqlExcuteSuc = True
        for fileSql in self.sqlList:
            with open(fileSql["path"], 'r', encoding='utf-8') as file_object:
                contents = file_object.read()
                if contents.startswith(bytes.decode(codecs.BOM_UTF8)):
                    contents = contents.encode('utf-8').decode('utf-8-sig')
                else:
                    contents = contents

                try:
                    self.Signal_buildFinished.emit('1', '执行'+fileSql["path"])
                    cur.execute(contents)
                except (Exception, psycopg2.DatabaseError) as e:
                    allsqlExcuteSuc = False
                    #print(e)
                    self.logger.info('执行失败'+ fileSql["path"])
                    self.logger.info(e)
                    #strPrint = e
                    #self.Signal_buildFinished.emit('1', strPrint)
                    break


        if allsqlExcuteSuc == True:
            self.Signal_buildFinished.emit('1', '执行完成...')
            conn.commit()
        else:
            self.Signal_buildFinished.emit('0','恢复失败--执行脚本出错')

            cur.close()
            conn.close()

            strcmd = u"drop database " + self.databaseName + ";"
            self.PsqlExcuteCmd(strcmd)

            self.buildReady = True
            return
        cur.close()
        conn.close()

        self.Signal_buildFinished.emit('1', '开始创建新备份...')
        createname = "database_STAR-" + self.strBranch + "-" + self.strVersion + "-" + self.strBackupType + "_base.backup"
        if self.PgdumpExcuteCmd(createname,self.databaseName) != 0:
            self.Signal_buildFinished.emit('0', '恢复数据库成功但重新生成备份失败')

        if False == self.checkBox.isChecked():
            strcmd = u"drop database " + self.databaseName + ";"
            self.Signal_buildFinished.emit('1', '删除新建数据库...')
            if self.PsqlExcuteCmd(strcmd) != 0:
                self.Signal_buildFinished.emit('0', '删除数据库失败.')
        self.Signal_buildFinished.emit('1', '')
        self.Signal_buildFinished.emit('0','恢复成功.已保存到应用程序同级目录下')
        self.WriteInitInfo()

        self.buildReady = True





