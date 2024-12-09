import time
#import openai
from openai import OpenAI
from dotenv import load_dotenv
from config import Config
from chatgpt import create_chat_completion
import csv
import re
from table_schema import read_tableinfo
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