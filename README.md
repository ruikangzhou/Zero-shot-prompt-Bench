# Zero-shot-prompt-Bench
The testing programm is zeroshottest.py. The 146 questions are stored in dev_new.json. 
To run the program, first unzip the databases.zip.
Then change "D:\XDF\ChatDB\zeroshot_prototype_model\databases" part of conn =sqlite3.connect("D:\XDF\ChatDB\zeroshot_prototype_model\databases\dev_databases\{}\{}.sqlite".format(db_name, db_name)) at 131 line of Zeroshottest.py to the place where you place the unzipped files.
