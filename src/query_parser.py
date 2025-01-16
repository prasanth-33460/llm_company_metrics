import os
import requests
import json
import spacy
from dotenv import load_dotenv

load_dotenv()

nlp = spacy.load("en_core_web_sm")
common_metrics = ['revenue', 'profit', 'sales', 'gmv', 'gross_margin', 'revenue_growth', 'earnings', 'margin']

class QueryParser:
    def __init__(self):
        self.llm_url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("API Key not found. Please set the GROQ_API_KEY environment variable.")

    def extract_companies_from_query(self, query):
        companies = set()
        doc = nlp(query.lower())
        for ent in doc.ents:
            if ent.label_ == "ORG":
                companies.add(ent.text.lower())
        return list(companies)

    def extract_metrics_from_query(self, query):
        metrics = set()
        query_tokens = query.lower().split()
        for token in query_tokens:
            if token in common_metrics:
                metrics.add(token)
        return list(metrics)

    def parse(self, query: str) -> dict:
        try:
            metrics = self.extract_metrics_from_query(query)
            if not metrics:
                metrics.append('revenue')

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that parses company performance queries into structured JSON data. "
                        "Return only a JSON object with the following structure:\n"
                        "{\n"
                        "  \"companies\": [\"Company1\", \"Company2\"],\n"
                        "  \"metrics\": {\n"
                        "      \"Company1\": [\"Metric1\", \"Metric2\"],\n"
                        "      \"Company2\": [\"Metric1\"]\n"
                        "  },\n"
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
                print("Extracted Data:", extracted_data)

                if extracted_data:
                    extracted_data = extracted_data.strip("```").strip()
                    if extracted_data.startswith("json"):
                        extracted_data = extracted_data[4:].strip()
                    try:
                        parsed_data = json.loads(extracted_data)
                        print("Parsed JSON Data:", json.dumps(parsed_data, indent=2))

                        metrics_map = parsed_data.get("metrics", {})
                        for company in parsed_data.get("companies", []):
                            if company not in metrics_map:
                                metrics_map[company] = metrics
                        return {
                            "companies": parsed_data.get("companies", []),
                            "metrics": metrics_map,
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