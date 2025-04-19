import boto3
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = 'capybara-inventory-store'
    key = 'orders.json'

    try:
        order_id = event['pathParameters']['id']
        update_data = json.loads(event['body'])

        response = s3.get_object(Bucket=bucket, Key=key)
        orders = json.loads(response['Body'].read())

        updated = False
        for order in orders:
            if order['order_id'] == order_id:
                for key in update_data:
                    order[key] = update_data[key]
                updated = True
                break

        if not updated:
            return {
                "statusCode": 404,
                "body": json.dumps({ "error": "Order not found" }),
                "isBase64Encoded": False
            }

        s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(orders))

        return {
            "statusCode": 200,
            "body": json.dumps({ "message": "Order updated" }),
            "isBase64Encoded": False
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({ "error": str(e) }),
            "isBase64Encoded": False
        }
