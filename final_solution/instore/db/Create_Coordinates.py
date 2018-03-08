import mysql.connector

def create_coordinates():
    connection, cursor = None, None
    try:
        #MySQL Database Connection Parameters
        arvind_cnx_str = {'host': 'f1.cemnrzna330w.ap-south-1.rds.amazonaws.com',
           'username': 'runcy',
           'password': 'enternow123',
           'db': 'f1'}
        connection = mysql.connector.connect(host=arvind_cnx_str['host'], user=arvind_cnx_str['username'],
                                             password=arvind_cnx_str['password'], database=arvind_cnx_str['db'])
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE Coordinates('
                       'Coordinate_ID DOUBLE NOT NULL AUTO_INCREMENT PRIMARY KEY,'
                       'TimeStamp DATETIME NOT NULL,'
                       'CX INTEGER NOT NULL,'
                       'CY INTEGER NOT NULL)'
                       ';')
        print("Table Coordinates created successfully.")
    except mysql.connector.Error as err:
        print(err)
    finally:
        if connection:
            connection.close()
        if cursor:
            cursor.close()

if __name__ == '__main__':
    create_coordinates()
