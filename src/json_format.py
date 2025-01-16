import json

class JSONFormatter:
    @staticmethod
    def format(data):
        try:
            if isinstance(data, dict) and "companies" in data:
                companies = data["companies"]
                metrics = data["metrics"]
                start_date = data["startDate"]
                end_date = data["endDate"]

                formatted_data = []
                for company in companies:
                    metric = metrics.get(company, "unknown")
                    formatted_data.append({
                        "entity": company,
                        "parameter": metric,
                        "startDate": start_date,
                        "endDate": end_date
                    })

                return json.dumps(formatted_data, indent=4)
            else:
                raise ValueError("Invalid data format")
        except Exception as e:
            return f"Error: {str(e)}"