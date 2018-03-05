import mysql.connector

def insert_loyaltycheck(phone):
    connection, cursor = None, None
    arvind_cnx_str = {'host': 'f1.cemnrzna330w.ap-south-1.rds.amazonaws.com',
           'username': 'runcy',
           'password': 'enternow123',
           'db': 'f1'}
    try:
        connection = mysql.connector.connect(host=arvind_cnx_str['host'], user=arvind_cnx_str['username'],
                                             password=arvind_cnx_str['password'], database=arvind_cnx_str['db'])
        # Update the existing only record again and again with the just entered phone no
        update_phone = "UPDATE LoyaltyCheck SET LastEnteredPhone='%s' WHERE Trans_ID=1" % (phone)

        cursor = connection.cursor()
        cursor.execute(update_phone)
        connection.commit()

        return {"update": "true"}
    except mysql.connector.Error as err:
            return {"update": err}
    finally:
        if connection:
            connection.close()
        if cursor:
            cursor.close()


def lambda_handler(event, context):
    phone = event['phone']

    return insert_loyaltycheck(phone)
