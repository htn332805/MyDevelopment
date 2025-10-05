# Getting Started with IAF0 Framework

## Quick Start

### 1. Context System Usage
```python
from orchestrator.context import Context

# Create context instance
ctx = Context()

# Store and retrieve data
ctx.set("app.name", "MyApp", who="setup")
app_name = ctx.get("app.name")

# Track changes
history = ctx.get_history()
```

### 2. Scriptlet Development
```python
from scriptlets import BaseScriptlet, register_scriptlet

@register_scriptlet
class DataProcessor(BaseScriptlet):
    def run(self, input_data=None):
        # Process data with context access
        config = self.context.get("processing.config", {})
        result = self.process_data(input_data, config)
        
        # Store results
        self.context.set("processing.result", result, who=self.name)
        return {"status": "success", "processed": len(result)}
```

### 3. Analysis Framework
```python
from src.analysis import EnhancedSummarizer, AnalysisConfig

# Configure analysis
config = AnalysisConfig(statistical_precision=4, debug_mode=True)

# Run analysis
summarizer = EnhancedSummarizer(config)
result = summarizer.analyze([1, 2, 3, 4, 5])
```

## Testing
```bash
pytest --disable-warnings -q
```

## Development Tools
```bash
# Format code
python -m black .

# Run compliance check
python tools/lint_checker.py

# Update documentation
python tools/documentation_updater.py
```
