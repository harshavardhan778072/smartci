import os
import sys
from pathlib import Path

from openai import OpenAI


LOG_FILE = Path("build.log")
SUMMARY_FILE = Path("error_summary.md")


def summarize_log():
    if not LOG_FILE.exists():
        print("Error: build.log was not found.")
        sys.exit(1)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Error: OPENAI_API_KEY is not configured.")
        sys.exit(1)

    log_text = LOG_FILE.read_text(
        encoding="utf-8",
        errors="replace"
    )

    # Send only the last part of the log to avoid very large requests.
    log_text = log_text[-12000:]

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5.5",
        instructions=(
            "You are a software build-log analysis assistant. "
            "Explain errors in simple language. Identify the likely "
            "cause, important error messages, and practical steps "
            "to fix the problem. Do not invent information."
        ),
        input=f"Analyze this build or test error log:\n\n{log_text}"
    )

    summary = response.output_text

    SUMMARY_FILE.write_text(
        "# AI Build Error Summary\n\n" + summary,
        encoding="utf-8"
    )

    print(summary)

    # Show the summary on the GitHub Actions run page.
    github_summary = os.getenv("GITHUB_STEP_SUMMARY")

    if github_summary:
        with open(github_summary, "a", encoding="utf-8") as file:
            file.write("# AI Build Error Summary\n\n")
            file.write(summary)
            file.write("\n")


if __name__ == "__main__":
    summarize_log()