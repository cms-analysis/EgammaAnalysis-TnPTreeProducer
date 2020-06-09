import os

def get_cmssw_version():
  return [int(x) for x in os.environ['CMSSW_VERSION'].split('_')[1:4]]

def isReleaseAbove(major, minor, sub=None):
  cmssw_version = get_cmssw_version()
  if   (cmssw_version[0] > major): return True
  elif (cmssw_version[0] == major) and (cmssw_version[1] > minor): return True
  elif (cmssw_version[0] == major) and (cmssw_version[1] == minor) and (cmssw_version[2] >= sub if sub else True): return True
  return False
