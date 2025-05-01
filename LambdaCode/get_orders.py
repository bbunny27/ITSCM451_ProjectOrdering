import boto3
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = 'capybara-inventory-store'
    key = 'orders.json'

    # Get the Cognito user ID from the request context
    try:
        claims = event['requestContext']['authorizer']['jwt']['claims']
        user_id = claims.get('sub', 'unknown')
    except Exception as e:
        return {
            "statusCode": 403,
            "body": json.dumps({"error": "Unauthorized"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "isBase64Encoded": False
        }

    try:
        # Load all orders from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        orders = json.loads(response['Body'].read())

        # Filter orders for this user
        user_orders = [o for o in orders if o.get('user_id') == user_id]

        return {
            "statusCode": 200,
            "body": json.dumps(user_orders),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "isBase64Encoded": False
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "isBase64Encoded": False
        }
