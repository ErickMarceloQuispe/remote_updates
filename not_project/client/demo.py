import requests
import json

def print_json(json_obj):
    arr_keys=json_obj.keys()
    for index in arr_keys:
        for item in json_obj[index]:
            print(str(item)+" | ")        

url="http://localhost:5000/sql"
_json = {"sql_sentence":
        """SELECT sql_sentence FROM sql_sentences where sql_sentence_id in (
        select sql_sentence_id from change_sql_sentences where change_id in 
        (select change_id from changes where update_id="v1.3" order by changes.sequence) 
        ORDER BY change_sql_sentences.sequence);"""
}
_json = {"sql_sentence":
        """SELECT * FROM updates;"""
}
response = requests.post(url,_json)
json_response=json.loads(response.text)
print_json(json_response)

