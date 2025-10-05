# Exercise 1: Hello Framework0 - Your First Recipe

**Duration:** 30-45 minutes  
**Difficulty:** Beginner  
**Prerequisites:** Framework0 environment setup  

## 🎯 Learning Objectives

By the end of this exercise, you will:

- Understand basic Framework0 recipe structure
- Create your first working recipe from scratch
- Learn YAML recipe syntax and metadata
- Execute recipes using the Framework0 orchestrator
- Understand the Context system basics
- Build a reusable "Hello World" scriptlet

## 📚 Concepts Introduction

### What is a Framework0 Recipe?

A **recipe** in Framework0 is a YAML file that defines an automation workflow. Think of it as a cooking recipe - it has:

- **Metadata**: Information about the recipe (name, version, description)
- **Steps**: Sequential or parallel tasks to execute
- **Dependencies**: Order of execution between steps
- **Context**: Shared data between steps

### Basic Recipe Structure

```yaml
metadata:
  name: "recipe_name"
  version: "1.0"
  description: "What this recipe does"
  
steps:
  - name: "step_name"
    idx: 1
    type: "python"
    module: "scriptlets.category"
    function: "ScriptletName"
    args:
      parameter1: "value1"
      parameter2: "value2"
```

## 🛠️ Exercise Steps

### Step 1: Create Your First Recipe

Let's create a simple "Hello Framework0" recipe that demonstrates basic concepts.

**📁 Create:** `FYI/exercises/hello_framework0.yaml`

```yaml
metadata:
  name: "hello_framework0"
  version: "1.0"
  description: "My first Framework0 recipe - Hello World introduction"
  author: "Your Name"
  tags: ["beginner", "tutorial", "hello-world"]
  created_date: "2025-01-05"

steps:
  - name: "welcome_message"
    idx: 1
    type: "python"
    module: "scriptlets.tutorial"
    function: "HelloWorldScriptlet"
    args:
      message: "Hello Framework0! This is my first recipe."
      user_name: "Student Developer"
      show_timestamp: true
      
  - name: "system_info"
    idx: 2
    type: "python"
    module: "scriptlets.tutorial"
    function: "SystemInfoScriptlet"
    depends_on: ["welcome_message"]
    args:
      show_python_version: true
      show_platform: true
      show_framework_version: true
```

### Step 2: Create the Hello World Scriptlet

Now we need to create the scriptlet that our recipe will use. This demonstrates Framework0's modular architecture.

**📁 Create:** `scriptlets/tutorial/__init__.py`

```python
# Tutorial scriptlets for Framework0 learning exercises
```

**📁 Create:** `scriptlets/tutorial/hello_world_scriptlet.py`

```python
"""
Framework0 Tutorial - Hello World Scriptlet

This scriptlet demonstrates basic Framework0 patterns:
- Inheriting from BaseScriptlet
- Using Context for data storage
- Proper logging and error handling
- Type hints and documentation
"""

from scriptlets.framework import BaseScriptlet, register_scriptlet
from orchestrator.context import Context
from typing import Dict, Any
from src.core.logger import get_logger
import os
import platform
import sys
from datetime import datetime

logger = get_logger(__name__, debug=os.getenv("DEBUG") == "1")

@register_scriptlet
class HelloWorldScriptlet(BaseScriptlet):
    """
    A simple Hello World scriptlet for Framework0 introduction.
    
    This scriptlet demonstrates:
    - Basic scriptlet structure and registration
    - Context usage for data storage
    - Parameter handling from recipes
    - Logging best practices
    """
    
    def __init__(self) -> None:
        """Initialize the Hello World scriptlet."""
        super().__init__()
        self.name = "hello_world"
        self.version = "1.0"
        self.description = "Framework0 Hello World demonstration"
        
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the Hello World functionality.
        
        Args:
            context: Framework0 context for data sharing
            params: Parameters from the recipe
            
        Returns:
            Dict containing execution results
        """
        try:
            logger.info(f"Starting {self.name} execution")
            
            # Extract parameters with defaults
            message = params.get("message", "Hello Framework0!")
            user_name = params.get("user_name", "Framework0 User")
            show_timestamp = params.get("show_timestamp", False)
            
            # Create welcome message
            welcome_text = f"🚀 {message}"
            if user_name:
                welcome_text += f" Welcome, {user_name}!"
            
            # Add timestamp if requested
            if show_timestamp:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                welcome_text += f" (Executed at: {timestamp})"
            
            # Display the message
            print("\n" + "=" * 60)
            print(welcome_text)
            print("=" * 60 + "\n")
            
            # Store results in context for other steps to use
            context.set("welcome.message", welcome_text, who=self.name)
            context.set("welcome.user", user_name, who=self.name)
            context.set("welcome.executed_at", datetime.now().isoformat(), who=self.name)
            
            # Log successful execution
            logger.info(f"✅ {self.name} completed successfully")
            
            return {
                "status": "success",
                "message": welcome_text,
                "user": user_name,
                "timestamp_shown": show_timestamp,
                "execution_time": self.get_execution_time()
            }
            
        except Exception as e:
            logger.error(f"❌ {self.name} execution failed: {e}")
            context.set(f"{self.name}.error", str(e), who=self.name)
            raise

@register_scriptlet
class SystemInfoScriptlet(BaseScriptlet):
    """
    System Information scriptlet for tutorial purposes.
    
    Demonstrates:
    - Dependency on previous steps (via depends_on)
    - Accessing context data from previous steps
    - System information gathering
    """
    
    def __init__(self) -> None:
        """Initialize the System Info scriptlet."""
        super().__init__()
        self.name = "system_info"
        self.version = "1.0"
        self.description = "Display system information for Framework0"
        
    def run(self, context: Context, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute system information gathering.
        
        Args:
            context: Framework0 context for data sharing
            params: Parameters from the recipe
            
        Returns:
            Dict containing system information
        """
        try:
            logger.info(f"Starting {self.name} execution")
            
            # Get parameters
            show_python = params.get("show_python_version", True)
            show_platform = params.get("show_platform", True)
            show_framework = params.get("show_framework_version", True)
            
            # Get previous step data from context
            welcome_user = context.get("welcome.user", "Unknown User")
            
            print(f"📊 System Information for {welcome_user}:")
            print("-" * 50)
            
            system_info = {}
            
            # Gather system information
            if show_python:
                python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
                system_info["python_version"] = python_version
                print(f"🐍 Python Version: {python_version}")
            
            if show_platform:
                platform_info = f"{platform.system()} {platform.release()}"
                system_info["platform"] = platform_info
                print(f"💻 Platform: {platform_info}")
                
            if show_framework:
                # For now, we'll use a placeholder version
                framework_version = "2.0.0-enhanced"
                system_info["framework_version"] = framework_version
                print(f"⚡ Framework0 Version: {framework_version}")
            
            print("-" * 50)
            
            # Store results in context
            context.set("system.info", system_info, who=self.name)
            context.set("system.gathered_at", datetime.now().isoformat(), who=self.name)
            
            logger.info(f"✅ {self.name} completed successfully")
            
            return {
                "status": "success",
                "system_info": system_info,
                "user": welcome_user,
                "execution_time": self.get_execution_time()
            }
            
        except Exception as e:
            logger.error(f"❌ {self.name} execution failed: {e}")
            context.set(f"{self.name}.error", str(e), who=self.name)
            raise
```

### Step 3: Test Your Recipe

Now let's execute your first Framework0 recipe!

**🚀 Execute the recipe:**

```bash
# Navigate to Framework0 directory
cd /home/hai/hai_vscode/MyDevelopment

# Activate Python environment
source ~/pyvenv/bin/activate

# Execute your recipe
python orchestrator/runner.py --recipe FYI/exercises/hello_framework0.yaml --debug
```

**Expected Output:**
```
🚀 Starting recipe execution: hello_framework0
📋 Recipe loaded successfully
⚡ Executing step 1: welcome_message
============================================================
🚀 Hello Framework0! This is my first recipe. Welcome, Student Developer! (Executed at: 2025-01-05 10:30:45)
============================================================

✅ Step welcome_message completed successfully
⚡ Executing step 2: system_info (depends on: welcome_message)
📊 System Information for Student Developer:
--------------------------------------------------
🐍 Python Version: 3.11.2
💻 Platform: Linux 5.15.0
⚡ Framework0 Version: 2.0.0-enhanced
--------------------------------------------------
✅ Step system_info completed successfully
🎉 Recipe execution completed successfully!
```

### Step 4: Understanding What Happened

Let's break down what your recipe accomplished:

1. **Recipe Loading**: Framework0 parsed your YAML file and validated the structure
2. **Step Execution**: Executed steps in order, respecting dependencies
3. **Context Usage**: Data flowed between steps via the Context system
4. **Scriptlet Registration**: Your custom scriptlets were automatically discovered
5. **Error Handling**: Built-in logging and error management

## ✅ Checkpoint Questions

Before proceeding, please answer these questions to confirm your understanding:

**Question 1:** What would happen if you removed the `depends_on: ["welcome_message"]` from the `system_info` step?

**Question 2:** How could you modify the recipe to show a different welcome message?

**Question 3:** What data is stored in the Context after this recipe runs?

**Question 4:** How would you add a third step that uses data from both previous steps?

## 🎯 Challenge: Enhance Your Recipe

Try these enhancements to solidify your learning:

### Challenge A: Add Recipe Metadata Display
Create a third step that displays the recipe's own metadata (name, version, author).

### Challenge B: Add User Input
Modify the recipe to accept a command-line parameter for the user name.

### Challenge C: Add Conditional Logic
Add a step that only runs if certain conditions are met (e.g., specific platform).

## 📁 Exercise Deliverable

**Reusable Component Created:** `scriptlets/tutorial/hello_world_scriptlet.py`

This scriptlet can be used in future recipes as a template for:
- Basic scriptlet structure
- Context usage patterns
- Parameter handling
- Logging best practices

**Recipe Template Created:** `FYI/exercises/hello_framework0.yaml`

This recipe serves as a template for:
- Basic recipe structure
- Step dependencies
- Metadata best practices
- Parameter passing

## 🚀 What's Next?

In **Exercise 2**, you'll learn:
- Advanced Context operations
- Data processing with variables
- Working with external data sources
- Parameter validation and error handling

## 📝 Exercise Completion Checklist

- [ ] Created `hello_framework0.yaml` recipe
- [ ] Created `HelloWorldScriptlet` and `SystemInfoScriptlet`
- [ ] Successfully executed the recipe
- [ ] Observed output and understood the flow
- [ ] Answered checkpoint questions
- [ ] Attempted at least one challenge

**Ready to continue?** 
✅ **Signal your completion and any questions you have before we proceed to Exercise 2!**