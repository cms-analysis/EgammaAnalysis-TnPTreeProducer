# Lepton mva xml files
This data directory contains the xml files for leptonMva trainings.
These are not to be confused with the electron mva. The leptonMva takes
the electron mva as one of its inputs, but adds additional high-level variables
like using close-jet information in order to optimally discriminate between
prompt and non-prompt leptons. Mostly used in top physics analyses.

Preparation and mapping of the input variables is done in
[leptonMva\_cff.py](EgammaAnalysis/TnPTreeProducer/python/leptonMva_cff.py) and [LeptonMvaProducer.cc](EgammaAnalysis/TnPTreeProducer/plugings/LeptonMvaProducer.cc)
Note that the leptonMva's often uses outdated effective areas (forced by older trainings and availability in nanoAOD which are not recommended by the EGamma POG.

## TOP lepton mva 
Most recent training with best performance, valid for full Run II data.
[2016](el_TOP16_BDTG.weights.xml)
[2017](el_TOP17_BDTG.weights.xml)
[2018](el_TOP18_BDTG.weights.xml)
developer: Kyrill Skovpen [@kvskovpen](https://github.com/kskovpen)

## tZq/ttV lepton mva (as documented in TOP-18-008, TOP-18-009)
Superseeded by the above one
[2016](el_tZqTTV16_BDTG.weights.xml)
[2017](el_tZqTTV17_BDTG.weights.xml)
developer: Willem Verbeke [@wverbeke](https:://github.com/wverbeke/)

## ttH lepton mva (as documented in HIG-18-019)
Superseeded by the above one
[2016](el_ttH16_BDTG.weights.xml)
[2017](el_ttH17_BDTG.weights.xml)
