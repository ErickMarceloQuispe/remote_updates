SELECT sql_sentence FROM sql_sentences where sql_sentence_id in (
  select sql_sentence_id from change_sql_sentences where change_id in 
  (select change_id from changes where update_id="v1.3"));