import MySQLdb
import random
import string

db = MySQLdb.connect(host="localhost", user="root", passwd="1480", db="test", charset='utf8')
cursor = db.cursor()

for i in range(1000000):
    a = random.randint(0,1000)
    b = random.randint(0,1000)
    c = random.randint(0,1000)
    d = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))

    sql = """INSERT INTO table2(a, b, c, d)
    VALUES (%d, %d, %d, '%s')
    """ % (a, b, c, d)

    cursor.execute(sql)

db.commit()
 
db.close()