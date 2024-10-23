import json
import sqlite3
from collections import Counter

def filter_unselected_data():
    with open('D:\XDF\ChatDB\zeroshot_prototype_model\databases\dev_new.json','rb') as f:
        d = json.load(f)
        set = []
        for id in range(len(d)):
            sql = d[id]["SQL"]
            if sql not in set:
                set.append(sql)
            else:
                print(id)
    with open('D:\XDF\ChatDB\zeroshot_prototype_model\databases\dev.json','rb') as f:
        d = json.load(f)
        oset = []
        for id in range(len(d)):

            if d[id]["difficulty"] == "challenging":
                sql = d[id]["SQL"]
                if sql not in set:
                    oset.append(sql)
                    print(id)
def delete_data():
    with open('D:\XDF\ChatDB\zeroshot_prototype_model\databases\dev_new.json','rb') as f:
        data = json.load(f)
        ids_to_delete = [2, 26, 30, 109]

        # Filter out the data (remove entries with question_id in ids_to_delete)
        filtered_data = [entry for entry in data if entry['question_id'] not in ids_to_delete]

        # Shift question_id values forward, making them sequential
        for i, entry in enumerate(filtered_data):
            entry['question_id'] = i  # Reassign question_id sequentially starting from 0
        print(i)
        # Print the modified data
    # Optionally, write the modified data to a new JSON file
    with open('D:\XDF\ChatDB\zeroshot_prototype_model\databases\dev_new.json', 'w') as json_file:
        json.dump(filtered_data, json_file, indent=4)
def check_error():
    v3 = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 14, 15, 19, 20, 22, 24, 25, 27, 28, 29, 31, 36, 38, 42, 43, 44, 45, 49, 50, 52,
         56, 57, 59, 60, 61, 62, 66, 67, 68, 69, 71, 77, 78, 81, 84, 86, 88, 89, 92, 97, 99, 100, 103, 104, 110, 112,
         114, 121, 123, 124, 126, 130, 131, 133, 134, 135, 136, 140, 143]

    v2 = [0, 1, 2, 3, 6, 8, 10, 11, 15, 17, 18, 24, 25, 27, 28, 29, 38, 42, 43, 44, 45, 48, 49, 50, 52, 56, 57, 59, 60,
         61, 62, 65, 66, 67, 68, 69, 71, 77, 78, 79, 81, 84, 86, 88, 89, 92, 97, 99, 100, 103, 104, 110, 112, 114, 121,
         123, 124, 126, 130, 131, 134, 140, 143]

    v1 = [1, 2, 5, 6, 8, 9, 10, 11, 14, 15, 18, 24, 25, 27, 28, 29, 38, 41, 42, 44, 45, 50, 52, 53, 57, 60, 61, 67, 68,
         69, 71, 77, 78, 79, 80, 81, 82, 84, 85, 86, 89, 92, 97, 99, 100, 101, 104, 105, 110, 112, 113, 114, 119, 122,
         126, 127, 130, 131, 133, 136, 140, 143]
    v4 = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 15, 18, 19, 24, 25, 27, 28, 31, 36, 38, 42, 43, 44, 45, 48, 49, 50, 52, 57, 59, 60, 61, 62, 65, 66, 67, 68, 71, 76, 77, 78, 81, 82, 86, 88, 89, 92, 97, 99, 100, 103, 107, 110, 112, 114, 121, 123, 126, 130, 131, 133, 134, 136, 140, 143]
    counter = 0
    missb = []
    for i in range(146):
        if i in v4 and i not in v1 and i not in v2 and i not in v3: #and i in d and i in e and i in f and i in g and i in h:
            counter += 1
            missb.append(i)
    """
    missa = [0, 1, 4, 6, 8, 9, 10, 11, 12, 14, 18, 24, 25, 27, 28, 29, 38, 41, 42, 44, 45, 50, 52, 53, 56, 57, 59, 61, 65, 67, 68, 71, 72, 75, 77, 78, 79, 80, 81, 82, 84, 85, 86, 89, 92, 97, 100, 101, 103, 104, 105, 106, 110, 112, 113, 114, 119, 122, 123, 127, 130, 131, 133, 136, 140, 143, 144]
    for i in range(146):
        if i in missa and i in missb:
            print(i)
            #counter += 1
    """
    print(counter)
    print(missb)
def check_sql():
    #def check_result(db):
    db = "debit_card_specializing"
    conn = sqlite3.connect(
        "D:\XDF\ChatDB\zeroshot_prototype_model\databases\dev_databases\{}\{}.sqlite".format(
            db, db))  # here define spider dataset position
    cur = conn.cursor()
    cur.execute("""SELECT
  CAST(ABS(
    SUM(CASE WHEN customers.Currency = 'CZK' THEN yearmonth.Consumption ELSE 0 END) -
    SUM(CASE WHEN customers.Currency = 'EUR' THEN yearmonth.Consumption ELSE 0 END)
  ) AS INTEGER) AS ConsumptionDifference
FROM yearmonth
JOIN customers ON yearmonth.CustomerID = customers.CustomerID
WHERE yearmonth.Date BETWEEN '201201' AND '201212';""")
    r1 = cur.fetchall()
    cur.execute("""SELECT
    ROUND(SUM(CASE WHEN customers.Currency = 'CZK' THEN yearmonth.Consumption END)) - ROUND(SUM(CASE WHEN customers.Currency = 'EUR' THEN yearmonth.Consumption END)) AS Difference
FROM
    yearmonth
JOIN
    customers ON yearmonth.CustomerID = customers.CustomerID
WHERE
    yearmonth.Date LIKE '2012%';""")
    r2 = cur.fetchall()
    if Counter(r1) == Counter(r2):
        print("yes")
    for i in r2:
        if i not in r1:
            print(i)
    for i in r1:
        if i not in r2:
            print(i)
def calc_avg_error():
    a = (0.4246575342465753+0.4657534246575342+0.3972602739726027+0.4178082191780822+0.3767123287671233)/5
    b = (0.4041095890410959+0.3287671232876712+0.3972602739726027+0.3493150684931507+0.363013698630137)/5
    print(a,b)
calc_avg_error()