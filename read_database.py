import sqlite3
import csv

from embedding import embedding

def read_database():
    db = sqlite3.connect('D:\XDF\ChatDB\BIRD dataset\dev\dev_databases\california_schools\california_schools.sqlite')
    cur = db.cursor()
    cur.execute("SELECT name _id FROM sqlite_master WHERE type ='table'")
    a = cur.fetchall()
    """
    filename = 'test.db'

    conn = sqlite3.connect(filename)
    #print(sqlite3.sqlite_version)

    cur2 = conn.cursor()
    for i in tables_clean:
        print(i)
        cur2.execute(i)
    """
    with open('testprofiles.csv', 'w', newline='', encoding="UTF-8") as file:
        writer = csv.writer(file)

        table_list = []
        embedding_list = []
        for table_name in a:
            table_name = table_name[0]

            query = "PRAGMA table_info([{}])".format(table_name)
            cur.execute(query)
            b = cur.fetchall()
            for column in b:
                flag = 0
                column_list = []
                column = column[1]
                #print(column,table_name)
                query = "SELECT `{}` FROM {}".format(column, table_name)
                #print(query)
                cur.execute(query)
                instances = cur.fetchall()
                column_list.append(table_name)
                column_list.append(column)
                testinstance = instances[0][0]
                for i in instances[0]:
                    if i != None:
                        testinstance = instances[0][0]
                        break
                #print(instances[0][0])
                if isinstance(testinstance, str):
                    testinstance = testinstance.replace(".", "")
                    testinstance = testinstance.replace("-", "")
                    #testinstance = testinstance.replace("@", "")
                    testinstance = testinstance.replace(" ", "")
                    #print(testinstance)
                    if str.isalpha(testinstance):
                        embedding_list.append(column)
                        for instance in instances:
                            instance = instance[0]
                            #print(instance)
                            if instance not in column_list:
                                column_list.append(instance)
                    else:
                        flag = 1

                else:
                    flag = 1

                if flag != 1:

                    writer.writerow(column_list)
                    table_list.append(column_list)
    #print(embedding_list)
    #embedding(embedding_list)
    return table_list


def get_valueposition(value):
    x = read_database()
    teststr = value
    str = ""
    for i in x:
        try:
            e = i.index(teststr)
            if e > 1:
                str += "table: {}, column: {};\n".format(i[0], i[1])
        except:
            1
    return str


#print(get_valueposition("Alameda"))
#read_database()