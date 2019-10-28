import functions.dbConnect as dbConnect
import insertOrder


def generateOrders(pair):
    # Create mySql connection
    con = dbConnect.dbConnect('staging')
    mycursor = con.cursor()

    # Check if pair is something we want to trade
    if is_active(con, pair):
        # Prepare query
        sql = "select *,CAST(dateTime AS char) as newdateTime,CAST(snapshotTimeUTC AS char) as newsnapshotTimeUTC from algo_forex where pair ='" + pair + """'
                order by dateTime desc limit 4"""

        # Execute query
        mycursor.execute(sql)
        results = mycursor.fetchall()
        mycursor.close()

        # Order of columns is important and a bit flakey imo
        orderDateOriginal = results[0][0]  # dateTime
        pair = results[0][1]  # pair
        snapshotTimeUTCOriginal = results[0][2]  # snapshotTimeUTC
        openPrice = results[0][3]  # openPrice
        closePrice = results[0][4]  # closePrice
        highPrice = results[0][5]  # highPrice
        lowPrice = results[0][6]  # lowPrice
        lastTradedVolume = results[0][7]  # lastTradedVolume
        EMA_12 = results[0][8]  # EMA_12
        ema26 = results[0][9]  # EMA_26
        EMA_50 = results[0][10]  # EMA_50
        sma15 = results[0][11]  # SMA_15
        SMA_25 = results[0][12]  # SMA_25
        SMA_60 = results[0][13]  # SMA_60
        stoch_k = results[0][14]  # stoch_k
        stoch_d = results[0][15]  # stoch_d
        williamsR = results[0][16]  # williamsR
        rsi = results[0][17]  # RSI
        macd = results[0][18]  # macd
        macd_signal = results[0][19]  # macd_signal
        macdHist = results[0][20]  # macd_hist
        insertDate = results[0][21]  # insertDate
        orderDate = results[0][22]  # newdateTime
        orderDateUTC = results[0][23]  # newsnapshotTimeUTC

        # Get prior periods (index of > 0)
        ema26Prior = results[1][9]
        stoch_d_prior = results[1][15]
        williamsRPrior = results[1][16]
        closePricePrior = results[1][4]
        rsiPrior = results[1][17]
        stochDPrior3 = results[2][15]
        sma15Prior = results[1][11]

        # Calculate some parameters
        smaEMADiff = sma15 - ema26
        smaEMADiffPrior = sma15Prior - ema26Prior
        williamsRDiff = williamsR - williamsRPrior
        emaCurrentDiff = abs(closePrice - ema26)
        emaPriorDiff = abs(closePricePrior - ema26Prior)

        # Prepare order Object
        order = {
            "id": 1,  # Default to 1, doesn't do anythin g because that column in DB is an auto - incr
            "orderDate": orderDate,
            "orderDateUTC": orderDateUTC,
            "pair": pair,
            "priceTarget": closePrice
        }

        # Set Long rules
        if (stoch_d < 80 and closePrice > ema26 and stoch_d > stoch_d_prior and williamsR > williamsRPrior and smaEMADiff > smaEMADiffPrior):
            order['direction'] = 'Long'
            order['actionType'] = 'Open'
            insertOrder.insertOrder(con, order)
        elif (stoch_d > 100 and stoch_d_prior > 90):
            order['direction'] = 'Long'
            order['actionType'] = 'Close'
            insertOrder.insertOrder(con, order)

        # Set Short rules
        if (stoch_d < stoch_d_prior and stoch_d > 85 and stoch_k > 80 and rsi > 60 and williamsRDiff < 30):
            order['direction'] = 'Short'
            order['actionType'] = 'Open'
            insertOrder.insertOrder(con, order)
        elif (stoch_d < 20 and stoch_d_prior < 20) or (stoch_d < 20 and williamsR < -105):
            order['direction'] = 'Short'
            order['actionType'] = 'Close'
            insertOrder.insertOrder(con, order)


def is_active(con, pair):
    # Prepare Query
    mycursor = con.cursor()
    sql = "select count(*) from main.pair_status where pair='" + \
        pair + "' and status='ACTIVE'"
    # Execute query
    mycursor.execute(sql)
    results = mycursor.fetchone()
    return(results[0])
    mycursor.close()
