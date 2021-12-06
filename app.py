from flask import Flask,render_template,request
import json
from database.server_database_controller import initial_config,execute_sql_sentences,run_build,get_build_sql_wId,get_build_sql_wDate,create_build

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

#TO ERASE: Execute a specific BUILD
@app.route('/build',methods=["POST"])
def building():
    result=run_build(  int(request.form.get("build_id"))  )
    return render_template("simple_msg.html",msg=result)

#Get build sql sentences with  to client
@app.route('/build-sql-date',methods=["POST"])
def get_build_sql_date():
    result=get_build_sql_wDate(request.form.get("last_update_date"))
    _json={}
    count=1 
    for item in result:
        _json[count]=item
        count+=1
    return (_json)

    #Get build sql sentences to client
@app.route('/build-sql-id',methods=["POST"])
def get_build_sql_id():
    result=get_build_sql_wId(request.form.get("build_id"))
    _json={}
    count=1 
    for item in result:
        _json[count]=item
        count+=1
    return (_json)

@app.route('/add-build',methods=["POST"])
def build():
    description=request.form.get("description")
    sql_sentences=request.form.get("sql_sentences")
    results=create_build(description,sql_sentences)
    return render_template("simple_msg.html",msg=results)

if __name__ == '__main__':
    app.run(debug=True)

#Pending: - Documentar Código 
#         - Eliminar el uso de updated_at
#         - Eliminar changes_sql_sentences y build_sql_sentences
#         - Evaluar sql_sentences como pedazos largos de código
#         - Servidor que Implemente los cambios automaticamente 
#         - Interfaz para agregar más facil los build
#         - Seguridad para interfaz gráfica

#builds.description , Update_Id , updates.name , changes.description , changes.sequence , sql_sentences(arr) , change_sql_sentences.sequence