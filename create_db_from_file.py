import csv
import datetime

from DAL.JSONDAL import JSONDal
from common import SMID_KEY, Model, FAMILY_ID_KEY, YEAR_KEY, STATISTIC_PRICE_KEY, ITEMS_AMOUNT_KEY, STDEV_KEY, \
    NEW_CAR_PRICE_KEY, ModelYear, FILE_DATA_BASE_PATH_KEY, SMALL_PIPE_NAME, PipeHistory
from data_reader import to_float

if __name__ == '__main__':
    file = ".\\data\\All_Cars_List.csv"
    models = {}
    with open(file, 'r') as data_file:
        reader = csv.DictReader(data_file)
        for row in reader:
            if row[SMID_KEY]:
                model = row[SMID_KEY]
                if model not in models:
                    models[model] = Model(model, row[FAMILY_ID_KEY])
                model_year = ModelYear(int(row[YEAR_KEY]), to_float(row[STATISTIC_PRICE_KEY]),
                                       to_float(row[ITEMS_AMOUNT_KEY]), to_float(row[STDEV_KEY]),
                                       to_float(row[NEW_CAR_PRICE_KEY]))
                model_year.new_price = row["PriceYad2"]
                model_year.past_pipes[SMALL_PIPE_NAME] = PipeHistory(model_year.new_price, 0, 0,
                                                                     datetime.datetime.now())
                if model_year.new_price and model_year.new_price != 0:
                    models[model].add_model_year(model_year)
                else:
                    if len(models[model].years) == 0:
                        models.pop(model, None)
    dal = JSONDal({FILE_DATA_BASE_PATH_KEY: ".\\data\\FileData.json"})
    dal.update_models(models)
    dal.flush()
