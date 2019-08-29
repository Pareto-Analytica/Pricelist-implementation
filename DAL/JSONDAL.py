import json

from DAL.DAL import DAL
from common import FILE_DATA_BASE_PATH_KEY


class YamlDal(DAL):
    def __init__(self, config):
        print("Starting to read saved data.")
        self.db_path = config[FILE_DATA_BASE_PATH_KEY]
        with open(self.db_path, 'r') as file:
            self.models = json.load(file)
            if not self.models:
                self.models={}
        print("Finished reading saved data.")

    def read_model(self, model):
        if model.id in self.models:
            for year_num, year in self.models[model.id]["years"].items():
                if year_num in model.years:
                    model.years[year_num].past_pipes = year["pipes"]
                    model.years[year_num].last_price = year["last_price"]
                    if "bigger_flag_amount" in year and year["bigger_flag_amount"]>0:
                        model.years[year_num].bigger_flag_amount = year["bigger_flag_amount"]

    def read_models(self, models):
        for id, model in models.items():
            self.read_model(model)

    def update_model(self, model):
        updated_model = {"id":   model.id}
        updated_model["years"] = {}
        for year_num, year in model.years.items():
            updated_model["years"][year_num] = {
                "pipes": year.past_pipes,
                "last_price": year.new_price,
                "bigger_flag_amount":year.bigger_flag_amount
            }
        self.models[model.id] = updated_model

    def update_models(self, models):
        for id, model in models.items():
            self.update_model(model)

    def flush(self):
        with open(self.db_path, 'w') as file:
            json.dump(self.models, file)
