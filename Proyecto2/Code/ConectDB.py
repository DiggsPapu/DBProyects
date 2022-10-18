import psycopg2
def connectDB():
    conn= psycopg2.connect(
        database="Proyect02",
        user='postgres',
        password='Manager123',
        host='localhost',
        port='5432'
    )
    conn.autocommit=True
    #Creating curso
    return conn.cursor()

