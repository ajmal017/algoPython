# %k = ( (C-L14)/(H14-L14) ) X 100
# ​
# C = The most recent closing price
# L14 = The lowest price traded of the 14 previous
# trading sessions
# H14 = The highest price traded during the same
# 14-day period
# %K = The current value of the stochastic indicator


def STOCHASTIC(period, latestClose, pair, con):
    # Prepare mysql connection
    mycursor = con.cursor()
    # Prepare query
    sqlSMA15 = "select min(lowPrice) as L_PERIOD, max(highPrice) as H_PERIOD from (select lowPrice, highPrice from algo_forex where pair='" + pair + """'
    order by dateTime desc limit """ + str(period) + " )a"
    # Run query
    mycursor.execute(sqlSMA15)
    results = mycursor.fetchall()
    H_PERIOD = results[0][0]
    L_PERIOD = results[0][1]

    # Calculate stochastic K first
    stoch_k = ((latestClose - L_PERIOD) / (H_PERIOD - L_PERIOD)) * 100

    # Now compute stochastic D which is 3 day average of stochastic K
    sqlStoch = "select sum(stoch_k) as stochKSum from (select stoch_k from algo_forex where pair='" + pair + """'
                order by dateTime desc limit 2)a"""

    # Execute query
    mycursor.execute(sqlSMA15)
    results = mycursor.fetchone()
    stochkSum = results[0]

    # Calculate stoch d
    stoch_d = stochkSum + stoch_k
    stoch_d = stoch_d / 3

    # Create return values
    return ({"STOCH_K": stoch_k, "STOCH_D": stoch_d})
