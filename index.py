import runAlgo


def handler(event, context):
    runAlgo.runAlgo()
    # generateOrders.generateOrders()
    return {'message': 'Lamnda finised Running'}
