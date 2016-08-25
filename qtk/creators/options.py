import QuantLib as ql
from qtk.fields import Field as F
from .common import CreatorBase


class EuropeanOptionCreator(CreatorBase):
    _templates = []
    _req_fields = [F.STRIKE, ]
    _opt_fields = []

    def _create(self, asof_date):
        pass