import json
import bz2
import os

class Configurator():

  __configFilePath = None
  __hasConfigFile = False
  __config = None

  def __init__(self, configFileDirPath):
    self.__configFilePath = configFileDirPath + "/config.json.bz2"
    if os.path.isfile(self.__configFilePath):
      configDataCompressed = open(self.__configFilePath, "rb").read()
      configDataJSON = bz2.decompress(configDataCompressed)
      self.__config = json.loads(configDataJSON)
    else:
      if not self.__doConfigure():
        return
      configDataJSON = json.dumps(self.__config, indent=2)
      configDataCompressed = bz2.compress(configDataJSON.encode("UTF-8"))
      if not os.path.exists(self.__configFilePath):
        configFileHandle = open(self.__configFilePath, "wb")
        configFileHandle.write(configDataCompressed)
        configFileHandle.close()

  def getConfigFilePath(self):
    return self.__configFilePath

  def isConfigured(self):
    if not self.__hasConfigFile:
      return False

  def __doConfigure(self):
    print("DBMS configuration:")
    dbmsusername = input("username: ")
    dbmspassword = input("password: ")
    dbmshostname = input("hostname: ")
    configDict = {}
    configDict["DBMS"] = {}
    configDict["DBMS"]["username"] = dbmsusername
    configDict["DBMS"]["password"] = dbmspassword
    configDict["DBMS"]["hostname"] = dbmshostname
    self.__config = configDict
    return True
