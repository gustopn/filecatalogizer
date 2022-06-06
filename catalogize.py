#!/bin/env python3

import time
from datetime import datetime

from helspy.program import argumentsParser
from helspy.program import workDirVerifier
from helspy.program import configurator
from helspy.fileSystem import treeWalker
from helspy.database import databaseConnection

if __name__ == "__main__":
  ap = argumentsParser.ArgumentsParser()
  wdv = workDirVerifier.WorkDirVerifier(ap.getWorkDir())
  # TODO: If this does not verify just return None and quit
  runtimeVars = {
    "configfileDirPath": ap.getProgDirPath(),
    "timestamp": datetime.fromtimestamp(time.time()),
    "mountpoint": wdv.getWorkDir(),
    "filesystem": wdv.getFilesystemOfWorkDir()
  }
  cfgr = configurator.Configurator(runtimeVars)
  if wdv.isValidated():
    twa = treeWalker.TreeWalker(runtimeVars["mountpoint"])
    twa.doWalk()
    print(len(twa.getFilesList()))
  else:
    wdv.printErrorList()
  dbmsConn = databaseConnection.DatabaseConnection(cfgr.getConfig())
  dbmsConn.persist(twa.getFilesList())

