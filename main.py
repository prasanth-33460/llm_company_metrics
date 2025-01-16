import json
from src.query_parser import QueryParser
from src.date_utils import DateUtils
from src.json_format import JSONFormatter

query_history = []

def main():
    query = input("Enter your query: ")
    query_history.append(query)
    if len(query_history) > 6:
        query_history.pop(0)

    query_parser = QueryParser()
    date_utils = DateUtils()
    json_formatter = JSONFormatter()
    extracted_data = query_parser.parse(query)

    if isinstance(extracted_data, dict):
        metrics = extracted_data.get("metrics", {})
        if "Tesla" in metrics and "Microsoft" in metrics:
            extracted_data["metrics"] = {
                "Tesla": metrics.get("Tesla", "revenue"),
                "Microsoft": metrics.get("Microsoft", "profit")
            }
        else:
            for company in extracted_data.get("companies", []):
                if company not in extracted_data["metrics"]:
                    extracted_data["metrics"][company] = "revenue"
        default_start, default_end = date_utils.get_default_dates()
        if not extracted_data.get("startDate"):
            extracted_data["startDate"] = default_start
        if not extracted_data.get("endDate"):
            extracted_data["endDate"] = default_end
        result_json = json_formatter.format(extracted_data)
    else:
        result_json = json_formatter.format({"error": f"Expected a dictionary but got {type(extracted_data)}. Data: {extracted_data}"})

    print("Formatted JSON Output:")
    print(result_json)
    print("\nQuery History:")
    for idx, history_query in enumerate(query_history, start=1):
        print(f"{idx}. {history_query}")

if __name__ == "__main__":
    main()