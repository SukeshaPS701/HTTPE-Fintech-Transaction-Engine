# Simple shard router based on user_id

SHARD_1 = "postgresql://fintech:fintech123@localhost:5432/httpe_shard1"
SHARD_2 = "postgresql://fintech:fintech123@localhost:5432/httpe_shard2"


def get_shard(user_id: int):

    # Basic hash-based sharding
    if user_id % 2 == 0:
        return SHARD_1
    else:
        return SHARD_2