import os

class TreeWalker():
  
  __workDir = None
  __filesList = []

  def __init__(self, workDir):
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
    return {
        "atime": fesAtime,
        "ctime": fesCtime,
        "mtime": fesMtime,
        "inode": fesInode,
        "mode": fesMode,
        "links": fesLinkN,
        "size": fesSize,
        "name": currentDirEntry.name,
        "path": currentDirEntry.path 
    }
    
