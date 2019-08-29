import csv

from common import OUT_FILE_KEY, SAVE_HEADERS


def write_output_data(config,rows):
    with open(config[OUT_FILE_KEY], "w",newline="") as file:
        writer = csv.DictWriter(file, fieldnames=SAVE_HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
