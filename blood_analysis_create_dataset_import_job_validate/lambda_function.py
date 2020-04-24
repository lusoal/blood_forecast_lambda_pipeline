import json
import boto3
import time
import os


def lambda_handler(event, context):
    forecast = boto3.client(service_name="forecast")

    request_body = dict(json.loads(event["Records"][0]["body"]))
    dataset_import_job_arn = request_body["responsePayload"]["body"]

    response = forecast.describe_dataset_import_job(
        DatasetImportJobArn=dataset_import_job_arn
    )

    count = 0
    dataset_import_status = None

    while count <= 5:
        dataset_import_status = response.get("Status")
        print(dataset_import_status)
        if (dataset_import_status) == "ACTIVE":
            break
        count += 1
        time.sleep(2)

    if str(dataset_import_status) == "ACTIVE":
        print(
            f"Vou remover o item da fila e triggar a outra lambda {dataset_import_job_arn}"
        )
        lambda_invoke_name = os.getenv("LAMBDA_INVOKE_NAME", "")
        client = boto3.client("lambda")
        response = {"statusCode": 200, "body": dataset_import_job_arn}

        invoke_response = client.invoke_async(
            FunctionName=lambda_invoke_name, InvokeArgs=json.dumps(response)
        )

        return invoke_response

    elif (
        str(dataset_import_status) == "CREATE_IN_PROGRESS"
        or str(dataset_import_status) == "CREATE_PENDING"
    ):
        print(f"[INFO] Vou manter o item na fila {dataset_import_job_arn}")
        raise Exception("[Warning] Item not ready yet")

    elif (
        str(dataset_import_status) == "CREATE_FAILED"
        or str(dataset_import_status) == "DELETE_FAILED"
    ):
        print(f"Vou remover o item da fila e notificar o erro {dataset_import_job_arn}")
