from locust import HttpUser
from locust import task
from locust import between


class PaymentUser(HttpUser):

    wait_time = between(1, 2)

    @task(1)
    def get_wallet(self):

        self.client.get(
            "/wallet/1"
        )

    @task(2)
    def transfer(self):

        self.client.post(
            "/transfer",
            json={
                "sender_id": 1,
                "receiver_id": 2,
                "amount": 1
            }
        )

    @task(1)
    def transactions(self):

        self.client.get(
            "/transactions/1"
        )