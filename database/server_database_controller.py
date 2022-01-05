import sqlite3
import database.global_sql_sentences as GSql

DB_NAME="database/test_remote.db"

#Convierte los bloques de SQL en un arreglo de sentencias sql individuales
def process_sql_sentences(sql_sentences):
    if(type(sql_sentences)==str):
        sql_sentences=sql_sentences.split(";")
    return sql_sentences

#Ejecuta el arreglo de sentencias sql y retorna los diferentes resultados del arreglo
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
        return results
    except sqlite3.IntegrityError:
        return ["Posible repetición de Primary Key"]
    except Exception as e:
        print(e)
        return [str(e)]
    finally:
        conn.commit()
        conn.close
    
#Configuración Inicial del Servidor (Build-Sql_Sentences)
def initial_config():
    exist_main_tables=execute_sql_sentences(GSql.reinit_server_required)[0][0]>0
    if(not exist_main_tables):
        execute_sql_sentences(GSql.initial_server_sql)
        execute_sql_sentences(GSql.desc_initial_server_sql)
        create_build("First Build",GSql.first_build)

#Crea un Build segun una descripción y un conjunto de sentencias; y lo ejecuta
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
    results=run_build(build_id)
    run_downloaded()
    return results

#Retorna las sentencias sql de los 'build' de cada 'update' realiazado posterior a la fecha indicada
def get_build_sql_wDate(last_update_date):
    sql_sentence="""SELECT sql_sentence FROM sql_sentences where sql_sentence_id in ( 
                    select sql_sentence_id from build_sql_sentences where build_id in 
                    (select build_id from updates where created_at > "%s" order by created_at));"""%last_update_date
    results=execute_sql_sentences([sql_sentence])
    build_sql_sentences=[]
    for item in results:
        build_sql_sentences.append(item[0])
    return build_sql_sentences

#Retorna las sentencias sql del 'build' cuyo ID es el especificado
def get_build_sql_wId(build_id):
    sql_sentence="""SELECT sql_sentence from sql_sentences where sql_sentence_id in 
                (SELECT sql_sentence_id from build_sql_sentences where build_id = %s ORDER By sequence desc)"""%build_id
    results=execute_sql_sentences([sql_sentence])
    build_sql_sentences=[]
    for item in results:
        build_sql_sentences.append(item[0])
    return build_sql_sentences

#Ejecuta un build especifico cuyo ID es el indicado
def run_build(build_id):
    results=execute_sql_sentences(get_build_sql_wId(build_id))
    results.append("Build Ejecutado Correctamente")
    return results


#Ejecuta todas las actualizaciones Descargadas y cambia su estado a Instaladas
def run_downloaded():
    sql_sentences=(execute_sql_sentences("""
    SELECT sql_sentence FROM sql_sentences where sql_sentence_id in 
        ( select sql_sentence_id from change_sql_sentences where change_id in 
            (SELECT change_id FROM changes WHERE update_id IN 
                (SELECT update_id from updates where status='Downloaded' ORDER BY created_at) ORDER BY sequence) ORDER BY sequence
        );"""))
    for item in sql_sentences:
        execute_sql_sentences(item[0].replace("`","'"))
    execute_sql_sentences("UPDATE updates SET status='Installed' WHERE status='Downloaded';")