import sys
import json
import time
import os

class ArgumentsParser():

  __progFilePath = None
  __progCmdLineArgs = None
  __progCmdLineArgsListSize = 0
  __isVerbose = False

  def __init__(self):
    if len(sys.argv) < 2:
      return
    self.__progFilePath = sys.argv[0]
    self.__progCmdLineArgs = sys.argv[1:]
    if "-v" in self.__progCmdLineArgs:
      self.__isVerbose = True
      self.__getRidOfMultipleVerboseArgs()
      self.__showVarsVerbose()
    self.__calcLenCmdLineArgsList()

  def __getRidOfMultipleVerboseArgs(self):
    if "-v" in self.__progCmdLineArgs:
      self.__progCmdLineArgs.pop(self.__progCmdLineArgs.index("-v"))
      self.__getRidOfMultipleVerboseArgs()

  def __calcLenCmdLineArgsList(self):
    self.__progCmdLineArgsListSize = len(self.__progCmdLineArgs) - 1

  def __showVarsVerbose(self):
    varsDict = { 
        "File Path": self.__progFilePath,
        "Command Line Arguments": self.__progCmdLineArgs
        }
    outputString = json.dumps(varsDict, indent=2)
    print(time.ctime(time.time()), "\n")
    print(outputString, "\n", "\n")

  def getWorkDir(self):
    if "-d" in self.__progCmdLineArgs:
      workDirArgPos = self.__progCmdLineArgs.index("-d") + 1
      if workDirArgPos > self.__progCmdLineArgsListSize:
        return
      workDir = self.__progCmdLineArgs[workDirArgPos]
      if self.__isVerbose == True:
        print(time.ctime(time.time()), "\n")
        print("Working directory argument recognized as:", workDir)
      return workDir
    return

  def getProgFilePath(self):
    return self.__progFilePath

  def getProgDirPath(self):
    absoluteProgPath = os.path.abspath(self.__progFilePath)
    return os.path.dirname(absoluteProgPath)

