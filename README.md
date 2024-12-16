# Agient: Psychologically-Grounded Agent Simulation Framework

Agient is a Python framework for creating psychologically realistic agent-based simulations that model human behavior, relationships, and decision-making processes. It combines psychological models with LLM capabilities to create more human-like agents.

## Features

- 🧠 **Psychological Modeling**
  - Five Factor Model (Big Five) personality traits
  - Emotional states and memory
  - Beliefs and values systems
  - Goal-oriented behavior

- 🤝 **Social Dynamics**
  - Agent-to-agent communication
  - Relationship tracking
  - Social network modeling
  - Influence mechanics

- 💭 **LLM Integration**
  - OpenAI GPT-4/3.5
  - Anthropic Claude
  - Extensible provider system

- 📊 **Memory Management**
  - SQLite-based persistent storage
  - Importance-based memory filtering
  - Emotional context tracking
  - Memory cleanup utilities

## File Structure

The project has been organized into a more structured format:

```
agient/
├── examples/
│   ├── senator_example.py
│   ├── teacher_example.py
│   └── student_example.py
├── llm/
│   ├── __init__.py
│   ├── base.py
│   ├── config.py
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── openai.py
│   │   └── anthropic.py
├── main.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── demographics.py
│   ├── memory.py
│   └── personality.py
├── storage.py
├── tests/
│   ├── __init__.py
│   └── test_storage.py
├── pyproject.toml
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 or later
- An OpenAI API key (for LLM integration)
- An Anthropic API key (for LLM integration)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/danielmerja/agient.git
   cd agient
   ```

2. Install dependencies:
   ```sh
   poetry install
   ```

3. Set up environment variables for API keys:
   ```sh
   export OPENAI_API_KEY="your_openai_api_key"
   export ANTHROPIC_API_KEY="your_anthropic_api_key"
   ```

### Running Examples

To run the provided examples, execute:
```sh
python examples/senator_example.py
python examples/teacher_example.py
python examples/student_example.py
```

### Running Tests

To run the tests, execute:
```sh
pytest
```
