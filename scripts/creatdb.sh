#!/bin/bash
HOSTNAME="localhost"
PORT="3306"
USERNAME="root"
PASSWORD="seuevege"
DBNAME="db_lanmonitor"
TABLENAME="lan"

MYSQL_CMD="mysql -h${HOSTNAME} -u${USERNAME} -p${PASSWORD}"
echo ${MYSQL_CMD}
echo "create database ${DBNAME}"
create_db_sql="create database IF NOT EXISTS ${DBNAME}"
echo ${create_db_sql} | ${MYSQL_CMD}
if [ $? -ne 0 ]
then
	echo "create databases ${DBNAME} failed ..."
	exit 1
fi

echo "create table ${TABLENAME}"
create_table_sql="create table ${TABLENAME}(
id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
time datetime,
lanid char(64),
user varchar(2048)
)"
echo ${create_table_sql} | ${MYSQL_CMD} ${DBNAME}
if [ $? -ne 0 ]
then
	echo "create  table ${DBNAME}.${TABLENAME}  fail ..."
fi
