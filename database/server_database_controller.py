import sqlite3
import database.global_sql_sentences as GSql

DB_NAME="database/test_remote.db"

def execute_sql_sentences(sql_sentences):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    results=[]
    for sql_sentence in sql_sentences:
        print(sql_sentence)
        c.execute(sql_sentence)
        for item in c.fetchall():
            results.append(item)
    conn.commit()
    conn.close()
    return results

def initial_config():
    exist_main_tables=execute_sql_sentences(GSql.reinit_server_required)[0][0]>0
    if(not exist_main_tables):
        execute_sql_sentences(GSql.initial_server_sql)
        execute_sql_sentences(GSql.desc_initial_server_sql)