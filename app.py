from flask import Flask,render_template,request

from database.server_database_controller import initial_config,execute_sql_sentences

app = Flask(__name__)

initial_config()

@app.route('/',methods=["GET"])
def hello_world():
    return render_template("sql_execute_form.html")

@app.route('/sql',methods=["POST"])
def sql_execute():
    result=execute_sql_sentences([request.form.get("sql_sentence")])
    return render_template("simple_msg.html",msg=result)

if __name__ == '__main__':
    app.run(debug=True)

#Pending: - Just Select Validator    