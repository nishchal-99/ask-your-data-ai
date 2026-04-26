from db import run_query
from sql_engine import analyze_sql_risk, fix_sql, generate_sql


def main():
    print("Ask Your Data - CLI Mode")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nAsk a question: ").strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            print("Please enter a question.")
            continue

        sql_query = generate_sql(user_input)

        if not sql_query:
            print("Failed to generate SQL.")
            continue

        print("\nGenerated SQL:")
        print(sql_query)

        risk_report = analyze_sql_risk(sql_query)

        if risk_report["risk"] == "warning":
            print("\n⚠️ Warning:")
            print(risk_report["message"])
            print("Detected:", ", ".join(risk_report["keywords"]))

            confirmation = input("Run this query anyway? Type YES to continue: ")

            if confirmation != "YES":
                print("Query cancelled.")
                continue

        try:
            columns, results = run_query(sql_query)

        except Exception as e:
            print("\nError detected. Trying to fix query...")
            fixed_query = fix_sql(user_input, sql_query, str(e))

            print("\nFixed SQL:")
            print(fixed_query)

            columns, results = run_query(fixed_query)

        print("\nResults:")

        if columns:
            print(columns)

        for row in results:
            print(row)

        if not results:
            print("No rows returned.")


if __name__ == "__main__":
    main()