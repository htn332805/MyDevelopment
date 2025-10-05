# Framework0 Enterprise Deployment Guide

*Updated on 2025-01-05*

Comprehensive deployment guide for Framework0 enterprise automation platform, covering recipe orchestration, enhanced context server, recipe isolation, and production deployment scenarios.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Recipe Isolation Deployment](#recipe-isolation-deployment)
4. [Production Infrastructure](#production-infrastructure)
5. [Docker & Container Deployment](#docker--container-deployment)
6. [High Availability Setup](#high-availability-setup)
7. [Security & Monitoring](#security--monitoring)
8. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

- **Python:** 3.11.2 or higher
- **Memory:** 512MB RAM minimum, 1GB recommended
- **Storage:** 100MB for application, additional space for context dumps
- **Network:** Ports 8080 (HTTP) and 8081 (WebSocket) configurable

### Supported Platforms

- **Linux:** Ubuntu 20.04+, CentOS 8+, Debian 11+
- **macOS:** macOS 11+ (Big Sur and later)
- **Windows:** Windows 10/11 with WSL2 recommended

## Installation Methods

### Full Framework0 Installation

```bash
# Clone the Framework0 repository
git clone <framework0-repository-url>
cd MyDevelopment

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Framework0 dependencies
pip install -r requirements.txt

# Start Framework0 components
python server/enhanced_context_server.py &
python orchestrator/runner.py --daemon
```

### Minimal Recipe Installation

```bash
# For deploying isolated recipe packages
mkdir framework0_minimal
cd framework0_minimal

# Extract isolated recipe package
tar -xzf recipe_package.tar.gz

# Run isolated recipe
python run_recipe.py
```

## Recipe Isolation Deployment

### Creating Deployment Packages

Framework0's Recipe Isolation CLI enables creation of standalone deployment packages:

```bash
# Analyze recipe dependencies
python tools/recipe_isolation_cli.py analyze orchestrator/recipes/production_pipeline.yaml

# Create complete deployment package
python tools/recipe_isolation_cli.py create orchestrator/recipes/production_pipeline.yaml \
    --output /deploy/packages

# Validate deployment package
python tools/recipe_isolation_cli.py validate /deploy/packages/production_pipeline

# Create minimal deployment package
python tools/recipe_isolation_cli.py minimal orchestrator/recipes/production_pipeline.yaml \
    --target /deploy/minimal
```

### Package Structure

Generated deployment packages contain:

```
production_pipeline/
├── run_recipe.py              # Main execution script
├── package_manifest.json      # Package metadata
├── production_pipeline.yaml   # Recipe definition
├── orchestrator/              # Framework0 core
│   ├── runner.py
│   ├── context.py
│   └── ...
├── scriptlets/                # Required scriptlets
│   ├── framework/
│   ├── data_loaders/
│   └── ...
├── src/                       # Core Framework0 modules
│   ├── core/
│   ├── analysis/
│   └── ...
└── requirements.txt           # Dependencies
```

### Deployment Workflows

#### Production Deployment Script

```bash
#!/bin/bash
# Framework0 Production Deployment Script

set -e

RECIPE_NAME="$1"
ENVIRONMENT="$2"
DEPLOY_DIR="/opt/framework0"

if [ -z "$RECIPE_NAME" ] || [ -z "$ENVIRONMENT" ]; then
    echo "Usage: $0 <recipe_name> <environment>"
    exit 1
fi

echo "🚀 Starting Framework0 deployment: $RECIPE_NAME -> $ENVIRONMENT"

# 1. Create deployment package
echo "📦 Creating deployment package..."
python tools/recipe_isolation_cli.py workflow \
    "orchestrator/recipes/${RECIPE_NAME}.yaml" \
    --output "/tmp/deploy_packages"

PACKAGE_DIR="/tmp/deploy_packages/$RECIPE_NAME"

# 2. Validate package
echo "✅ Validating deployment package..."
if ! python tools/recipe_isolation_cli.py validate "$PACKAGE_DIR"; then
    echo "❌ Package validation failed"
    exit 1
fi

# 3. Transfer to production
echo "📂 Deploying to $ENVIRONMENT..."
sudo mkdir -p "$DEPLOY_DIR/$ENVIRONMENT"
sudo cp -r "$PACKAGE_DIR" "$DEPLOY_DIR/$ENVIRONMENT/"

# 4. Set permissions
sudo chown -R framework0:framework0 "$DEPLOY_DIR/$ENVIRONMENT/$RECIPE_NAME"
sudo chmod +x "$DEPLOY_DIR/$ENVIRONMENT/$RECIPE_NAME/run_recipe.py"

# 5. Create systemd service
cat <<EOF | sudo tee "/etc/systemd/system/framework0-${RECIPE_NAME}-${ENVIRONMENT}.service"
[Unit]
Description=Framework0 Recipe: $RECIPE_NAME ($ENVIRONMENT)
After=network.target

[Service]
Type=simple
User=framework0
Group=framework0
WorkingDirectory=$DEPLOY_DIR/$ENVIRONMENT/$RECIPE_NAME
ExecStart=/usr/bin/python3 run_recipe.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 6. Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable "framework0-${RECIPE_NAME}-${ENVIRONMENT}"
sudo systemctl start "framework0-${RECIPE_NAME}-${ENVIRONMENT}"

echo "✅ Framework0 deployment completed successfully"
echo "📊 Service status: $(sudo systemctl is-active framework0-${RECIPE_NAME}-${ENVIRONMENT})"
```

#### Blue-Green Deployment

```bash
#!/bin/bash
# Blue-Green deployment for Framework0 recipes

RECIPE_NAME="$1"
NEW_VERSION="$2"

BLUE_DIR="/opt/framework0/blue/$RECIPE_NAME"
GREEN_DIR="/opt/framework0/green/$RECIPE_NAME" 
CURRENT_LINK="/opt/framework0/current/$RECIPE_NAME"

# Determine current and new environments
if [ -L "$CURRENT_LINK" ]; then
    CURRENT_TARGET=$(readlink "$CURRENT_LINK")
    if [[ "$CURRENT_TARGET" == *"blue"* ]]; then
        DEPLOY_TARGET="$GREEN_DIR"
        NEW_ENV="green"
    else
        DEPLOY_TARGET="$BLUE_DIR" 
        NEW_ENV="blue"
    fi
else
    DEPLOY_TARGET="$BLUE_DIR"
    NEW_ENV="blue"
fi

echo "🔄 Blue-Green deployment: $RECIPE_NAME v$NEW_VERSION -> $NEW_ENV"

# 1. Deploy to inactive environment
mkdir -p "$DEPLOY_TARGET"
python tools/recipe_isolation_cli.py create \
    "orchestrator/recipes/$RECIPE_NAME.yaml" \
    --output "$DEPLOY_TARGET"

# 2. Health check on new deployment
cd "$DEPLOY_TARGET"
if python run_recipe.py --health-check; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed - aborting deployment"
    exit 1
fi

# 3. Switch traffic to new environment
ln -sfn "$DEPLOY_TARGET" "$CURRENT_LINK"
echo "🔄 Traffic switched to $NEW_ENV environment"

# 4. Restart services
sudo systemctl restart "framework0-${RECIPE_NAME}"

echo "✅ Blue-Green deployment completed"
```

### Configuration Options

#### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CONTEXT_HOST` | `127.0.0.1` | Server bind address |
| `CONTEXT_PORT` | `8080` | HTTP server port |
| `CONTEXT_DEBUG` | `false` | Enable debug logging |
| `DUMP_DIRECTORY` | `./dumps` | Directory for context dumps |
| `MAX_HISTORY` | `1000` | Maximum history entries |

## Docker Deployment

### Using Docker Compose

```yaml
version: '3.8'
services:
  context-server:
    build: .
    ports:
      - "8080:8080"
    environment:
      - CONTEXT_HOST=0.0.0.0
      - CONTEXT_DEBUG=false
    volumes:
      - ./dumps:/app/dumps
```

## Production Deployment

### Security Considerations

- Use HTTPS in production with proper SSL certificates
- Configure firewall rules to restrict access to necessary ports
- Implement authentication for sensitive deployments
- Regularly backup context data and dumps

### Performance Optimization

- Use a reverse proxy (nginx/Apache) for static content
- Configure appropriate logging levels for production
- Monitor memory usage and configure limits
- Implement log rotation for long-running deployments

