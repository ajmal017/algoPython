def EMA(period, currentPrice, pair, con):
    # First create weighted multipler
    WeightedMultiplier = 2 / (period + 1)

    # Get last EMA price from database


# function EMA(period, currentPrice, pair, con) {
#   return new Promise((resolve, reject) => {
#     //First get Weighted multiplier
#     let WeightedMultiplier = 2 / (period + 1);

#     //Get last EMA price from DB
#     var sqlLastData =
#       "Select EMA_" +
#       period +
#       " as EMAResult from algo_forex where pair='" +
#       pair +
#       "' order by dateTime desc limit 1;";

#     //console.log("sqlLastData", sqlLastData);
#     //First retrieve last 26 data points from table
#     con.query(sqlLastData, function(err, sqlData) {
#       if (err) {
#         console.log("SQL ERROR RETRIEVING LAST PRICES", err);
#         reject(err);
#       }
#       if (sqlData) {
#         //Calc EMA first
#         let lastEMA = JSON.parse(JSON.stringify(sqlData[0])).EMAResult;
#         //Calculate EMA
#         let EMA =
#           currentPrice * WeightedMultiplier +
#           lastEMA * (1 - WeightedMultiplier);

#         let preFix = "EMA_" + period;
#         let EMAReturn = { [preFix]: EMA };

#         resolve(EMAReturn);
#       }
#     });
#   });
# }

# function EMA_MACD(period, currentPrice, pair, con) {
#   return new Promise((resolve, reject) => {
#     //First get Weighted multiplier
#     let WeightedMultiplier = 2 / (period + 1);

#     //Get last EMA price from DB
#     var sqlLastData =
#       "Select macd from algo_forex where pair='" +
#       pair +
#       "' order by dateTime desc limit 1;";

#     //First retrieve last 26 data points from table
#     con.query(sqlLastData, function(err, sqlData) {
#       if (err) {
#         console.log("SQL ERROR RETRIEVING LAST PRICES", err);
#         reject(err);
#       }
#       if (sqlData) {
#         //Calc EMA first
#         let lastMACD = JSON.parse(JSON.stringify(sqlData[0])).macd;
#         //Calculate EMA
#         //((last_price-@previous_ema)*@ema_multiplier_12) + @previous_ema;
#         //let EMA = (currentPrice - lastMACD) * WeightedMultiplier + lastMACD;
#         let EMA =
#           currentPrice * WeightedMultiplier +
#           lastMACD * (1 - WeightedMultiplier);

#         let preFix = "MACD_SIGNAL";
#         let EMAReturn = { [preFix]: EMA };

#         resolve(EMAReturn);
#       }
#     });
#   });
# }

# module.exports.EMA = EMA;
# module.exports.EMA_MACD = EMA_MACD;
