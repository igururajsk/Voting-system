# debug_test.py  (save as this name or overwrite test.py)
print("script started")

import mysql.connector
print("imported mysql.connector")

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Highmonk@5253',
        database='votingsystem',
        port=3306,
        connect_timeout=5
    )
    print("Connected to DB")
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print("Test query result:", cur.fetchone())
    conn.close()
except Exception as e:
    # show full exception info (safe to paste here)
    import traceback
    traceback.print_exc()
    print("repr:", repr(e))

print("script finished")
