from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import Browser, BrowserConfig
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

browser_config = BrowserConfig(headless=True)
browser = Browser(config=browser_config)


app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"])  # Allow all headers

class Test(BaseModel):
    test_case: str

class ScenarioRequest(BaseModel):
    description: str

@app.post("/generate-e2e-scenarios/")
async def generate_e2e_scenarios(data: ScenarioRequest):
    """
    Generate a list of e2e test scenarios using ChatGPT based on the provided description.
    """
    llm = ChatOpenAI(model="gpt-4o")
    prompt = (
        "Given the following application or feature description, generate a concise, numbered list of end-to-end (e2e) test scenarios that would comprehensively test the described functionality. "
        "Be specific and practical. Only return the list, no explanations.\n\n"
        f"Description: {data.description}\n\n"
        "e2e Test Scenarios:"
    )
    response = await llm.ainvoke(prompt)
    scenarios = response.content.strip()
    return {"scenarios": scenarios}

@app.post("/run-test/")
async def process_string(data: Test):
    output = await run_test(data.test_case)
    return {"received_string": output}


async def run_test(test_case: str):
    agent = Agent(
        task=test_case,
        llm=ChatOpenAI(model="gpt-4o"),
        generate_gif=True,
        browser=browser,
    )
    history = await agent.run()
    result = history.final_result()
    return result

@app.get("/jira-stories/")
async def get_jira_stories():
    jira_username = os.getenv("JIRA_EMAIL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    jira_base_url = os.getenv("JIRA_BASE_URL")

    if not jira_username or not jira_api_token or not jira_base_url:
        return {"error": "JIRA credentials or base URL not set in environment variables."}

    url = f"{jira_base_url}/rest/api/3/search"
    headers = {
        "Authorization": f"Basic {jira_username}:{jira_api_token}",
        "Content-Type": "application/json"
    }
    query = {
        'jql': 'type = Story'
    }

    try:
        response = requests.get(url, headers=headers, params=query)
        response.raise_for_status()
        stories = response.json()
        print(response.json())
        return {"stories": stories}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
