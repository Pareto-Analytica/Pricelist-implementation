# Yad 2 Car Price List Calculator

## Running The Program
We'll split the running scenario:

### Running For The First Time (If No Database Exists).
* We'll first of start by creating the database from the past prices in the first month. The script create_db_from_file.py is reading the models, and the last price column (PriceYad2), creating the databae from it.
* For the create_db_from_file.py script to be run, there should be config.yaml in the main directory, while the following keys should contain files that exists:
  1. Date File Path
  1. Data File Path
  1. Family File Path
* Again, it reads the data of the last month (**not the data of the statistic prices in the file itself**), and sets it as past prices of small model.
* After that, please continue with the every month scenario.

### Running When There Is Already Existing Database.
* The main file to run is main.py. It starts the price list calculator, while the prorgam itself is printing logs through its run.
* The script outputs an output.csv file (configured path in config), and updates the database.
* **IMPOTANT**: The script will read the date from the date file (configured path in config) and treat it as the current date, and will derive the small pipe prices from the date. Thus, please validate the date in the file to be the correct date to calculate from.

### Used Jargon Through The Project
* Model - The sub-model of the car, containing data regarding the model and its data regarding years.
* ModelYear - An object contained inside model, containg each year's data.
* Pipe - Because model is already take, the "מודל", for example small and big pipes ("מודל גדול" ו"מודל קטן")

### Configuration Explained
**IMPORTANT**: All the inserted files has to be **csv** and not **xlsx**
1. Date File Path: Self explanatory 
1. Data File Path: Self explanatory 
1. Family File Path: Self explanatory 
1. File Data Base Path: Self explanatory 
1. Output Csv File Path: Self explanatory 
1. First Monitor Minimal From Last Month In Percentage: **In big pipe, monitor 1, a certain precentage is used for defining minimal and maximal prices based on last month. This is it, insert it as a precentage out of 1 (0.05 for example)**
1. Minimal Day In Month: **We valdiate the date of the date file is bigger than certain date in the current month**
1. First Monitor Flag Model + Year Is Bigger Than Last Month: **Minimal amount of months that the months are bigger in sequence to actually increase the price** 
1. Small Model January Reduction: Self explanatory
1. Small Model February Reduction: Self explanatory
1. Small Model Other Months Reduction: Self explanatory
1. Small Model Maximal Percentage Than Last Month: **Same as "First Monitor Minimal From Last Month In Percentage", just in small pipe**
1. Minimal Price To Calculate From: **Beneath that value, the column "Smaller Than Minimal" in output file will be True**

Config example:
`<addr>`
1. Date File Path: .\\data\\Stat_Prices_ClacTime.csv
1. Data File Path: .\\data\\All_Cars_List.csv
1. Family File Path: .\\data\\InfoByFamily_CSV.csv
1. File Data Base Path: .\\data\\FileData.json
1. Output Csv File Path: .\\data\\output.csv
1. First Monitor Minimal From Last Month In Percentage: 0.05
1. Minimal Day In Month: 1
1. First Monitor Flag Model + Year Is Bigger Than Last Month: 3
1. Small Model January Reduction: 0.4
1. Small Model February Reduction: 0.3
1. Small Model Other Months Reduction: 0.03
1. Small Model Maximal Percentage Than Last Month: 0.05
1. Minimal Price To Calculate From: 10000
`</addr>`
