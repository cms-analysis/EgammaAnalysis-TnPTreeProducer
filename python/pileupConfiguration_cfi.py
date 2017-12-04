import FWCore.ParameterSet.Config as cms

#### MC PU DISTRIBUTIONS
from SimGeneral.MixingModule.mix_2015_25ns_Startup_PoissonOOTPU_cfi import mix as mix_2015_25ns
from SimGeneral.MixingModule.mix_2015_50ns_Startup_PoissonOOTPU_cfi import mix as mix_2015_50ns
from SimGeneral.MixingModule.mix_2015_25ns_FallMC_matchData_PoissonOOTPU_cfi import mix as mix_2015_25ns_realistScenario

from SimGeneral.MixingModule.mix_2016_25ns_SpringMC_PUScenarioV1_PoissonOOTPU_cfi import mix as mix_2016_25ns
from SimGeneral.MixingModule.mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi import mix as mix_2016_25ns_PUmoriond17
from SimGeneral.MixingModule.mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi import mix as mix_2017_MCv2

mix_2017_probValue = cms.vdouble(
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571,0.028571
)

pu_distribs = { "74X_mcRun2_asymptotic_v2"  : mix_2015_25ns.input.nbPileupEvents.probValue,
                "76X_mcRun2_asymptotic_v12" : mix_2015_25ns_realistScenario.input.nbPileupEvents.probValue,
                "80X_mcRun2_asymptotic_v1"  : mix_2016_25ns.input.nbPileupEvents.probValue,
                "80X_mcRun2_asymptotic_v2"  : mix_2016_25ns_PUmoriond17.input.nbPileupEvents.probValue,
                "90X_mcRun2"                : mix_2017_probValue,
                "92X_mcRun2"                : mix_2017_MCv2.input.nbPileupEvents.probValue
                }

#### DATA PU DISTRIBUTIONS
data_pu_distribs = {"Jamboree_golden_JSON" : [5.12e+04,3.66e+05,5.04e+05,4.99e+05,7.5e+05,1.1e+06,2.53e+06,9.84e+06,4.4e+07,1.14e+08,1.94e+08,2.63e+08,2.96e+08,2.74e+08,2.06e+08,1.26e+08,6.38e+07,2.73e+07,1.1e+07,5.2e+06,3.12e+06,1.87e+06,9.35e+05,3.64e+05,1.1e+05,2.64e+04,5.76e+03,1.53e+03,594,278,131,59.8,26,10.8,4.29,1.62,0.587,0.203,0.0669,0.0211,0.00633,0.00182,0.000498,0.00013,3.26e-05,7.77e-06,1.77e-06,3.85e-07,7.99e-08,1.58e-08,3e-09,5.43e-10],
                    "ICHEP2016_JSON_4.0fb_xSec71.3mb" : [1.78e+03,2.69e+04,1.78e+05,4.71e+05,7.61e+05,1.02e+06,1.48e+06,7.35e+06,2.3e+07,3.75e+07,6.01e+07,9.32e+07,1.41e+08,2.09e+08,2.88e+08,3.53e+08,3.93e+08,4.09e+08,4e+08,3.69e+08,3.23e+08,2.69e+08,2.12e+08,1.57e+08,1.09e+08,6.96e+07,4.09e+07,2.19e+07,1.07e+07,4.8e+06,1.99e+06,7.76e+05,2.9e+05,1.07e+05,4.22e+04,1.95e+04,1.16e+04,8.73e+03,7.5e+03,6.85e+03,6.44e+03,6.16e+03,5.96e+03,5.81e+03,5.67e+03,5.53e+03,5.38e+03,5.21e+03,5.01e+03,4.78e+03],
                    "ICHEP2016_JSON_5.7fb_xSec69.0mb" : [2.34e+03,7.7e+04,3.71e+05,7.77e+05,1.17e+06,1.64e+06,2.75e+06,1.34e+07,3.91e+07,8e+07,1.38e+08,1.94e+08,2.57e+08,3.41e+08,4.32e+08,5.08e+08,5.53e+08,5.63e+08,5.42e+08,4.98e+08,4.35e+08,3.6e+08,2.79e+08,2.01e+08,1.33e+08,8.23e+07,4.75e+07,2.58e+07,1.33e+07,6.59e+06,3.16e+06,1.47e+06,6.65e+05,2.91e+05,1.24e+05,5.3e+04,2.4e+04,1.28e+04,8.59e+03,7.04e+03,6.42e+03,6.13e+03,5.95e+03,5.79e+03,5.64e+03,5.47e+03,5.27e+03,5.04e+03,4.79e+03,4.51e+03],
                    "ICHEP2016_JSON_12.9fb_xSec63.0mb": [5.05e+03,2.41e+05,7.83e+05,1.74e+06,2.37e+06,3.41e+06,6.12e+06,2.43e+07,6.78e+07,1.45e+08,2.57e+08,4.06e+08,5.63e+08,7.06e+08,8.41e+08,9.54e+08,1.03e+09,1.06e+09,1.06e+09,1.02e+09,9.47e+08,8.51e+08,7.41e+08,6.19e+08,4.93e+08,3.72e+08,2.67e+08,1.82e+08,1.18e+08,7.18e+07,4.13e+07,2.24e+07,1.15e+07,5.57e+06,2.56e+06,1.12e+06,4.7e+05,1.92e+05,7.78e+04,3.3e+04,1.61e+04,9.87e+03,7.67e+03,6.92e+03,6.66e+03,6.56e+03,6.49e+03,6.4e+03,6.28e+03,6.12e+03],
                    "MORIOND2017_JSON_36fb_xSec69.2mb": [2.39e+05,8.38e+05,2.31e+06,3.12e+06,4.48e+06,6e+06,7e+06,1.29e+07,3.53e+07,7.87e+07,1.77e+08,3.6e+08,6.03e+08,8.77e+08,1.17e+09,1.49e+09,1.76e+09,1.94e+09,2.05e+09,2.1e+09,2.13e+09,2.15e+09,2.13e+09,2.06e+09,1.96e+09,1.84e+09,1.7e+09,1.55e+09,1.4e+09,1.24e+09,1.09e+09,9.37e+08,7.92e+08,6.57e+08,5.34e+08,4.27e+08,3.35e+08,2.58e+08,1.94e+08,1.42e+08,1.01e+08,6.9e+07,4.55e+07,2.88e+07,1.75e+07,1.02e+07,5.64e+06,2.99e+06,1.51e+06,7.32e+05,3.4e+05,1.53e+05,6.74e+04,3.05e+04,1.52e+04,8.98e+03,6.5e+03,5.43e+03,4.89e+03,4.52e+03,4.21e+03,3.91e+03,3.61e+03,3.32e+03,3.03e+03,2.75e+03,2.47e+03,2.21e+03,1.97e+03,1.74e+03,1.52e+03,1.32e+03,1.14e+03,983,839],
                    "2017_DATA_xSec69.2mb_2Nov": [5.55e+04,1.81e+05,3.55e+05,1.16e+06,1.69e+06,2.36e+06,3.16e+06,3.54e+06,4.19e+06,6.16e+06,1.17e+07,2.41e+07,4.82e+07,8.91e+07,1.49e+08,2.29e+08,3.32e+08,4.53e+08,5.71e+08,6.74e+08,7.6e+08,8.22e+08,8.59e+08,8.88e+08,9.22e+08,9.64e+08,1.01e+09,1.04e+09,1.06e+09,1.05e+09,1.02e+09,9.58e+08,8.83e+08,7.96e+08,7.03e+08,6.06e+08,5.11e+08,4.2e+08,3.37e+08,2.64e+08,2.02e+08,1.51e+08,1.11e+08,7.93e+07,5.56e+07,3.83e+07,2.59e+07,1.73e+07,1.14e+07,7.37e+06,4.73e+06,3e+06,1.88e+06,1.17e+06,7.18e+05,4.37e+05,2.62e+05,1.56e+05,9.2e+04,5.37e+04,3.11e+04,1.79e+04,1.02e+04]
 }

    
pileupProducer = cms.EDProducer("PileupWeightProducer",
                                #hardcodedWeights = cms.untracked.bool(True),
                                pileupInfoTag    = cms.InputTag("slimmedAddPileupInfo"),
                 #               PileupMC = cms.vdouble(pu_distribs["80X_mcRun2_asymptotic_v2"]),
                 #               PileupData = cms.vdouble(data_pu_distribs["MORIOND2017_JSON_36fb_xSec69.2mb"]),
                                ####2 Nov
                                PileupMC = cms.vdouble(pu_distribs["90X_mcRun2"]),
                                PileupData = cms.vdouble(data_pu_distribs["2017_DATA_xSec69.2mb_2Nov"]),
                                )
