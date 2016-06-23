drop table if exists article;
create table article (
	 id integer primary key autoincrement,
	 domain varchar(128),
	 title varchar(128),
	 category varchar(128),
	 data_type varchar(12),
	 link varchar(128),
	 pub_date datetime,
	 crawl_date datetime,
	 content text
);
create index crawl_date_idx on article (crawl_date asc);
create index domain_title_pub_date_idx on article (domain, title, pub_date);
drop table if exists feed;
create table feed (
	id integer primary key autoincrement,
	url varchar(128) unique not null,
	create_date datetime not null
);
