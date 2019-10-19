# This function returns the Expontential moving average of last price
def EMA(period, currentPrice, pair, con):
    # Prepare mysql connection
    mycursor = con.cursor()
    # First create weighted multipler
    WeightedMultiplier = 2 / (period + 1)

    # Get last EMA price from database
    sqlLastData = """Select EMA_""" + str(period) + """
      as EMAResult from algo_forex where pair='""" + pair + """'
      order by dateTime desc limit 1;"""

    # Return result as tuple, need to get first value as query returns 1 only
    mycursor.execute(sqlLastData)
    results = mycursor.fetchone()
    lastEMA = results[0]

    # Calculate EMA
    EMA = currentPrice * WeightedMultiplier + \
        lastEMA * (1 - WeightedMultiplier)

    # Return results
    preFix = "EMA_" + str(period)
    EMAReturn = {preFix: EMA}
    return(EMAReturn)


# This functions return the exponential moving average of the MACD
def EMA_MACD(period, currentPrice, pair, con):
    # Prepare mysql connection
    mycursor = con.cursor()

    # First create weighted multipler
    WeightedMultiplier = 2 / (period + 1)

    # Get last macd price from database
    sqlLastData = """Select macd""" + str(period) + """
      as EMAResult from algo_forex where pair='""" + pair + """'
      order by dateTime desc limit 1;"""

    # Return result as tuple, need to get first value as query returns 1 only
    mycursor.execute(sqlLastData)
    results = mycursor.fetchone()
    lastEMA = results[0]

    # Calculate EMA
    EMA = currentPrice * WeightedMultiplier + \
        lastEMA * (1 - WeightedMultiplier)

    # Return results
    preFix = "MACD_SIGNAL"
    EMAReturn = {preFix: EMA}
    return(EMAReturn)
