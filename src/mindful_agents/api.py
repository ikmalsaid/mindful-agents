from flask import Flask, request, jsonify, render_template
import tempfile
import os
import json

def MindfulWebAPI(client, host: str = "0.0.0.0", port: int = 6463, debug: bool = False):
    """
    Start Client API server with all endpoints.
    
    Parameters:
    - client (MindfulClient): Mindful Client instance
    - host (str): Host to run the server on
    - port (int): Port to run the server on
    - debug (bool): Enable Flask debug mode
    """
    try:
        app = Flask(__name__)

        @app.route('/v1/api/get/completions', methods=['POST'])
        def get_completions():
            """
            Handle completions requests via form data.
            
            Form Parameters:
            - prompt (str, required): User's positive prompt
            - image_path (file, optional): One or more uploaded image files
            - history (json, optional): Chat history (list format)
            - agent (str, optional): Agent to use ('default' or 'custom')
            - instruction (str, optional): Custom system prompt (will change agent to 'custom')
            """
            try:
                data = {
                    'prompt': request.form.get('prompt'),
                    'history': request.form.get('history', None),
                    'agent': request.form.get('agent', 'default'),
                    'instruction': request.form.get('instruction', None),
                    'chat_id': request.form.get('chat_id', None)
                }
                
                if not data['prompt']:
                    raise ValueError("Missing required parameter: prompt")

                # Convert history JSON string to list (if provided)
                if data['history']:
                    try:
                        data['history'] = json.loads(data['history'])
                        if not isinstance(data['history'], list):
                            raise ValueError("History must be a list")
                    
                    except json.JSONDecodeError:
                        raise ValueError("Invalid JSON format for history")

                # Handle multiple image files (save to temp and pass paths)
                image_paths = []
                if 'image_path' in request.files:
                    image_files = request.files.getlist('image_path')
                    for image_file in image_files:
                        if image_file.filename:
                            temp_dir = tempfile.gettempdir()
                            temp_path = os.path.join(temp_dir, image_file.filename)
                            image_file.save(temp_path)
                            image_paths.append(temp_path)

                # Add image_paths to data if any images were processed
                if image_paths:
                    data['image_path'] = image_paths

                result, updated_history = client.get_completions(**data)

                # Clean up temp image files after processing
                if image_paths:
                    for image_path in image_paths:
                        if os.path.exists(image_path):
                            os.remove(image_path)

                if not result:
                    raise ValueError("Get completions failed")

                return jsonify({"success": True,
                                "response": result,
                                "history": updated_history
                                })

            except Exception as e:
                client.logger.error(f"Error in get_completions: {e}")
                return jsonify({"success": False, "error": str(e)}), 400

        @app.route('/', methods=['GET'])
        def api_index():
            """Render the API documentation page"""
            return render_template('idx.py')

        client.logger.info(f"Starting API server on {host}:{port}")
        app.run(host=host, port=port, debug=debug)
    
    except Exception as e:
        client.logger.error(f"Error in API initialization: {e}")
        raise
