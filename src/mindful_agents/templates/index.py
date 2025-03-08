<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mindful Client API</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* Base styles */
        :root {
            --background: #09090b;
            --foreground: #fafafa;
            --muted: #27272a;
            --muted-foreground: #a1a1aa;
            --border: #27272a;
            --ring: #18181b;
            --primary: #fafafa;
            --primary-foreground: #18181b;
            --secondary: #27272a;
            --card: #09090b;
            --card-foreground: #fafafa;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--background);
            color: var(--foreground);
            line-height: 1.5;
            padding: 1rem;
        }

        /* Components */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        .card {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }

        .button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 0.375rem;
            font-weight: 500;
            padding: 0.5rem 1rem;
            transition: all 150ms;
            cursor: pointer;
            border: 1px solid var(--border);
        }

        .button-primary {
            background-color: var(--primary);
            color: var(--primary-foreground);
        }

        .button-secondary {
            background-color: var(--secondary);
            color: var(--foreground);
        }

        .input {
            width: 100%;
            padding: 0.5rem;
            background-color: var(--muted);
            border: 1px solid var(--border);
            border-radius: 0.375rem;
            color: var(--foreground);
            font-size: 0.875rem;
        }

        /* Modal */
        .modal-backdrop {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
            z-index: 50;
            display: none;
        }

        .modal {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            padding: 1.5rem;
            width: 95%;
            max-width: 1000px;
            height: 90vh;
            z-index: 51;
            display: flex;
            flex-direction: column;
        }

        /* Add styles for chat messages and markdown content */
        .message {
            margin: 0.5rem 0;
            padding: 0.5rem;
            border-radius: 0.375rem;
            overflow-wrap: break-word;
            word-wrap: break-word;
            word-break: break-word;
        }

        .message.user {
            background-color: var(--muted);
            text-align: right;
            flex-direction: row-reverse;
        }

        .message.user .thumbnail {
            margin-left: 12px;
            margin-right: 0;
        }

        .message.bot {
            background-color: transparent;
            text-align: left;
        }

        .message img {
            max-width: 100%;
            max-height: 250px;
            border-radius: 0.375rem;
            margin: 0.5rem 0;
            display: block;
        }

        /* Markdown specific styles */
        .message p {
            margin: 0.5rem 0;
        }

        .message pre {
            background-color: var(--muted);
            padding: 1rem;
            border-radius: 0.375rem;
            overflow-x: auto;
            margin: 0.5rem 0;
        }

        .message code {
            background-color: var(--muted);
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
            font-size: 0.875em;
        }

        .message pre code {
            background-color: transparent;
            padding: 0;
        }

        .message ul, .message ol {
            margin: 0.5rem 0;
            padding-left: 1.5rem;
        }

        .message blockquote {
            border-left: 3px solid var(--muted);
            margin: 0.5rem 0;
            padding-left: 1rem;
            color: var(--muted-foreground);
        }

        /* Grid */
        .grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin: 1rem 0;
        }

        .grid-item {
            aspect-ratio: 1;
            background-color: var(--muted);
            border-radius: 0.375rem;
            position: relative;
            overflow: hidden;
        }

        /* Table */
        .table-container {
            overflow-x: auto;
            border: 1px solid var(--border);
            border-radius: 0.5rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.875rem;
        }

        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        th {
            background-color: var(--muted);
            font-weight: 500;
            color: var(--muted-foreground);
        }

        /* Loader */
        .loader {
            width: 2.5rem;
            height: 2.5rem;
            border: 3px solid var(--muted-foreground);
            border-bottom-color: transparent;
            border-radius: 50%;
            display: none;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: translate(-50%, -50%) rotate(360deg); }
        }

        .grid-item.loading .loader {
            display: block;
        }

        .grid-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: none;
        }

        .warning {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #fda4af;
            font-size: 0.875rem;
            font-weight: 500;
            text-align: center;
        }

        .warning svg {
            width: 1.25rem;
            height: 1.25rem;
            stroke: currentColor;
        }

        /* Add styles for image upload preview */
        .image-upload-container {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .image-preview {
            width: 48px;
            height: 48px;
            border-radius: 0.375rem;
            border: 1px dashed var(--border);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            background-color: var(--muted);
        }

        .image-preview-label {
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            font-size: 0.75rem;
            color: var(--muted-foreground);
        }

        .image-preview img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .image-preview .remove-image {
            position: absolute;
            top: 2px;
            right: 2px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 50%;
            width: 16px;
            height: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 10px;
            color: var(--foreground);
        }

        /* Add these styles in the <style> section */
        .message-content {
            display: flex;
            gap: 1rem;
            align-items: flex-start;
        }

        .message-thumbnails {
            display: flex;
            margin-top: 0.5rem;
            flex-direction: column-reverse;
        }

        .message-thumbnail {
            width: 100px;
            height: 100px;
            border-radius: 0.375rem;
            object-fit: cover;
            border: 1px solid var(--border);
            background-color: var(--muted);
        }

        .copy-button {
            background-color: var(--muted);
            border: none;
            border-radius: 0.25rem;
            padding: 0.25rem 0.5rem;
            color: var(--muted-foreground);
            cursor: pointer;
            font-size: 0.75rem;
            margin-left: 0.5rem;
        }

        .copy-button:hover {
            background-color: var(--border);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;">Mindful Client API Server</h1>
            <p style="color: var(--muted-foreground);">Copyright (C) 2025 Ikmal Said. All rights reserved</p>
            <div style="display: flex; gap: 0.5rem; justify-content: center; margin-top: 1rem;">
                <button onclick="openTestDialog()" class="button button-primary">Open Chat</button>
            </div>
        </div>

        <!-- Modal Dialog -->
        <div id="testDialog" class="modal-backdrop">
            <div class="modal">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h2 style="font-size: 1.25rem; font-weight: 600;">Chat Interface</h2>
                </div>

                <div id="modal-chat-container" style="flex: 1; overflow-y: auto; margin-bottom: 1rem; text-align: left; background-color: var(--card); border: 1px solid var(--border); border-radius: 0.5rem; padding: 1rem;"></div>

                <form id="modal-chat-form" style="display: flex; flex-direction: column; gap: 0.5rem;">
                    <input type="text" id="system-prompt-input" class="input" placeholder="Optional: Custom system prompt...">
                    <div class="image-upload-container" id="image-upload-container">
                        <div class="image-preview">
                            <label for="image-upload-1" class="image-preview-label" title="Add image">
                                <span id="preview-1">+</span>
                            </label>
                            <input type="file" id="image-upload-1" style="display: none" accept="image/*" aria-label="Upload image">
                        </div>
                    </div>
                    <div style="display: flex; gap: 0.5rem;">
                        <input type="text" id="modal-prompt-input" class="input" placeholder="Enter your message..." required>
                        <button type="submit" class="button button-primary">Send</button>
                    </div>
                </form>

                <div style="display: flex; justify-content: center; margin-top: 1rem;">
                    <button onclick="closeTestDialog()" class="button button-secondary">Close</button>
                </div>
            </div>
        </div>

        <!-- API Documentation -->
        <div class="card">
            <h2 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem;">API Documentation</h2>
            <div class="table-container">
                <table>
                    <tr>
                        <th>POST Endpoints</th>
                        <th>Description</th>
                        <th>Parameters</th>
                    </tr>
                    <tr>
                        <td>/v1/api/get/completions</td>
                        <td>Get chat completions</td>
                        <td>
                            <ul>
                                <li><code>prompt</code> (required): User's positive prompt</li>
                                <li><code>image_path</code> (file, optional): One or more uploaded image files</li>
                                <li><code>history</code> (json, optional): Chat history (list format)</li>
                                <li><code>agent</code> (optional): Agent to use ('default' or 'custom')</li>
                                <li><code>instruction</code> (optional): Custom system prompt (will change agent to 'custom')</li>
                            </ul>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script>
        // Maintain chat history as an array of message objects
        let chatHistory = [];

        // Update the element selectors to use the new IDs
        const chatContainer = document.getElementById('modal-chat-container');
        const chatForm = document.getElementById('modal-chat-form');
        const promptInput = document.getElementById('modal-prompt-input');

        function openTestDialog() {
            document.getElementById('testDialog').style.display = 'block';
        }

        function closeTestDialog() {
            document.getElementById('testDialog').style.display = 'none';
        }

        // Function to append a plain text message to the chat container
        function appendMessage(sender, message, images = []) {
            const messageElem = document.createElement('div');
            messageElem.classList.add('message', sender);
            
            const contentWrapper = document.createElement('div');
            contentWrapper.classList.add('message-content');
            
            const textContent = document.createElement('div');
            textContent.style.flex = '1';
            
            const labelContainer = document.createElement('div');
            labelContainer.style.display = 'flex';
            labelContainer.style.alignItems = 'center';
            labelContainer.style.justifyContent = sender === 'user' ? 'flex-end' : 'flex-start';
            
            const label = document.createElement('strong');
            label.textContent = sender === 'user' ? '🧑 You: ' : '🤖 Mindful: ';
            label.style.color = sender === 'user' ? 'var(--primary)' : 'var(--muted-foreground)';
            
            const copyButton = document.createElement('button');
            copyButton.classList.add('copy-button');
            copyButton.textContent = 'Copy';
            copyButton.onclick = () => {
                navigator.clipboard.writeText(message);
                copyButton.textContent = 'Copied!';
                setTimeout(() => copyButton.textContent = 'Copy', 2000);
            };
            
            labelContainer.appendChild(label);
            labelContainer.appendChild(copyButton);
            textContent.appendChild(labelContainer);
            
            const messageText = document.createElement('div');
            messageText.textContent = message;
            textContent.appendChild(messageText);
            
            if (images.length > 0) {
                const thumbnails = document.createElement('div');
                thumbnails.classList.add('message-thumbnails');
                images.forEach(imageUrl => {
                    const img = document.createElement('img');
                    img.src = imageUrl;
                    img.classList.add('message-thumbnail');
                    thumbnails.appendChild(img);
                });
                textContent.appendChild(thumbnails);
            }
            
            contentWrapper.appendChild(textContent);
            messageElem.appendChild(contentWrapper);
            chatContainer.appendChild(messageElem);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        // Function to append a Markdown formatted message
        function appendMarkdownMessage(sender, markdownText) {
            const messageElem = document.createElement('div');
            messageElem.classList.add('message', sender);
            
            // Create a label container
            const labelContainer = document.createElement('div');
            labelContainer.style.display = 'flex';
            labelContainer.style.alignItems = 'center';
            labelContainer.style.justifyContent = sender === 'user' ? 'flex-end' : 'flex-start';
            
            const label = document.createElement('strong');
            label.textContent = sender === 'user' ? '🧑 You: ' : '🤖 Mindful: ';
            label.style.color = sender === 'user' ? 'var(--primary)' : 'var(--muted-foreground)';
            
            const copyButton = document.createElement('button');
            copyButton.classList.add('copy-button');
            copyButton.textContent = 'Copy';
            copyButton.onclick = () => {
                navigator.clipboard.writeText(markdownText);
                copyButton.textContent = 'Copied!';
                setTimeout(() => copyButton.textContent = 'Copy', 2000);
            };
            
            labelContainer.appendChild(label);
            labelContainer.appendChild(copyButton);
            messageElem.appendChild(labelContainer);
            
            // Create a content container for the markdown
            const contentContainer = document.createElement('div');
            contentContainer.classList.add('markdown-content');
            contentContainer.innerHTML = marked.parse(markdownText);
            messageElem.appendChild(contentContainer);
            
            chatContainer.appendChild(messageElem);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        // Update the image upload handling code
        function createImageUploadPreview(index) {
            const preview = document.createElement('div');
            preview.className = 'image-preview';
            preview.innerHTML = `
                <label for="image-upload-${index}" class="image-preview-label" title="Add image">
                    <span id="preview-${index}">+</span>
                </label>
                <input type="file" id="image-upload-${index}" style="display: none" accept="image/*" aria-label="Upload image">
            `;
            return preview;
        }

        function handleImageUpload(inputId, previewId) {
            const input = document.getElementById(inputId);
            const preview = document.getElementById(previewId);
            const container = document.getElementById('image-upload-container');
            const currentIndex = parseInt(inputId.split('-')[2]);

            input.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.innerHTML = `
                            <img src="${e.target.result}" alt="Preview of uploaded image">
                            <div class="remove-image" onclick="removeImage('${inputId}', '${previewId}', event)">×</div>
                        `;
                        
                        // Add new upload button if we haven't reached the maximum
                        if (currentIndex < 4 && !document.getElementById(`image-upload-${currentIndex + 1}`)) {
                            const newPreview = createImageUploadPreview(currentIndex + 1);
                            container.appendChild(newPreview);
                            handleImageUpload(`image-upload-${currentIndex + 1}`, `preview-${currentIndex + 1}`);
                        }
                    };
                    reader.readAsDataURL(file);
                }
            });
        }

        function removeImage(inputId, previewId, event) {
            event.stopPropagation();
            const container = document.getElementById('image-upload-container');
            const currentPreview = document.getElementById(inputId).parentElement;
            const currentIndex = parseInt(inputId.split('-')[2]);
            
            // Remove all preview elements after this one
            const allPreviews = container.getElementsByClassName('image-preview');
            Array.from(allPreviews).forEach(preview => {
                const previewIndex = parseInt(preview.querySelector('input').id.split('-')[2]);
                if (previewIndex > currentIndex) {
                    container.removeChild(preview);
                }
            });

            // Reset current preview
            document.getElementById(inputId).value = '';
            const label = document.createElement('label');
            label.className = 'image-preview-label';
            label.setAttribute('for', inputId);
            label.innerHTML = `<span id="${previewId}">+</span>`;
            currentPreview.innerHTML = '';
            currentPreview.appendChild(label);
            currentPreview.appendChild(document.getElementById(inputId));
        }

        // Initialize first image upload handler
        handleImageUpload('image-upload-1', 'preview-1');

        // Update the form submission handler
        chatForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const prompt = promptInput.value.trim();
            if (!prompt) return;

            const startTime = performance.now();

            // Get actual image files
            const images = [];
            // Check all 4 possible image uploads
            for (let i = 1; i <= 4; i++) {
                const imageUpload = document.getElementById(`image-upload-${i}`);
                if (imageUpload && imageUpload.files[0]) {
                    images.push(imageUpload.files[0]);
                }
            }

            // Create image URLs for display in chat
            const imageUrls = images.map(file => URL.createObjectURL(file));

            // Append the user's message to the chat log with images
            appendMessage('user', prompt, imageUrls);
            
            // Clear the input and reset image upload container
            promptInput.value = '';
            const container = document.getElementById('image-upload-container');
            container.innerHTML = ''; // Clear all existing previews
            
            // Add back single initial upload button
            const initialPreview = createImageUploadPreview(1);
            container.appendChild(initialPreview);
            handleImageUpload('image-upload-1', 'preview-1');

            // Create a FormData object and append the required parameters
            const formData = new FormData();
            formData.append('prompt', prompt);
            
            // Add actual image files if they exist
            if (images.length > 0) {
                images.forEach((file, index) => {
                    formData.append('image_path', file);
                });
            }
            
            // Only include history if we have it from previous responses
            if (chatHistory.length > 0) {
                formData.append('history', JSON.stringify(chatHistory));
            }

            // Get system prompt if provided
            const systemPrompt = document.getElementById('system-prompt-input').value.trim();
            if (systemPrompt) {
                formData.append('instruction', systemPrompt);
            }

            try {
                // Send a POST request with the FormData
                const response = await fetch('/v1/api/get/completions', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                
                const data = await response.json();

                // When success = true, show the results and update chat history
                if (data.success) {
                    let botResponse = data.response || 'No response received.';
                    
                    if (botResponse) {
                        // Calculate elapsed time
                        const endTime = performance.now();
                        const elapsedSeconds = ((endTime - startTime) / 1000).toFixed(2);
                        
                        // Calculate word count
                        const wordCount = botResponse.split(/\s+/).filter(word => word.length > 0).length;
                        
                        // Extract chat ID from history
                        const chatId = data.history && data.history[0] ? data.history[0].id : 'unknown';
                        
                        // Append the response with timing, word count, and chat ID
                        appendMarkdownMessage('bot', botResponse + `\n\n<span style="color: var(--muted-foreground); font-size: 0.75rem;">Request completed in ${elapsedSeconds} seconds • ${wordCount} words • ID: ${chatId}</span>`);
                    }
                    
                    // Update the chat history with the server's version
                    if (data.history) {
                        chatHistory = data.history;
                    }
                } else {
                    appendMessage('bot', 'Error: Request was unsuccessful.');
                }

            } catch (error) {
                console.error('Error fetching completions:', error);
                appendMessage('bot', 'Error: Could not fetch response.');
            }
        });

        promptInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });
    </script>
</body>
</html> 