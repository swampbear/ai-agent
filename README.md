# AI Agent

A Python-based AI coding agent powered by Google's Gemini AI that can interact with your file system to read, write, execute, and manage Python files within a sandboxed working directory.

> 🎓 **Built while learning from [Boot.dev](https://boot.dev)** - An interactive platform where I code a bit every day to level up my programming skills!

## Features

The AI agent can perform the following operations:

- 📂 **List files and directories** - Browse the file structure
- 📖 **Read file contents** - View the contents of files (up to 10,000 characters)
- ✍️ **Write/overwrite files** - Create new files or modify existing ones
- ▶️ **Execute Python files** - Run Python scripts and capture their output

All operations are constrained to a specified working directory for security.

## Prerequisites

- Python 3.12 or higher
- A Google Gemini API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/swampbear/ai-agent.git
cd ai-agenthttps://github.com/swampbear/ai-agent.git
```

2. Install dependencies using `uv`:

```bash
uv sync
```

3. Create a `.env` file in the project root and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the agent with a prompt:

```bash
python main.py "your prompt here"
```

### Examples

**List files in a directory:**

```bash
python main.py "List all files in the current directory"
```

**Read a file:**

```bash
python main.py "Show me the contents of main.py"
```

**Create a new Python file:**

```bash
python main.py "Create a file called hello.py that prints 'Hello, World!'"
```

**Run a Python script:**

```bash
python main.py "Run the tests.py file"
```

**Complex task:**

```bash
python main.py "Read the calculator.py file, identify any bugs, and fix them"
```

### Verbose Mode

For detailed output showing function calls and responses:

```bash
python main.py "your prompt" --verbose
```

## Configuration

Edit `config.py` to adjust settings:

- `CHARACTER_LIMIT_GET_FILE_CONTENT`: Maximum characters to read from a file (default: 10,000)
- `RUN_PY_TIMEOUT`: Timeout for Python file execution in seconds (default: 30)
- `MAX_ITER`: Maximum iterations for agent loop (default: 20)

## Project Structure

```
ai-agent/
├── main.py                 # Main entry point
├── config.py              # Configuration settings
├── prompts.py             # System prompt for the AI agent
├── functions/             # Available functions for the agent
│   ├── get_files_info.py      # List files and directories
│   ├── get_file_content.py    # Read file contents
│   ├── write_file.py          # Write/overwrite files
│   ├── run_python_file.py     # Execute Python files
│   └── call_function.py       # Function dispatcher
└── calculator/            # Example working directory
    └── ...
```

## How It Works

1. The agent receives your natural language prompt
2. It uses Google's Gemini 2.0 Flash model with function calling capabilities
3. The AI decides which functions to call based on your request
4. Functions are executed within the sandboxed `./calculator` directory
5. Results are processed and returned to you
6. The agent iterates until the task is complete or max iterations are reached

## Security

- All file operations are restricted to the working directory (`./calculator` by default)
- Path traversal attempts are blocked
- Python file execution has a configurable timeout
- File content reading is limited to prevent memory issues

## Limitations

- Currently hardcoded to work with the `./calculator` directory
- Only supports Python file execution
- File content reading is truncated at the character limit
- Maximum of 20 iterations per request
