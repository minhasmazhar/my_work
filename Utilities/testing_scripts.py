import psycopg2

try:
    connection = psycopg2.connect(user='minhas',
                                  password='admin',
                                  host='localhost',
                                  port=5432,
                                  database='hrms')

    cursor = connection.cursor()
    print(connection)
except Exception as e:
    print("Database connection failed!")
    print(e)
