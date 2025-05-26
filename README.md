# AI Alignment Space: A 3D Knowledge Universe

*An interactive 3D visualization exploring AI alignment through collaborative human-AI knowledge creation*

![AI Alignment Space](https://img.shields.io/badge/Status-V1%20Live-brightgreen) ![License](https://img.shields.io/badge/License-MIT-blue) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)

## 🌌 Vision

AI Alignment Space represents a groundbreaking approach to knowledge visualization and collaborative creation. This project transforms a 650-page academic framework into an interactive 3D cosmos where concepts float like celestial bodies, connected by the gravitational forces of their relationships.

**This is not just a visualization—it's an artistic statement about the relationship between organic human knowledge and inorganic technological systems.**

### The Larger Universe

AI Alignment is just one sphere in a planned constellation of approximately 200 knowledge domains. Each sphere represents a different field of human understanding, designed to eventually interconnect through standardized interfaces, creating a vast, explorable universe of interconnected knowledge.

## ✨ Features

### 🎨 Artistic & Interactive
- **3D Spherical Cosmos**: Navigate through floating conceptual nodes in 3D space
- **Orbital Mechanics**: Child concepts orbit their parents with realistic physics
- **Celestial Aesthetics**: Beautiful color-coded node types with smooth animations
- **Audio Feedback**: Immersive sound design enhancing exploration
- **Responsive Design**: Seamless experience across desktop and mobile devices

### 🧠 Knowledge Architecture
- **Hierarchical Structure**: Component Group → Component → Subcomponent → Capability → Function → Specification
- **Rich Metadata**: Detailed descriptions, literature connections, and academic citations
- **5000+ Academic Sources**: Comprehensive research foundation with verified citations
- **Interactive Exploration**: Click to expand, explore relationships, and dive deep into concepts

### 🤖 AI-Human Collaboration
- **Collaborative Creation**: Built through intensive human-AI partnership
- **Quality Assurance**: Rigorous verification against academic sources
- **Iterative Refinement**: Continuous improvement through feedback loops
- **Editorial Oversight**: Human guidance ensuring accuracy and coherence

## 🚀 Live Demo

**Experience the visualization**: [AI Alignment Space](https://ai-alignment-space.vercel.app) *(Replace with your actual deployment URL)*

## 📖 The Story

This project began with nothing but an idea and evolved through an intensive 10+ month journey:

1. **Conceptual Foundation** (2 months): 150-page whitepaper → 650-page comprehensive framework
2. **Structural Revolution**: Linear text → Hierarchical knowledge architecture  
3. **Visualization Journey** (January 2024 - Present): AI-assisted coding collaboration
4. **Pragmatic Evolution**: Complex TypeScript → Simple HTML/JS/Python on Vercel

*Read the complete story in our [Medium article](medium.md)*

## 🛠 Technical Architecture

### Backend (Flask/Python)
- RESTful API serving structured knowledge data
- Dynamic node detail generation with rich metadata
- Hierarchical path calculation for navigation
- Rate limiting and security measures

### Frontend (Three.js/JavaScript)
- 3D spherical visualization with orbital mechanics
- Interactive node expansion and exploration
- Smooth camera movements and transitions
- Audio feedback system for enhanced immersion

### Data Layer
- JSON-based knowledge representation
- Hierarchical component structure
- Rich literature connections and citations
- Standardized node types and relationships

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.9+
- Modern web browser with WebGL support

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hulrap/ai-alignment-space.git
   cd ai-alignment-space
   ```

2. **Set up Python environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   cd visualizer
   python app.py
   ```

4. **Open your browser**: Navigate to [http://localhost:3000](http://localhost:3000)

### Deployment (Vercel)

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel --force (in case some deployments conflict)
   vercel --prod (for production deployments)
   ```

The application is optimized for Vercel with automatic Python runtime detection and serverless function creation.

## 📁 Project Structure

```
ai-alignment-space/
├── 📄 medium.md                    # Complete project story and methodology
├── 🌐 api/                         # Vercel serverless functions
│   └── index.py                    # Flask WSGI entry point
├── 📊 components/                  # Main component definitions
│   ├── technical-safeguards.json
│   ├── value-learning.json
│   ├── interpretability-tools.json
│   ├── oversight-mechanisms.json
│   └── democratic-alignment.json
├── 🔧 subcomponents/               # Detailed subcomponent specifications
├── 🎨 visualizer/                  # Flask application
│   ├── static/                     # CSS, audio assets
│   ├── templates/                  # HTML templates
│   ├── app.py                      # Main Flask application
│   └── node_details_helper.py     # Data processing utilities
├── 📋 ai-alignment.json            # Root knowledge structure
├── ⚙️ vercel.json                  # Deployment configuration
└── 📦 requirements.txt             # Python dependencies
```

## 🗺 Roadmap

### V1: Foundational Skeleton & Artistic Statement ✅
- [x] Core 3D visualization framework
- [x] Complete AI alignment knowledge base
- [x] Interactive exploration capabilities
- [x] Comprehensive documentation

### V2: Content Refinement & Node Interaction 🔄
- [ ] Community collaboration platform
- [ ] Node editing capabilities
- [ ] Enhanced relationship mapping
- [ ] User contribution system

### V3: Input/Output Standardization & Modularization 🔮
- [ ] Standardized interfaces between knowledge spheres
- [ ] Modular architecture for sphere interconnection
- [ ] Cross-domain relationship mapping

### V4: AI-Integrated Structured Co-Creation 🚀
- [ ] AI assistance in content maintenance
- [ ] Automated quality assurance
- [ ] Structured collaborative knowledge creation at scale

## 🎯 Node Types & Hierarchy

The visualization employs a systematic hierarchy of node types:

- **🏛 Component Group** (Level 0): Highest-level organizational units
- **🔧 Component** (Level 1): Primary functional units
- **⚙️ Subcomponent** (Level 2): Specialized divisions
- **💪 Capability** (Level 3): High-level functional abilities
- **🔄 Function** (Level 4): Specific operational processes
- **📋 Specification** (Level 5): Technical requirements and standards
- **🔗 Integration** (Level 5): Implementation approaches
- **🛠 Technique** (Level 5): Methodological approaches
- **🎯 Application** (Level 5): Practical implementations
- **📥 Input** (Level 5): Data and resources entering the system
- **📤 Output** (Level 5): Results and products from processes

## 🤝 Contributing

We welcome contributions to expand and refine this knowledge universe! Here's how you can help:

### For V1 (Current)
- 🐛 Report bugs or visualization issues
- 📝 Suggest improvements to existing content
- 🎨 Propose UI/UX enhancements
- 📚 Contribute additional literature references

### For V2 (Planned)
- 🔧 Help build the collaborative editing platform
- 🌐 Contribute to the open-source development
- 📊 Assist with content verification and quality assurance

### Getting Started
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-contribution`)
3. Make your changes
4. Commit with descriptive messages (`git commit -m 'Add amazing contribution'`)
5. Push to your branch (`git push origin feature/amazing-contribution`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- **AI Collaboration**: Built through intensive partnership with Claude Sonnet and OpenAI o1
- **Academic Foundation**: Based on 5000+ verified academic sources
- **Open Source Community**: Inspired by the principles of collaborative knowledge creation
- **Three.js Community**: For the incredible 3D visualization capabilities

## 📞 Contact

**Project Creator**: Raphael Hulan  
**Email**: [ai-alignment-sphere@proton.me](mailto:ai-alignment-sphere@proton.me)  
**Company**: Raw Fiction e.U.  

---

*"This is not an actual universe, but a human-created mirror of cosmic organization. The spherical nodes embody the paradox of our technological age: inorganic information systems that organic humans must navigate, interpret, and apply to preserve what is fundamentally human and ecological."*

**⭐ Star this repository if you find it interesting!** 
5. Open a Pull Request 




# Security Implementation

This document outlines the security measures implemented in the AI Alignment Visualizer.

## Implemented Security Measures

### 1. Input Validation
- **Node ID Validation**: All node identifiers are validated to only allow alphanumeric characters, hyphens, and underscores
- **Prevents**: Path traversal attacks, injection attacks

### 2. Error Information Sanitization
- **Safe Error Messages**: Internal error details are not exposed to users
- **Prevents**: Information disclosure, system fingerprinting

### 3. Rate Limiting
- **100 requests per minute per IP address**
- **Purpose**: Prevents DDoS attacks and resource abuse
- **Implementation**: In-memory storage (suitable for Vercel serverless)

### 4. CORS (Cross-Origin Resource Sharing)
- **Restricted Origins**: Only allows requests from configured domains
- **Configuration**: See `visualizer/config.py` to update allowed domains
- **Prevents**: Unauthorized cross-origin requests

### 5. Security Headers
- **X-Content-Type-Options**: `nosniff` - Prevents MIME type sniffing
- **X-Frame-Options**: `DENY` - Prevents clickjacking
- **X-XSS-Protection**: `1; mode=block` - Enables XSS filtering
- **Content-Security-Policy**: Restricts resource loading to trusted sources

### 6. Content Security Policy (CSP)
- **Script Sources**: Only allows scripts from your domain and jsdelivr CDN
- **Style Sources**: Only allows styles from your domain and Google Fonts
- **Font Sources**: Only allows fonts from your domain and Google Fonts
- **Prevents**: XSS attacks, code injection

### 7. Logging Security
- **Production Logging**: Only logs warnings and errors (not info/debug)
- **No Sensitive Data**: Error messages don't include sensitive system information

## Configuration

### Updating Your Domain
When you get a custom domain, update `visualizer/config.py`:

```python
ALLOWED_ORIGINS = [
    'https://ai-alignment.vercel.app',  # Your main Vercel domain
    'https://yourdomain.com',           # Add your custom domain here
    'http://localhost:3000',            # Local development
]
```

### Vercel Preview URLs
The configuration automatically handles Vercel's dynamic preview URLs using a regex pattern:

```python
VERCEL_PREVIEW_PATTERN = r'^https://ai-alignment-[a-z0-9]+-raphaes-projects-7d61857d\.vercel\.app$'
```

This allows preview deployments like:
- `https://ai-alignment-fuwg2x7h5-raphaes-projects-7d61857d.vercel.app`
- `https://ai-alignment-abc123xyz-raphaes-projects-7d61857d.vercel.app`

**Note**: If your Vercel project ID changes, update the pattern accordingly.

### Rate Limiting Settings
Adjust rate limiting in `visualizer/config.py`:

```python
RATE_LIMIT_WINDOW = 60          # Time window in seconds
RATE_LIMIT_MAX_REQUESTS = 100   # Max requests per window per IP
```

## What's NOT Implemented (Intentionally)

### Authentication
- **Why**: This is an art project meant to be publicly accessible
- **Alternative**: Rate limiting prevents abuse

### CSRF Protection
- **Why**: All endpoints are read-only (GET requests only)
- **No Risk**: No state-changing operations

### Database Security
- **Why**: No database - only static JSON files
- **No Risk**: No SQL injection or database vulnerabilities

## Vercel-Specific Considerations

### Serverless Environment
- **Rate Limiting**: Uses in-memory storage (resets on cold starts)
- **Logging**: Uses stdout (captured by Vercel)
- **File System**: Read-only except for /tmp (not used)

### CDN and Edge
- **Static Files**: Served by Vercel's CDN
- **Caching**: Automatic caching of static assets
- **HTTPS**: Automatic HTTPS termination

## Monitoring and Maintenance

### Regular Updates
1. **Dependencies**: Keep Flask and other dependencies updated
2. **CDN Integrity**: Monitor CDN resources for changes
3. **Domain Configuration**: Update allowed origins when domains change

### Security Headers Testing
Test your security headers at: https://securityheaders.com/

### CDN Dependencies
- **TWEEN.js**: Loaded from jsdelivr CDN without integrity checks (appropriate for art project)
- **Three.js**: Loaded via import maps from jsdelivr CDN

### CSP Testing
Test your Content Security Policy at: https://csp-evaluator.withgoogle.com/

## Emergency Response

If you detect suspicious activity:
1. **Check Vercel Analytics**: Monitor for unusual traffic patterns
2. **Update Rate Limits**: Temporarily reduce rate limits in config.py
3. **Block Origins**: Remove suspicious origins from ALLOWED_ORIGINS
4. **Redeploy**: Push changes to trigger immediate deployment 
