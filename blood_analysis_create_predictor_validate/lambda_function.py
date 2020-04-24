import json
import time
import boto3
import os


def lambda_handler(event, context):
    forecast = boto3.client(service_name="forecast")

    # predictor_arn enviado a partir de uma fila do SQS
    request_body = dict(json.loads(event["Records"][0]["body"]))
    predictor_arn = request_body["responsePayload"]["body"]

    count = 0
    predictor_status = None

    while count <= 5:
        response = forecast.describe_predictor(PredictorArn=predictor_arn)
        predictor_status = response.get("Status")
        print(predictor_status)
        if (predictor_status) == "ACTIVE":
            break
        count += 1
        time.sleep(2)

    if str(predictor_status) == "ACTIVE":
        print(
            f"Vou remover o item da fila e triggar a outra lambda passando o {predictor_arn}"
        )
        lambda_invoke_name = os.getenv("LAMBDA_INVOKE_NAME", "")
        client = boto3.client("lambda")
        response = {"statusCode": 200, "body": predictor_arn}

        invoke_response = client.invoke_async(
            FunctionName=lambda_invoke_name, InvokeArgs=json.dumps(response)
        )

        return invoke_response

    elif (
        str(predictor_status) == "CREATE_FAILED"
        or str(predictor_status) == "DELETE_FAILED"
        or str(predictor_status) == "UPDATE_FAILED"
    ):
        # TODO: Notificar caso aconteça algum erro na validaçao
        print(f"Vou remover o item da fila e notificar o erro {predictor_arn}")
        return {"statusCode": 200, "body": "Notificar Erro"}

    else:
        raise Exception(
            "[Warning] Nao vou remover o item da file e tentar o reprocessamento"
        )
        print(f"Vou manter o item na fila {predictor_arn}")
