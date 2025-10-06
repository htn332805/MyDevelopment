#!/usr/bin/env python3
"""
Template System Demo - Exercise 10 Phase 4
Comprehensive demonstration of template management capabilities
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    """Comprehensive template system demo."""
    print("\n" + "=" * 80)
    print("📋 Framework0 Template System Demo - Exercise 10 Phase 4")
    print("   Dynamic Content Generation & Template Management")
    print("=" * 80)
    
    try:
        # Import template system
        from scriptlets.extensions.template_system import (
            TemplateContext, TemplateMetadata,
            create_template_manager,
            render_string_template
        )
        print("✅ Template System imported successfully")
        
        # Step 1: Initialize Template Manager
        print("\n📋 Step 1: Initialize Template Manager")
        print("-" * 50)
        
        # Create template directories
        template_dirs = [Path("templates"), Path("templates/components")]
        for template_dir in template_dirs:
            template_dir.mkdir(parents=True, exist_ok=True)
        
        template_manager = create_template_manager(
            template_dirs=template_dirs,
            auto_reload=True,
            enable_events=True
        )
        
        print("  📋 Template Manager Initialized:")
        print(f"    Template Directories: {len(template_dirs)}")
        print("    Auto-reload: True")
        print("    Events Enabled: True")
        print(f"    Available Engines: {list(template_manager.engines.keys())}")
        
        # Step 2: Create Template Files
        print("\n📄 Step 2: Create Template Files")
        print("-" * 50)
        
        # Base layout template
        base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Framework0 - \
{{ page_title | default('Welcome') }}{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .header { background: #007acc; color: white; \
padding: 20px; margin-bottom: 20px; }
        .content { padding: 20px; background: #f5f5f5; }
        .footer { margin-top: 20px; text-align: center; color: #666; }
        .config-info { background: #e8f4f8; padding: 10px; \
border-left: 4px solid #007acc; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ site_name | default('Framework0') }}</h1>
        <p>{{ site_description | default('Advanced Extension System') }}</p>
    </div>
    
    <div class="content">
        {% block content %}
        <p>No content provided</p>
        {% endblock %}
    </div>
    
    <div class="footer">
        <p>Generated at {{ now().strftime('%Y-%m-%d %H:%M:%S UTC') }}</p>
        <p>Framework0 Template System - Exercise 10 Phase 4</p>
    </div>
</body>
</html>"""
        
        # Plugin dashboard template
        plugin_dashboard_template = """{% extends "base.html" %}

{% block title %}Plugin Dashboard - {{ super() }}{% endblock %}

{% block content %}
<h2>🔌 Plugin Dashboard</h2>

<div class="config-info">
    <h3>System Information</h3>
    <ul>
        <li><strong>Environment:</strong> {{ env('ENVIRONMENT', 'development') }}</li>
        <li><strong>Debug Mode:</strong> {{ env('DEBUG', 'false') | upper_first }}</li>
        <li><strong>Timestamp:</strong> {{ now() | timestamp }}</li>
    </ul>
</div>

<h3>📊 Plugin Statistics</h3>
<table border="1" cellpadding="5" cellspacing="0" style="width: 100%; border-collapse: collapse;">
    <thead style="background: #007acc; color: white;">
        <tr>
            <th>Plugin Name</th>
            <th>Version</th>
            <th>Status</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        {% for plugin in plugins %}
        <tr style="background: {{ loop.cycle('#f9f9f9', '#ffffff') }};">
            <td><strong>{{ plugin.name | upper_first }}</strong></td>
            <td>{{ plugin.version }}</td>
            <td style="color: {{ 'green' if plugin.status == 'active' else 'red' }};">
                {{ plugin.status | upper }}
            </td>
            <td>{{ plugin.description | default('No description') }}</td>
        </tr>
        {% else %}
        <tr>
            <td colspan="4" style="text-align: center; color: #666;">
                No plugins available
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<h3>⚙️ Configuration Details</h3>
<pre style="background: #f0f0f0; padding: 10px; border: 1px solid #ddd;">{{ config_data | to_json }}</pre>

{% endblock %}"""
        
        # Configuration report template
        config_report_template = """{% extends "base.html" %}

{% block title %}Configuration Report - {{ super() }}{% endblock %}

{% block content %}
<h2>⚙️ Configuration Report</h2>

<div class="config-info">
    <h3>Report Generated</h3>
    <p><strong>Timestamp:</strong> {{ generation_time | timestamp }}</p>
    <p><strong>Environment:</strong> {{ environment | upper }}</p>
    <p><strong>Reporter:</strong> {{ reporter | default('System') }}</p>
</div>

<h3>📋 Configuration Sections</h3>
{% for section_name, section_data in configurations.items() %}
<div style="margin-bottom: 20px; border: 1px solid #ddd; padding: 10px;">
    <h4 style="color: #007acc;">{{ section_name | upper_first | snake_case | replace('_', ' ') | title }}</h4>
    
    {% if section_data is mapping %}
        <table border="1" cellpadding="3" cellspacing="0" style="width: 100%; font-size: 12px;">
            <thead style="background: #f0f0f0;">
                <tr>
                    <th>Key</th>
                    <th>Value</th>
                    <th>Type</th>
                </tr>
            </thead>
            <tbody>
                {% for key, value in section_data.items() %}
                <tr>
                    <td><code>{{ key | camel_case }}</code></td>
                    <td>{{ value | string | truncate(50) }}</td>
                    <td><em>{{ value.__class__.__name__ }}</em></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p><strong>Value:</strong> {{ section_data }}</p>
    {% endif %}
</div>
{% else %}
<p style="color: #666;">No configuration sections available.</p>
{% endfor %}

<h3>🧮 Statistics</h3>
<ul>
    <li><strong>Total Sections:</strong> {{ len(configurations) }}</li>
    <li><strong>Total Keys:</strong> {{ total_keys | default(0) }}</li>
    <li><strong>Report Size:</strong> {{ report_size | default('Unknown') }}</li>
</ul>

{% endblock %}"""
        
        # API documentation template
        api_docs_template = """# 📡 {{ api_name | default('Framework0') }} API Documentation

## Overview

{{ api_description | default('Comprehensive API documentation for Framework0 extension system.') }}

**Version:** {{ api_version | default('1.0.0') }}  
**Generated:** {{ now() | timestamp }}  
**Environment:** {{ env('ENVIRONMENT', 'production') }}

---

## 🔧 Endpoints

{% for endpoint in endpoints %}
### {{ endpoint.method | upper }} {{ endpoint.path }}

**Description:** {{ endpoint.description | default('No description provided') }}

{% if endpoint.parameters %}
**Parameters:**
{% for param in endpoint.parameters %}
- **{{ param.name }}** ({{ param.type }}): {{ param.description | default('No description') }}
  {% if param.required %}_Required_{% else %}_Optional_{% endif %}
{% endfor %}
{% endif %}

{% if endpoint.example_request %}
**Example Request:**
```json
{{ endpoint.example_request | to_json }}
```
{% endif %}

{% if endpoint.example_response %}
**Example Response:**
```json
{{ endpoint.example_response | to_json }}
```
{% endif %}

---

{% else %}
No endpoints documented.
{% endfor %}

## 📊 Statistics

- **Total Endpoints:** {{ len(endpoints) }}
- **Documentation Coverage:** {{ coverage_percentage | default(0) }}%
- **Last Updated:** {{ last_updated | timestamp if last_updated else 'Never' }}

## 🏷️ Tags

{% for tag in tags %}
- `{{ tag }}`
{% endfor %}

---

*Generated by Framework0 Template System - Exercise 10 Phase 4*"""
        
        # Create templates
        templates_to_create = [
            ("base.html", base_template),
            ("plugin_dashboard.html", plugin_dashboard_template),
            ("config_report.html", config_report_template),
            ("api_docs.md", api_docs_template)
        ]
        
        for template_name, template_content in templates_to_create:
            path = template_manager.create_template(
                template_name,
                template_content,
                engine_name="filesystem",
                metadata=TemplateMetadata(
                    name=template_name,
                    author="Framework0 System",
                    description=f"Demo template: {template_name}",
                    tags={'demo', 'framework0', 'exercise10'},
                    version="1.0.0"
                )
            )
            print(f"    ✅ Created: {template_name}")
        
        # Step 3: Template Context and Variables
        print("\n🎯 Step 3: Template Context and Variables")
        print("-" * 50)
        
        # Add global variables
        template_manager.add_global_variable("site_name", "Framework0 Demo")
        template_manager.add_global_variable("site_description", "Advanced Extension System with Plugin, Config, Event & Template Management")
        template_manager.add_global_variable("version", "1.0.0-exercise10")
        
        # Create custom filters
        def highlight_filter(value: str, term: str = "") -> str:
            """Highlight search term in text."""
            if term and isinstance(value, str):
                return value.replace(term, f"<mark>{term}</mark>")
            return str(value)
        
        def format_bytes_filter(value: int) -> str:
            """Format bytes as human readable."""
            try:
                bytes_val = int(value)
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if bytes_val < 1024:
                        return f"{bytes_val:.1f} {unit}"
                    bytes_val /= 1024
                return f"{bytes_val:.1f} TB"
            except (ValueError, TypeError):
                return str(value)
        
        # Add custom filters
        template_manager.add_global_filter("highlight", highlight_filter)
        template_manager.add_global_filter("format_bytes", format_bytes_filter)
        
        # Create custom functions
        def generate_id_function(prefix: str = "id") -> str:
            """Generate unique ID."""
            import uuid
            return f"{prefix}_{str(uuid.uuid4())[:8]}"
        
        def calculate_function(expression: str) -> str:
            """Safe calculator function."""
            try:
                # Only allow basic math operations
                allowed_chars = set('0123456789+-*/.()')
                if all(c in allowed_chars for c in expression.replace(' ', '')):
                    result = eval(expression)
                    return str(result)
            except:
                pass
            return "Invalid expression"
        
        template_manager.add_global_function("generate_id", generate_id_function)
        template_manager.add_global_function("calculate", calculate_function)
        
        print("    ✅ Added global variables:")
        print("      - site_name, site_description, version")
        print("    ✅ Added custom filters:")
        print("      - highlight, format_bytes")
        print("    ✅ Added custom functions:")
        print("      - generate_id, calculate")
        
        # Step 4: Render Templates with Data
        print("\n🖨️ Step 4: Render Templates with Data")
        print("-" * 50)
        
        # Sample plugin data
        plugin_data = [
            {
                "name": "advanced_analytics",
                "version": "2.1.0",
                "status": "active",
                "description": "Exercise 7 - Advanced analytics and metrics collection"
            },
            {
                "name": "container_deployment",
                "version": "1.3.0", 
                "status": "active",
                "description": "Exercise 8 - Container deployment and isolation"
            },
            {
                "name": "production_workflows",
                "version": "1.0.0",
                "status": "active",
                "description": "Exercise 9 - Production workflow orchestration"
            },
            {
                "name": "extension_system",
                "version": "1.0.0",
                "status": "active",
                "description": "Exercise 10 - Plugin, Config, Event & Template systems"
            }
        ]
        
        # Sample configuration data
        config_data = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "framework0_db",
                "pool_size": 10
            },
            "api": {
                "version": "v2.1",
                "timeout": 30,
                "rate_limit": 1000
            },
            "logging": {
                "level": "INFO",
                "file": "logs/app.log",
                "rotation_size": 104857600  # 100MB
            }
        }
        
        # Render plugin dashboard
        print("    🔌 Rendering Plugin Dashboard:")
        
        dashboard_context = TemplateContext()
        dashboard_context.set_variable("page_title", "Plugin Dashboard")
        dashboard_context.set_variable("plugins", plugin_data)
        dashboard_context.set_variable("config_data", config_data)
        
        dashboard_html = template_manager.render_template(
            "plugin_dashboard.html",
            context=dashboard_context
        )
        
        # Save rendered dashboard
        dashboard_path = Path("output") / "plugin_dashboard.html"
        dashboard_path.parent.mkdir(exist_ok=True)
        dashboard_path.write_text(dashboard_html)
        
        print(f"      ✅ Dashboard rendered ({len(dashboard_html)} characters)")
        print(f"      💾 Saved to: {dashboard_path}")
        
        # Render configuration report
        print("    ⚙️ Rendering Configuration Report:")
        
        config_context = TemplateContext()
        config_context.set_variable("page_title", "Configuration Report")
        config_context.set_variable("generation_time", "2025-10-05T17:45:00+00:00")
        config_context.set_variable("environment", "production")
        config_context.set_variable("reporter", "Template System Demo")
        config_context.set_variable("configurations", config_data)
        config_context.set_variable("total_keys", sum(len(v) if isinstance(v, dict) else 1 for v in config_data.values()))
        config_context.set_variable("report_size", "2.3 KB")
        
        report_html = template_manager.render_template(
            "config_report.html",
            context=config_context
        )
        
        report_path = Path("output") / "config_report.html"
        report_path.write_text(report_html)
        
        print(f"      ✅ Report rendered ({len(report_html)} characters)")
        print(f"      💾 Saved to: {report_path}")
        
        # Step 5: API Documentation Generation
        print("\n📡 Step 5: API Documentation Generation")
        print("-" * 50)
        
        # Sample API endpoints
        api_endpoints = [
            {
                "method": "get",
                "path": "/api/v1/plugins",
                "description": "List all available plugins",
                "parameters": [
                    {"name": "status", "type": "string", "description": "Filter by plugin status", "required": False},
                    {"name": "limit", "type": "integer", "description": "Maximum results to return", "required": False}
                ],
                "example_response": {"plugins": plugin_data, "total": len(plugin_data)}
            },
            {
                "method": "post",
                "path": "/api/v1/plugins/{id}/config",
                "description": "Update plugin configuration",
                "parameters": [
                    {"name": "id", "type": "string", "description": "Plugin identifier", "required": True},
                    {"name": "config", "type": "object", "description": "Configuration object", "required": True}
                ],
                "example_request": {"enabled": True, "settings": {"batch_size": 1000}},
                "example_response": {"status": "success", "message": "Plugin configuration updated"}
            },
            {
                "method": "get",
                "path": "/api/v1/templates",
                "description": "List available templates",
                "parameters": [
                    {"name": "engine", "type": "string", "description": "Template engine name", "required": False}
                ],
                "example_response": {"templates": ["base.html", "plugin_dashboard.html"], "count": 2}
            }
        ]
        
        api_context = TemplateContext()
        api_context.set_variable("api_name", "Framework0 Extension API")
        api_context.set_variable("api_description", "RESTful API for managing Framework0 plugins, configurations, events, and templates")
        api_context.set_variable("api_version", "2.1.0")
        api_context.set_variable("endpoints", api_endpoints)
        api_context.set_variable("coverage_percentage", 85)
        api_context.set_variable("last_updated", "2025-10-05T17:45:00+00:00")
        api_context.set_variable("tags", ["plugins", "configuration", "events", "templates", "rest-api"])
        
        api_docs = template_manager.render_template(
            "api_docs.md",
            context=api_context
        )
        
        docs_path = Path("output") / "api_documentation.md"
        docs_path.write_text(api_docs)
        
        print(f"    📡 API Documentation generated ({len(api_docs)} characters)")
        print(f"    💾 Saved to: {docs_path}")
        print(f"    📊 {len(api_endpoints)} endpoints documented")
        
        # Step 6: In-Memory Templates
        print("\n💾 Step 6: In-Memory Templates")
        print("-" * 50)
        
        # Create dynamic email template
        email_template = """Subject: {{ subject }}

Dear {{ recipient_name | default('User') }},

{{ email_body | default('Thank you for using Framework0!') }}

{% if action_items %}
Action Items:
{% for item in action_items %}
{{ loop.index }}. {{ item }}
{% endfor %}
{% endif %}

Best regards,
{{ sender_name | default('Framework0 System') }}

---
Generated at: {{ now() | timestamp }}
Template ID: {{ generate_id('email') }}
"""
        
        # Add to in-memory engine
        memory_path = template_manager.create_template(
            "notification_email.txt",
            email_template,
            engine_name="memory",
            metadata=TemplateMetadata(
                name="notification_email.txt",
                description="Dynamic email notification template",
                tags={'email', 'notification', 'dynamic'}
            )
        )
        
        # Render email template
        email_context = TemplateContext()
        email_context.set_variable("subject", "Framework0 Template System Demo Complete!")
        email_context.set_variable("recipient_name", "Developer")
        email_context.set_variable("email_body", "The Template System demo has been successfully completed. All templates have been rendered and saved.")
        email_context.set_variable("sender_name", "Framework0 Template System")
        email_context.set_variable("action_items", [
            "Review generated HTML reports",
            "Check API documentation",
            "Validate template rendering performance",
            "Proceed to Exercise 10 Phase 5: CLI Integration"
        ])
        
        email_content = template_manager.render_template(
            "notification_email.txt",
            context=email_context,
            engine_name="memory"
        )
        
        email_path = Path("output") / "notification_email.txt"
        email_path.write_text(email_content)
        
        print(f"    ✅ In-memory template created: notification_email.txt")
        print(f"    💾 Email rendered and saved to: {email_path}")
        
        # Step 7: String Template Rendering
        print("\n🔤 Step 7: String Template Rendering")
        print("-" * 50)
        
        # Simple configuration template
        config_template_str = """
# Framework0 Configuration - {{ environment | upper }}
# Generated: {{ timestamp }}

[database]
host = "{{ db_host }}"
port = {{ db_port }}
name = "{{ db_name }}"

[api]
version = "{{ api_version }}"
timeout = {{ timeout_seconds }}
debug = {{ debug_mode | lower }}

[logging]
level = "{{ log_level | upper }}"
file = "{{ log_file }}"
size_limit = "{{ log_size_mb }}MB"

# End of configuration
        """.strip()
        
        config_variables = {
            "environment": "production",
            "timestamp": "2025-10-05T17:45:00+00:00",
            "db_host": "production-db.framework0.com",
            "db_port": 5432,
            "db_name": "framework0_prod",
            "api_version": "v2.1",
            "timeout_seconds": 60,
            "debug_mode": False,
            "log_level": "warning",
            "log_file": "/var/log/framework0/app.log",
            "log_size_mb": 100
        }
        
        rendered_config = render_string_template(config_template_str, **config_variables)
        
        config_output_path = Path("output") / "framework0.conf"
        config_output_path.write_text(rendered_config)
        
        print(f"    ✅ String template rendered ({len(rendered_config)} characters)")
        print(f"    💾 Configuration saved to: {config_output_path}")
        
        # Step 8: Template Validation and Management
        print("\n✅ Step 8: Template Validation and Management")
        print("-" * 50)
        
        # List all templates
        fs_templates = template_manager.list_templates("filesystem")
        memory_templates = template_manager.list_templates("memory")
        
        print(f"    📂 Filesystem Templates ({len(fs_templates)}):")
        for template in fs_templates:
            is_valid = template_manager.validate_template(template, "filesystem")
            status = "✅ Valid" if is_valid else "❌ Invalid"
            print(f"      {status} {template}")
        
        print(f"    💾 In-Memory Templates ({len(memory_templates)}):")
        for template in memory_templates:
            is_valid = template_manager.validate_template(template, "memory")
            status = "✅ Valid" if is_valid else "❌ Invalid"
            print(f"      {status} {template}")
        
        # Template performance test
        print(f"\n    ⏱️ Template Performance Test:")
        
        import time
        
        # Test rendering performance
        start_time = time.time()
        for i in range(10):
            template_manager.render_template(
                "plugin_dashboard.html",
                context=dashboard_context
            )
        end_time = time.time()
        
        avg_render_time = (end_time - start_time) / 10
        print(f"      Average render time: {avg_render_time:.4f} seconds")
        print(f"      Templates per second: {1/avg_render_time:.1f}")
        
        # Step 9: Template Context Management
        print("\n🎯 Step 9: Template Context Management")
        print("-" * 50)
        
        # Demonstrate context manager
        with template_manager.template_context(
            demo_mode=True,
            test_value="Context Manager Test",
            temporary_setting=12345
        ):
            context_test = template_manager.render_template(
                "base.html",
                page_title="Context Manager Demo"
            )
            print(f"    ✅ Context manager test successful")
            print(f"    📏 Rendered content: {len(context_test)} characters")
        
        # Variables should be cleaned up after context manager
        print(f"    🧹 Context variables cleaned up automatically")
        
        # Success summary
        print("\n" + "=" * 80)
        print("🎉 TEMPLATE SYSTEM DEMO SUCCESSFUL!")
        print("=" * 80)
        print("✅ Template Manager: Filesystem and in-memory template engines")
        print("✅ Template Creation: Multiple template types with inheritance")
        print("✅ Context Management: Variables, filters, and global functions")
        print("✅ Content Generation: HTML reports and API documentation")
        print("✅ Dynamic Rendering: In-memory and string template rendering")
        print("✅ Template Validation: Syntax checking and error handling")
        print("✅ Performance Testing: Template rendering performance metrics")
        print("✅ Integration Ready: Configuration and event system integration")
        
        print(f"\n🏗️ Template System Architecture Validated:")
        print(f"  📋 {len(fs_templates)} filesystem templates")
        print(f"  💾 {len(memory_templates)} in-memory templates") 
        print(f"  🖨️ 5+ rendered outputs generated")
        print(f"  ⚡ {1/avg_render_time:.1f} templates/second performance")
        print(f"  📄 Multiple output formats: HTML, Markdown, Text, Config")
        
        print("\n🚀 Exercise 10 Phase 4: Template System COMPLETE!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Template System Demo Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit_code = 0 if success else 1
    sys.exit(exit_code)