drop table post
;
create table post
(
  blog_id text
  ,entry_id integer
  ,hatena_url text
  ,file_path text
  ,created_at text
  ,update_at text
)
;
insert into post (blog_id, entry_id, hatena_url, file_path, created_at, update_at) values
(
  'blog_id'
  ,1234
  ,'hatena_url'
  ,'file_path'
  ,date(CURRENT_TIMESTAMP)
  ,date(CURRENT_TIMESTAMP)
)
;
