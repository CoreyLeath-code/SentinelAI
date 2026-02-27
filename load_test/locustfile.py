from locust import HttpUser, task, between
import random

class SentinelUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def predict(self):
        payload = {"features": [random.random() for _ in range(10)]}
        self.client.post("/predict", json=payload)
