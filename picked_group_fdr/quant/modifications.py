from typing import List, Dict
import logging

from .. import helpers
from .base import ProteinGroupColumns

# for type hints only
from .precursor_quant import PrecursorQuant
from ..results import ProteinGroupResults

logger = logging.getLogger(__name__)


class ModificationsColumns(ProteinGroupColumns):
    def append_headers(
        self,
        protein_group_results: ProteinGroupResults,
        experiments: List[str],
    ) -> None:
        protein_group_results.append_headers(
            ["Razor Assigned Modifications", "Razor Observed Modifications"]
        )

    def append_columns(
        self,
        protein_group_results: ProteinGroupResults,
        experiment_to_idx_map: Dict[str, int],
        post_err_prob_cutoff: float,
    ) -> None:
        logger.info("Doing quantification: Assigned and observed modifications")
        for pgr in protein_group_results:
            pepCounts = _collect_modifications(
                pgr.precursorQuants, post_err_prob_cutoff
            )
            pgr.extend(pepCounts)


def _collect_modifications(
    precursor_list: List[PrecursorQuant],
    post_err_prob_cutoff: float,
):
    assigned_mods = dict()
    observed_mods = dict()
    for precursor in precursor_list:
        if (
            helpers.isMbr(precursor.post_err_prob)
            or precursor.post_err_prob <= post_err_prob_cutoff
        ):
            if len(precursor.assigned_mods) > 0:
                assigned_mods[(precursor.peptide, precursor.charge)] = precursor.assigned_mods
            if len(precursor.observed_mods) > 0:
                observed_mods[(precursor.peptide, precursor.charge)] = precursor.observed_mods
    assigned_modifications = ", ".join(assigned_mods.values())
    observed_modifications = ", ".join(observed_mods.values())
    return [assigned_modifications, observed_modifications]