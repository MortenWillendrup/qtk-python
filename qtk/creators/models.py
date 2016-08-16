import QuantLib as ql

from qtk.fields import Field as F
from qtk.templates import Template as T
from .common import CreatorBase
from .utils import ScheduleCreator


class InterestModelMixin(object):

    def swaption_helper(self):
        pass


class SwaptionHelperCreator(CreatorBase):
    _vol_type_map = {"SHIFTEDLOGNORMAL": ql.ShiftedLognormal, "NORMAL": ql.Normal}
    _templates = [T.INST_DERIVATIVE_SWAPTION_HELPER]
    _req_fields = [F.VOLATILITY, F.INDEX, F.DISCOUNT_CURVE]
    _opt_fields = [F.MATURITY_DATE, F.MATURITY_TENOR,
                   F.UNDERLYING_MATURITY_DATE, F.UNDERLYING_MATURITY_TENOR,
                   F.FIXED_LEG_TENOR, F.FIXED_LEG_BASIS, F.FLOAT_LEG_BASIS,
                   F.VOLATILITY, F.STRIKE, F.NOTIONAL, F.VOLATILITY_TYPE,
                   F.VOLATILITY_SHIFT]

    def _create(self, asof_date):
        maturity = self.get(F.MATURITY_DATE) or \
                   self.get(F.MATURITY_TENOR)
        undl_maturity = self.get(F.UNDERLYING_MATURITY_DATE) or \
                        self.get(F.UNDERLYING_MATURITY_TENOR)
        assert maturity is not None
        assert undl_maturity is not None
        vols = self[F.VOLATILITY]
        vol_quote = ql.QuoteHandle(ql.SimpleQuote(vols))
        index = self[F.INDEX]
        fixed_tenor = self.get(F.FIXED_LEG_TENOR)
        fixed_basis = self.get(F.FIXED_LEG_BASIS)
        float_basis = self.get(F.FLOAT_LEG_BASIS) or fixed_basis
        fixed_basis = fixed_basis or float_basis
        yield_curve = self[F.DISCOUNT_CURVE]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        strike = self.get(F.STRIKE, ql.nullDouble())
        notional = self.get(F.NOTIONAL, 1.0)
        vol_type = self.get(F.VOLATILITY_TYPE, "ShiftedLogNormal")
        vol_type = vol_type.upper()
        vol_type_enum = self._vol_type_map.get(vol_type, ql.ShiftedLognormal)
        vol_shift = self.get(F.VOLATILITY_SHIFT, 0.0)
        swaption_helper = ql.SwaptionHelper(
            maturity, undl_maturity, vol_quote, index, fixed_tenor, fixed_basis,
            float_basis, yield_handle, ql.CalibrationHelper.RelativePriceError)
        #    strike, notional, vol_type_enum, vol_shift
        #)
        return swaption_helper







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
