CREATE DATABASE test;
use test;
create table work(
	wno INT auto_increment primary key,
    subcode varchar(20) not null,
    wname varchar(20) not null,
    labno varchar(10) not null,
    adate varchar(15) not null,
    ddate varchar(15) not null,
    status INT DEFAULT 0
);
desc work;