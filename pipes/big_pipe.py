from datetime import date

from common import Pipe, Model, ModelYear, BIG_PIPE_NAME, FIRST_MONITOR_MIN_KEY, FIRST_MONITOR_MIN_FLAG_KEY, \
    PipeHistory, SMID_SAVE_KEY, YEAR_KEY, NEW_REAL_PRICE_KEY, NEW_ROUNDED_PRICE_KEY, FIRST_MONITOR_MIN_SAVE_KEY, \
    FIRST_MONITOR_MAX_SAVE_KEY, FIRST_MONITOR_PRICE_SAVE_KEY, SECOND_MONITOR_PRICE_SAVE_KEY, \
    SECOND_MONITOR_DIFF_BETWEEN_YEARS_SAVE_KEY, SECOND_MONITOR_DIFF_BETWEEN_STDEV_YEARS_SAVE_KEY, LAST_PRICE_SAVE_KEY, \
    ITEMS_AMOUNT_SAVE_KEY, STDEV_SAVE_KEY, round_to_nearest_hundred, STATISTIC_PRICE_KEY, ENTERING_PRICE_KEY, \
    THIS_MONTH_HAS_STATISTIC_PRICE, ENTERING_PRICE_INFIX_DIGIT, PAST_MONTH_HAD_STATISTIC_PRICE, \
    PRICE_BASED_ON_OTHER_MONTH, MINIMAL_PRICE_TO_CALCULATE_KEY, PRICE_LOWER_THAN_MINIMAL_TO_SHOW, \
    FIRST_MONITOR_INFIX_DIGIT, FIRST_MONITOR_VALID, FIRST_MONITOR_SMALLER_THAN_VALID, FIRST_MONITOR_BIGGER_THAN_VALID, \
    SECOND_MONITOR_UP_INFIX_DIGIT, SECOND_MONITOR_VALID, SECOND_MONITOR_SMALLER, SECOND_MONITOR_BIGGER, \
    SECOND_MONITOR_DOWN_INFIX_DIGIT, DEFAULT_INFIX_DIGIT_VALUE, SECOND_MONITOR_DID_CAR_PRICE_CHANGE_INFIX_DIGIT, \
    SECOND_MONITOR_CHANGED_CAR_WITH_LOWER_YEAR, SECOND_MONITOR_CHANGED_CAR_TWICE, \
    SECOND_MONITOR_CHANGED_CAR_WITH_HIGHER_YEAR, SECOND_MONITOR_CHECK_INFIX_DIGIT, \
    SECOND_MONITOR_CHECK_FIXED_AND_SMALLER, SECOND_MONITOR_CHECK_FIXED_AND_BIGGER, SHOULD_BE_CHECKED_MANUALLY, \
    INFIX_KEY, \
    ROUND_DIGITS, SMALLER_THAN_MINIMAL_KEY


def get_year_index(years, year_to_find):
    for idx, year in enumerate(years):
        if year.year == year_to_find.year:
            return idx
    return -1


def set_infix(year, infix_digit, infix_value, infix_if_exists):
    if year.infix[infix_digit] == DEFAULT_INFIX_DIGIT_VALUE:
        year.infix[infix_digit] = infix_value
    else:
        year.infix[infix_digit] = infix_if_exists


# Relies on first being smaller than second
def is_first_stronger_than_second(first_year, second_year):
    items_diff = first_year.items_amount - second_year.items_amount
    stdev_diff = first_year.stdev - second_year.stdev
    if -1 <= items_diff < 4 and stdev_diff > 4:
        return False
    if -4 <= items_diff < 1 and stdev_diff < -4:
        return True
    else:
        years = [first_year, second_year]
        years.sort(key=lambda year: (year.items_amount, year.stdev), reverse=True)
        return years[0] == first_year


def second_control_fix_values(first_year, second_year, family_stat):
    if is_first_stronger_than_second(first_year, second_year):
        if not first_year.second_monitor_price:
            first_year.second_monitor_price = first_year.first_monitor_price
        second_year.second_monitor_price = first_year.second_monitor_price * (
                family_stat ** (second_year.year - first_year.year))
        second_year.items_amount = first_year.items_amount
        second_year.stdev = first_year.stdev
        if second_year.infix[SECOND_MONITOR_DID_CAR_PRICE_CHANGE_INFIX_DIGIT] == DEFAULT_INFIX_DIGIT_VALUE:
            second_year.infix[
                SECOND_MONITOR_DID_CAR_PRICE_CHANGE_INFIX_DIGIT] = SECOND_MONITOR_CHANGED_CAR_WITH_LOWER_YEAR
        else:
            set_infix(second_year, SECOND_MONITOR_DID_CAR_PRICE_CHANGE_INFIX_DIGIT,
                      SECOND_MONITOR_CHANGED_CAR_WITH_LOWER_YEAR, SECOND_MONITOR_CHANGED_CAR_TWICE)

    else:
        if not second_year.second_monitor_price:
            second_year.second_monitor_price = second_year.first_monitor_price
        first_year.second_monitor_price = second_year.second_monitor_price / (
                family_stat ** (second_year.year - first_year.year))
        first_year.items_amount = second_year.items_amount
        first_year.stdev = second_year.stdev
        set_infix(first_year, SECOND_MONITOR_DID_CAR_PRICE_CHANGE_INFIX_DIGIT,
                  SECOND_MONITOR_CHANGED_CAR_WITH_HIGHER_YEAR, SECOND_MONITOR_CHANGED_CAR_TWICE)


def validate_smaller_than_new_car(model):
    for year_num, year in model.years.items():
        if year.new_car_price:
            if year.new_car_price * (1 - model.family_data.new_car_nylon_reduction) <= year.second_monitor_price:
                year.should_be_checked_manually = True


def get_price_from_other_year(model, year_num, reference_year_num, reference_year_price):
    if year_num < reference_year_num:
        return reference_year_price * (
                (1 - model.family_data.avg_reduction_annually) ** (reference_year_num - year_num))
    else:

        return reference_year_price * (
                (1 + model.family_data.avg_reduction_annually) ** (year_num - reference_year_num))


class BigPipe(Pipe):
    def __init__(self, config):
        self.name = BIG_PIPE_NAME
        self.first_monitor_min = float(config[FIRST_MONITOR_MIN_KEY])
        self.first_monitor_flag = float(config[FIRST_MONITOR_MIN_FLAG_KEY])
        self.minimal_price_to_calculate = float(config[MINIMAL_PRICE_TO_CALCULATE_KEY])

    def validate(self, model):
        if model.was_pipe(self.name):
            return True
        for year_num, year in model.years.items():
            if year.stat_price is not None and year.stat_price:
                return True
        return False

    def process(self, model):
        self.set_model_entering_prices(model)
        self.first_monitor(model)
        self.second_monitor(model)
        validate_smaller_than_new_car(model)
        for year_num, year in model.years.items():
            year.new_price = year.second_monitor_price

        for year_num, year in model.years.items():
            print(
                "Model : {} Year : {} First Monitor : {}    Second Monitor : {} Items : {} Should be checked manually : {}".format(
                    model.id, year_num,
                    int(year.first_monitor_price),
                    int(year.second_monitor_price),
                    year.items_amount,
                    year.should_be_checked_manually))

    def save_and_get_row(self, model):
        rows = []
        for year_num, year in model.years.items():
            row = {}
            year.past_pipes[self.name] = PipeHistory(
                year.new_price,
                year.items_amount,
                year.stdev,
                date.today()
            )
            row[SMID_SAVE_KEY] = model.id
            row[YEAR_KEY] = year.year
            row[STATISTIC_PRICE_KEY] = year.stat_price
            row[ENTERING_PRICE_KEY] = year.entering_price
            row[NEW_REAL_PRICE_KEY] = year.new_price
            row[NEW_ROUNDED_PRICE_KEY] = round_to_nearest_hundred(year.new_price)
            row[FIRST_MONITOR_MIN_SAVE_KEY] = year.min_price
            row[FIRST_MONITOR_MAX_SAVE_KEY] = year.max_price
            row[FIRST_MONITOR_PRICE_SAVE_KEY] = year.first_monitor_price
            row[SECOND_MONITOR_PRICE_SAVE_KEY] = year.second_monitor_price
            row[SECOND_MONITOR_DIFF_BETWEEN_YEARS_SAVE_KEY] = year.monitoring_2_prec_change
            row[SECOND_MONITOR_DIFF_BETWEEN_STDEV_YEARS_SAVE_KEY] = year.monitoring_2_stdev_change
            row[LAST_PRICE_SAVE_KEY] = year.last_price
            row[ITEMS_AMOUNT_SAVE_KEY] = year.items_amount
            row[STDEV_SAVE_KEY] = year.stdev
            row[SHOULD_BE_CHECKED_MANUALLY] = year.should_be_checked_manually
            if year.new_price and year.new_price < self.minimal_price_to_calculate:
                row[SMALLER_THAN_MINIMAL_KEY] = True
            row[INFIX_KEY] = ''.join([str(i) for i in year.infix])
            rows.append(row)
        return rows

    def set_model_entering_prices(self, model):
        is_there_reference_in_current_year, reference_year = self.get_reference_year(model)
        for year_num, year in model.years.items():
            self.get_year_entering_price(model, year, is_there_reference_in_current_year, reference_year)
            if year.entering_price < self.minimal_price_to_calculate:
                year.infix[ENTERING_PRICE_INFIX_DIGIT] = PRICE_LOWER_THAN_MINIMAL_TO_SHOW

    def first_monitor(self, model):
        for year_num, year in model.years.items():
            # If there is no past price, no reason checking.
            if year.last_price:
                curr_price = year.entering_price
                max_price = year.last_price
                min_price = max_price * (1 - self.first_monitor_min)
                year.min_price = min_price
                year.max_price = max_price
                if max_price >= curr_price >= min_price:
                    year.bigger_flag_amount = 0
                    year.first_monitor_price = curr_price
                    year.infix[FIRST_MONITOR_INFIX_DIGIT] = FIRST_MONITOR_VALID
                elif curr_price < min_price:
                    year.first_monitor_price = min_price
                    year.bigger_flag_amount = 0
                    year.infix[FIRST_MONITOR_INFIX_DIGIT] = FIRST_MONITOR_SMALLER_THAN_VALID
                elif curr_price > max_price:

                    year.infix[FIRST_MONITOR_INFIX_DIGIT] = FIRST_MONITOR_BIGGER_THAN_VALID
                    if year.bigger_flag_amount <= self.first_monitor_flag:
                        year.first_monitor_price = max_price
                        year.bigger_flag_amount += 1
                    else:
                        bigger_max = max_price * (1 + self.first_monitor_min)
                        year.min_price = max_price
                        year.max_price = bigger_max
                        if curr_price > bigger_max:
                            year.first_monitor_price = bigger_max
                            year.bigger_flag_amount += 1
                        else:
                            year.first_monitor_price = curr_price
                            year.bigger_flag_amount = 0
            else:
                year.first_monitor_price = year.entering_price

    def second_monitor(self, model):
        is_there_reference_in_current_year, reference_year = self.get_reference_year(model)
        years = [year for year_num, year in model.years.items()]
        years.sort(key=lambda year: year.year)
        reference_index = get_year_index(years, reference_year)
        reference_year.second_monitor_price = reference_year.first_monitor_price
        reference_year.infix[SECOND_MONITOR_UP_INFIX_DIGIT] = SECOND_MONITOR_VALID

        # Going from biggest items amount up
        for i in range(reference_index, len(years) - 1, 1):
            smaller = years[i]
            bigger = years[i + 1]
            ratio = round(bigger.first_monitor_price / smaller.second_monitor_price, ROUND_DIGITS)
            self.second_monitor_calculate_years(model, ratio, bigger, smaller, bigger, SECOND_MONITOR_UP_INFIX_DIGIT)
        # Going from biggest items amount down
        for i in range(reference_index, 0, -1):
            smaller = years[i - 1]
            bigger = years[i]
            ratio = bigger.second_monitor_price / smaller.first_monitor_price
            self.second_monitor_calculate_years(model, ratio, bigger, smaller, smaller, SECOND_MONITOR_DOWN_INFIX_DIGIT)

        self.second_monitor_validate_years_diff_after(model, years)
        self.second_monitor_validate_years_max(years)

    def second_monitor_calculate_years(self, model, ratio, bigger, smaller, year_to_update, infix_digit):
        second_monitor_max, second_monitor_min = self.get_min_max(bigger, model, smaller)
        year_to_update.monitoring_2_prec_change = ratio
        year_to_update.monitoring_2_stdev_change = bigger.stdev - smaller.stdev
        if second_monitor_min <= ratio <= second_monitor_max:
            year_to_update.second_monitor_price = year_to_update.first_monitor_price
            year_to_update.infix[SECOND_MONITOR_UP_INFIX_DIGIT] = SECOND_MONITOR_VALID
            year_to_update.infix[SECOND_MONITOR_DOWN_INFIX_DIGIT] = SECOND_MONITOR_VALID

        elif ratio < model.family_data.family_bottom:
            second_control_fix_values(smaller, bigger, model.family_data.family_bottom)
            year_to_update.infix[infix_digit] = SECOND_MONITOR_SMALLER
        else:
            second_control_fix_values(smaller, bigger, model.family_data.family_top)
            year_to_update.infix[infix_digit] = SECOND_MONITOR_BIGGER

    def get_min_max(self, bigger, model, smaller):
        second_monitor_min = model.family_data.family_bottom ** (bigger.year - smaller.year)
        second_monitor_max = model.family_data.family_top ** (bigger.year - smaller.year)
        return second_monitor_max, second_monitor_min

    def second_monitor_validate_years_max(self, years):
        for year in years:
            if year.last_price and year.second_monitor_price:
                if not (year.min_price <= year.second_monitor_price <= year.max_price):
                    year.should_be_checked_manually = True

    def second_monitor_validate_years_diff_after(self, model, years):
        for i in range(len(years) - 1):
            ratio = round(years[i + 1].second_monitor_price / years[i].second_monitor_price, ROUND_DIGITS)
            second_monitor_max, second_monitor_min = self.get_min_max(years[i + 1], model, years[i])
            if not (second_monitor_min <= ratio <= second_monitor_max):
                if is_first_stronger_than_second(years[i], years[i + 1]):
                    if ratio < second_monitor_min:
                        years[i + 1].infix[SECOND_MONITOR_CHECK_INFIX_DIGIT] = SECOND_MONITOR_CHECK_FIXED_AND_SMALLER
                    else:
                        years[i + 1].infix[SECOND_MONITOR_CHECK_INFIX_DIGIT] = SECOND_MONITOR_CHECK_FIXED_AND_BIGGER
                    years[i + 1].should_be_checked_manually = True
                else:
                    years[i].should_be_checked_manually = True
                    if ratio < second_monitor_min:
                        years[i].infix[SECOND_MONITOR_CHECK_INFIX_DIGIT] = SECOND_MONITOR_CHECK_FIXED_AND_SMALLER
                    else:
                        years[i].infix[SECOND_MONITOR_CHECK_INFIX_DIGIT] = SECOND_MONITOR_CHECK_FIXED_AND_BIGGER

    def get_reference_year(self, model):
        is_there_reference_in_current_year = False
        years = [year for year_num, year in model.years.items()]
        sorted_years = sorted(years, key=lambda year: (year.items_amount, -year.stdev), reverse=True)
        if sorted_years[0].items_amount > 0:
            reference_year = sorted_years[0]
            is_there_reference_in_current_year = True

        else:
            old_years = []
            for year_num, year in model.years.items():
                if self.was_big_model_in_past(year):
                    old_years.append(year)
            sorted_old_years = sorted(old_years, key=lambda year: (
                year.past_pipes[self.name].items_amount, -year.past_pipes[self.name].stdev), reverse=True)
            reference_year = sorted_old_years[0]
        return is_there_reference_in_current_year, reference_year

    def get_year_entering_price(self, model, year, is_there_reference_in_current_year, reference_year):
        if year.stat_price:
            year.entering_price = year.stat_price
            year.items_amount = year.items_amount
            year.stdev = year.stdev
            year.infix[ENTERING_PRICE_INFIX_DIGIT] = THIS_MONTH_HAS_STATISTIC_PRICE
            return
        if self.was_big_model_in_past(year):
            # print(" Model : {} , Year : {} is in based on past of himself".format(model.id, year.year))
            year.entering_price = year.last_price * (1 + model.family_data.p_age)
            year.infix[ENTERING_PRICE_INFIX_DIGIT] = PAST_MONTH_HAD_STATISTIC_PRICE
            return
        if is_there_reference_in_current_year:
            year.entering_price = get_price_from_other_year(model, year.year, reference_year.year,
                                                            reference_year.stat_price)
            year.infix[ENTERING_PRICE_INFIX_DIGIT] = PRICE_BASED_ON_OTHER_MONTH
            return
        if year.last_price:
            year.entering_price = year.last_price * (1 + model.family_data.p_age)
            year.infix[ENTERING_PRICE_INFIX_DIGIT] = PRICE_BASED_ON_OTHER_MONTH
            return
        year.entering_price = get_price_from_other_year(model, year.year, reference_year.year,
                                                        reference_year.past_pipes[self.name].price)
        year.infix[ENTERING_PRICE_INFIX_DIGIT] = PRICE_BASED_ON_OTHER_MONTH

    def was_big_model_in_past(self, year):
        if self.name in year.past_pipes:
            return True
        return False
