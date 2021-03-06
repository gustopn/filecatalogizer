import json
import bz2
import os
import socket

class Configurator():

  def __init__(self, runtimeVars):
    self.__configFilePath = runtimeVars["configfileDirPath"] + "/config.json.bz2"
    self.__hasConfigFile = False
    self.__config = None
    self.__runtimeVars = runtimeVars

    if os.path.isfile(self.__configFilePath):
      configDataCompressed = open(self.__configFilePath, "rb").read()
      configDataJSON = bz2.decompress(configDataCompressed)
      self.__config = json.loads(configDataJSON)
    else:
      if not self.__doConfigure():
        return
      configDataJSON = json.dumps(self.__config, indent=2)
      configDataCompressed = bz2.compress(configDataJSON.encode("UTF-8"))
      if os.path.exists(self.__configFilePath):
        return
      configFileHandle = open(self.__configFilePath, "wb")
      configFileHandle.write(configDataCompressed)
      configFileHandle.close()
    self.__hasConfigFile = True

  def getConfigFilePath(self):
    return self.__configFilePath

  def isConfigured(self):
    if self.__config is None:
      return False
    if not self.__hasConfigFile:
      return False
    return True

  def __doConfigure(self):

    print("DBMS configuration:")
    dbmsusername = input("username: ")
    dbmspassword = input("password: ")
    dbmshostname = input("hostname: ")
    dbmsdatabase = input("database: ")

    if len(dbmsusername) < 1:
      return False
    if len(dbmsdatabase) < 1:
      return False

    configDict = {}
    configDict["DBMS"] = {}
    configDict["DBMS"]["username"] = dbmsusername
    if len(dbmspassword) > 0:
      configDict["DBMS"]["password"] = dbmspassword
    if len(dbmshostname) > 0:
      configDict["DBMS"]["hostname"] = dbmshostname
    configDict["DBMS"]["database"] = dbmsdatabase
    configDict["hostname"] = socket.gethostname()

    self.__config = configDict
    return True

  def getConfig(self):
    config = self.__config.copy()
    config.update(self.__runtimeVars)
    return config

