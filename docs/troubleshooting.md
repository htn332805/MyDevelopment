# Framework0 Enhanced Context Server - Troubleshooting Guide

*Generated on 2025-10-05 18:53:51 UTC*

Common issues, solutions, and frequently asked questions.

## Connection Issues

### Server Won't Start

**Problem:** Context server fails to start with port binding error.

**Solutions:**
1. Check if another process is using the port:
   ```bash
   lsof -i :8080  # Linux/macOS
   netstat -ano | findstr :8080  # Windows
   ```

2. Use a different port:
   ```bash
   export CONTEXT_PORT=8090
   python server/enhanced_context_server.py
   ```

### Client Connection Refused

**Problem:** Client cannot connect to context server.

**Solutions:**
1. Verify server is running:
   ```bash
   curl http://127.0.0.1:8080/ctx/status
   ```

2. Check firewall settings and network connectivity
3. Verify host and port configuration match

## Performance Issues

### High Memory Usage

**Problem:** Server memory usage grows over time.

**Solutions:**
1. Limit history size:
   ```bash
   export MAX_HISTORY=500
   ```

2. Regular context dumps and cleanup:
   ```bash
   ./tools/context.sh dump --dump-format json --filename cleanup_backup
   # Clear old history after backup
   ```

### Slow Response Times

**Problem:** Server responses are slow under load.

**Solutions:**
1. Enable performance monitoring:
   ```bash
   export CONTEXT_DEBUG=true
   ```

2. Optimize context key structure (avoid deeply nested keys)
3. Use batch operations when possible

## File Dumping Issues

### Dump Directory Permission Error

**Problem:** Cannot create dump files due to permissions.

**Solutions:**
1. Check directory permissions:
   ```bash
   ls -la dumps/
   chmod 755 dumps/  # If needed
   ```

2. Use a different dump directory:
   ```bash
   export DUMP_DIRECTORY=/tmp/context_dumps
   mkdir -p /tmp/context_dumps
   ```

### Invalid Dump Format Error

**Problem:** Dump request fails with format error.

**Solutions:**
1. Use supported formats: `json`, `csv`, `txt`, `pretty`
2. Check format parameter spelling and case

## Client Integration Issues

### Python Import Errors

**Problem:** Cannot import context client modules.

**Solutions:**
1. Verify Python path includes project directory:
   ```python
   import sys
   sys.path.append('/path/to/MyDevelopment')
   from src.context_client import ContextClient
   ```

2. Install required dependencies:
   ```bash
   pip install requests aiohttp
   ```

### Shell Script Permission Error

**Problem:** Shell script context.sh not executable.

**Solutions:**
1. Make script executable:
   ```bash
   chmod +x tools/context.sh
   ```

2. Use bash directly if needed:
   ```bash
   bash tools/context.sh get status
   ```

## Debugging and Logging

### Enable Debug Mode

```bash
# Server debug mode
export CONTEXT_DEBUG=true
python server/enhanced_context_server.py

# Client debug mode
export DEBUG=1
./tools/context.sh get status
```

### Log Analysis

Common log patterns and their meanings:

- `Connection refused`: Server not running or port blocked
- `Timeout error`: Network latency or server overload
- `Permission denied`: File system or directory access issues
- `Invalid JSON`: Request format or parsing errors

## Frequently Asked Questions

### Q: Can I run multiple context servers?

**A:** Yes, use different ports for each instance:
```bash
CONTEXT_PORT=8080 python server/enhanced_context_server.py &
CONTEXT_PORT=8081 python server/enhanced_context_server.py &
```

### Q: How do I backup context data?

**A:** Use regular dumps with different formats:
```bash
./tools/context.sh dump --dump-format json --filename daily_backup_$(date +%Y%m%d)
```

### Q: Is the context server thread-safe?

**A:** Yes, the server uses proper locking for concurrent access. Multiple clients can safely access the context simultaneously.

### Q: What's the maximum context size?

**A:** No hard limits, but consider memory usage. Monitor with debug mode and use regular dumps to manage size.

