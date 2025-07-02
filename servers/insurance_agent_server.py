import yaml
import nest_asyncio

from crewai import Crew, Task, Agent, LLM
from crewai_tools import RagTool

from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from collections.abc import AsyncGenerator
from dotenv import load_dotenv

nest_asyncio.apply()

with open("../config.yaml", "r") as f:
    config = yaml.safe_load(f)

load_dotenv()
server = Server()


# === Agent ===

# Define LLM
llm = LLM(
    model=config["agents"]["insurance"]["llm_model"],
    max_tokens=config["agents"]["insurance"]["max_tokens"]
)

# Define RAG tool
rag_tool = RagTool(
    config={
        "llm": {
            "provider": "google",
            "config": {
                "model": config["rag"]["insurance"]["llm_model"]
            }
        },
        "embedding_model": {
            "provider": "google",
            "config": {
                "model": config["rag"]["insurance"]["embedding_model"]
            }
        }
    },
    chunk_size=config["rag"]["insurance"]["chunk_size"],
    chunk_overlap=config["rag"]["insurance"]["chunk_overlap"]
)

for doc in config["documents"]:
    rag_tool.add(
        source=doc["path"], 
        data_type=doc["data_type"]
    )


# === ACP Server ===

@server.agent()
async def insurance_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    This is an agent for questions around policy coverage. 
    Use it to help answer questions on coverage and waiting periods.
    It uses a RAG pattern to find answers based on policy documentation.
    """

    insurance_agent = Agent(
        role="Senior Insurance Coverage Assistant", 
        goal="Determine whether something is covered or not",
        backstory="You are an expert insurance agent designed to assist with coverage queries",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[rag_tool], 
        max_retry_limit=5
    )
    
    task1 = Task(
         description=input[0].parts[0].content,
         expected_output = "A comprehensive response as to the users question",
         agent=insurance_agent
    )
    
    crew = Crew(
        agents=[insurance_agent], 
        tasks=[task1], 
        verbose=True
    )
    
    task_output = await crew.kickoff_async()
    yield Message(parts=[MessagePart(content=str(task_output))])


if __name__ == "__main__":
    server.run(port=8001)