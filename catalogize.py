#!/bin/env python3

from helspy.program import argumentsParser
from helspy.program import workDirVerifier
from helspy.program import configurator
from helspy.fileSystem import treeWalker

if __name__ == "__main__":
  ap = argumentsParser.ArgumentsParser()
  cfgr = configurator.Configurator(ap.getProgDirPath())
  wdv = workDirVerifier.WorkDirVerifier(ap.getWorkDir())
  if wdv.isValidated():
    workDir = wdv.getWorkDir()
    twa = treeWalker.TreeWalker(workDir)
    twa.doWalk()
    print(len(twa.getFilesList()))
  else:
    wdv.printErrorList()
