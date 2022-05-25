import sys
import json
import time

class ArgumentsParser():

  progFilePath = None
  progCmdLineArgs = None
  progCmdLineArgsListSize = 0
  __isVerbose = False

  def __init__(self):
    if len(sys.argv) < 2:
      return
    self.progFilePath = sys.argv[0]
    self.progCmdLineArgs = sys.argv[1:]
    if "-v" in self.progCmdLineArgs:
      self.__isVerbose = True
      self.__getRidOfMultipleVerboseArgs()
      self.__showVarsVerbose()
    self.__calcLenCmdLineArgsList()

  def __getRidOfMultipleVerboseArgs(self):
    if "-v" in self.progCmdLineArgs:
      self.progCmdLineArgs.pop(self.progCmdLineArgs.index("-v"))
      self.__getRidOfMultipleVerboseArgs()

  def __calcLenCmdLineArgsList(self):
    self.progCmdLineArgsListSize = len(self.progCmdLineArgs) - 1

  def __showVarsVerbose(self):
    varsDict = { 
        "File Path": self.progFilePath,
        "Command Line Arguments": self.progCmdLineArgs
        }
    outputString = json.dumps(varsDict, indent=2)
    print(time.ctime(time.time()), "\n")
    print(outputString, "\n", "\n")

  def getWorkDir(self):
    if "-d" in self.progCmdLineArgs:
      workDirArgPos = self.progCmdLineArgs.index("-d") + 1
      if workDirArgPos > self.progCmdLineArgsListSize:
        return
      workDir = self.progCmdLineArgs[workDirArgPos]
      if self.__isVerbose == True:
        print(time.ctime(time.time()), "\n")
        print("Working directory argument recognized as:", workDir)
      return workDir
    return

