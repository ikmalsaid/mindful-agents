# mindful-agents

A powerful toolkit for interacting with large language models featuring vision capabilities and customizable agents.

## Installation

```bash
pip install mindful-agents
```

## Key Features

- 🤖 **Multimodal Conversations**
  - Text and image-based chat
  - Support for multiple images
  - Customizable system prompts
- 🔄 **Flexible Integration**
  - Interactive CLI chat
  - REST API server
  - Python library
- 💾 **History Management**
  - Save conversations (JSON/TXT/Markdown)
  - Load and continue chats
  - Organized by date and session

## Usage

### Python Library

```python
from mindful_agents import MindfulAgents

# Initialize
mindful = MindfulAgents(
    mode='default', # Mode (default/chat/api)
    log_on=True, # Enable logging
    log_to='logs', # Log directory
    model='omni', # Model selection
    save_to='outputs', # History save path
    save_as='json', # Save format (json/txt/md)
    timeout=60 # Request timeout
)

# Text chat
response, history = mindful.get_completions(
    prompt="Your question here",
    agent='default',          # Agent type
    instruction=None,         # Custom system prompt
    history=None,            # Optional chat history
    chat_id=None             # Optional chat ID
)

# Image analysis
response, history = mindful.get_completions(
    prompt="Analyze this image",
    image_path="image.jpg", # Single image
    # OR
    image_path=["img1.jpg", "img2.jpg"],  # Multiple images
    agent='default', # Agent type
    instruction=None, # Custom system prompt
    history=None, # Optional chat history
    chat_id=None # Optional chat ID
)

# Load chat history
history = mindful.load_history("path/to/history.json")
```

### Interactive CLI

Start the chat interface:

```python
from mindful_agents import MindfulAgents
MindfulAgents(mode='chat')
# OR
mindful = MindfulAgents()
mindful.start_chat(
    agent='default', # Agent type
    instruction=None # Custom system prompt
)
```

Available commands:
- `/exit` - Exit chat
- `/reset` - Reset conversation
- `/image "path" "question"` - Send image
- `/image ["path1", "path2"] "question"` - Send multiple images
- `/instruction "new prompt"` - Change system prompt
- `/load "history.json"` - Load chat history
- `/help` - Show commands

### REST API

Start the Flask API server:

```python
from mindful_agents import MindfulAgents
MindfulAgents(mode='api')
# OR
mindful = MindfulAgents()
mindful.start_api(
    host="0.0.0.0", # Server host
    port=5000, # Server port
    debug=False # Enable debug mode
)
```

#### API Endpoints

- `POST /v1/api/get/completions`

## Configuration

### Save Formats
- `json` (default) - Complete conversation data
- `txt` - Plain text format
- `md` - Markdown format with images

### Chat History
Chat histories are automatically saved and organized:
```
{save_to}/
  └── YYYY-MM-DD/
      └── YYYYMMDD_HHMMSS_UUID8.{format}
```

## License

See [LICENSE](LICENSE) for details.


