import boto3
from datetime import datetime


def lambda_handler(event, context):
    forecast = boto3.client(service_name="forecast")
    now = (datetime.now()).strftime("%Y_%m_%d")
    forecast_name = f"blood_analysis_forecast_{now}"
    forecast_types = ["0.1", "0.5", "0.9", "mean"]

    # Get predictor ARN from event trigger
    predictor_arn = event["body"]
    print(f"[INFO] predictor_arn {predictor_arn}")

    try:
        response = forecast.create_forecast(
            ForecastName=forecast_name,
            PredictorArn=predictor_arn,
            ForecastTypes=forecast_types,
        )

        forecast_arn = response.get("ForecastArn")

        return {"statusCode": 200, "body": forecast_arn}
    except Exception as e:
        print("[Error] error while creating forecast")
        raise e
