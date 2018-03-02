import mysql.connector

def drop_reco():
    connection, cursor = None, None
    try:
        #Database Connection Parameters - Replace this with your DB endpoint
        arvind_cnx_str = {'host': 'dbnode.testing112ws.ap-south-1.rds.amazonaws.com',
           'username': 'user',
           'password': 'password',
           'db': 'dbname'}
        connection = mysql.connector.connect(host=arvind_cnx_str['host'], user=arvind_cnx_str['username'],
                                             password=arvind_cnx_str['password'], database=arvind_cnx_str['db'])
        cursor = connection.cursor()
        cursor.execute('DROP TABLE Reco;')
        print("Table Reco dropped successfully.")
    except mysql.connector.Error as err:
        print(err)
    finally:
        if connection:
            connection.close()
        if cursor:
            cursor.close()

if __name__ == '__main__':
    drop_reco()
