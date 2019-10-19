import functions.dbConnect as dbConnect
import functions.EMA as EMA
import functions.RSI as RSI
import functions.SMA as SMA
import functions.STOCHASTIC as STOCHASTIC
import functions.WILLIAMSR as WILLIAMSR

# Create mySql connection
con = dbConnect.dbConnect('Staging')

# Test EMA function
# ema26 = EMA.EMA(26, 0.68567, 'AUD/USD', con)
# rsi = RSI.RSI(14, 0.68567, 'AUD/USD', con)
# sma = SMA.SMA(14, 0.68567, 'AUD/USD', con)
# stoch = STOCHASTIC.STOCHASTIC(14, 0.68567, 'AUD/USD', con)
williamsr = WILLIAMSR.WILLIAMSR(14, 0.68567, 'AUD/USD', con)

# Test output
# print(ema26)
# print(rsi)
# print(sma)
# print(stoch)
print(williamsr)
