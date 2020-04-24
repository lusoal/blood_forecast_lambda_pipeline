import boto3
from datetime import datetime


def get_dynamo_item(date_to_get):
    client = boto3.client("dynamodb")
    table_name = "blood_analysis_forecasting"

    forecast_arn = None
    try:
        response = client.query(
            TableName=table_name,
            KeyConditions={
                "timestamp": {
                    "AttributeValueList": [{"S": date_to_get}],
                    "ComparisonOperator": "EQ",
                }
            },
        )

        for item in response.get("Items"):
            forecast_arn = item.get("forecast_arn").get("S")
            break
        return forecast_arn
    except Exception as e:
        print(f"[ERROR] {e}")
        raise e


def lambda_handler(event, context):
    user_id = event.get("params").get("querystring").get("user_id")
    forecastquery = boto3.client(service_name="forecastquery")
    percentille = "p50"

    now = (datetime.now()).strftime("%Y_%m_%d")
    forecast_arn = get_dynamo_item(now)

    if not user_id:
        raise Exception("Not found user_id in querystring params")

    # Generate Forecast Graph
    try:
        forecastResponse = forecastquery.query_forecast(
            ForecastArn=forecast_arn, Filters={"item_id": user_id}
        )

        data = {"time": [], "glicose": []}

        for value in forecastResponse["Forecast"]["Predictions"][percentille]:
            data["time"].append(value["Timestamp"])
            data["glicose"].append(value["Value"])

        return data

    except Exception as e:
        raise e
