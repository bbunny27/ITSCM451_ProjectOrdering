import pymysql
import json

def lambda_handler(event, context):
    print("Lambda started")
    print(json.dumps(event))

    try:
        user_id = event['requestContext']['authorizer']['jwt']['claims']['sub']
        print("User ID:", user_id)
    except Exception as e:
        print("Auth Error:", str(e))
        return {
            "statusCode": 403,
            "body": json.dumps({"error": "Unauthorized"}),
            "headers": {"Access-Control-Allow-Origin": "*"}
        }

    try:
        connection = pymysql.connect(
            host='3.147.73.212',
            user='shopadmin',
            password='I<3Capybara',
            database='capybara_shop',
            connect_timeout=5
        )

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
            orders = cursor.fetchall()

        # Serialize datetime objects
        for order in orders:
            if 'timestamp' in order and isinstance(order['timestamp'], (str, bytes)) is False:
                order['timestamp'] = order['timestamp'].isoformat()

        return {
            "statusCode": 200,
            "body": json.dumps(orders),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

    except Exception as e:
        print("DB Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }
