import runAlgo
import generateOrders


def my_handler(event, context):
    runAlgo.runAlgo()
    generateOrders.generateOrders()
    return {'message': 'Lamnda finised Running'}
