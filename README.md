# Yad 2 Car Price List Calculator
## Running The program
We'll split the running scenario:
### Running for the first time (no db exists).
* We'll first of start by creating the database from the past prices in the first month. The script create_db_from_file.py is reading the models, and the last price column (PriceYad2), creating the databae from it.
* For the create_db_from_file.py script to be run, there should be config.yaml in the main directory, while the following keys should contain files that exists:
  1. Date File Path
  1. Data File Path
  1. Family File Path
* Again, it reads the data of the last month (**not the data of the statistic prices in the file itself**), and sets it as past prices of small model.
* After that, please continue with the every month scenario.
### Running when there is already existing db.
The main file to run is main.py. It starts the price list calculator, while the prorgam itself is printing logs through its run.
