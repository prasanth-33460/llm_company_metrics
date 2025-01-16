import json

class JSONFormatter:
    @staticmethod
    def format(data):
        try:
            if not isinstance(data, dict):
                raise ValueError("Input data must be a dictionary.")
            if "companies" not in data or "metrics" not in data:
                raise ValueError("Data must include 'companies' and 'metrics' keys.")

            companies = data.get("companies", [])
            metrics = data.get("metrics", {})
            start_date = data.get("startDate", None)
            end_date = data.get("endDate", None)

            if not isinstance(companies, list) or not isinstance(metrics, dict):
                raise ValueError("'companies' should be a list and 'metrics' should be a dictionary.")

            formatted_data = []

            for company in companies:
                metric = metrics.get(company, "unknown")

                entry = {
                    "entity": company,
                    "parameter": metric
                }

                if start_date:
                    entry["startDate"] = start_date
                if end_date:
                    entry["endDate"] = end_date

                formatted_data.append(entry)
            return json.dumps(formatted_data, indent=4)

        except Exception as e:
            return f"Error formatting JSON: {str(e)}"
