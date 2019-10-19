import functions.dbConnect as dbConnect
import functions.EMA as EMA
import functions.RSI as RSI
import functions.SMA as SMA
import functions.STOCHASTIC as STOCHASTIC
import functions.WILLIAMSR as WILLIAMSR
import aws.sqs as sqs


def runAlgo():
    # Create mySql connection
    con = dbConnect.dbConnect('staging')
    mycursor = con.cursor()

    # Get SQS messages off queue
    results = sqs.getSQSMessages(
        'https://sqs.us-east-2.amazonaws.com/123188106252/preAlgo')

    # If we have messages start going through them
    if results:
        sql_insert = "INSERT INTO algo_forex (dateTime,pair,snapshotTimeUTC,openPrice,closePrice,highPrice,lowPrice,lastTradedVolume,EMA_12,EMA_26,EMA_50,SMA_15,SMA_25,SMA_60,stoch_k,stoch_d,williamsR,RSI,macd,macd_signal,macd_hist,insertDate)"
        returnArray = []
        print(results)
        exitLength = len(results)
        print(exitLength)
        messageID = ""
        body = {}
        pair = ""
        tickData = {}
        # Loop through messages
        for x in results:
            # Pull apart message from SQS
            messageID = x['MessageId']
            ReceiptHandle = x['ReceiptHandle']
            body = x['Body']
            print(body)
            pair = body.pair
            tickData = body.data
            dateTime = tickData.dateTime
            snapshotTimeUTC = tickData.snapshotTimeUTC
            openPrice = tickData.openPrice
            currentPrice = tickData.closePrice
            highPrice = tickData.highPrice
            lowPrice = tickData.lowPrice
            lastTradedVolume = tickData.lastTradedVolume

            # Compute all technical indicators
            EMA_12 = EMA.EMA(12, currentPrice, pair, con)
            EMA_26 = EMA.EMA(26, currentPrice, pair, con)
            EMA_50 = EMA.EMA(50, currentPrice, pair, con)
            SMA_15 = SMA.SMA(15, currentPrice, pair, con)
            SMA_25 = SMA.SMA(25, currentPrice, pair, con)
            SMA_60 = SMA.SMA(60, currentPrice, pair, con)
            stochastic_base = STOCHASTIC.STOCHASTIC(
                14, currentPrice, pair, con)
            STOCH_K = stochastic_base['STOCH_K']
            STOCH_D = stochastic_base['STOCH_D']
            WILLIAMS_R = WILLIAMSR.WILLIAMSR(14, currentPrice, pair, con)
            RSI = RSI.RSI(14, currentPrice, pair, con)
            MACD = EMA_12 - EMA_26
            MACD_SIGNAL = EMA.EMA_MACD(9, MACD, pair, con)
            MACD_HIST = MACD - MACD_SIGNAL

    # If there are no messages simply exit out of function
    return('No Messages in queue to process')


#                                             // Insert algo results in algoDB
#                                             let sql=sql_insert +
#                                             " VALUES ('" +
#                                             dateTime +
#                                             "','" +
#                                             pair +
#                                             "','" +
#                                             snapshotTimeUTC +
#                                             "'," +
#                                             openPrice +
#                                             "," +
#                                             currentPrice +
#                                             "," +
#                                             highPrice +
#                                             "," +
#                                             lowPrice +
#                                             "," +
#                                             lastTradedVolume +
#                                             "," +
#                                             EMA_12 +
#                                             "," +
#                                             EMA_26 +
#                                             "," +
#                                             EMA_50 +
#                                             "," +
#                                             SMA_15 +
#                                             "," +
#                                             SMA_25 +
#                                             "," +
#                                             SMA_60 +
#                                             "," +
#                                             STOCH_K +
#                                             "," +
#                                             STOCH_D +
#                                             "," +
#                                             WILLIAMS_R +
#                                             "," +
#                                             RSI +
#                                             "," +
#                                             MACD +
#                                             "," +
#                                             MACD_SIGNAL +
#                                             "," +
#                                             MACD_HIST +
#                                             ",NOW()); "
#                                             new Promise((resolve, reject)= > {
#                                                 con.query(sql.toString(), function(err, sqlData) {
#                                                     if (err) {
#                                                         // console.log("ALGO INSERT - ", i, " UNSUCCESSFUL")
#                                                         reject(err)
#                                                     }
#                                                     if (sqlData) {
#                                                         let msg="ALGO INSERT - " + i + " SUCCESSFUL"
#                                                         console.log(
#                                                             "msg", msg)
#                                                         resolve(i)
#                                                     }
#                                                 })
#                                             }).then(()= > {
#                                                     // Only delete message if it successfully inserts into DB
#                                                     var params={
#                                                         Entries: [
#                                                             {
#                                                                 Id: messageID,
#                                                                 ReceiptHandle: ReceiptHandle
#                                                             }
#                                                         ],
#                                                         QueueUrl:
#                                                         "https://sqs.us-east-2.amazonaws.com/123188106252/preAlgo"
#                                                     }
#                                                     sqs.deleteMessageBatch(params, function(err, data) {
#                                                         if (err)
#                                                         console.log(
#                                                             "SQS Message delete failed",
#                                                             err,
#                                                             err.stack
#                                                         )
#                                                         // an error occurred
#                                                         else
#                                                         console.log(
#                                                             "SQS Messaged delete successful",
#                                                             data
#                                                         )
#                                                         // successful response
#                                                     })
#                                                     resolve()
#                                                     })
#                                         })
#                                     })
#                                 })
#                             ),
#                             Promise.resolve()
#                         )
#                     }
#                 }
#             })
#         })
#     })
# }
runAlgo()
