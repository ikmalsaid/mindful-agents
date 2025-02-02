<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atelier D3 Client API</title>
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
            width: 90%;
            max-width: 800px;
            z-index: 51;
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
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;">Atelier D3 Client API Server</h1>
            <p style="color: var(--muted-foreground);">Copyright (C) 2025 Ikmal Said. All rights reserved</p>
            <button onclick="openTestDialog()" class="button button-primary" style="margin-top: 1rem;">
                Test Image Generation
            </button>
        </div>

        <!-- Modal Dialog -->
        <div id="testDialog" class="modal-backdrop">
            <div class="modal">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; place-content: center;">
                    <h2 style="font-size: 1.25rem; font-weight: 600;">Test Image Generation</h2>
                </div>

                <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
                    <input type="text" id="prompt" placeholder="Enter your prompt" class="input">
                    <button onclick="generateImages()" class="button button-primary">Generate</button>
                </div>

                <div class="grid">
                    <div class="grid-item" id="image0">
                        <div class="loader"></div>
                        <img>
                    </div>
                    <div class="grid-item" id="image1">
                        <div class="loader"></div>
                        <img>
                    </div>
                    <div class="grid-item" id="image2">
                        <div class="loader"></div>
                        <img>
                    </div>
                    <div class="grid-item" id="image3">
                        <div class="loader"></div>
                        <img>
                    </div>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; place-content: center;">
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
                        <td>/v1/api/image/generate</td>
                        <td>Generate images from text prompts</td>
                        <td>
                            <ul>
                                <li><code>prompt</code> (required): Text prompt</li>
                            </ul>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>

    <script>
        function openTestDialog() {
            document.getElementById('testDialog').style.display = 'block';
            updateCurlExample();
        }

        function closeTestDialog() {
            document.getElementById('testDialog').style.display = 'none';
            // Reset the grid
            for (let i = 0; i < 4; i++) {
                const container = document.getElementById(`image${i}`);
                container.classList.remove('loading');
                container.querySelector('img').style.display = 'none';
                container.querySelector('img').src = '';
            }
        }

        async function generateImages() {
            const prompt = document.getElementById('prompt').value;
            if (!prompt) {
                alert('Please enter a prompt');
                return;
            }

            // Reset and show loading for all containers
            for (let i = 0; i < 4; i++) {
                const container = document.getElementById(`image${i}`);
                // Clear any existing content first
                container.querySelector('img').style.display = 'none';
                const existingWarning = container.querySelector('.warning');
                if (existingWarning) {
                    existingWarning.remove();
                }
                // Then show loading state
                container.classList.add('loading');
            }

            try {
                const formData = new FormData();
                formData.append('prompt', prompt);
                const response = await fetch('/v1/api/image/generate', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                // Clear loading state from all containers
                for (let i = 0; i < 4; i++) {
                    const container = document.getElementById(`image${i}`);
                    container.classList.remove('loading');
                }

                if (data.success && data.results) {
                    data.results.forEach((dataUrl, index) => {
                        if (index < 4) {  // Ensure we don't exceed our grid
                            const container = document.getElementById(`image${index}`);
                            const img = container.querySelector('img');
                            img.src = dataUrl;
                            img.style.display = 'block';
                        }
                    });
                } else {
                    // Show error in grid items
                    for (let i = 0; i < 4; i++) {
                        const container = document.getElementById(`image${i}`);
                        const warning = document.createElement('div');
                        warning.className = 'warning';
                        warning.textContent = data.error || 'Generation failed';
                        container.appendChild(warning);
                    }
                }
            } catch (error) {
                // Clear loading state and show error
                for (let i = 0; i < 4; i++) {
                    const container = document.getElementById(`image${i}`);
                    container.classList.remove('loading');
                    const warning = document.createElement('div');
                    warning.className = 'warning';
                    warning.textContent = error.message || 'Request failed';
                    container.appendChild(warning);
                }
            }
        }
    </script>
</body>
</html> 