
import subprocess
import sys

TEST_MAPPING = {
    "src/pricing.py": "tests/test_pricing.py",
    "src/cart.py": "tests/test_cart.py",
    "src/inventory.py": "tests/test_inventory.py",
}


def get_changed_files():
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError:
        return []


def select_tests(changed_files):
    selected_tests = set()

    for file in changed_files:
        if file in TEST_MAPPING:
            selected_tests.add(TEST_MAPPING[file])

        elif file.startswith("tests/") and file.endswith(".py"):
            selected_tests.add(file)

        else:
            # Run all tests if a shared or unknown file changes
            return ["tests/"]

    return sorted(selected_tests)


if __name__ == "__main__":
    changed_files = get_changed_files()

    print("Changed files:", changed_files)

    tests = select_tests(changed_files)

    if tests:
        print("Selected tests:", tests)
        sys.exit(0)

    print("No relevant changes detected.")
    sys.exit(0)
