import json
import bz2

class Configurator():

  __configFilePath = None
  __hasConfigFile = False
  __config = None

  def __init__(self, configFileDirPath):
    self.__configFilePath = configFileDirPath + "/config.json.bz2"
    if os.path.isfile(self.__configFilePath):
      configDataCompressed = open(self.__configFilePath, "r").read()
      configDataJSON = bz2.decompress(configDataCompressed)
      self.__config = json.loads(configDataJSON)
    else:
      if not self.__doConfigure():
        return
      configDataJSON = json.dumps(self.__config, indent=2)
      configDataCompressed = bz2.compress(configDataJSON)
      if not os.path.exists(self.__configFilePath):
        configFileHandle = open(self.__configFilePath, "w")
        configFileHandle.write(configDataCompressed)

  def getConfigFilePath(self):
    return self.__configFilePath

  def isConfigured(self):
    if not self.__hasConfigFile:
      return False

  def __doConfigure(self):
    configDict = {}
    configDict["DBMS"] = {}
    configDict["DBMS"]["username"] = ""
    configDict["DBMS"]["password"] = ""
    configDict["DBMS"]["hostname"] = ""
    self.__config = configDict
    return False
