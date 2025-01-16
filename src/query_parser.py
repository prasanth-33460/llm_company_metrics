import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

company_aliases = {
    'amazon': 'Amazon',
    'amzn': 'Amazon',
    'flipkart': 'Flipkart',
    'walmart': 'Walmart',
}

metric_aliases = {
    'revenue': 'revenue',
    'profit': 'profit',
    'gmv': 'GMV', 
    'sales': 'revenue',
}

class QueryParser:
    def __init__(self):
        self.llm_url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("API Key not found. Please set the GROQ_API_KEY environment variable.")

    def normalize_company_name(self, name):
        return company_aliases.get(name.lower(), name.capitalize())

    def normalize_metric(self, metric):
        return metric_aliases.get(metric.lower(), metric.lower())

    def parse(self, query: str) -> dict:
        try:
            companies = []
            metrics = {}

            for alias, company in company_aliases.items():
                if alias in query.lower():
                    companies.append(company)

            for alias, metric in metric_aliases.items():
                if alias in query.lower():
                    for company in companies:
                        metrics[company] = metric

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that parses company performance queries into structured JSON data. "
                        "Return only a JSON object with the following structure:\n"
                        "{\n"
                        "  \"companies\": [\"Company1\", \"Company2\"],\n"
                        "  \"metrics\": {\"Company1\": \"Metric1\", \"Company2\": \"Metric2\"},\n"
                        "  \"time_frame\": \"Time Period\"\n"
                        "}"
                    )
                },
                {"role": "user", "content": query}
            ]

            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "n": 1
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            response = requests.post(self.llm_url, headers=headers, json=payload)
            response.raise_for_status()  
            
            data = response.json()
            print("Full API Response:", json.dumps(data, indent=2))  

            if 'choices' in data and data['choices']:
                extracted_data = data['choices'][0].get('message', {}).get('content', "").strip()
                
                if extracted_data:
                    extracted_data = extracted_data.strip("```").strip()
                    if extracted_data.startswith("json"):
                        extracted_data = extracted_data[4:].strip()

                    try:
                        parsed_data = json.loads(extracted_data)
                        for company in parsed_data.get("companies", []):
                            companies.append(self.normalize_company_name(company))
                        for company in parsed_data.get("metrics", {}):
                            metrics[company] = self.normalize_metric(metrics.get(company, "unknown"))

                        return {
                            "companies": companies,
                            "metrics": metrics,
                            "time_frame": parsed_data.get("time_frame", "unknown")
                        }

                    except json.JSONDecodeError:
                        print("Received non-JSON content. Returning as plain text.")
                        return {"raw_content": extracted_data}
                else:
                    print("Error: No valid response content in 'choices[0].message.content'")
                    return {}
            else:
                print("Error: 'choices' field is missing or empty in the response")
                return {}

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the LLM API: {e}")
            return {}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {}