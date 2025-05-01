import json
import pymysql
import uuid
from datetime import datetime

def lambda_handler(event, context):
    print("Lambda started")
    print(json.dumps(event))

    # Parse HTTP method
    method = event['requestContext']['http']['method']
    print("HTTP Method:", method)

    # Only allow POST
    if method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method not allowed"}),
            "headers": {
                "Access-Control-Allow-Origin": "https://www.capybaraparadise.xyz",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type,Authorization"
            }
        }

    try:
        claims = event['requestContext']['authorizer']['jwt']['claims']
        user_id = claims.get('sub')
        print("User ID:", user_id)
    except Exception as e:
        print("Error extracting user_id:", str(e))
        return {
            "statusCode": 403,
            "body": json.dumps({"error": "Unauthorized"}),
            "headers": {
                "Access-Control-Allow-Origin": "https://www.capybaraparadise.xyz",
                "Access-Control-Allow-Headers": "Content-Type,Authorization"
            }
        }

    try:
        body = json.loads(event['body'])
        item_id = body.get('item_id')
        quantity = int(body.get('quantity', 1))
        order_id = str(uuid.uuid4())

        print("Inserting order:", item_id, quantity)

        connection = pymysql.connect(
            host='YOUR_EC2_PUBLIC_IP',
            user='admin',
            password='I<3Capybara',
            database='capybara_shop',
            connect_timeout=5
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO orders (order_id, user_id, item_id, quantity, timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """, (order_id, user_id, item_id, quantity, datetime.utcnow().isoformat()))
            connection.commit()

        print("Order successfully placed.")
        return {
            "statusCode": 201,
            "body": json.dumps({
                "order_id": order_id,
                "user_id": user_id,
                "item_id": item_id,
                "quantity": quantity
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "https://www.capybaraparadise.xyz",
                "Access-Control-Allow-Headers": "Content-Type,Authorization"
            }
        }

    except Exception as e:
        print("DB or JSON Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Access-Control-Allow-Origin": "https://www.capybaraparadise.xyz",
                "Access-Control-Allow-Headers": "Content-Type,Authorization"
            }
        }
