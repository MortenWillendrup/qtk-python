import QuantLib as ql
from .common import CreatorBase


class EuropeanOptionCreator(CreatorBase):
    _templates = []
    _req_fields = []
    _opt_fields = []

    def _create(self, asof_date):
        pass