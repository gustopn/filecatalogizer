import os
import json

class WorkDirVerifier():

  __workDirPath = None
  __isVerified = False
  __verificationErrors = []

  def __init__(self, workDirPath):
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

