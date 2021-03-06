from flask import Flask,render_template,request
from database.server_database_controller import initial_config,execute_sql_sentences,get_build_sql_wId,get_build_sql_wDate,create_build,run_build

app = Flask(__name__)

#Inicia la configuración (Tablas Primarias de Base de Datos)
initial_config()

#Retorna un form sencillo para la ejecución de sentencias SQL
@app.route('/',methods=["GET"])
def sql_interface():
    return render_template("sql_execute_form.html")

#Ejecuta el sql mandado desde el form
@app.route('/sql',methods=["POST"])
def sql_execute():
    result=execute_sql_sentences(request.form.get("sql_sentence"))
    _json={}
    count=1 
    for item in result:
        _json[count]=item
        count+=1
    return (_json)

#Retorna todas las sentencias sql de los 'build' de 'updates' posteriores a la fecha enviada
@app.route('/build-sql-date',methods=["POST"])
def get_build_sql_date():
    result=get_build_sql_wDate(request.form.get("last_update_date"))
    _json={}
    count=1 
    for item in result:
        _json[count]=item
        count+=1
    return (_json)

#Retorna todas las sentencias sql del 'build' cuyo id es el enviado
@app.route('/build-sql-id',methods=["POST"])
def get_build_sql_id():
    result=get_build_sql_wId(request.form.get("build_id"))
    _json={}
    count=1 
    for item in result:
        _json[count]=item
        count+=1
    return (_json)

#Retorna un form sencillo para la adición de un build
@app.route('/add-build',methods=["GET"])
def add_build_interface():
    return render_template("create_build.html")

#Construye un build segun la descripción y las sentencias sql enviadas
#(La estructura lógica de update-change-sql_sentence depende de las sentencias enviadas)
@app.route('/add-build',methods=["POST"])
def build():
    description=request.form.get("description")
    sql_sentences=request.form["sql_sentences"]
    sql_sentences=sql_sentences.replace(chr(13),'')
    is_new_build_needed=request.form.get("create_build")
    if not is_new_build_needed=="False":
        is_new_build_needed=True
    else:
        is_new_build_needed=False
    results=create_build(description,sql_sentences,is_new_build_needed)
    return render_template("simple_msg.html",msg=results)

#Retorna un form sencillo para la ejecución de un build
@app.route('/build',methods=["GET"])
def run_build_interface():
    return render_template("execute_build.html")

#Ejecuta un build en el servidor según un build_id específico
@app.route('/build',methods=["POST"])
def run_build_wId():
    build_id=request.form.get("build_id")
    results=run_build(build_id)
    return render_template("simple_msg.html",msg=results)

#Inicio de Aplicación en modo Debug
if __name__ == '__main__':
    app.run(debug=True)

#Pending: - Interfaz para agregar más facil los build
#         - Seguridad para interfaz gráfica

#builds.description , Update_Id , updates.name , changes.description , changes.sequence , sql_sentences(arr) , change_sql_sentences.sequence