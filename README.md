# mindful-client

A comprehensive toolkit for interacting with large language models featuring vision capabilities and customizable agents for the edge.

## Installation
Install via pip:
```python
pip install mindful-client
```

## Key Features

- Text and image-based conversations
- Customizable agents and system prompts
- Interactive chat mode with command support
- Conversation history management
- Multiple export formats (JSON, TXT, Markdown)

## Core Functions

### Client Initialization

```python
client = MindfulClient(
    log_on=True, # Enable logging
    log_to='logs', # Log file path
    model='omniverse', # Model selection
    save_to='outputs', # History save directory
    save_as='json', # History format (json/txt/md)
    timeout=60 # Request timeout
    stream_output=True # Enable streaming output
    stream_delay=0.01 # Delay between characters during streaming
)   

# Note that when saving in TXT or Markdown format, the client will create both the specified format file AND a JSON file to preserve all conversation metadata.
```

### Chat Completion

```python
# Basic text completion
response, history = client.get_completions(
    prompt="What is the capital of Malaysia?",
    stream=True # Enable streaming response
)

# Image analysis
response, history = client.get_completions(
    prompt="What's in this image?",
    image_path="path/to/image.jpg"
)

# Multiple images
response, history = client.get_completions(
    prompt="Compare these images",
    image_path=["image1.jpg", "image2.jpg"]
)
```

### Chat History Management

```python
# Load existing chat history
loaded_history = client.load_history("path/to/history.json")

# Continue conversation with loaded history
response, updated_history = client.get_completions(
    prompt="Next question",
    history=loaded_history
)
```

### Interactive Chat

```python
client.interactive_chat(
    instruction='You are a helpful assistant.' # Optional: Custom instruction
    stream=True # Optional: Enable streaming response
)
```

The interactive chat mode supports several commands:

- `/exit` - Exit the chat session
- `/reset` - Reset the conversation
- `/agent "agent_name"` - Change the agent (default/custom)
- `/image "path" "question"` - Send image with optional question
- `/instruction "new instruction"` - Change system instruction
- `/load "path/to/history.json"` - Load chat history from file
- `/help` - Show available commands


## Chat History Storage

Chat histories are automatically saved in the specified format and organized by date:
- Location: `{save_to}/{YYYY-MM-DD}/{timestamp_uuid}.{format}`
- Supported formats: JSON, TXT, Markdown
- Each conversation includes system prompts, user messages, and assistant responses

## Requirements
- Python 3.8+
- Internet connection

## Error Handling

The client includes comprehensive error handling for:
- Network connectivity issues
- API timeouts
- Invalid file paths
- Malformed chat histories
- Authentication errors

All errors are logged when logging is enabled.

## License

See [LICENSE](LICENSE) for details.


