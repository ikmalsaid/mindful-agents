from datetime import datetime
import gradio as gr

def preprocess(message, history, client=None, chat_history=None):
    """
    Process chat messages and handle image uploads.
    
    Parameters:
    - message: Dict containing text and files from the multimodal textbox
    - history: List of Gradio chat messages (UI history)
    - client: MindfulClient instance
    - chat_history: List of mindful client chat messages (session history)
    """
    try:
        if not client:
            return history, None
            
        # Process the message content
        if isinstance(message, dict):
            text = message.get("text", "").strip()
            files = message.get("files", [])
        else:
            # Handle direct text input
            text = str(message).strip()
            files = []
        
        # Add user message to history immediately
        history = history + [(text, None)]
        yield history, chat_history
        
        # Get response from client with streaming
        response = ""
        for chunk, updated_history in client.get_completions_stream(
            prompt=text,
            image_path=files if files else None,
            history=chat_history if chat_history else None
        ):
            response += chunk
            # Update the last assistant message
            history[-1] = (text, response)
            chat_history = updated_history
            yield history, chat_history
        
    except Exception as e:
        history = history + [(text, f"Error: {str(e)}")]
        yield history, chat_history

def MindfulWebUI(client, host: str = None, port: int = None, browser: bool = True, upload_size: str = "4MB",
                   public: bool = False, limit: int = 1, quiet: bool = True):
    """
    Start Mindful WebUI with all features.
    
    Parameters:
    - client (Client): Mindful Client instance
    - host (str): Server host
    - port (int): Server port
    - browser (bool): Launch browser automatically
    - upload_size (str): Maximum file size for uploads
    - public (bool): Enable public URL mode
    - limit (int): Maximum number of concurrent requests
    - quiet (bool): Enable quiet mode
    """
    try:        
        system_theme = gr.themes.Default(
            primary_hue=gr.themes.colors.rose,
            secondary_hue=gr.themes.colors.rose,
            neutral_hue=gr.themes.colors.zinc
        )
        
        css = '''
        @import url('https://db.onlinewebfonts.com/c/91365a119c448bf9da6d8f710e3bdda6?family=Nokia+Sans+S60+Regular');

        @font-face {
            font-family: "Nokia Sans S60 Regular";
            src: url('https://db.onlinewebfonts.com/c/91365a119c448bf9da6d8f710e3bdda6?family=Nokia+Sans+S60+Regular') format('woff2');
        }

        * {
            font-family: "Nokia Sans S60 Regular";
        }

        ::-webkit-scrollbar {
            display: none;
        }

        ::-webkit-scrollbar-button {
            display: none;
        }

        body {
            background-color: #000000;
            background-image: linear-gradient(45deg, #111111 25%, #000000 25%, #000000 50%, #111111 50%, #111111 75%, #000000 75%, #000000 100%);
            background-size: 40px 40px;
            -ms-overflow-style: none;
        }

        gradio-app {
            --body-background-fill: None;
        }
        footer {
            display: none !important;
        }

        
        /* Touch device optimizations */
        @media (hover: none) {
            button, input, select {
                min-height: 44px;
            }
        }

        /* Prevent zoom on input focus for iOS */
        @media screen and (-webkit-min-device-pixel-ratio: 0) { 
            select,
            textarea,
            input {
                font-size: 16px;
            }
        }
        '''
                
        def Markdown(name:str):
            return gr.Markdown(f"{name}")

        def State(name:list):
            return gr.State(name)
        
        with gr.Blocks(title=f"Mindful Client", css=css, analytics_enabled=False, theme=system_theme, fill_height=True).queue(default_concurrency_limit=limit) as demo:
            
            with gr.Row():
                with gr.Column(scale=1):
                    Markdown(f"## <br><center>Mindful Client")
                    Markdown(f"<center>Copyright (C) 2023-{datetime.now().year} Ikmal Said. All rights reserved")
            
            with gr.Tab("Mindful Interactive Chat"):
                chat_history = gr.State([])
                
                with gr.Row(equal_height=False):
                    with gr.Column(variant="panel", scale=3) as result:
                        chatbot = gr.Chatbot(
                            height=500,
                            show_label=False,
                            avatar_images=["🧑", "🤖"],
                            bubble_full_width=False,
                        )
                        
                        # Update the textbox to return a dictionary
                        textbox = gr.Textbox(
                            placeholder="Type a message...",
                            show_label=False,
                            container=False,
                            scale=7,
                        )
                        
                        # Add separate file upload component
                        file_upload = gr.File(
                            file_types=["image"],
                            file_count="multiple",
                            visible=True,
                            scale=7,
                        )
                        
                        with gr.Row():
                            submit = gr.Button("Send", variant="primary", scale=1)
                            clear = gr.Button("Clear", variant="secondary", scale=1)
                        
                        # Bind client to the chat function
                        client_state = gr.State(client)
                        
                        # Function to format inputs as dictionary
                        def format_inputs(text, files):
                            if not text and not files:
                                return None
                            return {"text": text, "files": files if files else []}
                        
                        # Set up chat interface events with session state
                        submit_click = submit.click(
                            format_inputs,
                            inputs=[textbox, file_upload],
                            outputs=gr.State(),  # Temporary state for formatted input
                        ).then(
                            preprocess,
                            inputs=[gr.State(), chatbot, client_state, chat_history],
                            outputs=[chatbot, chat_history],
                            api_name="chat"
                        )
                        
                        textbox_submit = textbox.submit(
                            format_inputs,
                            inputs=[textbox, file_upload],
                            outputs=gr.State(),  # Temporary state for formatted input
                        ).then(
                            preprocess,
                            inputs=[gr.State(), chatbot, client_state, chat_history],
                            outputs=[chatbot, chat_history],
                            api_name=False
                        )
                        
                        # Clear both UI and session history
                        def clear_history():
                            return None, [], None  # Clear chatbot, history, and file upload
                        
                        clear.click(clear_history, None, [chatbot, chat_history, file_upload], queue=False)
                        
                        # Example messages
                        gr.Examples(
                            examples=[
                                "What is the meaning of life?",
                                "Tell me a joke.",
                                "What is the capital of France?",
                            ],
                            inputs=textbox
                        )

            Markdown("<center>Mindful can make mistakes. Check important info.")

        demo.launch(
            server_name=host,
            server_port=port,
            inbrowser=browser,
            max_file_size=upload_size,
            share=public,
            quiet=quiet
        )
        
    except Exception as e:
        client.logger.error(f"{str(e)}")
        raise