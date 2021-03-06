import os
import json
import psutil

class WorkDirVerifier():

  def __init__(self, workDirPath):
    self.__workDirPath = None
    self.__isVerified = False
    self.__verificationErrors = []

    workDirPath = os.path.abspath(workDirPath)
    if type(workDirPath) is not str:
      self.__verificationErrors.append( (workDirPath, "variable is not a string") )
      return
    if not os.path.exists(workDirPath):
      self.__verificationErrors.append( (workDirPath, "does not exist") )
      return
    if not os.path.isdir(workDirPath):
      self.__verificationErrors.append( (workDirPath, "is not a directory") )
      return
    if not os.path.ismount(workDirPath):
      self.__verificationErrors.append( (workDirPath, "is not a filesystem") )
      return
    if os.path.samefile(workDirPath, workDirPath + "/.."):
      self.__verificationErrors.append( (workDirPath, "is the root filesystem") )
      return
    self.__workDirPath = workDirPath
    self.__isVerified = True

  def getWorkDir(self):
    return self.__workDirPath

  def isValidated(self):
    return self.__isVerified 

  def getErrorList(self):
    return self.__verificationErrors

  def printErrorList(self):
    print(json.dumps(self.getErrorList(), indent=2))

  def hasErrors(self):
    if len(self.__verificationErrors) > 0:
      return True
    return False

  def getFilesystemOfWorkDir(self):
    if self.__workDirPath is None:
      return None
    for diskPartitionInstance in psutil.disk_partitions():
      if self.__workDirPath == diskPartitionInstance.mountpoint:
        return diskPartitionInstance.fstype
    return None

