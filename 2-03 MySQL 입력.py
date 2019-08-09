import pymysql

### 1. 커넷션 생성 및 커서 준비

conn = pymysql.connect(host='127.0.0.1',user='aiUser' , password='1234', database= 'aidb', charset='utf8')
curr = conn.cursor()

### 2. sql 준비 및 실행
sql = "CREATE TABLE IF NOT EXISTS imageTable(fname CHAR(20), X SMALLINT , Y SMALLINT, R SMALLINT, G SMALLINT, B SMALLINT)"
curr.execute(sql)

### 3. (필요시) 커밋
conn.commit()

### 4. 연결 종료
conn.close()
curr.close()
