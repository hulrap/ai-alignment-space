# AI Alignment 3D Visualization

A 3D hierarchical visualization for AI alignment components, showing relationships between various components, subcomponents, and capabilities in an interactive 3D environment.

## Features

- Interactive 3D visualization of AI alignment components
- Hierarchical structure with expandable/collapsible nodes
- Details panel showing information about selected nodes
- Smooth orbital animations for child nodes
- Draggable nodes for customizing the visualization
- Responsive design supporting different screen sizes

## Live Demo

The application can be deployed to Vercel for instant hosting.

## Local Development

### Prerequisites

- Python 3.9+
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-alignment-visualization.git
   cd ai-alignment-visualization
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   cd visualizer
   python app.py
   ```

5. Open your browser and navigate to [http://localhost:3000](http://localhost:3000)

## Deployment

### Vercel (Recommended)

1. Install the Vercel CLI:
   ```
   npm i -g vercel
   ```

2. Deploy to Vercel:
   ```
   vercel
   ```

3. Follow the prompts to configure your deployment.

The application is now ready for Vercel deployment with:
- `api/index.py` - Flask WSGI application entry point exposing `app` variable
- `vercel.json` - Simple rewrites configuration for routing
- `requirements.txt` - Python dependencies (Flask 3.0.3)
- Automatic Python runtime detection and serverless function creation

### Heroku (Alternative)

1. Make sure you have the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed.

2. Log in to Heroku:
   ```
   heroku login
   ```

3. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```

4. Push to Heroku:
   ```
   git push heroku main
   ```

5. Open the deployed app:
   ```
   heroku open
   ```

### Docker

1. Build the Docker image:
   ```
   docker build -t ai-alignment-visualization .
   ```

2. Run the container:
   ```
   docker run -p 3000:3000 ai-alignment-visualization
   ```

3. Open your browser and navigate to [http://localhost:3000](http://localhost:3000)

## Configuration

The application can be configured with the following environment variables:

- `PORT`: Port to run the application on (default: 3000)
- `FLASK_ENV`: Environment setting (development/production)
- `LOG_LEVEL`: Logging level (default: INFO)

## Project Structure

```
.
├── api/                 # Vercel API functions
│   └── index.py         # Main Flask app entry point
├── components/          # Component JSON files
├── subcomponents/       # Subcomponent JSON files
├── visualizer/          # Flask application
│   ├── static/          # Static assets (CSS, JS)
│   ├── templates/       # HTML templates
│   ├── app.py           # Flask application
│   └── node_details_helper.py  # Helper functions
├── ai-alignment.json    # Root data file
├── vercel.json          # Vercel deployment configuration
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## License

[MIT License](LICENSE)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 