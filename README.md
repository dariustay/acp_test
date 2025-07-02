## Requirements

- **Python 3.11 or newer**
- **acp-sdk==0.10.1**
- **crewai**
- **crewai-tools**
- **python-dotenv**
- **pyyaml**
- **smolagents==1.18.0**
- **uvicorn**

## Configuration

1. Copy the example environment file and populate your API keys
2. Adjust agent and RAG settings in `config.yaml` (YAML format)

## Usage

- **Start the agent server**

  ```bash
  uv run servers/insurance_agent_server.py
  ```

- **Run examples and tests**

  Open and execute `test_call_agent_server.ipynb` in Jupyter Notebook to interact with your agents.

## Project Structure

```
.
├── .env.example                     # Sample environment variables
├── config.yaml                      # Agent & RAG configuration
├── docs/                            # Reference documents for RAG demos
├── servers/                         # Agent server implementations
├── utils/                           # Helper modules
├── test_call_agent_server.ipynb     # Quick-start Jupyter notebook
└── .gitignore
```
