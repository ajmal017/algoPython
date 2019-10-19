
def SMA(period, latestClose, pair, con):
    # Prepare mysql connection
    mycursor = con.cursor()

    # Prepare query
    periodForQuery = period - 1
    sqlSMA15 = "select sum(closePrice) as sumClose from (select closePrice from algo_forex where pair='" + pair + """'
    order by dateTime desc limit """ + str(periodForQuery) + " )a "

    # Run query
    mycursor.execute(sqlSMA15)
    results = mycursor.fetchone()
    sumClose = results[0]

    # Calculate SMA
    SMARolling = (sumClose + latestClose) / period

    # Return results
    preFix = "SMA_" + str(period)
    SMA_return = {preFix: SMARolling}
    return(SMA_return)
