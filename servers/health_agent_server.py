import yaml
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Context, RunYield, RunYieldResume, Server
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, VisitWebpageTool
from collections.abc import AsyncGenerator
from dotenv import load_dotenv

with open("../config.yaml", "r") as f:
    config = yaml.safe_load(f)

load_dotenv() 
server = Server()


# === Agent ===

# Define LLM
model = LiteLLMModel(
    model_id=config["agents"]["health"]["llm_model"],
    max_tokens=config["agents"]["health"]["max_tokens"]
)


# === ACP Server ===

@server.agent()
async def health_agent(input: list[Message], context: Context) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    This is a CodeAgent which supports the hospital to handle health-based questions for patients. 
    Current or prospective patients can use it to find answers about their health and hospital treatments.
    """

    agent = CodeAgent(
        model=model,
        tools=[DuckDuckGoSearchTool(), VisitWebpageTool()]
    )

    prompt = input[0].parts[0].content
    response = agent.run(prompt)

    yield Message(parts=[MessagePart(content=str(response))])


if __name__ == "__main__":
    server.run(port=8000)