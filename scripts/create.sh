#!/bin/bash
sqlite3 frases.db <<EOF
DROP TABLE IF EXISTS JOKES;
CREATE TABLE IF NOT EXISTS JOKES(
ID INTEGER PRIMARY KEY,
AUTHOR TEXT,
VALUE TEXT,
CREATED_AT NUMERIC,
UPDATED_AT NUMERIC);
EOF
author="'Chiquito de la calzada'"
timestamp=$(date +%s)
sql=""
while read line
do
    frase="'$line'"
    #echo "INSERT INTO JOKES (AUTHOR, VALUE, CREATED_AT, UPDATED_AT) VALUES ($author,  $frase, $timestamp, $timestamp)" | sqlite3 frases.db
    sql="$sql INSERT INTO JOKES (AUTHOR, VALUE, CREATED_AT, UPDATED_AT) VALUES ($author,  $frase, $timestamp, $timestamp);"
done < frases.txt
echo $sql | sqlite3 frases.db
