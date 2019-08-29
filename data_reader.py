import yaml
from datetime import datetime
import csv
from dateutil.relativedelta import relativedelta

from common import CONFIG_PATH, DATE_FILE_NAME_KEY, MINIMAL_DAY_IN_MONTH_KEY, DATA_FILE_NAME_KEY, SMID_KEY, Model, \
    FAMILY_ID_KEY, ModelYear, YEAR_KEY, STATISTIC_PRICE_KEY, ITEMS_AMOUNT_KEY, NEW_CAR_PRICE_KEY, STDEV_KEY, \
    FAMILY_FILE_NAME_KEY, Family, P_AGE_KEY, AVG_REDUCTION_ANNUALLY_KEY, FAMILY_TOP_KEY, FAMILY_BOTTOM_KEY, \
    FIRST_YEAR_REDUCTION_KEY, NEW_CAR_NYLON_REDUCTION_KEY


# We use this function as well to get the "current" month - in the small pipe for example
def get_and_validate_input_date(config):
    with open(config[DATE_FILE_NAME_KEY], 'r') as date_file:
        reader = csv.reader(date_file)
        time_row = [row for idx, row in enumerate(reader) if idx == 1][0]
        try:
            time = datetime.strptime(time_row[0], '%d/%m/%Y %H:%M:%S')
        except Exception as e:
            time = datetime.strptime(time_row[0], '%d/%m/%Y %H:%M')
        minimal_time = datetime.now().replace(month=6, day=int(config[MINIMAL_DAY_IN_MONTH_KEY]), hour=0, minute=0)
        if time < minimal_time:
            raise Exception(
                "Read file date is smaller than the minimal date which is : {} ".format(minimal_time.isoformat()))

        # Adding one month, because if in the file written 20.8 it will be run on september.
        return time + relativedelta(months=1)


def get_models(config, dal):
    print("Reading families data.")
    families = read_families(config)
    print("Reading models new file.")
    models = read_models(config, families)
    print("Aggregating models data from db.")
    dal.read_models(models)
    return models


def read_families(config):
    families = {}
    with open(config[FAMILY_FILE_NAME_KEY], 'r') as family_file:
        reader = csv.DictReader(family_file)
        for row in reader:
            id = row[FAMILY_ID_KEY]
            family = Family(id)
            family.p_age = float(row[P_AGE_KEY])
            family.avg_reduction_annually = float(row[AVG_REDUCTION_ANNUALLY_KEY])
            family.family_bottom = float(row[FAMILY_BOTTOM_KEY])
            family.family_top = float(row[FAMILY_TOP_KEY])
            family.first_year_reduction = float(row[FIRST_YEAR_REDUCTION_KEY])
            family.new_car_nylon_reduction = float(row[NEW_CAR_NYLON_REDUCTION_KEY])
            families[id] = family
    return families


def to_float(str):
    if str:
        return float(str)


def read_models(config, families):
    models = {}
    with open(config[DATA_FILE_NAME_KEY], 'r') as data_file:
        reader = csv.DictReader(data_file)
        for row in reader:
            if row[SMID_KEY]:
                model = row[SMID_KEY]
                if model not in models:
                    models[model] = Model(model, row[FAMILY_ID_KEY])
                model_year = ModelYear(int(row[YEAR_KEY]), to_float(row[STATISTIC_PRICE_KEY]),
                                       to_float(row[ITEMS_AMOUNT_KEY]), to_float(row[STDEV_KEY]),
                                       to_float(row[NEW_CAR_PRICE_KEY]))
                models[model].family_data = families[row[FAMILY_ID_KEY]]
                models[model].add_model_year(model_year)
    return models


def get_config():
    with open(CONFIG_PATH, 'r') as file:
        return yaml.load(file, Loader=yaml.BaseLoader)
