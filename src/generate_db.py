#python2!!
import MySQLdb
import random
import string

db = MySQLdb.connect(host="localhost", user="root", passwd="1", db="test", charset='utf8')
cursor = db.cursor()

for i in range(100000):
    a = random.randint(0, 10)
    b = random.randint(0, 10)
    c = random.randint(0, 10)
    d = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(30))

    sql = """INSERT INTO t1(a, b, c, d)
    VALUES (%d, %d, %d, '%s')
    """ % (a, b, c, d)

    cursor.execute(sql)

db.commit()
 
db.close()
