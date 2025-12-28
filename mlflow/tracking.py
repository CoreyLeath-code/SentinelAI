import mlflow

mlflow.set_experiment("SentinelAI")

def log_run(prompt, response):
    with mlflow.start_run():
        mlflow.log_param("prompt", prompt)
        mlflow.log_text(response, "response.txt")
