import os
import sys
from pathlib import Path

# Add the project root to Python path for Vercel
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Also add the visualizer directory for module imports
visualizer_dir = project_root / "visualizer"
sys.path.insert(0, str(visualizer_dir))

# Import the Flask app
from visualizer.app import create_app

# Create the app instance - Vercel expects this to be named 'app'
app = create_app()

# For local development
if __name__ == "__main__":
    app.run(debug=False) 