# Lambdas Forecast Pipeline

Projeto dedicado para criar um pipeline utilizando Lambdas e outros serviços AWS para realizar o a criação de um Forecast utilizando o Amazon Forecast.

* [Criar Dataset Job Import](blood_analysis_create_dataset_import_job/lambda_function.py)
* [Validar Dataset Job Import](blood_analysis_create_dataset_import_job_validate/lambda_function.py)
* [Criar Forecast Predictor](blood_analysis_create_predictor/lambda_function.py)
* [Validar Forecast Predictor](blood_analysis_create_forecast_validate/lambda_function.py)
* [Criar Forecast](blood_analysis_create_forecast/lambda_function.py)
* [Validar Forecast](blood_analysis_create_forecast_validate/lambda_function.py)
* [Realizar a Get de um Forecast criado previamente](lamda_function.py)


## Como testar cada lambda localmente

### Requisitos

* python 3.6+
* [virtualenv](https://virtualenv.pypa.io/en/latest/)
* [python-lambda-local](https://pypi.org/project/python-lambda-local/)
* Credenciais da AWS previamente configuradas no sistema
* [Ter um Dataset Group já criado no Amazon Forecast](https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html)
* [Ter um Dataset já criado no Amazon Forecast](https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html)

### Instalação

* Instalar Virtualenv

```shell
pip install virtualenv
```

* Ativar o virtualenv dentro do projeto

```shell
virtualenv venv
```
Este comando criará uma pasta chamada virtualenv dentro da raiz do projeto.

* Instalar dependências para as lambdas "rodarem" localmente

```shell
pip install -r ./requirements.txt
```

* Instalar o python-lambda-local

```shell
pip install python-lambda-local
```

Esta é a biblioteca que iremos utilizar para testar cada lambda localmente.

### Testando as Lambdas

Dentro de cada pasta de cada lambda existem três arquivos:

```
├── README.md - Instruções sobre a Lambda e o que ela faz.
├── lambda_function.py - A lambda.
└── test.json - O evento de teste que você pode enviar para a lambda para testar.
```

* Como executar a lambda localmente

```shell
python-lambda-local -f lambda_handler -t 5 lambda_function.py event.json
```

* -f - O Lambda Handler
* -t - Tempo de timeout em segundos que a Lambda levará para executar.
