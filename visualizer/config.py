# Security Configuration for AI Alignment Visualizer

# Your domain configuration - update this when you get your custom domain
ALLOWED_ORIGINS = [
    'https://ai-alignment.vercel.app',  # Your main Vercel domain
    'http://localhost:3000',            # Local development
    'http://127.0.0.1:3000',           # Local development alternative
    # Add your custom domain here when you get one:
    # 'https://yourdomain.com',
]

# Vercel preview URL pattern - matches dynamic preview deployments
VERCEL_PREVIEW_PATTERN = r'^https://ai-alignment-[a-z0-9]+-raphaes-projects-7d61857d\.vercel\.app$'

# Rate limiting settings (per IP address)
RATE_LIMIT_WINDOW = 60          # Time window in seconds (1 minute)
RATE_LIMIT_MAX_REQUESTS = 100   # Max requests per window per IP

# Security headers
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
}

# Content Security Policy
CSP_POLICY = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://vercel.live; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "connect-src 'self' https://vercel.live wss://vercel.live; "
    "img-src 'self' data:; "
    "media-src 'self'; "
    "frame-ancestors 'none';"
)

# Audio Configuration
AUDIO_CONFIG = {
    # Sound files for interaction feedback
    'hover_sound': '/static/sounds/hover.mp3',      # Sound when hovering over nodes
    'click_sound': '/static/sounds/click.mp3',      # Sound when clicking nodes
    'background_sound': '/static/sounds/background.mp3',  # Background music (loops continuously)
    
    # Audio settings
    'volume': 1.0,                                  # Master volume (0.0 to 1.0)
    'background_volume': 1.0,                      # Background music volume (usually lower)
    'enabled_by_default': True,                     # Whether sound is enabled on page load
    
    # Individual sound control
    'hover_sounds_enabled': False,                   # Enable/disable hover sounds globally
    'click_sounds_enabled': True,                   # Enable/disable click sounds globally
    'background_music_enabled': True,               # Enable/disable background music globally
    
    # Fallback to generated sounds if files don't exist
    'fallback_to_generated': True,                  # Use Web Audio API if files fail to load
} 