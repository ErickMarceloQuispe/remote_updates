import requests
import json

DB_NAME="client.db"

def print_json(json_obj):
    arr_keys=json_obj.keys()
    for index in arr_keys:
		print("")
		# if(type(json_obj[index])==list):
		# 	for item in json_obj[index]:
		# 		print(str(item)+" | ")  
		# else:


def execute_sql_sentences(sql_sentences):
    if(type(sql_sentences)==str):
        sql_sentences=sql_sentences.split(";")
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
def init_config():
	exist_main_tables=execute_sql_sentences(["""
	select DISTINCT count(tbl_name) from sqlite_master 
	WHERE tbl_name='builds' or tbl_name='sql_sentences' OR tbl_name='build_sql_sentences';"""])[0][0]>0
	if(not exist_main_tables):
		url="http://localhost:5000/sql"




url="http://localhost:5000/build-sql"
_json = {"sql_sentence":
         """SELECT sql_sentence FROM sql_sentences where sql_sentence_id in (
         select sql_sentence_id from change_sql_sentences where change_id in 
         (select change_id from changes where update_id="v1.3" order by changes.sequence) 
         ORDER BY change_sql_sentences.sequence);"""
}
_json = {"sql_sentence":
        """SELECT * FROM updates;"""
}
_json = {"build_id":
        "1"
}
response = requests.post(url,_json)
#print(response.text)
json_response=json.loads(response.text)
print(type([1,2]))
#print_json(json_response)