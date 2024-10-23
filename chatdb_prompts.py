from langchain.prompts import PromptTemplate
#from sql_examples import choose_egs
#from sql_examples import egs
from table_schema import read_tableinfo



def usr_prompt(db_name,usr_inp):
    read_tableinfo(db_name)
    prmpt = """
Please tell me what standard SQL statements should I use in order to respond to the "USER INPUT". \
Please finish request in one step, with the help of following table information:
{}
Please remember to follow the output format in system prompt.
USER INPUT:{}
""".format(read_tableinfo(db_name),usr_inp)
    return(prmpt)


if __name__ == '__main__':
    print(prompt_ask_steps_no_egs.format(user_inp="Who bought 100kg apple on 2010-03-27 and what is he/she name, detailed information and costumer id?"))
