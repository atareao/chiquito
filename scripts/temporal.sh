#!/bin/bash
while read line
do
	author="Chiquito de la calzada"
	frase="'$line'"
	timestamp=$(date +%s)
	echo "INSERT INTO JOKES (AUTHOR, VALUE, CREATED_AT, UPDATED_AT) VALUES ($author, $frase, $timestamp, $timestamp)"
done < frases.txt

