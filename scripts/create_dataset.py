import random
import pandas as pd

random.seed(42)

rows = []

for _ in range(200):
    previous_failures = random.randint(0, 5)
    changed_files = random.randint(1, 20)
    code_churn = random.randint(10, 500)
    test_count = random.randint(5, 100)

    # Create a sample failure-risk score.
    risk = (
        previous_failures * 3
        + changed_files * 0.5
        + code_churn * 0.02
        - test_count * 0.05
    )

    # Sample historical outcome: 1 = failure, 0 = success.
    failed = 1 if risk + random.uniform(-3, 3) > 12 else 0

    rows.append({
        "previous_failures": previous_failures,
        "changed_files": changed_files,
        "code_churn": code_churn,
        "test_count": test_count,
        "failed": failed
    })

df = pd.DataFrame(rows)
df.to_csv("data/build_history.csv", index=False)

print("Sample build-history dataset created successfully!")
print(df.head())