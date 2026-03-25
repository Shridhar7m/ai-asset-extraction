#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip list


# In[6]:


pip install google-search-results


# In[9]:


pip install openai


# In[15]:


import os

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "your_actual_serpapi_key"


# In[21]:


import os
import json
import time
from dotenv import load_dotenv
from serpapi import GoogleSearch

# API Keys (for Jupyter use os.environ instead)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERPAPI_API_KEY")


# 1. Web Search

def search_web(query):
    print("\n Searching:", query)

    params = {
        "q": query,
        "api_key": SERP_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    snippets = []
    for res in results.get("organic_results", []):
        snippet = res.get("snippet", "")
        if snippet:
            snippets.append(snippet)

    context = " ".join(snippets[:5])

    if not context:
        print(" No search results found")

    return context



# 2. Prompt Builder

def build_prompt(context, input_data):
    return f"""
You are an AI system that extracts product metadata.

Context:
{context}

Extract the following fields in STRICT JSON format:

{{
  "asset_classification": "",
  "manufacturer": "",
  "model_number": "",
  "product_line": "",
  "summary": ""
}}

Rules:
- Keep model_number exactly as: {input_data['model_number']}
- Do NOT guess unknown values
- Output ONLY JSON
"""



# 3. Mock LLM (No API needed)

def call_llm(prompt):
    print(" Using mock response (no API)")

    return """
    {
      "asset_classification": "Marine Generator",
      "manufacturer": "Cummins",
      "model_number": "MRN85HD",
      "product_line": "Onan",
      "summary": "The Cummins MRN85HD is a marine generator used for power generation in marine environments."
    }
    """



# 4. Validate Output

def is_valid(output):
    required_fields = [
        "asset_classification",
        "manufacturer",
        "model_number",
        "product_line",
        "summary"
    ]

    for field in required_fields:
        if field not in output or not output[field]:
            return False

    return True



# 5. Main Logic

def process_asset(input_data):
    print("\n Input:", input_data)

    query = f"{input_data['model_number']} {input_data['asset_classification_name']} specifications manufacturer"

    context = search_web(query)

    for attempt in range(5):
        print(f" Attempt {attempt + 1}")

        prompt = build_prompt(context, input_data)
        response = call_llm(prompt)

        response = response.strip().replace("```json", "").replace("```", "")

        try:
            parsed = json.loads(response)

            if is_valid(parsed):
                print(" Success")
                return parsed
            else:
                print(" Incomplete fields, retrying...")

        except Exception as e:
            print(" JSON Parsing Failed:", e)

        time.sleep(2)

    print(" Fallback triggered")

    return {
        "asset_classification": "Generator Emissions/UREA/DPF Systems",
        "manufacturer": "",
        "model_number": input_data["model_number"],
        "product_line": "",
        "summary": ""
    }



# 6. USER INPUT SECTION

if __name__ == "__main__":
    print("==== Asset Information Extraction ====\n")

    model_number = input("Enter Model Number: ")
    asset_name = input("Enter Asset Classification Name: ")
    manufacturer = input("Enter Manufacturer (optional): ")

    input_json = {
        "model_number": model_number,
        "asset_classification_name": asset_name,
        "manufacturer": manufacturer,
        "asset_classification_guid2": ""
    }

    result = process_asset(input_json)

    print("\n Final Output:")
    print(json.dumps(result, indent=4))


# In[ ]:




