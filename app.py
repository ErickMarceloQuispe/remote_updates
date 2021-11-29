from flask import Flask,render_template,request
import json
from database.server_database_controller import initial_config,execute_sql_sentences,run_build

app = Flask(__name__)

initial_config()

@app.route('/',methods=["GET"])
def hello_world():
    return render_template("sql_execute_form.html")

@app.route('/sql',methods=["POST"])
def sql_execute():
    result=execute_sql_sentences(request.form.get("sql_sentence"))
    _json={}
    count=1 
    for item in result:
        _json[count]=item
        count+=1
    return (_json)
    #return render_template("simple_msg.html",msg=result)

@app.route('/build',methods=["POST"])
def building():
    result=run_build(  int(request.form.get("build_id"))  )
    return render_template("simple_msg.html",msg=result)

if __name__ == '__main__':
    app.run(debug=True)

#Pending: - Just Select Validator
#         - Añadir build_id en updates 