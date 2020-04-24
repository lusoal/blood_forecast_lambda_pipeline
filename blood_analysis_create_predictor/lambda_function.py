import os
import boto3
from datetime import datetime


def lambda_handler(event, context):
    forecast = boto3.client(service_name="forecast")

    # dataset_group_arn pode ser fixo, não é necessário o ARN do Job import
    dataset_group_arn = os.getenv("DSG_ARN", "")
    forecastHorizon = 24  # Horizon of forecast, projetar as proximas 24 Horas
    now = (datetime.now()).strftime("%Y_%m_%d")
    predictor_name = f"blood_analysis_pred_{now}"

    # EvaluationParameters - Is to split data into train and test
    # NumberOfBacktestWindows - The number of times to split the input data
    # BackTestWindowOffset - The point from the end of the dataset where you want
    # to split the data for model training and testing (evaluation).

    # Verificar o minimo de dados necessário para projetar as próximas 24H
    try:
        response = forecast.create_predictor(
            PredictorName=predictor_name,
            ForecastHorizon=forecastHorizon,
            PerformAutoML=True,
            InputDataConfig={"DatasetGroupArn": dataset_group_arn},
            FeaturizationConfig={
                "ForecastFrequency": "H",
                "Featurizations": [
                    {
                        "AttributeName": "target_value",
                        "FeaturizationPipeline": [
                            {
                                "FeaturizationMethodName": "filling",
                                "FeaturizationMethodParameters": {
                                    "aggregation": "sum",
                                    "backfill": "zero",
                                    "frontfill": "none",
                                    "middlefill": "zero",
                                },
                            }
                        ],
                    }
                ],
            },
        )

        # Este item será enviado para a fila para validacao
        predictor_arn = response.get("PredictorArn")
        return {"statusCode": 200, "body": predictor_arn}
    except Exception as e:
        print("[ERROR] Error while creating predictor")
        raise (e)
