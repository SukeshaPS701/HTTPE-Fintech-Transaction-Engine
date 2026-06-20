from simulator.sim_engine import TransactionSimulator


def main():

    sim = TransactionSimulator(users=200)

    sim.create_wallets()

    sim.seed_balance()

    sim.run_simulation(
        total_requests=3000,
        workers=100
    )

    sim.print_leaderboard()


if __name__ == "__main__":
    main()