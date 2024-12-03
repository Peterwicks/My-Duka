import psycopg2

conn=psycopg2.connect(user="postgres", host="localhost", port="5432", password="Ptr123mtd", database="duka")

cur = conn.cursor()