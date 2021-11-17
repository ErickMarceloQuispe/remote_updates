initial_server_sql=[
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
            sql_sentence_id INTEGER NOT NULL,
            sequence INTEGER NOT NULL,
            FOREIGN KEY (build_id) REFERENCES builds(build_id),
            FOREIGN KEY (sql_sentence_id) REFERENCES sql_sentences(sql_sentence_id)
        );"""]
desc_initial_server_sql=["pragma table_info(builds)","pragma table_info(sql_sentences)","pragma table_info(build_sql_sentences)"]
reinit_server_required=["""select DISTINCT count(tbl_name) from sqlite_master WHERE tbl_name='builds' or tbl_name='sql_sentences' OR tbl_name='build_sql_sentences';"""]