# Framework0 Step Packager

## 📦 New Feature: Step Packager

The Framework0 Step Packager allows you to create portable, minimal packages of specific orchestrator steps with their dependencies. This solves the problem of sharing individual automation steps without requiring the entire workspace structure.

### Problem Solved

Previously, to share a specific step or automation command, you would need to:
- Share the entire Framework0 workspace (large and complex)
- Manually identify and copy all dependencies
- Create custom execution scripts
- Handle path and import issues in the target environment

### Solution

The Step Packager automatically:
- Analyzes dependencies for a specific step
- Creates minimal zip archives with only required files
- Generates portable execution wrappers
- Provides clear documentation and usage instructions

### Quick Start

```bash
# Interactive mode - browse and select steps
python tools/step_packager.py

# Command line mode - package specific steps  
python tools/step_packager.py --recipe orchestrator/recipes/example.yaml --step "step_name"

# Extract and run packages
unzip step_package.zip
cd extracted_folder
pip install pyyaml networkx
python run_packaged_step.py --debug
```

### Key Benefits

- **🚀 Minimal Size**: Only includes essential files (typically 10-50KB)
- **📦 Self-Contained**: Everything needed to run the step
- **🔄 Portable**: Runs on any system with Python
- **📋 Interactive**: User-friendly step selection interface
- **🐛 Debug-Ready**: Comprehensive logging and error handling
- **📚 Documented**: Auto-generated README with usage instructions

### Use Cases

1. **Sharing Automation Steps**: Send specific steps to team members or other systems
2. **Deployment Packages**: Create minimal deployments for production environments
3. **Testing Isolation**: Test individual steps in clean environments
4. **Training Materials**: Package example steps for documentation and training

### Example Workflow

1. **Create a Step Package**:
   ```bash
   python tools/step_packager.py
   # Select: test_compute.yaml -> check_prime
   # Output: check_prime_package.zip (12.6 KB)
   ```

2. **Share the Package**:
   ```bash
   # Email, copy, or upload the small zip file
   scp check_prime_package.zip user@remote:/tmp/
   ```

3. **Use on Target System**:
   ```bash
   cd /tmp && unzip check_prime_package.zip
   cd extracted_folder
   pip install pyyaml networkx
   python run_packaged_step.py --debug --only check_prime
   ```

### Generated Package Structure

```
package/
├── run_packaged_step.py      # Execution wrapper
├── README.md                 # Usage instructions  
├── orchestrator/             # Core framework
│   ├── __init__.py
│   ├── context.py
│   ├── runner.py
│   └── recipes/
│       └── recipe_file.yaml
└── scriptlets/               # Step implementation
    └── steps/
        └── step_module.py
```

For detailed documentation, see [docs/step_packager.md](docs/step_packager.md).