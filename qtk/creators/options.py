import QuantLib as ql
from qtk.fields import Field as F
from qtk.templates import Template as T
from .common import InstrumentCreatorBase


class EuropeanOptionCreator(InstrumentCreatorBase):
    _templates = [T.INSTRUMENT_DERIVATIVE_EUROPEANOPTION]
    _req_fields = [F.STRIKE, F.OPTION_TYPE, F.MATURITY_DATE]
    _opt_fields = []

    def _create(self, asof_date):
        strike_price = self[F.STRIKE]
        option_type = self[F.OPTION_TYPE]
        maturity_date = self[F.MATURITY_DATE]

        payoff = ql.PlainVanillaPayoff(option_type, strike_price)
        exercise = ql.EuropeanExercise(maturity_date)
        european_option = ql.VanillaOption(payoff, exercise)
        return european_option