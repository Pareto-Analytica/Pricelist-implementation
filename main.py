from DAL.JSONDAL import JSONDal
from common import BIG_PIPE_NAME,  SMALL_PIPE_NAME, CURRENT_DATE_KEY
from data_reader import get_config, get_and_validate_input_date, get_models
from csv_data_writer import write_output_data
from pipes.big_pipe import BigPipe
from pipes.small_pipe import SmallPipe

if __name__ == '__main__':
    print("Starting Program.")
    config = get_config()
    config[CURRENT_DATE_KEY] = get_and_validate_input_date(config)
    print("Finished reading configuration.")
    pipes = {
        BIG_PIPE_NAME: BigPipe(config)
        , SMALL_PIPE_NAME: SmallPipe(config)
    }
    print("Validating date is valid.")
    print("Date is valid.")
    dal = JSONDal(config)
    print("Reading and aggregating models.")
    models = get_models(config, dal)
    print("Finsihed aggregating models.")
    out_rows = []
    for id, model in models.items():
        for name, pipe in pipes.items():
            if pipe.validate(model):
                print("{} goes to  {}".format(id, pipe.name))
                pipe.process(model)
                out_rows.extend(pipe.save_and_get_row(model))
                break
    print("Finished processing models.")
    print("Writing data to database.")
    write_output_data(config, out_rows)
    print("Creating csv output")
    dal.update_models(models)
    dal.flush()
    print("Finished.")
