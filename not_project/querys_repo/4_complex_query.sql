SELECT changes.description,sql_sentences.sql_sentence FROM sql_sentences 
inner join change_sql_sentences on sql_sentences.sql_sentence_id=change_sql_sentences.sql_sentence_id
INNER JOIN changes on changes.change_id=change_sql_sentences.change_id
where update_id = "v1.3"