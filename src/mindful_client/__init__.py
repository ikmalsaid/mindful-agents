import os
import json
import uuid
import time
import base64
import requests
import tempfile
from importlib import resources
from colorpaws import setup_logger
from datetime import datetime

class MindfulClient:
    def __init__(self, log_on=True, log_to=None, agent='default', model='omni', instruction=None,
                 save_to='outputs', save_as='json', timeout=60):
        """Initialize the MindfulClient.
        
        Parameters:
        - log_on (bool): Whether to log to console or file
        - log_to (str): The file to log to (if log_on is True)
        - agent (str): The agent to use
        - model (str): The model to use
        - instruction (str): The system prompt to use
        - save_to (str): The directory to save the chat history
        - save_as (str): The format to save the chat history ('json', 'txt', 'md')
        - timeout (int): The timeout for API requests
        """
        self.__online_check()
        
        self.logger = setup_logger(
            name=self.__class__.__name__,
            log_on=log_on,
            log_to=log_to
        )
        
        self.version = "25.1"
        self.timeout = timeout

        self.__load_preset()
        self.__load_locale()
        
        self.__init_checks(save_to, save_as, model)        
        
        if instruction:
            self.logger.info("System prompt provided, setting agent to custom")
            agent = 'custom'
            
        self.__agent = self.__get_agent(agent, instruction)
        self.logger.info("Mindful Client is ready!")
          
    def __init_checks(self, save_to: str, save_as: str, model: str):
        """
        Initialize essential checks.
        """
        try:
            self.save_to = save_to if save_to else tempfile.gettempdir()
            self.save_to = os.path.join(self.save_to, "mindful")
            
            if save_as.lower() in ['json', 'txt', 'md']:
                self.save_as = save_as.lower()
            else:
                self.logger.warning("Invalid save_as format, defaulting to 'json'")
                self.save_as = 'json'
            
            self.__model = self.__preset['model'][model]
            if not self.__model:
                raise ValueError(f"Invalid model: {model}")
        
        except Exception as e:
            self.logger.error(f"Error in init_modules: {e}")
            raise RuntimeError(f"Error in init_modules: {e}")
        
    def __online_check(self, url: str = 'https://www.google.com', timeout: int = 10):
        """
        Check if there is an active internet connection.
        """
        try:
            requests.get(url, timeout=timeout)
        
        except Exception:
            self.logger.error("No internet! Please check your network connection.")
            raise RuntimeError("No internet! Please check your network connection.")

    def __load_preset(self, preset_path='__mf__.py'):
        """
        Load the preset file.
        """
        try:
            preset_file = resources.path(__name__, preset_path)
            with open(str(preset_file), encoding="utf-8") as f:
                content = f.read()
                self.__preset = json.loads(content)
        
        except Exception as e:
            self.logger.error(f"Error in load_preset: {e}")
            raise RuntimeError(f"Error in load_preset: {e}")

    def __get_agent(self, agent: str, sysprompt: str = None):
        """
        Get the agent prompt, handling custom system prompts if provided.
        """
        try:
            agent_template = self.__preset["agent"][agent]
            
            # If this is a custom agent with sysprompt, format the template
            if agent == 'custom' and sysprompt:
                return agent_template.format(system_prompt=sysprompt)
            
            return agent_template
            
        except Exception as e:
            self.logger.error(f"Error in get_agent: {e}")
            raise RuntimeError(f"Error in get_agent: {e}")

    def __load_locale(self):
        """
        Load the locales.
        """
        try:
            self.__hd = {'bearer': base64.b64decode(self.__preset["locale"][0]).decode('utf-8')}
            self.__ur = base64.b64decode(self.__preset["locale"][1]).decode('utf-8')
            self.__up = base64.b64decode(self.__preset["locale"][2]).decode('utf-8')
            
        except Exception as e:
            self.logger.error(f"Error in load_locale: {e}")
            raise RuntimeError(f"Error in load_locale: {e}")

    def __upload_image(self, image_path: str) -> str:
        """
        Upload an image to the server and return the URL.
        """
        try:
            image_file = open(image_path, 'rb')
            files = {'files': ('file.jpg', image_file, 'image/jpeg')}
            response = requests.post(self.__up, files=files, headers=self.__hd)
            response.raise_for_status()
            result = response.json().get('file.jpg')
            return result
        
        except Exception as e:
            self.logger.error(f"Error in upload_image: {e}")
            raise RuntimeError(f"Error in upload_image: {e}")

    def __get_task_id(self):
        """
        Generate a unique task ID for request tracking.
        Returns a combination of timestamp and UUID to ensure uniqueness.
        Format: YYYYMMDD_HHMMSS_UUID8
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            uuid_part = str(uuid.uuid4())[:8]
            task_id = f"{timestamp}_{uuid_part}"
            return task_id
        
        except Exception as e:
            self.logger.error(f"Error in get_task_id: {e}")
            raise RuntimeError(f"Error in get_task_id: {e}")

    def __stream_response(self, response, stream=""):
        """
        Process the streaming response and return the full response.
        """
        try:
            buffer = ""  # Buffer for incomplete chunks
            
            for chunk in response.iter_content(chunk_size=1024):
                if not chunk:
                    continue
                    
                # Add chunk to buffer and split into lines
                buffer += chunk.decode('utf-8')
                lines = buffer.split('\n')
                
                # Process all complete lines
                for line in lines[:-1]:  # Keep the last line in buffer as it might be incomplete
                    if line.strip() and line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])
                            if 'content' in data:
                                stream += data['content']
                        except json.JSONDecodeError:
                            self.logger.debug(f"Incomplete JSON chunk: {line}")
                            continue
                
                # Keep the last potentially incomplete line in buffer
                buffer = lines[-1]
            
            # Process any remaining data in buffer
            if buffer.strip() and buffer.startswith('data: '):
                try:
                    data = json.loads(buffer[6:])
                    if 'content' in data:
                        stream += data['content']
                except json.JSONDecodeError:
                    self.logger.debug(f"Incomplete final JSON chunk: {buffer}")
            
            return stream.strip('"')
            
        except Exception as e:
            self.logger.error(f"Error in stream_response: {e}")
            raise RuntimeError(f"Error in stream_response: {e}")

    def __convert_chat(self, history: list, file_path: str, format: str):
        """
        Convert chat history to specified format while preserving JSON.
        Supports: textfile, markdown
        """
        try:
            base_path = os.path.splitext(file_path)[0]
            task_id = history[0].get('id', 'unknown')
            
            if format == 'textfile':
                output = []
                for msg in history:
                    role = msg.get('role', '')
                    content = msg.get('content', '')
                    
                    # Handle different content types
                    if isinstance(content, list):
                        text_parts = []
                        for item in content:
                            if item.get('type') == 'text':
                                text_parts.append(item.get('text', ''))
                            elif item.get('type') == 'image_url':
                                text_parts.append(f"[Image: {item.get('file_url', {}).get('url', 'No URL')}]")
                        content = ' '.join(text_parts)
                        
                    output.append(f"{role.upper()}: {content}\n")
                
                with open(f"{base_path}.txt", 'w', encoding='utf-8') as f:
                    f.writelines(output)
                    
            elif format == 'markdown':
                output = ["# Chat History\n\n"]
                for msg in history:
                    role = msg.get('role', '')
                    content = msg.get('content', '')
                    
                    # Handle different content types
                    if isinstance(content, list):
                        text_parts = []
                        for item in content:
                            if item.get('type') == 'text':
                                text_parts.append(item.get('text', ''))
                            elif item.get('type') == 'image_url':
                                url = item.get('file_url', {}).get('url', 'No URL')
                                text_parts.append(f"\n![Image]({url})\n")
                        content = '\n'.join(text_parts)
                        
                    output.append(f"### {role.title()}\n{content}\n\n")
                
                with open(f"{base_path}.md", 'w', encoding='utf-8') as f:
                    f.writelines(output)
            
            self.logger.info(f"[{task_id}] Successfully converted chat to {format} format")
            
        except Exception as e:
            self.logger.error(f"Error in convert_chat: {e}")
            raise RuntimeError(f"Error converting chat to {format}: {e}")

    def __save_history(self, history: list):
        """
        Save the chat history to a file organized by date and task ID.
        """
        try:
            task_id = history[0].get('id', 'unknown')
            
            date_part = task_id.split('_')[0]
            formatted_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}"
            
            chat_dir = os.path.join(self.save_to, formatted_date)
            os.makedirs(chat_dir, exist_ok=True)
            
            file_path = os.path.join(chat_dir, f'{task_id}.json')
            
            # Check if file exists and load existing history
            if os.path.exists(file_path):
                self.logger.info(f"[{task_id}] Updating existing chat history file")
                try:
                    with open(file_path, 'r') as f:
                        existing_history = json.load(f)
                        
                    # Compare and append only new messages
                    existing_len = len(existing_history)
                    new_messages = history[existing_len:]
                    if new_messages:
                        existing_history.extend(new_messages)
                        history = existing_history
                
                except json.JSONDecodeError:
                    self.logger.warning(f"[{task_id}] Existing file was corrupted, overwriting")
            else:
                self.logger.info(f"[{task_id}] Creating new chat history file")


            with open(file_path, 'w') as f:
                json.dump(history, f, indent=2)
            self.logger.info(f"[{task_id}] Successfully saved JSON chat history")
            
            try:
                if self.save_as != 'json':
                    self.__convert_chat(history, file_path, self.save_as)
            
            except Exception as conv_error:
                raise Exception(f"[{task_id}] Failed to convert chat to {self.save_as} format: {conv_error}")
            
            self.logger.info(f"[{task_id}] Chat history save process completed")

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in save_history: {e}")
            raise RuntimeError(f"[{task_id}] Error in save_history: {e}")

    def load_history(self, file_path: str):
        """
        Load chat history from a JSON file.
        
        Parameters:
        - file_path (str): Path to the JSON file containing chat history
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
                
            if not isinstance(history, list) or not history:
                raise ValueError("Invalid chat history format")
                
            # Validate required fields in first message
            first_msg = history[0]
            required_fields = ['id', 'role', 'content', 'model']
            if not all(field in first_msg for field in required_fields):
                raise ValueError("Chat history missing required fields")
                
            self.logger.info(f"[{first_msg['id']}] Loaded chat history with {len(history)} messages")
            return history

        except Exception as e:
            self.logger.error(f"Error in load_history: {e}")
            raise RuntimeError(f"Error in load_history: {e}")

    def get_completions(self, prompt, image_path=None, history=None):
        """
        Integrated chat function supporting multimodal conversations (text and images).
        The system prompt from history (if provided) will be preserved, otherwise uses the initialized system prompt.
        
        Parameters:
        - prompt (str): The user's input prompt
        - image_path (str): Optional path to image file or list of image paths
        - history (list): Optional chat history for continuing conversations
        """
        try:
            start_time = time.time()
            task_id = None
            
            if history and len(history) > 0:
                task_id = history[0].get('id')
                system_prompt = history[0].get('content', self.__agent)
                if task_id:
                    self.logger.info(f"[{task_id}] Using existing task id and system prompt from history")
            
            # Only generate new task_id if we don't have one from history
            if not task_id:
                task_id = self.__get_task_id()
                system_prompt = self.__agent
                self.logger.info(f"[{task_id}] Created task id with initialized system prompt")
            
            if not history:
                history = [{
                    "id": task_id,
                    "role": "system",
                    "content": system_prompt,
                    "model": self.__model
                }]
                self.logger.info(f"[{task_id}] Initialized chat history with system prompt")
            else:
                self.logger.info(f"[{task_id}] Using existing chat history with {len(history)} messages")
            
            message_content = []
            
            if prompt:
                message_content.append({
                    "type": "text",
                    "text": prompt
                })
            
            if image_path:
                if isinstance(image_path, str):
                    image_paths = [image_path]
                elif isinstance(image_path, (list, tuple)):
                    image_paths = image_path
                else:
                    raise ValueError("image_path must be a string or list of strings")
                
                for img_path in image_paths:
                    image_url = self.__upload_image(img_path)
                    message_content.append({
                        "type": "image_url",
                        "file_url": {"url": image_url}
                    })
                    self.logger.info(f"[{task_id}] Added image URL to message content: {img_path}")
            
            history.append({
                "id": task_id,
                "role": "user",
                "content": message_content,
                "model": self.__model
            })
            self.logger.info(f"[{task_id}] Added user message to chat history with {len(message_content)} content items")
            
            data = json.dumps({
                "id": task_id,
                "messages": history,
                "model": self.__model,
                "stream": False
            })
            
            files = {
                'model_version': (None, '1'),
                'data': (None, data)
            }
            
            self.logger.info(f"[{task_id}] Processing request in {self.timeout} seconds")
            with requests.post(self.__ur, files=files, headers=self.__hd, stream=True, timeout=self.timeout) as response:
                response.raise_for_status()
                full_response = self.__stream_response(response)
            
            history.append({
                "id": task_id,
                "role": "assistant",
                "content": full_response,
                "model": self.__model
            })
            
            self.__save_history(history)
            self.logger.info(f"[{task_id}] Request completed in {time.time() - start_time:.2f} seconds")
            
            return full_response, history

        except Exception as e:
            self.logger.error(f"[{task_id}] Error in get_completions: {e}")
            return None, history