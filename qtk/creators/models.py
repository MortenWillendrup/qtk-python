import QuantLib as ql

from qtk.fields import Field as F
from qtk.templates import Template as T
from .common import CreatorBase
from .utils import ScheduleCreator


class InterestModelMixin(object):

    def swaption_helper(self):
        pass


class SwaptionHelperCreator(CreatorBase):
    _templates = [T.INST_DERIVATIVE_SWAPTION_HELPER]
    _req_fields = [F.CURRENCY]
    _opt_fields = [F.MATURITY_DATE, F.MATURITY_TENOR,
                   F.UNDERLYING_MATURITY_DATE, F.UNDERLYING_MATURITY_TENOR,
                   F.VOLATILITY, F.INDEX,


    ]





class HullWhite1FCreator(CreatorBase):
    _templates = [T.MODELS_YIELD_HW1F]
    _req_fields = [F.YIELD_CURVE]
    _opt_fields = [F.ALPHA, F.SIGMA1, F.INSTRUMENT_COLLECTION]

    def _create(self, asof_date):
        alpha = self.get(F.ALPHA)
        sigma1 = self.get(F.SIGMA1)
        yield_curve = self[F.YIELD_CURVE]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)

        model = ql.HullWhite(yield_handle, alpha, sigma1)

        return model
