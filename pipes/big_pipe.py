from common import Validator, Model, ModelYear, BIG_PIPE_NAME


class BigPipeValidator(Validator):
    def __init__(self):
        self.name = BIG_PIPE_NAME

    def validate(self, model):
        if model.was_pipe(self.name):
            return True
        for year_num, year in model.years.items():
            if year.stat_price is not None and year.stat_price:
                return True
        return False

    def set_entering_prices(self, model):
        pass

    def process(self, model):
        self.set_entering_prices(model)


class BigPipeData:
    def __init__(self):
        self.entering_price = None
