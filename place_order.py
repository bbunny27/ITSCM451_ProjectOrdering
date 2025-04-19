import boto3
import json
import uuid
from datetime import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = 'capybara-inventory-store'
    key = 'orders.json'

    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub', 'unknown')

    try:
        body = json.loads(event['body'])

        new_order = {
            "order_id": str(uuid.uuid4()),
            "user_id": user_id,
            "item_id": body['item_id'],
            "quantity": body['quantity'],
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            orders = json.loads(response['Body'].read())
        except s3.exceptions.NoSuchKey:
            orders = []

        orders.append(new_order)

        s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(orders))

        return {
            "statusCode": 201,
            "body": json.dumps(new_order),
            "headers": { "Content-Type": "application/json" },
            "isBase64Encoded": False
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({ "error": str(e) }),
            "isBase64Encoded": False
        }
