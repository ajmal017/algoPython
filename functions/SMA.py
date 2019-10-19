
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
    mycursor.close()

    # Calculate SMA
    SMARolling = (sumClose + latestClose) / period

    # Return results
    return(SMARolling)
