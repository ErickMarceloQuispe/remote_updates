/* Building build ------- Cambian: "Update_id,change sequence, change_sql_sentence_sequence, main sql sentence"*/
INSERT INTO updates(update_id,name,build_id) values("v1.3",
                                                    "Primera Actualización",
                                                   (SELECT build_id FROM builds ORDER BY build_id DESC LIMIT 1));
                                                   
INSERT INTO changes(update_id,description,sequence) VALUES ("v1.3","Modulo de Prueba",1);

INSERT INTO sql_sentences(sql_sentence) values ("CREATE TABLE test(test_col VARCHAR(255))");
INSERT INTO change_sql_sentences(change_id,sql_sentence_id,sequence)
                VALUES (
                    (SELECT change_id FROM changes ORDER BY change_id DESC LIMIT 1),
                    (SELECT sql_sentence_id FROM sql_sentences ORDER BY sql_sentence_id DESC LIMIT 1),
                    1);
                    
INSERT INTO sql_sentences(sql_sentence) values ("INSERT INTO test VALUES('Hola')");
INSERT INTO change_sql_sentences(change_id,sql_sentence_id,sequence)
                VALUES (
                    (SELECT change_id FROM changes ORDER BY change_id DESC LIMIT 1),
                    (SELECT sql_sentence_id FROM sql_sentences ORDER BY sql_sentence_id DESC LIMIT 1),
                    2);