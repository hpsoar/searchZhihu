# SQL statements used to create tables for the project.

# use zhihu;

create table pages (
    id int unsigned not null auto_increment,
    page_id int unsigned not null,
    url varchar(1023) not null,
    title char(255) not null,
    content mediumtext not null,
    update_time timestamp,
    primary key (id),
    unique (page_id)
);

create table keywords (
    id int unsigned not null auto_increment,
    keyword char(31) not null,
    page_id int unsigned not null,
    score smallint not null,
    primary key (id),
    index (keyword),
    index (page_id)
);