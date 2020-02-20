#include "PhysicsTools/SelectorUtils/interface/CutApplicatorBase.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "RecoEgamma/ElectronIdentification/interface/EBEECutValues.h"

class PatEleEBEECut : public CutApplicatorBase {
public:
  PatEleEBEECut(const edm::ParameterSet& c)
      : CutApplicatorBase(c),
      cutFormula_(c.getParameter<std::string>("cutString")),
      cutValue_(c, "cutValue") {}

  result_type operator()(const pat::ElectronPtr& cand) const final {
    return cutFormula_(*cand) < cutValue_(cand);
  }

  double value(const reco::CandidatePtr& cand) const final {
    pat::ElectronPtr ele(cand);
    return cutFormula_(*ele);
  }

  CandidateType candidateType() const final { return PATELECTRON; }

private:
  StringObjectFunction<pat::Electron> cutFormula_;
  const EBEECutValuesT<double> cutValue_;
};

DEFINE_EDM_PLUGIN(CutApplicatorFactory, PatEleEBEECut, "PatEleEBEECut");
