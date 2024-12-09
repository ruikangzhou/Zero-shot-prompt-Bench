import sqlite3
import os
import csv
import sqlite3
from pathlib import Path
def read_tableinfo(db):
    """"
    str = ""
    full_path = "D:\XDF\spider\spider\database\{}\{}.sqlite".format(db, db)
    conn = sqlite3.connect(full_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cur.fetchall()
    for i in table_names:
        cur.execute("SELECT sql FROM sqlite_master WHERE type='table' and name = '{}';".format(i[0]))
        str += cur.fetchall()[0][0] +'\n'

    """
    script_dir = Path(__file__).parent.resolve()
    dir = script_dir/"databases\dev_databases\{}\database_description".format(db)
    tabinfo = ''
    for root, dirs, files in os.walk(dir):
        for name in files:
            filename = os.path.join(root, name)
            with open(filename, encoding='utf-8', errors='ignore') as f:
                i = 0
                name = name.replace('.csv', '')
                tab = "CREATE TABLE {} (\n".format(name)
                for row in csv.reader(f, skipinitialspace=True):
                    if i != 0:
                        new_row = "`" + row[0].strip() + "`" + " " + row[3] + ", "

                        if (row[1] != '') and (row[2] == ''):
                            new_row = new_row + "#column description: " + row[1].replace('\n', '') + "; "
                        if (row[1] == '') and (row[2] != ''):
                            new_row = new_row + "#column description: " + row[2].replace('\n', '') + "; "
                        if (row[1] != '') and (row[2] != '') and (row[1] != row[2]):
                            new_row = new_row + "#column description: " + row[1].replace('\n', '') + " ("+row[2].replace('\n', '')+ "); "
                        if (row[1] == row[2]) and (row[1] != ''):
                            new_row = new_row + "#column description: " + row[1].replace('\n', '') + "; "

                        if row[4] != '':
                            new_row = new_row + "#value description: " + row[4].replace('\n','') + "; "

                        """
                        # print(i,table)
                        column = str(row[0].strip())
                        table = str(name.strip())
                        sentence = "SELECT MAX(`{}`), MIN(`{}`) FROM `{}` ".format(column, column, table)
                        sentence2 = "SELECT DISTINCT `{}`FROM `{}` ORDER BY Random() LIMIT 10 ".format(column, table)
                        #print(sentence)
                        # print(r)
                        conn = sqlite3.connect(
                            "D:\XDF\ChatDB\zeroshot_prototype_model\databases\dev_databases\{}\{}.sqlite".format(
                                db, db))  # here define spider dataset position
                        cur = conn.cursor()
                        # print(r)
                        """


                        line = ''
                        line += """Data range of this column is: {}, """.format(row[5])
                        if row[6] != '':
                            line += "typical data values in this column are: {}".format(row[6])


                        new_row += line

                        new_row = new_row + '\n'

                        tab = tab + new_row
                    else:
                        i = 1
            tab += ');\n'
            tabinfo += tab

    return tabinfo



#print(read_tableinfo("D:\XDF\ChatDB\zeroshot_prototype_model\databases\dev_databases\california_schools\california_schools.sqlite"))
#print(read_tableinfo("formula_1"))
#print(search_tableinfo("NumGE1500","satscores","california_schools"))
#tables = [tab_frpm, tab_satscores, tab_schools]
#tables_clean = [tab_frpm_clean, tab_satscores_clean, tab_schools_clean]