import aws.sqs as sqs


def insertOrder(con, order):

    # Start by inserting order to DB
    result = insertOrderDB(con, order)

    # If order didn't already exist ..
    if result:
        # Create AWS client first
        client = sqs.createClient()
        # Printing here so we have visibility
        print(order)
        # Add order to next queue
        # 03-Jan-10 RC Renabling
        sqs.sendMessage(client, order)
        # Trigger Lamnda by sending an sns
        sqs.sendSNS()
        return True
    return False


def insertOrderDB(con, order):
    # Prepare connection
    mycursor = con.cursor()

    # prepare query
    sql = "insert into orders (id, orderDate, orderDateUTC, pair, direction, priceTarget, actionType, insertDate) values (null, '" + order['orderDate'] + \
        "','" + order['orderDateUTC'] + "','" + order['pair'] + "','" + order['direction'] + \
        "'," + str(order['priceTarget']) + ",'" + \
        order['actionType'] + "',NOW()); "

    try:
        mycursor.execute(sql)
        con.commit()
        print('New order added to DB')
        return True
    except Exception as err:
        print(err)
        return False
