import FWCore.ParameterSet.Config as cms

#
# Sequence to add lepton MVA
#
def leptonMvaSequence(process, options, tnpVars):
    #
    # One difficulty with lepton mva's is that their input variables are dependent on jet variables, so we need JEC etc... to be in sync
    # By default we simply re-run the JEC and needed b-tag algorithms, to be sure they are in sync with the used global tag, assuming the training was also up to date
    #
    if(options['isMC']): jetCorrectorLevels = ['L1FastJet', 'L2Relative', 'L3Absolute']
    else:                jetCorrectorLevels = ['L1FastJet', 'L2Relative', 'L3Absolute','L2L3Residual']

    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
    updateJetCollection(
       process,
       jetSource = cms.InputTag('slimmedJets'),
       labelName = 'Updated',
       jetCorrections = ('AK4PFchs', cms.vstring(jetCorrectorLevels), 'None'),
       btagDiscriminators = [
      # 'pfDeepCSVJetTags:probb', # ghent lepton mva uses older version of pfDeepCSV it seems, so do not re-run these
      # 'pfDeepCSVJetTags:probbb',
        'pfDeepFlavourJetTags:probb',
        'pfDeepFlavourJetTags:probbb',
        'pfDeepFlavourJetTags:problepb',
       ],
    )
    leptonMva_sequence = cms.Sequence(process.patAlgosToolsTask)

    #
    # For the calculation of isolations and jet-lep variables we rely on the NanoAOD modules
    # Because in some PAGs people like to use prehistoric effective areas (or some lepton mva developer found 0.00001% better discrimination with those),
    # we need to have the PFIso and MiniIso in all its variations (at least they all use them relative to the lepton pt)
    #
    from PhysicsTools.NanoAOD.electrons_cff import isoForEle, ptRatioRelForEle
    process.ptRatioRelForEle        = ptRatioRelForEle
    process.ptRatioRelForEle.srcJet = cms.InputTag('selectedUpdatedPatJetsUpdated')
    leptonMva_sequence += cms.Sequence(process.ptRatioRelForEle)

    def makeIsoForEle(leptonMva_sequence, name, effAreas):
      isoForEleModule = isoForEle.clone(relative = cms.bool(True))
      setattr(isoForEleModule, 'EAFile_MiniIso', cms.FileInPath(effAreas))
      setattr(isoForEleModule, 'EAFile_PFIso',   cms.FileInPath(effAreas))
      setattr(process, name, isoForEleModule)
      leptonMva_sequence += cms.Sequence(getattr(process, name))

    makeIsoForEle(leptonMva_sequence, 'isoForEleFall17',   'RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_94X.txt')
    makeIsoForEle(leptonMva_sequence, 'isoForEleSummer16', 'RecoEgamma/ElectronIdentification/data/Summer16/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_80X.txt')
    makeIsoForEle(leptonMva_sequence, 'isoForEleSpring15', 'RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_25ns.txt')

    #
    # Calculate the lepton mva's
    #   (at some point we can clean up the older TTH and Ghent ones, keeping only the TOP)
    #
    process.leptonMvaTTH = cms.EDProducer('LeptonMvaProducer',
      leptonMvaType        = cms.string("leptonMvaTTH"),
      weightFile           = cms.FileInPath('EgammaAnalysis/TnPTreeProducer/data/el_ttH%s_BDTG.weights.xml' % ('16' if '2016' in options['era'] else '17')),
      probes               = cms.InputTag('slimmedElectrons'),
      miniIsoChg           = cms.InputTag('isoForEle%s:miniIsoChg' % ('Spring15' if '2016' in options['era'] else 'Fall17')),
      miniIsoAll           = cms.InputTag('isoForEle%s:miniIsoAll' % ('Spring15' if '2016' in options['era'] else 'Fall17')),
      ptRatio              = cms.InputTag('ptRatioRelForEle:ptRatio'),
      ptRel                = cms.InputTag('ptRatioRelForEle:ptRel'),
      jetNDauChargedMVASel = cms.InputTag('ptRatioRelForEle:jetNDauChargedMVASel'),
      closestJet           = cms.InputTag('ptRatioRelForEle:jetForLepJetVar'),
      mvas                 = cms.InputTag('electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2Values'),
      debug                = cms.bool(False), # set to True if you want to sync with your analysis
    )

    process.leptonMvaGhent = cms.EDProducer('LeptonMvaProducer',
      leptonMvaType        = cms.string("leptonMvaGhent"),
      weightFile           = cms.FileInPath('EgammaAnalysis/TnPTreeProducer/data/el_tZqTTV%s_BDTG.weights.xml' % ('16' if '2016' in options['era'] else '17')),
      probes               = cms.InputTag('slimmedElectrons'),
      miniIsoChg           = cms.InputTag('isoForEle%s:miniIsoChg' % ('Spring15' if '2016' in options['era'] else 'Fall17')),
      miniIsoAll           = cms.InputTag('isoForEle%s:miniIsoAll' % ('Spring15' if '2016' in options['era'] else 'Fall17')),
      PFIsoAll             = cms.InputTag('isoForEle%s:PFIsoAll' % ('Summer16' if '2016' in options['era'] else 'Fall17')),
      ptRatio              = cms.InputTag('ptRatioRelForEle:ptRatio'),
      ptRel                = cms.InputTag('ptRatioRelForEle:ptRel'),
      jetNDauChargedMVASel = cms.InputTag('ptRatioRelForEle:jetNDauChargedMVASel'),
      closestJet           = cms.InputTag('ptRatioRelForEle:jetForLepJetVar'),
      mvas                 = cms.InputTag('electronMVAValueMapProducer:ElectronMVAEstimator%sValues' % ('Run2Spring16GeneralPurposeV1' if '2016' in options['era'] else 'Run2Fall17NoIsoV1')),
      debug                = cms.bool(False), # set to True if you want to sync with your analysis
    )

    process.leptonMvaTOP = cms.EDProducer('LeptonMvaProducer',
      leptonMvaType        = cms.string("leptonMvaTOP"),
      weightFile           = cms.FileInPath('EgammaAnalysis/TnPTreeProducer/data/el_TOP%s_BDTG.weights.xml' % (options['era'].replace('20', '').replace('UL', ''))),
      probes               = cms.InputTag('slimmedElectrons'),
      miniIsoChg           = cms.InputTag('isoForEle%s:miniIsoChg' % ('Spring15' if '2016' in options['era'] else 'Fall17')),
      miniIsoAll           = cms.InputTag('isoForEle%s:miniIsoAll' % ('Spring15' if '2016' in options['era'] else 'Fall17')),
      PFIsoAll             = cms.InputTag('isoForEle%s:PFIsoAll' % ('Summer16' if '2016' in options['era'] else 'Fall17')),
      ptRatio              = cms.InputTag('ptRatioRelForEle:ptRatio'),
      ptRel                = cms.InputTag('ptRatioRelForEle:ptRel'),
      jetNDauChargedMVASel = cms.InputTag('ptRatioRelForEle:jetNDauChargedMVASel'),
      closestJet           = cms.InputTag('ptRatioRelForEle:jetForLepJetVar'),
      mvas                 = cms.InputTag('electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV2Values'),
      debug                = cms.bool(False), # set to True if you want to sync with your analysis
    )

    leptonMva_sequence += cms.Sequence(
      process.leptonMvaTTH +
      process.leptonMvaGhent +
      process.leptonMvaTOP
    )

    #
    # Adding the new variables to the trees
    #   (currently only adding most recent version of miniIso)
    #
    newVariables = {
      'el_leptonMva_ttH'         : cms.InputTag('leptonMvaTTH:leptonMvaTTH'),
      'el_leptonMva_ghent'       : cms.InputTag('leptonMvaGhent:leptonMvaGhent'),
      'el_leptonMva_TOP'         : cms.InputTag('leptonMvaTOP:leptonMvaTOP'),
      'el_miniIsoAll_fall17'     : cms.InputTag('isoForEleFall17:miniIsoAll'),
      'el_miniIsoChg_fall17'     : cms.InputTag('isoForEleFall17:miniIsoChg'),
      'el_relIso_fall17'         : cms.InputTag('isoForEleFall17:PFIsoAll'),
      'el_ptRatio'               : cms.InputTag('ptRatioRelForEle:ptRatio'),
      'el_ptRel'                 : cms.InputTag('ptRatioRelForEle:ptRel'),
      'el_closestJetDeepFlavour' : cms.InputTag('leptonMvaTOP:closestJetDeepFlavour'), # For those crazy people who want to add even more cuts on top of their leptonMva but can't tell why they need it
      'el_closestJetDeepCsv'     : cms.InputTag('leptonMvaTOP:closestJetDeepCsv'),
    }
    for i, j in newVariables.iteritems():
      setattr(tnpVars.CommonStuffForGsfElectronProbe.variables, i, j)

    return leptonMva_sequence
