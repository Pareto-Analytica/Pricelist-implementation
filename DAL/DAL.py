class DAL:
    def read_model(self, model):
        raise NotImplementedError()

    def read_models(self, models):
        raise NotImplementedError()

    def update_model(self, model):
        raise NotImplementedError()

    def update_models(self, models):
        raise NotImplementedError()

    def flush(self):
        raise NotImplementedError()
