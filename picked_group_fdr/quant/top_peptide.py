from typing import List, Dict
import logging

from .. import helpers
from .base import ProteinGroupColumns

# for type hints only
from .precursor_quant import PrecursorQuant
from ..results import ProteinGroupResults

logger = logging.getLogger(__name__)


class TopPeptideProbabilityColumns(ProteinGroupColumns):
    def append_headers(
        self,
        protein_group_results: ProteinGroupResults,
        experiments: List[str],
    ) -> None:    
        protein_group_results.append_header("Top Peptide Probability")

    def append_columns(
        self,
        protein_group_results: ProteinGroupResults,
        experiment_to_idx_map: Dict[str, int],
        post_err_prob_cutoff: float,
    ) -> None:
        logger.info("Doing quantification: Top Peptide Probability")
        for pgr in protein_group_results:
            top_peptide_probability = _top_peptide_probability(
                pgr.precursorQuants
            )
            pgr.append("%.3f" % (top_peptide_probability, ))


def _top_peptide_probability(
    precursor_list: List[PrecursorQuant],
) -> float:
    top_peptide_probability = 0.0
    for precursor in precursor_list:
        if (
            not helpers.isMbr(precursor.post_err_prob) and
            1.0 - precursor.post_err_prob > top_peptide_probability
        ):
            top_peptide_probability = 1.0 - precursor.post_err_prob
    return top_peptide_probability