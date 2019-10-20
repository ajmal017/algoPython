import functions.dbConnect as dbConnect
import functions.EMA as EMA
import functions.RSI as RSI
import functions.SMA as SMA
import functions.STOCHASTIC as STOCHASTIC
import functions.WILLIAMSR as WILLIAMSR
import aws.sqs as sqs
import json


def runAlgo():
    # Get SQS messages off queue
    client = sqs.createClient()
    queueURL = 'https://sqs.us-east-2.amazonaws.com/123188106252/preAlgo'
    results = sqs.getSQSMessages(client, queueURL)

    # If we have messages start going through them
    if results:
        # Create mySql connection
        con = dbConnect.dbConnect('staging')
        mycursor = con.cursor()
        sql_insert = "INSERT INTO algo_forex (dateTime,pair,snapshotTimeUTC,openPrice,closePrice,highPrice,lowPrice,lastTradedVolume,EMA_12,EMA_26,EMA_50,SMA_15,SMA_25,SMA_60,stoch_k,stoch_d,williamsR,RSI,macd,macd_signal,macd_hist,insertDate)"
        returnArray = []
        messageID = ""
        body = {}
        pair = ""
        tickData = {}
        # Loop through messages
        for x in results:
            # Pull apart message from SQS
            messageID = x['MessageId']
            ReceiptHandle = x['ReceiptHandle']
            json_acceptable_string = x['Body'].replace("'", "\"")
            body = json.loads(json_acceptable_string)
            pair = body['pair']
            tickData = body['tickData']
            dateTime = tickData['dateTime']
            snapshotTimeUTC = tickData['snapshotTimeUTC']
            openPrice = tickData['openPrice']
            currentPrice = tickData['closePrice']
            highPrice = tickData['highPrice']
            lowPrice = tickData['lowPrice']
            lastTradedVolume = tickData['lastTradedVolume']

            # Compute all technical indicators
            EMA_12 = EMA.EMA(12, currentPrice, pair, con)
            EMA_26 = EMA.EMA(26, currentPrice, pair, con)
            EMA_50 = EMA.EMA(50, currentPrice, pair, con)
            SMA_15 = SMA.SMA(15, currentPrice, pair, con)
            SMA_25 = SMA.SMA(25, currentPrice, pair, con)
            SMA_60 = SMA.SMA(60, currentPrice, pair, con)
            stoch = STOCHASTIC.STOCHASTIC(14, currentPrice, pair, con)
            STOCH_K = stoch['STOCH_K']
            STOCH_D = stoch['STOCH_D']
            WILLIAMS_R = WILLIAMSR.WILLIAMSR(14, currentPrice, pair, con)
            rsi = RSI.RSI(14, currentPrice, pair, con)
            MACD = EMA_12 - EMA_26
            MACD_SIGNAL = EMA.EMA_MACD(9, MACD, pair, con)
            MACD_HIST = MACD - MACD_SIGNAL

            # Insert indicator data into DB
            sql = sql_insert + " VALUES ('" + dateTime + "','" + pair + "','" + snapshotTimeUTC + "'," + str(openPrice) + "," + str(currentPrice) + "," + str(highPrice) + "," + str(lowPrice) + "," + str(lastTradedVolume) + "," + str(EMA_12) + \
                "," + str(EMA_26) + "," + str(EMA_50) + "," + str(SMA_15) + "," + str(SMA_25) + "," + str(SMA_60) + "," + str(STOCH_K) + "," + \
                str(STOCH_D) + "," + str(WILLIAMS_R) + "," + str(rsi) + "," + str(MACD) + \
                "," + str(MACD_SIGNAL) + "," + str(MACD_HIST) + ",NOW()); "

            # Execute SQL insert, if fails means it violated a primary key
            try:
                mycursor.execute(sql)
                con.commit()
                print('Inserted new Algo Data')
                # Delete SQS message off Queue
                response = client.delete_message(
                    QueueUrl=queueURL,
                    ReceiptHandle=ReceiptHandle
                )
            except:
                print('Algo data already exists, shutting down app')
                # Delete SQS message off Queue
                response = client.delete_message(
                    QueueUrl=queueURL,
                    ReceiptHandle=ReceiptHandle
                )
                return('Algo data already exists, shutting down app')
    # If there are no messages simply exit out of function
    print('No Messages in queue to process')
    return('No Messages in queue to process')
