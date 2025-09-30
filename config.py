# config.py

import os

# ==============================
# General Application Settings
# ==============================

# The application's base URL for API requests.
# Default: 'http://localhost:8000'
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

# The port number on which the application will run.
# Default: 8000
PORT = int(os.getenv('PORT', 8000))

# ============================
# Database Configuration
# ============================

# Database connection string.
# Format: 'postgresql://user:password@host:port/database'
# Default: 'postgresql://user:password@localhost:5432/mydatabase'
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/mydatabase')

# ============================
# Security Settings
# ============================

# Secret key used for cryptographic operations.
# Default: 'your-secret-key'
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

# ============================
# Logging Configuration
# ============================

# Log level for the application.
# Options: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
# Default: 'INFO'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# ============================
# External API Keys
# ============================

# API key for accessing external services.
# Default: 'your-api-key'
EXTERNAL_API_KEY = os.getenv('EXTERNAL_API_KEY', 'your-api-key')

# ============================
# Feature Flags
# ============================

# Flag to enable or disable a specific feature.
# Default: False
FEATURE_X_ENABLED = bool(int(os.getenv('FEATURE_X_ENABLED', 0)))

# ============================
# Email Settings
# ============================

# Email address used for sending notifications.
# Default: 'no-reply@example.com'
EMAIL_FROM = os.getenv('EMAIL_FROM', 'no-reply@example.com')

# ============================
# Utility Functions
# ============================

def get_config():
    """
    Retrieves all configuration settings as a dictionary.

    Returns:
        dict: A dictionary containing all configuration settings.
    """
    return {
        'BASE_URL': BASE_URL,
        'PORT': PORT,
        'DATABASE_URL': DATABASE_URL,
        'SECRET_KEY': SECRET_KEY,
        'LOG_LEVEL': LOG_LEVEL,
        'EXTERNAL_API_KEY': EXTERNAL_API_KEY,
        'FEATURE_X_ENABLED': FEATURE_X_ENABLED,
        'EMAIL_FROM': EMAIL_FROM,
    }
