#!/bin/env python

#
# This function allows to get the L1 threshold of the first leg of the DoubleEle trigger
# Accepts:
#   - year of data-taking (2016, 2017 or 2018)
#   - hltTrigger
# Returns list generator of:
#   - leg1 threshold
#   - json for these thresholds
#
def getLeg1ThresholdForDoubleEle(year, hltTrigger='HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL', debug=False):
  import urllib, os, glob
  from FWCore.PythonUtilities.LumiList import LumiList
  def download(url, destination):
    if(debug): print 'Downloading from %s' % url
    try:    os.makedirs(destination)
    except: pass
    urllib.urlretrieve(url, os.path.join(destination, url.split('/')[-1]))

  def subtractLumis(json, jsonToSubtract):
    if(debug): print 'Subtracting %s from %s' % (jsonToSubtract, json)
    lumis = LumiList(filename = json) - LumiList(filename = jsonToSubtract)
    lumis.writeJSON(fileName=json)

  def mergeLumis(json, jsonToMerge):
    if(debug): print 'Merging %s into %s' % (jsonToMerge, json)
    lumis = LumiList(filename = json) + LumiList(filename = jsonToMerge)
    lumis.writeJSON(fileName=json)

  prescalePage = 'https://tomc.web.cern.ch/tomc/triggerPrescales/%s/' % year
  dirToStore   = os.path.join('prescaleInformation', year, hltTrigger)
  download(prescalePage + hltTrigger + '.php', dirToStore)
  with open(os.path.join(dirToStore, hltTrigger + '.php')) as f:
    for line in f:
      if 'prescale1' in line and 'L1_DoubleEG' in line:
	download(prescalePage + line.split('>')[0].split('=')[-1], dirToStore)

  jsonForThreshold = {}
  for json in glob.glob(os.path.join(dirToStore, '*.json')):
    leg1 = int(json.split('L1_DoubleEG_')[-1].split('_')[0].replace('LooseIso', ''))
    leg2 = int(json.split('L1_DoubleEG_')[-1].split('_')[1].replace('LooseIso', ''))
    if leg1 in jsonForThreshold: mergeLumis(jsonForThreshold[leg1], json) # this theshold already exists, so we merge them into the existing one
    else:                        jsonForThreshold[leg1] = json

  thresholdsToSubtract = []
  for threshold in sorted(jsonForThreshold.keys()):  # sorting from low to high thresholds
    if(debug): 
      print
      print 'Preparing json for threshold %s' % str(threshold)
    json = jsonForThreshold[threshold]
    for t in thresholdsToSubtract:
      subtractLumis(json, jsonForThreshold[t])
    if not len(LumiList(filename = json)):
      if(debug): print "empty json"
      continue
    yield threshold, json
    thresholdsToSubtract.append(threshold)

if __name__ == '__main__':
  print 'Testing:'
  for threshold, json in getLeg1ThresholdForDoubleEle('2018', debug=True):
    print threshold, json
