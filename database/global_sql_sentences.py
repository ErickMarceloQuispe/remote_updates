#Construcción de builds-sql_sentences
initial_server_sql=[
    """PRAGMA foreign_keys = ON;""",
    """DROP TABLE IF EXISTS build_sql_sentences;""",
    """DROP TABLE IF EXISTS builds;""",
    """DROP TABLE IF EXISTS sql_sentences;""",
    """CREATE TABLE builds (
            build_id INTEGER PRIMARY KEY AUTOINCREMENT,
            description varchar(255)
        );""",

    """CREATE TABLE sql_sentences(
            sql_sentence_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sql_sentence BLOB NOT NULL
        );""",

    """CREATE TABLE build_sql_sentences (
            build_id INTEGER NOT NULL,
            sql_sentence_id INTEGER NOT NULL,
            sequence INTEGER NOT NULL,
            FOREIGN KEY (build_id) REFERENCES builds(build_id),
            FOREIGN KEY (sql_sentence_id) REFERENCES sql_sentences(sql_sentence_id)
        );"""]

#Descripción de las tablas principales creadas con anterioridad
desc_initial_server_sql=["pragma table_info(builds)","pragma table_info(sql_sentences)","pragma table_info(build_sql_sentences)"]

#Consulta la existencia de las tablas principales
reinit_server_required=["""select DISTINCT count(tbl_name) from sqlite_master WHERE tbl_name='builds' or tbl_name='sql_sentences' OR tbl_name='build_sql_sentences';"""]

#Primer Build ejecutado al iniciar el servidor
first_build=[
        """DROP TABLE IF EXISTS updates;""",
        """DROP TABLE IF EXISTS changes;""",
        """DROP TABLE IF EXISTS change_sql_sentences;""",
        """PRAGMA foreign_keys = ON;""",
        """Create TABLE updates(update_id VARCHAR(255) NOT NULL PRIMARY KEY,
                            name VARCHAR(255),
                            build_id INTEGER NOT NULL DEFAULT 0,
                            status VARCHAR(255) DEFAULT "Downloaded",
                            created_at timestamp  NOT NULL  DEFAULT current_timestamp,
                            updated_at timestamp  NOT NULL  DEFAULT current_timestamp,
                            FOREIGN KEY (build_id) REFERENCES builds(build_id));""",

        """CREATE TRIGGER LastUpdate_Updates UPDATE OF update_id,name ON updates
                BEGIN
                UPDATE updates SET updated_at=CURRENT_TIMESTAMP WHERE id=id;
                END;""",

        """CREATE TABLE changes(change_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            update_id VARCHAR(255) NOT NULL,
                            description VARCHAR(255),
                            sequence INTEGER not NULL,
                            FOREIGN KEY (update_id) REFERENCES updates(update_id));""",

        """CREATE TABLE change_sql_sentences(change_id INTEGER NOT NULL,
                            sql_sentence_id VARCHAR(255) NOT NULL,
                            sequence INTEGER not NULL,
                            FOREIGN KEY (change_id) REFERENCES changes(change_id),
                            FOREIGN KEY (sql_sentence_id) REFERENCES sql_sentences(sql_sentence_id));"""]