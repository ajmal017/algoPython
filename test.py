import dbConnect
import EMA

# Create mySql connection
con = dbConnect.dbConnect()

# Test EMA function
ema26 = EMA.EMA(26, 0.7, 'AUD/USD', con)

# Works!!!
print(ema26)
