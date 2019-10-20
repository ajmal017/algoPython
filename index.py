import runAlgo
import generateOrders


def handler(event, context):
    runAlgo.runAlgo()
    generateOrders.generateOrders()
    return {'message': 'Lamnda finised Running'}
