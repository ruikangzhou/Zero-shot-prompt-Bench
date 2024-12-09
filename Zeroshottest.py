import re
from table_schema import read_tableinfo
from chatgpt import create_chat_completion
import sqlite3
import json
from judge import judge
from collections import Counter
from pathlib import Path


def read_json(id):
    script_dir = Path(__file__).parent.resolve()
    with open(script_dir/'dev_new.json','rb') as f:
        d = json.load(f)
        return d[id]['question'],d[id]['SQL'], d[id]['db_id'],d[id]['difficulty']#here id = real id - 1, altogether 1034

def get_sql_from_response(response):
    pattern = r"Evidence:\s+(.*?)+ANSWER:\s+(.*?);"
    matches = re.findall(pattern, response, re.DOTALL)
    # Extract information and create list of dictionaries
    result = []
    for match in matches:
        description = match[0]
        sql_query = match[1]
        result = {
            "description": description.strip(),
            "sql": sql_query.strip(),
        }
    #print(result['sql'])
    return result

def init_system_msg_prototype():
    sys_temp = """
You are a powerful AI assistant, a variant of ChatGPT that can transform user queries into SQL commands. You are an expert in databases, proficient in SQL statements, and can use the database to help users.

**Rules:**

1. **Database Type:** The databases are `.sqlite`, so use SQLite grammar instead of MySQL grammar.

2. **Column Names with Spaces:** If the column name contains spaces (e.g., `"xxx xxx"`), use backticks like `xxx xxx` as the column name.

3. **Output Format:** Please answer the user's question in the following format, including the leading and trailing "```" and "```", and ";" at the end of the SQL command:

```
Evidence: <reasoning your decision according to the columns in the table>
ANSWER: <SQL command>;
```
**Important Guidelines:**

- **Accurate Column Selection:**
- Only select the columns explicitly requested in the user's query.
- Do not include extra columns used for sorting or filtering unless they are specifically requested.
- Avoid over-selection to ensure the result set contains only the necessary information.

- **Use `DISTINCT` When Necessary:**
- If the query requires unique records or there's a possibility of duplicates, use the `DISTINCT` keyword to eliminate duplicate results.
- Ensure that `DISTINCT` is applied appropriately to the correct columns.

- **Handle Logical Operators Correctly:**
- Pay close attention to logical operators such as `AND` and `OR` in the user's query.
- Ensure conditions are combined correctly in the SQL statement to match the user's intent.

- **Consider Tied Results:**
- When dealing with `MAX`, `MIN`, `TOP`, or ranking queries, consider that multiple records may share the same value.
- Include all relevant records that meet the criteria, accounting for possible ties.

- **Data Types and Precision:**
- Be mindful of data types when performing calculations.
- Use appropriate type casting or functions to prevent precision loss, especially with integer division.
- Ensure calculations yield accurate and precise results.

- **Handle Special Data Formats:**
- If the data contains special formats (e.g., dates, times), use appropriate SQL functions to handle them correctly.
- Consider edge cases, such as leap years or time zones, if relevant.

- **Avoid Assumptions Based on Common Sense:**
- Rely on the provided table schemas and data descriptions.
- Do not make assumptions that contradict the given information, even if it seems counterintuitive.

- **Combine Conditions Appropriately:**
- Where possible, combine multiple conditions into a single SQL query rather than splitting them into separate queries.
- Use subqueries or joins as needed to meet complex query requirements.

- **Null and Empty Data Handling:**
- Consider the possibility of `NULL` or missing data.
- Use appropriate SQL functions (e.g., `COALESCE`, `IS NULL`) to handle such cases.
- Ensure that queries do not fail due to unhandled `NULL` values.

- **Thorough Reasoning:**
- In the Evidence section, provide a detailed explanation of your reasoning.
- Explain how you interpret the user's request and map it to the table columns.
- Mention how you handle potential issues like duplicates, ties, or special data formats.

**Example:**
```
Evidence: We need the name column, country column and age column of the table singers, in descending order of age.
ANSWER: SELECT name, country, age FROM singer ORDER BY age DESC;
```
"""
    sys_temp_old = """
    You are a powerful AI assistant, a variant of ChatGPT that can transform user queries into SQL commands. You are an expert in databases, proficient in SQL statements, and can use the database to help users.

    **Rules:**

    1. **Database Type:** The databases are `.sqlite`, so use SQLite grammar instead of MySQL grammar.

    2. **Column Names with Spaces:** If the column name contains spaces (e.g., `"xxx xxx"`), use backticks like `xxx xxx` as the column name.

    3. **Output Format:** Please answer the user's question in the following format, including the leading and trailing "```" and "```", and ";" at the end of the SQL command:

    ```
    Evidence: <reasoning your decision according to the columns in the table>
    ANSWER: <SQL command>;
    ```

    **Example:**
    ```
    Evidence: We need the name column, country column and age column of the table singers, in descending order of age.
    ANSWER: SELECT name, country, age FROM singer ORDER BY age DESC;
    ```
    """
    return sys_temp


def sql_execeute(response, target_sql, user_inp, db_name):

    ori_sql_cmd = response['sql']
    #print(f"\nEvidence0: {response['description']}\n")

    ori_sql_cmd = ori_sql_cmd.replace('\n',' ')
    script_dir = Path(__file__).parent.resolve()
    conn =sqlite3.connect(script_dir/"databases\dev_databases\{}\{}.sqlite".format(db_name, db_name))#here define spider dataset position
    cur = conn.cursor()
    try:
        #print(ori_sql_cmd, db_name)
        cur.execute(ori_sql_cmd)

    except:

        print("error sql:{}".format(ori_sql_cmd))
        ori_sql_cmd = judge(ori_sql_cmd, user_inp, db_name)
        ori_sql_cmd = ori_sql_cmd.replace(';', '')
        if ori_sql_cmd != 'None':
            try:
                cur.execute(ori_sql_cmd)
            except:
                print("AGAIN error sql:{}".format(ori_sql_cmd))
                return 0
        else:
            print("AGAIN error sql.")
            return 0


    r1 = cur.fetchall()
    cur.execute(target_sql)
    r2 = cur.fetchall()
    r1 = Counter(r1)
    r2 = Counter(r2)
    print("ours:" + ori_sql_cmd)
    print("target:" +target_sql)
    #print(r1,r2)
    """
    for i in r1:
        if i not in r2:
            print(i)
    """
    if dict(r1) == dict(r2):
    #if r1 == r2:
        return 1
    else:
        """
        for i in r2:
            if i not in r1:
                print(i)
        """
        return 0

def generate_chat_responses(user_inp,target_sql, db_name):
    # ask stepsF

    #print(user_inp)
    full_msg = []
    usr_prompt = """
    Please tell me what standard SQL statements should I use in order to respond to the "USER INPUT". \
    Please finish request in one step, with the help of following table information:
    {}
    Please remember to follow the output format in system prompt.
    USER INPUT:{}
    """.format(read_tableinfo(db_name), user_inp)
    dict_sys = {'role': 'system', 'content': init_system_msg_prototype()}
    dict_usr = {'role': 'user', 'content': usr_prompt}
    full_msg.append(dict_sys)
    full_msg.append(dict_usr)
    #print(full_msg)
    try:

        response = create_chat_completion(full_msg)
    except Exception as e:
        print(f"API request failed after retries: {e}")
    response = get_sql_from_response(response)

    #print(response)
    #response = []
    #data_relevance = check_relevant_data(user_inp, response, db_name)
    #response = get_sql_from_response(data_relevance)
    #response = end_judge(response, user_inp, db_name)
    #print(response)
    #response = get_sql_from_response(response)
    #print(response)
    if len(response) == 0:
        print(f"NOT NEED MEMORY: {response}")
        return 0

    #sql_results_history, new_mem_ops = chain_of_memory(response_steps_list_of_dict, mysql_db)
    i = sql_execeute(response,target_sql, user_inp, db_name)
    #print("Finish!")
    return i





if __name__ == '__main__':
    his_msgs = []
    print("START!")
    #text = input("USER INPUT: ")
    right_counter = 0
    counter = 0
    boundary = 146
    index = []
    i = 0
    diff_counter = [0, 0, 0]
    diff_rcounter = [0, 0, 0]
    wrong_list = []
    while counter < boundary:
        #i = random.randint(0, 1033)

        text = read_json(i)[0]
        #text = 'For the client who first applied the loan in 1993/7/5, what is the increase rate of his/her account balance from 1993/3/22 to 1998/12/27 in percent?'
        #text = "The oldest SJS patient's medical laboratory work was completed on what date, and what age was the patient when he or she initially arrived at the hospital?"
        target_sql = read_json(i)[1]
        db_name = read_json(i)[2]
        difficulty = read_json(i)[3]
        if difficulty == "challenging":
            diff_flag = 0
        if difficulty == "moderate":
            diff_flag = 1
        if difficulty == "simple":
            diff_flag = 2
        #flag = sql_execeute({'sql':"SELECT races.year, AVG(results.milliseconds*0.001) as average_finish_time_seconds FROM races JOIN results ON races.raceId = results.raceId WHERE results.position = 1 GROUP BY races.year",'description':'1'},target_sql,'1','formula_1')
        print("Q{}".format(i))


        flag = generate_chat_responses(text, target_sql, db_name)
        if flag == 1:
            print("correct.")
            diff_rcounter[diff_flag] = diff_rcounter[diff_flag] + 1
        else:
            print("wrong answer.")
            wrong_list.append(i)
        right_counter = right_counter + flag
        diff_counter[diff_flag] = diff_counter[diff_flag] + 1
        counter = counter + 1

        print("current scores:{}".format(right_counter/counter))
        print("Challenging Accuracy:{}/{}".format(diff_rcounter[0], diff_counter[0]))
        print("Moderate Accuracy:{}/{}".format(diff_rcounter[1], diff_counter[1]))
        print("Simple Accuracy:{}/{}".format(diff_rcounter[2], diff_counter[2]))
        #time.sleep(0.2)
        i = i + 1
        print(wrong_list)
