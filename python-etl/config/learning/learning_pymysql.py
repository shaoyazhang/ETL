import pymysql

conn = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd= 'Alph@2025',
    charset= 'utf8',
    database= 'metadata'
)

cursor = conn.cursor()

cursor.execute("show tables")

result = cursor.fetchall()

print(result)
if ('test', ) in result:
    print('存在')