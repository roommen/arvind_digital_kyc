import mysql.connector

def create_wifi_track():
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
        cursor.execute('CREATE TABLE WiFiTrack('
                       'Track_ID DOUBLE NOT NULL AUTO_INCREMENT PRIMARY KEY,'
                       'MAC_ID VARCHAR(50) NOT NULL,'
                       'Manufacturer VARCHAR(75) NOT NULL,'
                       'Signal_Strength INTEGER NOT NULL,'
                       'Time_In DATETIME NOT NULL,'
                       'Time_Out DATETIME NOT NULL)'
                       ';')
        print("Table WiFiTrack created successfully.")
    except mysql.connector.Error as err:
        print(err)
    finally:
        if connection:
            connection.close()
        if cursor:
            cursor.close()

if __name__ == '__main__':
    create_wifi_track()
