import sqlite3
DB_NAME="test_remote"

def execute_sql_sentences(sql_sentences,db_name):
    conn = sqlite3.connect(db_name)
    c=conn.cursor()
    for sql_sentence in sql_sentences:
        print(sql_sentence)
        c.execute(sql_sentence)
        for item in c.fetchall():
            print(item)
    conn.commit()
    conn.close()

def dropTables(table_names,db_name):
    for table_name in table_names:
        execute_sql_sentences([
            """IF EXIST DESC pragma table_info({table_name}) drop table {table_name}';""",
        ],db_name)

def initial_config():
    building_builds=[
    """PRAGMA foreign_keys = ON;""",
    """DROP TABLE IF EXISTS build_sql_sentences""",
    """DROP TABLE IF EXISTS builds""",
    """DROP TABLE IF EXISTS sql_sentences""",
    """create table builds (
            build_id INTEGER NOT NULL PRIMARY KEY,
            description varchar(255)
        );""",

    """create table sql_sentences (
            sql_sentence_id INTEGER NOT NULL PRIMARY KEY,
            description varchar(255),
            sql_sentence varchar(1000) NOT NULL
        );""",

    """create table build_sql_sentences (
            build_id INTEGER NOT NULL,
            FOREIGN KEY (build_id) REFERENCES builds(build_id)
        );""",

    """alter table build_sql_sentences add foreign KEY(build_id) references builds(build_id);""",

    """alter table build_sql_sentences add foreign KEY(sql_sentence_id) references sql_sentences(sql_sentence_id);"""]
    execute_sql_sentences(building_builds,DB_NAME)

initial_config()
execute_sql_sentences(["pragma table_info(builds)","pragma table_info(sql_sentences)","pragma table_info(build_sql_sentences)"],DB_NAME)
#sql_sentence_id INTEGER NOT NULL,
#            sequence INTEGER NOT NULL
#FOREIGN KEY (sql_sentence_id) REFERENCES sql_sentences(sql_sentence_id),