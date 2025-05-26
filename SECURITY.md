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