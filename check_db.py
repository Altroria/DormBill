import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='495648',
    database='dormbill'
)

cursor = conn.cursor()
cursor.execute("SELECT id, room_no, room_name, is_guest_room FROM rooms WHERE id=1")
result = cursor.fetchone()
print(f"查询结果: {result}")

cursor.close()
conn.close()
