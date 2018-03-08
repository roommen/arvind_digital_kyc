import mysql.connector

def create_zones():
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
        cursor.execute('CREATE TABLE Zones('
                       'Zone_ID DOUBLE NOT NULL AUTO_INCREMENT PRIMARY KEY,'
                       'TimeStamp DATETIME NOT NULL,'
                       'Old_Zone VARCHAR(3) NOT NULL,'
                       'New_Zone VARCHAR(3) NOT NULL)'
                       ';')
        print("Table Zones created successfully.")
    except mysql.connector.Error as err:
        print(err)
    finally:
        if connection:
            connection.close()
        if cursor:
            cursor.close()

if __name__ == '__main__':
    create_zones()
