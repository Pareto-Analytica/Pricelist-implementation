import datetime
import json
import os
from json import JSONEncoder
from DAL.DAL import DAL
from common import FILE_DATA_BASE_PATH_KEY, PipeHistory, Model


# def convert_models_from_dic(models_as_dict):
#     models={}
#     for old_model in models_as_dict:
#         new_model=Model()

class JSONDal(DAL):
    def __init__(self, config):
        print("Starting to read saved data.")
        self.db_path = config[FILE_DATA_BASE_PATH_KEY]
        if not os.path.isfile(self.db_path):
            with open(self.db_path, 'w') as file:
                json.dump({}, file)
        with open(self.db_path, 'r') as file:
            self.models = json.load(file)
            if not self.models:
                self.models = {}
        print("Finished reading saved data.")

    def read_model(self, model):
        if model.id in self.models:
            for year_num, year in self.models[model.id]["years"].items():
                year_num_as_int = int(year_num)
                if year_num_as_int in model.years:
                    for pipe_name, pipe in year["pipes"].items():
                        model.years[year_num_as_int].past_pipes[pipe_name] = \
                            PipeHistory(float(pipe["price"]),
                                        float(pipe["items_amount"]),
                                        float(pipe["stdev"]),
                                        ["date"],
                                        bool(pipe["should_be_checked_manually"]))
                    model.years[year_num_as_int].last_price =float( year["last_price"])
                    if "bigger_flag_amount" in year and year["bigger_flag_amount"] > 0:
                        model.years[year_num_as_int].bigger_flag_amount = year["bigger_flag_amount"]

    def read_models(self, models):
        for id, model in models.items():
            self.read_model(model)

    def update_model(self, model):
        updated_model = {"id": model.id}
        updated_model["years"] = {}
        for year_num, year in model.years.items():
            updated_model["years"][year_num] = {
                "pipes": year.past_pipes,
                "last_price": year.new_price,
                "bigger_flag_amount": year.bigger_flag_amount
            }
        self.models[model.id] = updated_model

    def update_models(self, models):
        for id, model in models.items():
            self.update_model(model)

    def flush(self):
        with open(self.db_path, 'w') as file:
            json.dump(self.models, file, cls=MyEncoder)


class MyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PipeHistory):
            o=obj.__dict__
            return o
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
