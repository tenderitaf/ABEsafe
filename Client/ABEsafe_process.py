import wx.lib.delayedresult as DR
import os
import sys
import re

import platform
from ctypes import *

class CPABE:
    """
        Declarations of ABEsafe system environment variables
        - The path of the key is exposed here and shall be protected by the user his own,
        it should be secure unless the user intentionally share the key to others outside
        this system

        Encryption, decryption, and validation methods are defined
        - Currently, the methods are executed through system call. It would be unsecure
        only if this code has been modified and ABEsafe is executed with administrator
        privilege.
    """
    ENC,DEC,OPEN,MKEY,CISPEC,POK = range(6)
    TMP = '/private/tmp/org.astri.cpabe'
    SHARED_FOLDER_NAME = ""
    HOME_PATH = ""
    LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
    SHARED_FOLDER_PATH = ""
    ABEsafe_PATH = os.path.join(SHARED_FOLDER_PATH,"ABEsafe")
    KEYS_PATH = os.path.join(LOCAL_PATH,".keys")
    CONFIG_PATH = os.path.join(ABEsafe_PATH,".configs")
    IMG_PATH = os.path.join(ABEsafe_PATH,"userImages")
    DATABASE_file = "test.db"
    DATABASE = os.path.join(CONFIG_PATH,DATABASE_file)
    ABE_LIBRARY = 'libabe_linux.so' if platform.system().lower() == 'linux' else 'libabe.so'
    libc = cdll.LoadLibrary(os.path.join(LOCAL_PATH,os.path.join('lib',ABE_LIBRARY)))
    @staticmethod
    def runcpabe(runtype,jid,onresult,*args):
        """
            Environment variables exposed to all other modules,
            including the home path, shared folder path and name,
            key path, ABEsafe configuration path, and the database file
        """
        if runtype==CPABE.ENC:
            fcreate = args[0]
            f_seg2 = fcreate.rpartition('.')
            f_seg = f_seg2[0].rpartition('.')
            fcheck = fcreate
            replica = 1
            while os.path.exists(fcheck) and replica<=sys.maxint:
                fcheck = f_seg[0]+"("+str(replica)+")"+f_seg[1]+f_seg[2]+f_seg2[1]+f_seg2[2]
                replica += 1
            import tempfile
            ftmp = tempfile.NamedTemporaryFile()
            result = CPABE.libc.abe_encrypt(str(ftmp.name), str(os.path.join(CPABE.CONFIG_PATH,".pub_key")), str(args[1]), str(args[2].replace(';','')))
            DR.startWorker(onresult,CPABE.execbg,cargs=(ftmp,fcheck),wargs=(result,),jobID=jid)
        elif runtype==CPABE.DEC:
            result = CPABE.libc.abe_decrypt(str(args[0]), str(os.path.join(CPABE.CONFIG_PATH,".pub_key")), str(os.path.join(CPABE.KEYS_PATH,args[1])), str(args[2].replace(';','')))
            DR.startWorker(onresult,CPABE.execbg,wargs=(result,),jobID=jid)
        elif runtype==CPABE.OPEN:
            status = CPABE.libc.abe_checkopen(str(os.path.join(CPABE.CONFIG_PATH,".pub_key")), str(os.path.join(CPABE.KEYS_PATH,args[0])), str(args[1].replace(';','')))
            return status
        elif runtype==CPABE.MKEY:
            result = CPABE.libc.abe_checkmetapriv(str(os.path.join(CPABE.CONFIG_PATH,".pub_key")), str(args[0]), str(os.path.join(CPABE.KEYS_PATH,args[1]).replace(';','')))
            DR.startWorker(onresult,CPABE.execbg,wargs=(result,),jobID=jid)
        elif runtype==CPABE.POK:
            if re.sub(r"\s+", '', args[0]) == "":
                return 1
            status = CPABE.libc.abe_checkmeta(str(os.path.join(CPABE.CONFIG_PATH,".pub_key")), str(args[0].replace(';','')))
            return status
    
    @staticmethod
    def execbg(result):
        return result
