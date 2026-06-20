import random
import time
import requests
from collections import defaultdict


GATEWAY_URL = "http://localhost:8000"


class TransactionSimulator:

    def __init__(self, users=100):

        self.users = users
        self.sent_volume = defaultdict(float)
        self.received_volume = defaultdict(float)

        self.success = 0
        self.failed = 0

    def safe_post(self, url, payload):

        try:
            return requests.post(
                url,
                json=payload,
                timeout=3
            )
        except Exception:
            return None

    def create_wallets(self):

        print("Creating wallets...")

        for user_id in range(1, self.users + 1):

            self.safe_post(
                f"{GATEWAY_URL}/wallet/create",
                {"user_id": user_id}
            )

        print("Wallets created")

    def seed_balance(self):

        print("Seeding balances...")

        for user_id in range(1, self.users + 1):

            self.safe_post(
                f"{GATEWAY_URL}/wallet/deposit",
                {
                    "user_id": user_id,
                    "amount": 1000
                }
            )

        print("Balance seeded")

    def run_simulation(self, iterations=500):

        print("Running simulation...")

        start = time.time()

        for _ in range(iterations):

            sender = random.randint(1, self.users)
            receiver = random.randint(1, self.users)

            if sender == receiver:
                continue

            amount = random.randint(1, 50)

            res = self.safe_post(
                f"{GATEWAY_URL}/transfer",
                {
                    "sender_id": sender,
                    "receiver_id": receiver,
                    "amount": amount
                }
            )

            if res and res.status_code == 200:

                self.success += 1
                self.sent_volume[sender] += amount
                self.received_volume[receiver] += amount

            else:
                self.failed += 1

            time.sleep(0.005)

        end = time.time()

        duration = end - start
        tps = self.success / duration

        print("\nSIMULATION COMPLETE")
        print(f"Success: {self.success}")
        print(f"Failed: {self.failed}")
        print(f"Duration: {duration:.2f}s")
        print(f"Estimated TPS: {tps:.2f}")

    def print_leaderboard(self):

        print("\nTOP SENDERS:")

        for user, amount in sorted(
            self.sent_volume.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]:

            print(f"User {user}: {amount}")

        print("\nTOP RECEIVERS:")

        for user, amount in sorted(
            self.received_volume.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]:

            print(f"User {user}: {amount}")