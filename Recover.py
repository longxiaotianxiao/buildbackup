import subprocess
import chardet
import codecs
import logging

module_logger = logging.getLogger("mainModule.sub")

logger = logging.getLogger('mainModule.sub.module')
def ExecteCmd(cmd):
    try:
        subRet = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #不需要判断是否成功吗
        strout,strerror = subRet.communicate()

        if strout != None:
            code = chardet.detect(strout)["encoding"]
            if code != None:
                strout = strout.decode(code)
        if strerror != None:
            code = chardet.detect(strerror)["encoding"]
            if code != None:
                strerror = strerror.decode(code)

        for line in strout.splitlines():
            logger.info(line)
        for line in strerror.splitlines():
            logger.info(line)

        if subRet.returncode == 0:
            return  0
        else:
            return  -1
    except(Exception) as e:
        print(e)
        logger.info(e)
        return -1