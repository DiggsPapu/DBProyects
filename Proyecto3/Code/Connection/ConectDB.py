import psycopg2
def getUser(use,p):
    cursor = connect()
    cursor.execute('''select * from usuario where userid = '{}' and password = '{}' '''.format(use,p))
    values = cursor.fetchone()
    if (values!=None):       
        valores = []
        count = 0
        for x in values:
            valores.append(x)
            count+=1
        valores.append('usuario')
        return valores
    cursor.execute('''select * from worker where workerid = '{}' and workerpassword = '{}' and workertype = 'Instructor' '''.format(use,p))
    values = cursor.fetchone()
    if (values!=None):
        valores = []
        count = 0
        for x in values:
            valores.append(x)
            count+=1
        valores.append('Instructor')
        return valores
    cursor.execute('''select * from worker where workerid = '{}' and workerpassword = '{}' and workertype = 'admin_reportery' '''.format(use,p))
    values = cursor.fetchone()
    if (values!=None):
        valores = []
        count = 0
        for x in values:
            valores.append(x)
            count+=1
        valores.append('admin_reportery')
        return valores
    cursor.execute('''select * from worker where workerid = '{}' and workerpassword = '{}' and workertype = 'admin_create_role' or workertype = 'Superuser' '''.format(use,p))
    values = cursor.fetchone()
    if (values!=None):
        valores = []
        count = 0
        for x in values:
            valores.append(x)
            count+=1
        valores.append('admin_create_role')
        return valores
    return None  
def connect():
    conn= psycopg2.connect(
        database="proyect",
        user='postgres',
        password='Manager123',
        host='localhost',
        port='5432'
    )
    conn.autocommit=True
    #Creating curso
    return conn.cursor()
def connectAdmin(worker_id, worker_password):
    conn= psycopg2.connect(
        database="proyect",
        user=worker_id,
        password=worker_password,
        host='localhost',
        port='5432'
    )
    conn.autocommit=True
    #Creating curso
    return conn.cursor()


