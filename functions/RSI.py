#
#                   100
#     RSI = 100 - --------
#                  1 + RS
#
#     RS = Average Gain / Average Loss
# ​
# Sum of Gains over the past 14 periods / 14
# Sum of Losses over the past 14 periods / 14
#
# Get sum of gains and losses from past 13 trades
# then add in latest price (if gain or loss)
#
# Then divide both numbers by 14
#


# This function returns the Expontential moving average of last price
def RSI(period, latestClose, pair, con):
    # Prepare mysql connection
    mycursor = con.cursor()
    # Prepare parameters
    periodQuery = period - 1

    # Get last EMA price from database
    sql = """ select sum(case when Gain >= 0 then Gain else 0 end) as Gains
                    ,sum(case when Gain < 0 then abs(Gain) else 0 end) as Losses
                from (
                    SELECT l.pair,l.dateTime,l.closePrice
                            ,round(l.closePrice - (SELECT closePrice FROM algo_forex x WHERE x.dateTime < l.dateTime AND x.pair = l.pair ORDER BY dateTime DESC LIMIT 1),7) Gain
                            FROM algo_forex l    where pair = '""" + pair + """'
          order by dateTime desc limit """ + str(periodQuery) + ")a "

    # Get gains and losses for past period-1 values
    mycursor.execute(sql)
    results = mycursor.fetchall()
    gains = results[0][0]  # 1st column returns is Gains
    losses = results[0][1]  # 2nd column returns is Lossses
    mycursor.close()
    # Need to get pervios close prices to determine if current price is a gain or a loss
    sql = "select closePrice from algo_forex where pair='" + pair + """'
      order by dateTime desc limit 1;"""

    # Get Latest close
    mycursor.execute(sql)
    results = mycursor.fetchone()
    lastClosePrice = results[0]
    mycursor.close()

    # Calculate RSI
    if latestClose > lastClosePrice:
        gains = gains + latestClose - lastClosePrice
    else:
        losses = losses + abs(latestClose - lastClosePrice)

    averageGain = gains / period
    averageLoss = losses / period
    RS = averageGain / averageLoss
    RSI = RSI = 100 - 100 / (1 + RS)

    # Return results
    return(RSI)
