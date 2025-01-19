# Deployment Documentation

## Environment Overview
- **Server**: Ubuntu 24
- **Web Server**: Apache2
- **Working Directory**: `/home/ubuntu/gilzero.dev/EditorDocAIAgentV1`
- **Python Version**: 3.12 (virtual environment)
- **Domain**: agenteditor.dreamer.xyz

## Key Configuration Files

### Apache Virtual Host
Location: `/etc/apache2/sites-available/agenteditor.dreamer.xyz.conf`

This file configures:
- Domain routing
- SSL settings
- WSGI configuration
- Directory permissions
- UTF-8 encoding settings

### WSGI Bridge
Location: `/home/ubuntu/gilzero.dev/EditorDocAIAgentV1/wsgi.py`

Acts as the interface between Apache and Flask:
- Loads environment variables
- Sets up Python path
- Imports Flask application
- Handles encoding settings

### Environment Variables
Location: `.env`
- Contains application configuration
- API keys and secrets
- Database settings

## Directory Structure and Permissions

### Critical Directories:
```bash
/home/ubuntu/gilzero.dev/EditorDocAIAgentV1/
├── uploads/    # File uploads (775, www-data:www-data)
├── instance/   # Instance data (775, www-data:www-data)
└── debug/      # Debug logs (775, www-data:www-data)
```

### Permission Commands:
```bash
sudo chmod -R 775 uploads instance debug
sudo chown -R www-data:www-data uploads instance debug
```

## Auto-start Configuration
The application automatically starts with Apache:
1. Apache starts on system boot (enabled via systemd)
2. mod_wsgi loads with Apache
3. WSGI loads Flask application

### Verification Commands:
```bash
# Check Apache status
sudo systemctl status apache2

# Check if enabled on boot
sudo systemctl is-enabled apache2
```

## Request Flow
```
Client Request
    ↓
Apache (HTTP/HTTPS handling)
    ↓
mod_wsgi (WSGI implementation)
    ↓
wsgi.py (WSGI entry point)
    ↓
Flask Application
    ↓
Response
```

## Common Commands

### Apache Control:
```bash
# Start Apache
sudo systemctl start apache2

# Stop Apache
sudo systemctl stop apache2

# Restart Apache
sudo systemctl restart apache2

# Check Status
sudo systemctl status apache2
```

### Log Monitoring:
```bash
# Error logs
sudo tail -f /var/log/apache2/agenteditor_dreamer_xyz_ssl_error.log

# Access logs
sudo tail -f /var/log/apache2/agenteditor_dreamer_xyz_ssl_access.log
```

### Configuration Testing:
```bash
# Test Apache configuration
sudo apache2ctl configtest
```

## Troubleshooting

### Common Issues:
1. **File Upload Errors**
   - Check directory permissions
   - Verify uploads directory exists
   - Check file size limits

2. **Apache Not Starting**
   - Check configuration syntax
   - Review error logs
   - Verify port availability

3. **WSGI Issues**
   - Check Python path
   - Verify virtual environment
   - Review wsgi.py configuration

### Debug Steps:
1. Check Apache logs
2. Verify file permissions
3. Test Apache configuration
4. Check environment variables
5. Verify Python dependencies

## Security Considerations

### SSL Configuration:
- Using wildcard certificate
- SSL certificates location: `/etc/apache2/ssl/dreamer_xyz/`
- Automatic HTTP to HTTPS redirection

### File Permissions:
- Restricted directory access
- Proper ownership settings
- Limited execution permissions

### Headers:
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Strict-Transport-Security
