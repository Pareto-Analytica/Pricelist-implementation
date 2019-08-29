from common import Validator, Model, ModelYear, BIG_PIPE_NAME, SMALL_PIPE_NAME


class SmallPipeValidator(Validator):
    def __init__(self):
        self.name = SMALL_PIPE_NAME

    def validate(self, model):
        return True
