import sqlite3
import database.global_sql_sentences as GSql

DB_NAME="database/test_remote.db"

#Convierte los bloques de SQL en un arreglo de sentencias sql individuales usando como divisor ';\n'
def dividir_sql_sentences(sql_sentences):
    if(type(sql_sentences)==str):
        sql_sentences=sql_sentences.split(";\n")
    return sql_sentences

#Transforma los simbolos especiales usados en muchas sentencias dentro de otras a simbolos compatibles con SQL
def tranform_symbols(sql_sentence):
    sql_sentence=sql_sentence.replace("`","'")
    sql_sentence=sql_sentence.replace(";",";\n")
    return sql_sentence

#Ejecuta una sentencia sql (la divide por defecto) y retorna los resultados de la ejecución
def execute_sql_sentences(sql_sentences,dividir=True):
    try:
        if(dividir):
            sql_sentences=dividir_sql_sentences(sql_sentences)
        else:
            sql_sentences=[sql_sentences]
        conn = sqlite3.connect(DB_NAME)
        c=conn.cursor()
        results=[]
        for sql_sentence in sql_sentences:
            print("-> "+sql_sentence)
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
        create_build("First Build",GSql.first_build,True)
    run_downloaded()

#Crea un Build segun una descripción y un conjunto de sentencias; y lo ejecuta
def create_build(build_desc,sql_sentences,is_new_build_needed): 
    if(sql_sentences==None):
        return ["Ingrese los datos necesarios"]
    count=0
    if(is_new_build_needed):
        if(build_desc==None):
            return ["Ingrese los datos necesarios"]
        execute_sql_sentences("INSERT INTO builds(description) VALUES ('%s');" %build_desc)
    count+=1
    execute_sql_sentences("""INSERT INTO sql_sentences(sql_sentence) VALUES ('%s');"""%sql_sentences,False)
    execute_sql_sentences("""INSERT INTO build_sql_sentences(build_id,sql_sentence_id,sequence)
            VALUES (
                (SELECT build_id FROM builds ORDER BY build_id DESC LIMIT 1),
                (SELECT sql_sentence_id FROM sql_sentences ORDER BY sql_sentence_id DESC LIMIT 1),
                %s
        );"""%count)
    build_id=execute_sql_sentences("SELECT build_id FROM builds ORDER BY build_id DESC LIMIT 1;")[0][0]
    results=run_build(build_id)
    return results

#Retorna las sentencias sql de los 'build' de cada 'update' realiazado posterior a la fecha indicada
def get_build_sql_wDate(last_update_date):
    sql_sentence="""SELECT sql_sentence FROM sql_sentences WHERE sql_sentence_id IN ( 
                    SELECT sql_sentence_id FROM build_sql_sentences WHERE build_id IN 
                    (SELECT build_id FROM updates WHERE created_at > "%s" ORDER BY created_at) ORDER BY sequence);\n"""%last_update_date
    results=execute_sql_sentences(sql_sentence)
    build_sql_sentences=[]
    for item in results:
        build_sql_sentences.append(item[0])
    return build_sql_sentences

#Retorna las sentencias sql del 'build' cuyo ID es el especificado
def get_build_sql_wId(build_id):
    sql_sentence="""SELECT sql_sentence FROM sql_sentences WHERE sql_sentence_id IN 
                (SELECT sql_sentence_id FROM build_sql_sentences WHERE build_id = %s ORDER BY sequence);\n"""%build_id
    results=execute_sql_sentences(sql_sentence)
    sql_sentence_arr=[]
    for item in results:
        item=list(item)
        sql_sentence_arr.append(item[0])
    return sql_sentence_arr

#Ejecuta un build especifico cuyo ID es el indicado
def run_build(build_id):
    results=[]
    for sql_sentence in get_build_sql_wId(build_id):
        results+=execute_sql_sentences(sql_sentence)
    results.append("Build Ejecutado Correctamente")
    run_downloaded()
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
        aux=tranform_symbols(item[0])
        print(aux)
        execute_sql_sentences(aux)
    execute_sql_sentences("UPDATE updates SET status='Installed' WHERE status='Downloaded';")