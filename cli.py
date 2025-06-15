import argparse
from config.loader import load_config
from runner.launcher import launch_test

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--runner", type=str, default="local")
    parser.add_argument("--test_type", type=str, required=True)
    parser.add_argument("--data", type=str, help="Optional: JSON string or file with message data.")
    args = parser.parse_args()

    config = load_config(args.config)
    # Optionally: parse and load data for --data
    test_id = launch_test(args.test_type, config, args.runner)
    print(f"Test {test_id} started and finished!")

if __name__ == "__main__":
    main()