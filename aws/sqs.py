import boto3


def getSQSMessages(queue_url):

    # Get the AWS service resource for SQS
    sqs = boto3.client('sqs', region_name='us-east-2', aws_access_key_id="AKIARZLUVKQGALPFJIM4",
                       aws_secret_access_key="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")

    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    # SQS will return a object of type messages if there is anything on the queue
    try:
        results = response['Messages']
    except:
        results = 0

    return results
