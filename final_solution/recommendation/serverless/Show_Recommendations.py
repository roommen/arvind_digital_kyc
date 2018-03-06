import mysql.connector

def show_recommendations():
    connection, cursor = None, None
    arvind_cnx_str = {'host': 'f1.cemnrzna330w.ap-south-1.rds.amazonaws.com',
           'username': 'runcy',
           'password': 'enternow123',
           'db': 'f1'}
    try:
        connection = mysql.connector.connect(host=arvind_cnx_str['host'], user=arvind_cnx_str['username'],
                                             password=arvind_cnx_str['password'], database=arvind_cnx_str['db'])
        # Get phone no of the only row in the table
        sql = "SELECT LastEnteredPhone FROM LoyaltyCheck WHERE Trans_ID=1"
        cursor = connection.cursor()
        cursor.execute(sql)
        (phone, ) = cursor.fetchone()
        if phone:
            sql = "SELECT Reco1, Reco2, Reco3, Reco4, Reco5 FROM Reco WHERE Phone='%s'" % (phone)
            cursor = connection.cursor()
            cursor.execute(sql)
            (r1, r2, r3, r4, r5 ) = cursor.fetchone()
            return {"reco": "true", "r1": r1, "r2": r2,"r3": r3,"r4": r4,"r5": r5}
        else:
            return {"reco": "false"}
    except mysql.connector.Error as err:
            return {"reco": err}
    finally:
        if connection:
            connection.close()
        if cursor:
            cursor.close()


def lambda_handler(event, context):
    return show_recommendations()
