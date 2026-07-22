import sys
import traceback
from leetcode_api import LeetCodeAPI
from github_sync import GitHubSynchronizer


def banner():

    print("=" * 60)
    print("LeetCode Synchronizer")
    print("=" * 60)
    print()


def main():

    banner()

    try:

        print("Connecting to LeetCode...\n")

        api = LeetCodeAPI()

        print("Fetching submissions...\n")

        submissions = api.fetch_all_submissions()

        print()

        print(
            f"Fetched {len(submissions)} accepted submissions.\n"
        )

        print("Synchronizing GitHub...\n")

        github = GitHubSynchronizer()

        github.synchronize(submissions)

        print()

        print("=" * 60)
        print("Synchronization Successful")
        print("=" * 60)

    except KeyboardInterrupt:

        print("\nCancelled by user.")

        sys.exit(1)

    except Exception:

        print()

        print("=" * 60)
        print("Synchronization Failed")
        print("=" * 60)

        traceback.print_exc()

        sys.exit(1)


if __name__ == "__main__":
    main()