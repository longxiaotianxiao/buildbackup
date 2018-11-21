from PyQt5.QtGui import QStandardItem
from ui_BuildDialog import Ui_dialog
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject,pyqtSignal,pyqtSlot
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTreeWidgetItem
from distutils.version import LooseVersion
import os
import logging
module_logger = logging.getLogger("mainModule.sub")
from LoginDatabase import LoginDatabase
import Recover

def getVersionAndBranch(filename):
    versionTmp = []
    branchTmp = []
    nameList = filename.split('_')
    if nameList.__len__() >= 3:
        versionstr = nameList[1]

        versionlist = versionstr.split('-')
        branchTmp = versionlist[1]
        versionTmp = versionlist[2]

    return  branchTmp,versionTmp



def getFileList(dir,fileList,branchList):

    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if os.path.isdir(file_path):
            print(file_path)
            getFileList(file_path,fileList,branchList)
        else:
            (filepath, tempfilename) = os.path.split(file_path)
            print(tempfilename)
            (shotname, extension) = os.path.splitext(tempfilename)
            print(shotname)
            strStart = shotname[:14]
            if extension == '.sql' and strStart == 'DBscript_STAR-':
                strBranch,strVersion = getVersionAndBranch(shotname)
                if strBranch not in branchList:
                    print(strBranch)
                    branchList.append(strBranch)
                fileList.append(file_path)
    pass
def getSplitBranch(branch,nLoc,branchList):#B1.1.1返回B1，B1.1，B1.1.1
    npos = branch.find('.',nLoc)

    if npos == -1:
        branchList.append(branch)
    else:
        branchList.append(branch[0:npos])
        if npos <= branch.__len__():
            getSplitBranch(branch,npos+1,branchList)

    return  branchList


def getSqlName(brach,lastFileName,path,sqlNameList):#获取当前文件加下符合版本的.sql
    branchList = []
    getSplitBranch(brach,0,branchList)
    for file in os.listdir(path):
        file_path = os.path.join(path, file)

        if os.path.isdir(file_path):
            Flist = file_path.split('\\')
            strLastName = Flist[Flist.__len__()-1]

            if strLastName == lastFileName:
                sqlfile = os.listdir(file_path)
                for sqlname in sqlfile:
                    (filepath, tempfilename) = os.path.split(sqlname)
                    print(tempfilename)
                    (shotname, extension) = os.path.splitext(tempfilename)
                    print(shotname)
                    strStart = shotname[:14]
                    if extension == '.sql' and strStart == 'DBscript_STAR-':
                        strBranch,strVersion = getVersionAndBranch(shotname)
                        if strBranch in branchList:
                            sqlNameList.append(shotname)

                return

    pass


def getSqlFile(brach,sqlVersion,backupversion,SqlList,path):#获取当前文件加下符合版本的.sql

    branchList = []
    getSplitBranch(brach,0,branchList)

    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            getSqlFile(brach,sqlVersion,backupversion,SqlList,file_path)
        else:
            (filepath, tempfilename) = os.path.split(file_path)
            print(tempfilename)
            (shotname, extension) = os.path.splitext(tempfilename)
            print(shotname)
            strStart = shotname[:14]
            if extension == '.sql' and strStart == 'DBscript_STAR-':
                strBranch, strVersion = getVersionAndBranch(shotname)
                if strBranch in branchList:
                    tmpL = {}
                    if LooseVersion(strVersion) > LooseVersion(backupversion) and LooseVersion(strVersion) <= LooseVersion(sqlVersion):
                        tmpL["branch"] =strBranch
                        tmpL["version"] = strVersion
                        tmpL["path"] = file_path
                        SqlList.append(tmpL)




def getBackupList(path, list_name):  # 传入存储的list

    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            getBackupList(file_path, list_name)
        else:
            tmpfileinfo = os.path.splitext(file)
            tmpL = {}
            if tmpfileinfo[1] == '.backup':
                tmpL["branch"], tmpL["version"] = getVersionAndBranch(tmpfileinfo[0])
                tmpL["path"] = file_path
                list_name.append(tmpL)
                print(tmpL)

class BuildDialog(QtWidgets.QWidget,Ui_dialog):
    def __init__(self):
        self.logger = logging.getLogger('mainModule.sub.module')
        super(BuildDialog, self).__init__()
        self.setupUi(self)
        self.FilePathLabel.setVisible(False)
        #self.DatabaseLabel.setVisible(False)
        #self.DatabaseNameLineEdit.setVisible(False)
        self.BackupLabel.setVisible(False)
        self.FileTreeWidget.setColumnCount(1)
        self.FileTreeWidget.setAlternatingRowColors(True)
        self.FileTreeWidget.clear()
        self.WarehouseComBox.activated[str].connect(self.on_WarehouseComBox_activated)
        self.FileTreeWidget.itemClicked['QTreeWidgetItem*','int'].connect(self.on_FileTreeWidget_itemClicked)
        self.strBackupPath = ''
        self.sqlList = []
        self.backupType = ''
        self.branch = ''


    @pyqtSlot()
    def on_OpenFileBtn_clicked(self):
        self.path = QFileDialog.getExistingDirectory()
        self.logger.info('打开文件路径:'+ self.path)
        if self.path:
            self.FilePathLabel.setText('已选择合集路径:'+self.path)
            self.FilePathLabel.setVisible(True)
            self.fileList = []
            branchList = []
            getFileList(self.path,self.fileList,branchList)

            #for strFile in self.fileList:
                #self.logger.info(strFile)

            #TODO:combox根据配置文件从branchlist中筛选显示
            self.WarehouseComBox.clear()
            self.FileTreeWidget.clear()
            for iter in branchList:
                self.WarehouseComBox.addItem(iter)

            self.WarehouseComBox.setCurrentIndex(0)

            branch = self.WarehouseComBox.currentText()
            self.DisplayFileTree(branch,self.path)
    @pyqtSlot()
    def on_WarehouseComBox_activated(self):
        self.branch = self.WarehouseComBox.currentText()
        self.strBackupPath = ''
        self.sqlList.clear()
        self.DisplayFileTree(self.branch, self.path)

    @pyqtSlot()
    def on_FileTreeWidget_itemClicked(self):
        item_list = self.FileTreeWidget.selectedItems()
        for item in item_list:
            self.logger.info(item.text(0))
            strItem = item.text(0)
            if strItem.find('DBscript_STAR-') != -1:
                branch =self.WarehouseComBox.currentText()
                self.GetBaseBackup(strItem,branch)


    @pyqtSlot()
    def on_BuildBtn_clicked(self):
        if self.strBackupPath == '':
            self.logger.info('没有备份不能生成')
            QMessageBox.information(self, '提示', '没有可用的backup，请正确选择后再操作')
            return

        self.login = LoginDatabase()
        self.login.SetBackuPath(self.strBackupPath)
        self.login.SetNeedExcuteSqlFile(self.sqlList)
        self.login.ReadInitInfo(self.selectedVersion,self.branch,self.backupType)

        self.login.show()
        self.login.exec_()

        #下面两条在loginDlg中做了
        #TODO:创建数据库并且恢复banckup成功后执行要升级的.sql文件(需要按version排序)

        #TODO:.sql脚本都执行完成后再将数据库备份到本地
        pass




    def DisplayFileTree(self,branch,path):

        lastFileName = self.GetLastFileName(self.fileList)

        if lastFileName.__len__() > 0:
            self.FileTreeWidget.clear()

        for item in lastFileName:
            child =  QTreeWidgetItem(self.FileTreeWidget)
            child.setText(0,item)

            sqlNameList = []
            getSqlName(branch,item,path,sqlNameList)
            for value in sqlNameList:
                child1 = QTreeWidgetItem(child)
                child1.setText(0, value)
        pass


    def GetLastFileName(self,fileList):#获取.sql最后一层级的文件名
        LastFileNameList = []
        for strFile in fileList:
            Flist = strFile.split('\\')
            if Flist.__len__() >=2 :
                strfilename = Flist[Flist.__len__() - 2]

                if strfilename not in LastFileNameList:
                    LastFileNameList.append(strfilename)

        return  LastFileNameList

    #如果存在和分支号相同的backup则从中选择离sql文件version最近的
    #如果没有则需要在上一级中选择最小的sql版本
    def GetNearSqlVersion(self,strSelectBranch,strParentBranch,strVersion):
        strSqlNearVersion = strVersion
        if strSelectBranch == strParentBranch:
            strSqlNearVersion = strVersion
        else :
            strSqlNearVersion = 'V999999.999999.999999.999999'
            for itr in self.fileList:
                      strBranch, sqlVersion = getVersionAndBranch(itr)
                      if strParentBranch == strBranch and LooseVersion(sqlVersion) <= LooseVersion(strSqlNearVersion):
                          strSqlNearVersion = sqlVersion

        return strSqlNearVersion;

    def GetBaseBackup(self,sqlFile,branch):
        self.BackupLabel.setText("")
        self.StatusTextEdit.setText("")

        strBranch,sqlVersion = getVersionAndBranch(sqlFile)

        self.selectedVersion = sqlVersion
        self.selectedBranch = branch
        if sqlVersion == None or strBranch == None or branch == None:
            return

        backupList = []
        getBackupList(self.path,backupList)


        branchList = []
        getSplitBranch(branch,0,branchList)

        isHaveBackup = False
        isBreak = False
        strUsedBranch = branch
        strBranchParent = branch
        sqlNearVersion = 'V0.0.0.0'
        for itrBranch in reversed(branchList):
            sqlNearVersion = self.GetNearSqlVersion(itrBranch,strBranchParent,sqlVersion)
            strBranchParent = itrBranch
            if LooseVersion(sqlNearVersion) > LooseVersion(sqlVersion):
                continue
            for itr in backupList:
              if itrBranch == itr["branch"] and  LooseVersion(itr["version"]) <= LooseVersion(sqlNearVersion) :
                  strUsedBranch = itrBranch
                  isHaveBackup = True
                  isBreak = True
                  break
            if isBreak == True:
                break

        strVersionTmp = 'V0.0.0.0'
        self.strBackupPath = ''
        if True == isHaveBackup:
            for item in backupList:
                if item["branch"]  == strUsedBranch:
                    if LooseVersion(strVersionTmp) < LooseVersion(item["version"]) and LooseVersion(item["version"]) <= LooseVersion(sqlNearVersion):
                        strVersionTmp = item["version"]
                        self.strBackupPath = item["path"]


        if isHaveBackup and strVersionTmp != 'V0.0.0.0' and self.strBackupPath != None:
            Flist = self.strBackupPath.split('\\')
            if Flist.__len__() >= 1:
                strfilename = Flist[Flist.__len__() - 1]
            if Flist.__len__() >= 2:
                self.backupType = Flist[Flist.__len__()-2]

            self.BackupLabel.setVisible(True)
            self.BackupLabel.setText('最近版本的backup:'+strfilename)

            if sqlVersion == strVersionTmp:
                self.logger.info('要恢复的sql正好有相同的backup:%-%', sqlVersion, self.strBackupPath)

            self.GetNeedExecutetSql(sqlFile,branch,strVersionTmp)
        else:
            self.strBackupPath = ''
            self.sqlList.clear()
            QMessageBox.information(self, '提示', '此分支没有备份可用于恢复')


    #根据选中的sql,backup及branch获取需要执行的sql文件
    def GetNeedExecutetSql(self,sqlName,branch,backupVersion):
        strBranch, sqlVersion = getVersionAndBranch(sqlName)


        self.sqlList = []
        getSqlFile(branch,sqlVersion,backupVersion,self.sqlList,self.path)

        if (self.sqlList.__len__() > 0):
            self.sqlList.sort(key=lambda obj: LooseVersion(obj.get('version')), reverse=False)

        self.logger.info(self.sqlList)

        self.StatusTextEdit.clear()
        for item in self.sqlList:
            strText = self.StatusTextEdit.toPlainText()
            self.StatusTextEdit.setText(strText + item.get("path") + '\n')





