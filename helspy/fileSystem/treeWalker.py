import os
from datetime import datetime

class TreeWalker():
  
  def __init__(self, workDir):
    self.__filesList = []
    self.__workDir = workDir

  def doWalk(self):
    self.__filesList = self.__walkDir(self.__workDir)

  def getFilesList(self):
    return self.__filesList

  def __walkDir(self, currentDirInstance):
    filesList = []
    for currentDirEntryInstance in os.scandir(currentDirInstance):
      if currentDirEntryInstance.is_symlink():
        continue
      if currentDirEntryInstance.is_dir():
        if not os.access(currentDirEntryInstance.path, os.X_OK):
          continue
        if os.path.ismount(currentDirEntryInstance.path):
          continue
        filesList.extend(self.__walkDir(currentDirEntryInstance.path))
      if currentDirEntryInstance.is_file():
        fileEntryDict = self.__createFileEntryDict(currentDirEntryInstance)
        filesList.append(fileEntryDict)
    return filesList
  
  def __createFileEntryDict(self, currentDirEntry):
    fileEntryStat = currentDirEntry.stat()
    fesAtime = fileEntryStat.st_atime
    fesCtime = fileEntryStat.st_ctime
    fesMtime = fileEntryStat.st_mtime
    fesInode = fileEntryStat.st_ino
    fesMode = oct(fileEntryStat.st_mode)
    fesLinkN = fileEntryStat.st_nlink
    fesSize = fileEntryStat.st_size
    feFileName = currentDirEntry.name
    feFileNameList = feFileName.split(".")
    feFileNameExtension = ""
    if len(feFileNameList) > 1:
      feFileNameExtension = feFileNameList.pop()
    return {
        "atime": datetime.fromtimestamp(fesAtime),
        "ctime": datetime.fromtimestamp(fesCtime),
        "mtime": datetime.fromtimestamp(fesMtime),
        "inode": fesInode,
        "mode": fesMode,
        "links": fesLinkN,
        "size": fesSize,
        "name": feFileName,
        "path": currentDirEntry.path,
        "filenameExtension": feFileNameExtension
    }

