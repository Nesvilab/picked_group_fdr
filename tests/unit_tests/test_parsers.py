import pytest

import picked_group_fdr.parsers.modifications as mod


class TestMaxQuantToInternal:
  def test_maxquant_to_internal_carbamidomethylation(self):
    assert mod.maxquant_mod_to_unimod(["_ABCDEFGH_"]) == ["ABC[UNIMOD:4]DEFGH"]
  
  def test_maxquant_to_internal_tmt(self):
    fixed_mods = {'C': 'C[UNIMOD:4]',
                  '^_':'_[UNIMOD:737]', 
                  'K': 'K[UNIMOD:737]'}
    assert mod.maxquant_mod_to_unimod(["_ABCDEFGHK_"], fixed_mods) == ["[UNIMOD:737]ABC[UNIMOD:4]DEFGHK[UNIMOD:737]"]
  
  def test_maxquant_to_internal_silac(self):
    fixed_mods = {'C': 'C[UNIMOD:4]',
                  'K': 'K[UNIMOD:259]', 
                  'R': 'R[UNIMOD:267]'}
    assert mod.maxquant_mod_to_unimod(["_ABCDEFGHRK_"], fixed_mods) == ["ABC[UNIMOD:4]DEFGHR[UNIMOD:267]K[UNIMOD:259]"]
  
