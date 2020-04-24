import json
import boto3
import time
from datetime import datetime


def persist_to_dynamo(forecast_arn):
    client = boto3.client("dynamodb")
    table_name = "blood_analysis_forecasting"
    now = (datetime.now()).strftime("%Y_%m_%d")

    dynamo_item = {"forecast_arn": {"S": forecast_arn}, "timestamp": {"S": now}}
    try:
        response = client.put_item(TableName=table_name, Item=dynamo_item)
        return response
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def lambda_handler(event, context):
    forecast = boto3.client(service_name="forecast")

    # forecast_arn sera enviado a partir do SQS
    request_body = dict(json.loads(event["Records"][0]["body"]))
    forecast_arn = request_body["responsePayload"]["body"]

    count = 0
    forecast_status = None

    while count <= 5:
        response = forecast.describe_forecast(ForecastArn=forecast_arn)
        forecast_status = response.get("Status")
        print(forecast_status)
        if (forecast_status) == "ACTIVE":
            break
        count += 1
        time.sleep(2)

    if str(forecast_status) == "ACTIVE":
        print(
            f"Vou remover o item da fila e triggar a outra lambda passando o {forecast_arn}"
        )
        response_dynamo = persist_to_dynamo(forecast_arn)

        if not response_dynamo:
            print("Notify SNS")

        return {"statusCode": 200, "body": forecast_arn}
    elif (
        str(forecast_status) == "CREATE_FAILED"
        or str(forecast_status) == "DELETE_FAILED"
    ):
        print(f"Vou remover o item da fila e notificar o erro {forecast_arn}")
        return {"statusCode": 200, "body": "Notificar Erro"}
    else:
        raise Exception(
            "[Warning] Nao vou remover o item da file e tentar o reprocessamento"
        )
        print(f"Vou manter o item na fila {forecast_arn}")
