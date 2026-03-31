"""Aggregated topic tree."""
from .filters_branch import FILTERS_BRANCH
from .op_amp_branch import OP_AMP_BRANCH

TOPICS = {
    "Filters": FILTERS_BRANCH,
    "Op-Amp Circuits": OP_AMP_BRANCH,
}
