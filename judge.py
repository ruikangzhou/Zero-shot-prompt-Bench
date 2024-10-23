import time
#import openai
from openai import OpenAI
from dotenv import load_dotenv
from config import Config
from chatgpt import create_chat_completion
import csv
import re
from table_schema import read_tableinfo, search_tableinfo
import sqlite3
import ast

#cfg = Config()
#model = cfg.fast_llm_model
def judge(sql, user_inp, db_name):
    prompt ="""
You are an expert in databases, proficient in SQL statements and can use the database to help users. \
You will receive a wrong sql command and check if it can run successfully according to the table information given by user.\
please fix it according to the table information.\

Please follow the output format below, including the leading and trailing "\`\`\`" and "\`\`\`", remember not to add any symbols like '\;' or '\,' or '\.' on the end of the sql:
```
USER INPUT: <user input>
ANSWER: SELECT T1.template_type_code ,  count(*) FROM Templates AS T1 JOIN Documents AS T2 ON T1.template_id  =  T2.template_id GROUP BY T1.template_type_code
```
"""
    wrong_sql="""
USER INPUT: The following user query: {} \n
has got a false sql command: {}; \
Fix it according to the following table information.\
The details of tables in the database are delimited by triple quotes:
\"\"\"
{}
\"\"\"              
""".format(user_inp, sql, read_tableinfo(db_name))
    #print(sql)
    try:
        response = create_chat_completion([{'role': 'system', 'content': prompt}, {'role': 'user', 'content': wrong_sql}])
    except Exception as e:
        print(f"API request failed after retries: {e}")
    pattern = "ANSWER: (.*)"
    #print(str)
    str = re.findall(pattern, response)
    try:
        str = str[0]
    except:
        str = "None"
    #print(str)
    return(str)


def judge_data(sql,user_inp, db_name):
    tabinfo = read_tableinfo(db_name)
    #print(tabinfo)
    prompt ="""
You are an expert in databases, proficient in SQL statements and can use the database to help users. \
You will receive a user query and check which colums of which table in the database are required according to the table information given by user.\
Please give the table name and column name of the relevant data.\
Remember not to mistaken which column belongs to which table.\

Please keep your output in the format of the following output example, remember not to add any symbols like ';' or ',' or '.' on the end of the sql:
```
USER INPUT: <user input>
ANSWER: {'<column owner table name>':['<column name under the table>','<column name under the table>', ...], '<column owner table name>':['<column name under the table>','<column name under the table>', ...], ... }
```
"""
    input="""
Question: {} \n

Check which columns are relevant in this question according to the following table information.\
Indicate as more as possible relevant columns in your answer.\
The details of tables in the database are delimited by triple quotes:
\"\"\"
{}
\"\"\"              
""".format(user_inp, tabinfo)
    """
    client = OpenAI()
    response = client.chat.completions.create(
        # model=model,
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": input}],
        temperature=1,
        max_tokens=None
    )

    str = response.choices[0].message.content.strip()
    """
    str = create_chat_completion([{"role": "system", "content": prompt}, {"role": "user", "content": input}])
    pattern = "ANSWER: (.*)"
    #print(str)
    str = re.findall(pattern, str)
    try:
        str = str[0]
    except:
        str = "None"

    table_dict = ast.literal_eval(str)
    relevant_table = ""
    conn =sqlite3.connect("D:\XDF\ChatDB\zeroshot_prototype_model\databases\dev_databases\{}\{}.sqlite".format(db_name, db_name))#here define spider dataset position
    cur = conn.cursor()

    for table in table_dict:
        for i in table_dict[table]:
            line = search_tableinfo(i,table,db_name)
            #print(i,table)
            sentence = "SELECT MAX(`{}`), MIN(`{}`) FROM `{}` ".format(i,i,table)
            sentence2 = "SELECT DISTINCT `{}`FROM `{}` ORDER BY Random() LIMIT 10 ".format(i,table)
            #print(r)

            #print(r)
            #if 1:
            try:
                cur.execute(sentence)
                r = cur.fetchall()
                if r is not None:
                    line += """Data range of this column is: {}, """.format(r)
                    cur.execute(sentence2)
                    r = cur.fetchall()
                    line += "typical data values in this column are: {}\n".format(r)
                    relevant_table += line
                else:
                    line += """All data are "NULL" in this column."""

            except:
                line ="""Note that column "{}" does not exist in table "{}"\n""".format(i, table)
                relevant_table += line


    print(relevant_table)
    return(relevant_table)


def end_judge(sql, user_inp, db_name):
    prompt ="""
You are an expert in databases, proficient in SQL statements and can use the database to help users. \
You will receive a sketchy sql command and check if it can:
1. satisfy the demand of user question\
2. run successfully \
according to the table information given by user.\

If either of the 2 points above is violated, please fix it according to the table information.\

Please answer the question of user in following format, including the leading and trailing "\`\`\`" and "\`\`\`", remember not to add any symbols like '\,' or '\.' on the end of the sql,but always ends with "\;":

```
Evidence: <reasoning your judgment and state what you have changed in the sql>
SELECT `Element` FROM `Meta` ORDER BY `Range` DESC LIMIT 4;
```

Here is an example:
USER INPUT: <user input with table information>

```
Evidence: The "name" column required by the user question is missed in the sketchy sql. Add it to the sql.
SELECT name, country, age FROM singer ORDER BY age DESC;
```
"""
    wrong_sql="""
The following user query: {} \n
has got a sketchy sql command: {}; \
It can be incorrect or can't satisfy user demand.\
Fix it if necessary according to the following table information.\
The details of tables in the database are delimited by triple quotes:
\"\"\"
{}
\"\"\"              
""".format(user_inp, sql, read_tableinfo(db_name))
    #print(sql)
    """
    str = create_chat_completion(
        model=model,
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": wrong_sql}])
    """
    str = create_chat_completion([{"role": "system", "content": prompt}, {"role": "user", "content": wrong_sql}])
    #print(str)
    return(str)


if __name__ == '__main__':
    judge_data("SELECT SUM(T1.points), T2.name, T2.nationality FROM constructorResults AS T1 INNER JOIN constructors AS T2 ON T1.constructorId = T2.constructorId INNER JOIN races AS T3 ON T3.raceid = T1.raceid WHERE T3.name = 'Monaco Grand Prix' AND T3.year BETWEEN 1980 AND 2010 GROUP BY T2.name ORDER BY SUM(T1.points) DESC LIMIT 1",
    "Which constructor scored most points from Monaco Grand Prix between 1980 and 2010? List the score, name and nationality of this team.",
               'formula_1')
