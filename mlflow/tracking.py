import mlflow
import mlflow.pytorch

def log_model(model, metrics: dict):
    mlflow.set_experiment("SentinelAI")
    with mlflow.start_run():
        mlflow.pytorch.log_model(model, "model")
        for key, value in metrics.items():
            mlflow.log_metric(key, value)
