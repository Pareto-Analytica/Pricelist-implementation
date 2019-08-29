from datetime import date

from common import Pipe, SMALL_PIPE_NAME, SMALL_MODEL_JANUARY_DECREASE_KEY, \
    SMALL_MODEL_FEBRUARY_DECREASE_KEY, SMALL_MODEL_MONTH_DECREASE_KEY, SMALL_MODEL_MAX_DIFF_KEY, SMID_SAVE_KEY, \
    NEW_REAL_PRICE_KEY, YEAR_KEY, NEW_ROUNDED_PRICE_KEY, round_to_nearest_hundred, CURRENT_DATE_KEY, SMALL_PIPE_YEAR, \
    ENTERING_PRICE_INFIX_DIGIT, FIRST_MONITOR_INFIX_DIGIT, SMALL_PIPE_THERE_IS_NEW_CAR_PRICE, \
    SMALL_PIPE_LAST_MONTH_PRICE_EXISTS, SMALL_PIPE_SHOULD_BE_CHECKED_MANUALLY, LAST_PRICE_SAVE_KEY, \
    SHOULD_BE_CHECKED_MANUALLY, INFIX_KEY, PipeHistory, MINIMAL_PRICE_TO_CALCULATE_KEY, SMALLER_THAN_MINIMAL_KEY


class SmallPipe(Pipe):
    def __init__(self, config):
        self.name = SMALL_PIPE_NAME
        self.january_decrease = float(config[SMALL_MODEL_JANUARY_DECREASE_KEY])
        self.february_decrease = float(config[SMALL_MODEL_FEBRUARY_DECREASE_KEY])
        self.month_decrease = float(config[SMALL_MODEL_MONTH_DECREASE_KEY])
        self.max_diff = float(config[SMALL_MODEL_MAX_DIFF_KEY])
        self.file_date = config[CURRENT_DATE_KEY]
        self.minimal_price_to_calculate = float(config[MINIMAL_PRICE_TO_CALCULATE_KEY])

    def validate(self, model):
        return True

    def process(self, model):
        for year_num, year in model.years.items():
            price = 0
            year.infix[ENTERING_PRICE_INFIX_DIGIT] = SMALL_PIPE_YEAR
            if year.new_car_price:
                year.infix[FIRST_MONITOR_INFIX_DIGIT] = SMALL_PIPE_THERE_IS_NEW_CAR_PRICE
                this_year_number = self.file_date.year
                month = self.file_date.month
                if this_year_number == year_num:
                    reduction = self.january_decrease
                    month -= 1
                    if month >= 1:
                        reduction += self.february_decrease
                        month -= 1
                    reduction += self.month_decrease * month
                    reduction = 1 - reduction * model.family_data.first_year_reduction
                    price = year.new_car_price * reduction
                else:
                    year_diff = this_year_number - year_num - 1
                    reduction = (1 - model.family_data.first_year_reduction) * (
                            (1 - model.family_data.avg_reduction_annually) ** year_diff)
                    price = year.new_car_price * reduction
                    price = price * (1 + month * model.family_data.p_age)
            else:
                if year.last_price:
                    year.infix[FIRST_MONITOR_INFIX_DIGIT] = SMALL_PIPE_LAST_MONTH_PRICE_EXISTS
                    price = year.last_price * (1 + model.family_data.p_age)
                else:
                    year.infix[FIRST_MONITOR_INFIX_DIGIT] = SMALL_PIPE_SHOULD_BE_CHECKED_MANUALLY
                    year.should_be_checked_manually = True
            year.new_price = price
            if year.last_price and not year.should_be_checked_manually:
                min_price = year.last_price * (1 - self.max_diff)
                max_price = year.last_price * (1 + self.max_diff)
                if price > max_price:
                    year.new_price = max_price
                elif price < min_price:
                    year.new_price = min_price

    def save_and_get_row(self, model):
        rows = []
        for year_num, year in model.years.items():
            year.past_pipes[self.name] = PipeHistory(
                year.new_price,
                year.items_amount,
                year.stdev,
                date.today()
            )
            row = {
                SMID_SAVE_KEY: model.id,
                YEAR_KEY: year.year,
                NEW_REAL_PRICE_KEY: year.new_price,
                NEW_ROUNDED_PRICE_KEY: round_to_nearest_hundred(year.new_price),
                LAST_PRICE_SAVE_KEY: year.last_price,
                SHOULD_BE_CHECKED_MANUALLY: year.should_be_checked_manually,
                INFIX_KEY: ''.join([str(i) for i in year.infix])
            }
            if year.new_price:
                row[SMALLER_THAN_MINIMAL_KEY] = year.new_price < self.minimal_price_to_calculate
            rows.append(row)
        return rows
