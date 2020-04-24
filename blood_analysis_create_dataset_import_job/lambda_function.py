import boto3
import os
from datetime import datetime


def lambda_handler(event, context):

    role_arn = os.getenv("ROLE_ARN", "")  # Role necessária para o Forecast acessar o S3
    dataset_arn = os.getenv("DATASET_ARN", "")  # Constante Dataset já criado
    now = (datetime.now()).strftime("%Y_%m_%d")
    dataset_import_name = (
        f"IMPORT_JOB_{now}"
    )  # Como vai rodar de madrugada vai ser a data de processamento
    TIMESTAMP_FORMAT = "yyyy-MM-dd hh:mm:ss"

    # O Path será coletado via evento
    s3_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    s3_object = event["Records"][0]["s3"]["object"]["key"]

    s3_path = f"s3://{s3_bucket}/{s3_object}"
    print(s3_path)

    forecast = boto3.client(service_name="forecast")

    print(now, dataset_import_name)

    try:
        ds_import_job_response = forecast.create_dataset_import_job(
            DatasetImportJobName=dataset_import_name,
            DatasetArn=dataset_arn,
            DataSource={"S3Config": {"Path": s3_path, "RoleArn": role_arn}},
            TimestampFormat=TIMESTAMP_FORMAT,
        )

        ds_import_job_arn = ds_import_job_response["DatasetImportJobArn"]

        # Sending request to SQS destination using Lambda destinations
        return {"statusCode": 200, "body": ds_import_job_arn}

    except Exception as e:
        # TODO: Notificar que o JOB não funcionou
        print(e)
        raise Exception("Error Creating dataset import JOB")
