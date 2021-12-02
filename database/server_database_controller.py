from re import A
import sqlite3
#from app import building
import database.global_sql_sentences as GSql

DB_NAME="database/test_remote.db"

def process_sql_sentences(sql_sentences):
    if(type(sql_sentences)==str):
        sql_sentences=sql_sentences.split(";")
    return sql_sentences

def execute_sql_sentences(sql_sentences):
    try:
        sql_sentences=process_sql_sentences(sql_sentences)
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
    except sqlite3.IntegrityError:
        return ["Posible repetición de Primary Key"]
    except Exception as e:
        print(e)
        conn.commit()
        conn.close
        return ["Fallo"]
    

def initial_config():
    exist_main_tables=execute_sql_sentences(GSql.reinit_server_required)[0][0]>0
    if(not exist_main_tables):
        execute_sql_sentences(GSql.initial_server_sql)
        execute_sql_sentences(GSql.desc_initial_server_sql)
        create_build("First Build",GSql.first_build)
        run_build(1)

def create_build(build_desc,sql_sentences): 
    if(build_desc==None or sql_sentences==None):
        return ["Ingrese los datos necesarios"]
    sql_sentences=process_sql_sentences(sql_sentences)
    count=0
    sql_complete=["INSERT INTO builds(description) VALUES ('%s');" %build_desc]
    for sql_sentence in sql_sentences:
        count+=1
        sql_complete.append("""INSERT INTO sql_sentences(sql_sentence) VALUES ('%s');""" %sql_sentence)
        sql_complete.append(
            """INSERT INTO build_sql_sentences(build_id,sql_sentence_id,sequence)
                VALUES (
                    (SELECT build_id FROM builds ORDER BY build_id DESC LIMIT 1),
                    (SELECT sql_sentence_id FROM sql_sentences ORDER BY sql_sentence_id DESC LIMIT 1),
                    %s
            );"""%count)
    execute_sql_sentences(sql_complete)
    build_id=execute_sql_sentences(["SELECT build_id FROM builds ORDER BY build_id DESC LIMIT 1"])[0][0]
    print("BUILD: "+str(build_id))
    results=run_build(build_id)
    return results

def get_build_sql_sentences(build_id):
    sql_sentence="""SELECT sql_sentence from sql_sentences where sql_sentence_id in 
                (SELECT sql_sentence_id from build_sql_sentences where build_id = %s ORDER By sequence desc)"""%build_id
    results=execute_sql_sentences([sql_sentence])
    build_sql_sentences=[]
    for item in results:
        build_sql_sentences.append(item[0])
    return build_sql_sentences

def run_build(build_id):
    results=execute_sql_sentences(get_build_sql_sentences(build_id))
    return results

#TO CLIENT
def update_needs_query(date):
    sql_sentence="" 
    if(date!=None):
        sql_sentence="""select * from updates where created_at > %s order by created_at;
                    select * from updates order by created_at;"""%date
    else:
        sql_sentence="select * from updates order by created_at;"
    results=execute_sql_sentences([sql_sentence])
    print(results)