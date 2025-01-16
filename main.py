import json
from src.query_parser import QueryParser
from src.date_utils import DateUtils

def main():
    query = input("Enter your query: ")
    query_parser = QueryParser()
    date_utils = DateUtils()
    extracted_data = query_parser.parse(query)

    if isinstance(extracted_data, dict):
        default_start, default_end = date_utils.get_default_dates()
        if not extracted_data.get("startDate"):
            extracted_data["startDate"] = default_start
        if not extracted_data.get("endDate"):
            extracted_data["endDate"] = default_end
        final_output = []
        if "metrics" in extracted_data:
            for company, metric in extracted_data["metrics"].items():
                final_output.append({
                    "entity": company,
                    "parameter": metric,
                    "startDate": extracted_data["startDate"],
                    "endDate": extracted_data["endDate"]
                })
            result_json = json.dumps(final_output, indent=2)
        else:
            result_json = json.dumps({"error": "Failed to extract relevant data from the query."}, indent=2)
    else:
        result_json = json.dumps({"error": f"Expected a dictionary but got {type(extracted_data)}. Data: {extracted_data}"}, indent=2)

    print("Formatted JSON Output:")
    print(result_json)

if __name__ == "__main__":
    main()