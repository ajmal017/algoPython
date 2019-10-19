# Wiliams %R= Highest High− Close / Highest High − Lowest Low
# ​
# where
# Highest High=Highest price in the lookback period, typically 14 days.
# Close=Most recent closing price.
# Lowest Low=Lowest price in the lookback period, typically 14 days.


def WILLIAMSR(period, latestClose, pair, con):
    # Prepare mysql connection
    mycursor = con.cursor()
    # Prepare query
    sqlSMA15 = "select min(lowPrice) as L_PERIOD, max(highPrice) as H_PERIOD from (select lowPrice, highPrice from algo_forex where pair='" + pair + """'
    order by dateTime desc limit """ + str(period) + " ) a"
    # Execute query
    mycursor.execute(sqlSMA15)
    results = mycursor.fetchall()
    mycursor.close()
    L_PERIOD = results[0][0]
    H_PERIOD = results[0][1]
    # Calculate WilliamsR
    wiliamsR = ((H_PERIOD - latestClose) / (H_PERIOD - L_PERIOD)) * 100 * -1
    return(wiliamsR)
