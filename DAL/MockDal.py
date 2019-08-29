from DAL.DAL import DAL


class MockDal(DAL):
    def __init__(self, config):
        self.models = {}

    def read_model(self, model_id):
        pass
    def update_model(self, model):
        pass

    def update_models(self, models):
        pass

    def flush(self):
        pass
