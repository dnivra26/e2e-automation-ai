from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import Browser, BrowserConfig


async def execute(test_scenario: str):

    agent = Agent(
        task=test_scenario,
        llm=ChatOpenAI(model="gpt-4o"),
        generate_gif=True,
        # browser=browser,
    )
    history = await agent.run()
    result = history.final_result()
    return result

