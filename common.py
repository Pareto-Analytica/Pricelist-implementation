# Config Constants
import json

CONFIG_PATH = ".\\config.yaml"

# Config Keys

OUT_FILE_KEY = "Output Csv File Path"
DATE_FILE_NAME_KEY = "Date File Path"
DATA_FILE_NAME_KEY = "Data File Path"
FAMILY_FILE_NAME_KEY = "Family File Path"
MINIMAL_DAY_IN_MONTH_KEY = "Minimal Day In Month"
FILE_DATA_BASE_PATH_KEY = "File Data Base Path"
FIRST_MONITOR_MIN_KEY = "First Monitor Minimal From Last Month In Percentage"
FIRST_MONITOR_MIN_FLAG_KEY = "First Monitor Flag Model + Year Is Bigger Than Last Month"
SMALL_MODEL_JANUARY_DECREASE_KEY = "Small Model January Reduction"
SMALL_MODEL_FEBRUARY_DECREASE_KEY = "Small Model February Reduction"
SMALL_MODEL_MONTH_DECREASE_KEY = "Small Model Other Months Reduction"
SMALL_MODEL_MAX_DIFF_KEY = "Small Model Maximal Percentage Than Last Month"
MINIMAL_PRICE_TO_CALCULATE_KEY = "Minimal Price To Calculate From"
# Only read when validating dates.
CURRENT_DATE_KEY = "Current Date"

# All Cars List Constants
SMID_KEY = "ï»¿SMID"
YEAR_KEY = "Year"
STATISTIC_PRICE_KEY = "StatPrice"
ITEMS_AMOUNT_KEY = "N_Rows"
STDEV_KEY = "STDEV"
FAMILY_ID_KEY = "FamilyID"
NEW_CAR_PRICE_KEY = "NewCarPrice"

# Families File Constants
P_AGE_KEY = "P_Age"
AVG_REDUCTION_ANNUALLY_KEY = "AvgRedAnnual"
FAMILY_BOTTOM_KEY = "FamilyButtom"
FAMILY_TOP_KEY = "FamilyTop"
FIRST_YEAR_REDUCTION_KEY = "RedPercentFirstYear"
NEW_CAR_NYLON_REDUCTION_KEY = "NewCarMonitor"

BIG_PIPE_NAME = "Big Pipe"
SMALL_PIPE_NAME = "Small Pipe"

# Save Csv Keys
SMID_SAVE_KEY = "SMID"
NEW_ROUNDED_PRICE_KEY = "Yad2_Price"
NEW_REAL_PRICE_KEY = "Yad2_Price_NotRounded"
FIRST_MONITOR_MIN_SAVE_KEY = "MinPrice"
FIRST_MONITOR_MAX_SAVE_KEY = "MaxPrice"
FIRST_MONITOR_PRICE_SAVE_KEY = "Mon1_Price"
SECOND_MONITOR_PRICE_SAVE_KEY = "Mon2_Price"
SECOND_MONITOR_DIFF_BETWEEN_YEARS_SAVE_KEY = "Mon2_PercChange"
SECOND_MONITOR_DIFF_BETWEEN_STDEV_YEARS_SAVE_KEY = "Mon2_Gap_StdevAvg"
LAST_PRICE_SAVE_KEY = "LastPL_Price"
ITEMS_AMOUNT_SAVE_KEY = "comp_N_Rows"
STDEV_SAVE_KEY = "comp_StdevToStatPrice"
ENTERING_PRICE_KEY = "Entering Price"
SHOULD_BE_CHECKED_MANUALLY = "Manually"
INFIX = "InfoFix"
SAVE_HEADERS = [SMID_SAVE_KEY, YEAR_KEY, NEW_ROUNDED_PRICE_KEY, NEW_REAL_PRICE_KEY, STATISTIC_PRICE_KEY,
                FIRST_MONITOR_MIN_SAVE_KEY, FIRST_MONITOR_MAX_SAVE_KEY, ENTERING_PRICE_KEY
    , FIRST_MONITOR_PRICE_SAVE_KEY, SECOND_MONITOR_PRICE_SAVE_KEY, SECOND_MONITOR_DIFF_BETWEEN_YEARS_SAVE_KEY
    , SECOND_MONITOR_DIFF_BETWEEN_STDEV_YEARS_SAVE_KEY, LAST_PRICE_SAVE_KEY, ITEMS_AMOUNT_SAVE_KEY, STDEV_SAVE_KEY,
                SHOULD_BE_CHECKED_MANUALLY, INFIX]
# INFIX_CONSTANTS
# Entering Infixes
INFIX_LENGTH = 6

DEFAULT_INFIX_DIGIT_VALUE = 0

ENTERING_PRICE_INFIX_DIGIT = 0
THIS_MONTH_HAS_STATISTIC_PRICE = 1
PAST_MONTH_HAD_STATISTIC_PRICE = 2
PRICE_BASED_ON_OTHER_MONTH = 3
PRICE_LOWER_THAN_MINIMAL_TO_SHOW = 4
SMALL_PIPE_YEAR = 5

FIRST_MONITOR_INFIX_DIGIT = 1
FIRST_MONITOR_VALID = 1
FIRST_MONITOR_BIGGER_THAN_VALID = 2
FIRST_MONITOR_SMALLER_THAN_VALID = 3
SMALL_PIPE_THERE_IS_NEW_CAR_PRICE = 4
SMALL_PIPE_LAST_MONTH_PRICE_EXISTS = 5
SMALL_PIPE_SHOULD_BE_CHECKED_MANUALLY = 6

SECOND_MONITOR_UP_INFIX_DIGIT = 2
SECOND_MONITOR_DOWN_INFIX_DIGIT = 3
SECOND_MONITOR_VALID = 1
SECOND_MONITOR_SMALLER = 2
SECOND_MONITOR_BIGGER = 3

SECOND_MONITOR_DID_CAR_PRICE_CHANGE_INFIX_DIGIT = 4
SECOND_MONITOR_CHANGED_CAR_WITH_HIGHER_YEAR = 1
SECOND_MONITOR_CHANGED_CAR_WITH_LOWER_YEAR = 2
SECOND_MONITOR_CHANGED_CAR_TWICE = 3

SECOND_MONITOR_CHECK_INFIX_DIGIT = 5
SECOND_MONITOR_CHECK_FIXED_AND_VALID = 1
SECOND_MONITOR_CHECK_FIXED_AND_BIGGER = 2
SECOND_MONITOR_CHECK_FIXED_AND_SMALLER = 3


class ModelYear:
    def __init__(self, year, stat_price, items_amount, stdev, new_car_price):
        self.year = year
        self.new_car_price = new_car_price

        self.past_pipes = {}

        # Empty if less than 5 obs in month.
        self.stat_price = stat_price
        if items_amount:
            self.items_amount = items_amount
        else:
            self.items_amount = 0
        if stdev:
            self.stdev = stdev
        else:
            self.stdev = 0
        # Past Data
        self.last_price = None
        self.last_price_before_rounding = None
        # Flagging and Shit
        self.bigger_flag_amount = 0

        # Out Data
        self.new_price = None
        self.infix = [0 for i in range(6)]

        # Big Pipe
        self.entering_price = None

        # Monitor 1
        self.first_monitor_price = None
        self.min_price = None
        self.max_price = None
        # Monitor 2
        self.second_monitor_price = None
        self.monitoring_2_prec_change = None
        self.monitoring_2_stdev_change = None
        self.should_be_checked_manually = None


class Model:
    def __init__(self, id, family_id):
        self.years = {}
        self.id = id
        self.family_id = family_id
        self.family_data = None

    def set_family_data(self, family_data):
        self.family_data = None

    def was_pipe(self, pipe_name):
        for year_num, year in self.years.items():
            if pipe_name in year.past_pipes:
                return True
        return False

    def add_model_year(self, model_year):
        if model_year.year in self.years:
            raise Exception('There 2 instance of the year {} in the model {}'.format(model_year.year, self.id))
        self.years[model_year.year] = model_year


class Family:
    def __init__(self, family_id):
        self.id = family_id
        self.p_age = None
        self.avg_reduction_annually = None
        self.first_year_reduction = None
        self.new_car_nylon_reduction = None
        self.family_bottom = None
        self.family_top = None
        self.min_reduction_annually = None
        self.max_reduction_annually = None


class PipeHistory:
    def __init__(self, price, items_amount, stdev, date, should_be_checked_manually=False):
        self.price = price
        self.items_amount = items_amount
        self.stdev = stdev
        self.date = date
        self.should_be_checked_manually = should_be_checked_manually

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Pipe:
    # Should be implemented in derived class
    def validate(self, model):
        raise NotImplementedError()

    def process(self, model):
        raise NotImplementedError()


def round_to_nearest_hundred(num):
    if num % 100 > 100 / 2:
        return num - num % 100 + 100
    else:
        return num - num % 100
