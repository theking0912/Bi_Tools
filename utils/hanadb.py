import pyhdb

# get connection
def conn_db():
    connection = pyhdb.connect(
    host="172.16.0.62",
    port=34015,
    user="XDSW_BI",
    password="QAH_Bi_2019"
    )

    return connection

# select date
def getData(conn,query_sql):
    cursor = conn.cursor()
    cursor.execute(query_sql)
    result = cursor.fetchmany(60)
    print(typeof(result))
    cursor.close()
    return result
    
# insert data
# 测试
# def insertdata(value_dic):
#     for index in range(len(value_dic)):
#         print 'Current fruit :', fruits[index]
#     print "Good bye!"

#         cursor.execute("INSERT INTO HANA_DIM.ZT_MAP_ADDR VALUES('"+LNG+','+LAT+','+country+','+PROVINCE+','+CITY+','+DISTRICT+','+STREET+','+TOWNSHIP+','+INS_DATE+"')")
#         cursor.rowcount

def typeof(variate):
    type=None
    if isinstance(variate,int):
        type = "int"
    elif isinstance(variate,str):
        type = "str"
    elif isinstance(variate,float):
        type = "float"
    elif isinstance(variate,list):
        type = "list"
    elif isinstance(variate,tuple):
        type = "tuple"
    elif isinstance(variate,dict):
        type = "dict"
    elif isinstance(variate,set):
        type = "set"
    return type        

if __name__ == '__main__':
    conn = conn_db()
    result = getdata(conn,query_sql)
    print(result)