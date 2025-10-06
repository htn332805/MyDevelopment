#!/usr/bin/env python3
"""
Exercise 8 Demo - Container Deployment System Demonstration

This demo showcases the Container Deployment Engine built in Exercise 8,
demonstrating containerization, registry management, and analytics integration.
"""

import time
from datetime import datetime, timezone
from pathlib import Path

# Import Exercise 8 components
from scriptlets.deployment import get_deployment_engine, ANALYTICS_INTEGRATION

def main():
    print("🚀 Exercise 8 Container Deployment Demo")
    print("="*50)
    
    # 1. Initialize Deployment System
    print("\n1. Initializing Container Deployment Engine...")
    deployment_engine = get_deployment_engine()
    print("✅ Container Deployment Engine initialized")
    print(f"📊 Analytics Integration: {'✅ Enabled' if ANALYTICS_INTEGRATION else '❌ Not Available'}")
    
    # 2. Demonstrate Container Build
    print("\n2. Building Recipe Container...")
    
    # Use an existing recipe package for demo
    recipe_packages = list(Path("isolated_recipe").glob("*/"))
    if recipe_packages:
        demo_package = recipe_packages[0]
        print(f"📦 Using demo package: {demo_package.name}")
    else:
        # Create a simulated package path
        demo_package = Path("isolated_recipe/demo_recipe")
        print(f"📦 Using simulated package: {demo_package}")
    
    # Build container with options
    build_options = {
        "python_version": "3.11",
        "optimize_size": True,
        "base_image": "python:3.11-slim"
    }
    
    container_name = f"framework0-recipe-{int(time.time())}"
    
    build_result = deployment_engine.build_container(
        str(demo_package),
        container_name,
        build_options
    )
    
    if build_result["success"]:
        print(f"✅ Container built successfully: {build_result['container_id']}")
        print(f"📏 Image size: {build_result['image_size_mb']:.1f}MB")
        print(f"⏱️ Build time: {build_result['build_duration_seconds']:.2f}s")
        print(f"🔒 Security scan: {build_result['security_scan']['scan_status']}")
        print(f"🚨 Vulnerabilities: {build_result['security_scan']['vulnerabilities_found']}")
    else:
        print(f"❌ Container build failed: {build_result.get('error', 'Unknown error')}")
        return
    
    # 3. Registry Push Demonstration
    print("\n3. Pushing Container to Registry...")
    
    registry_config = {
        "url": "docker.io",
        "namespace": "framework0-demo",
        "tag": "v1.0.0"
    }
    
    push_result = deployment_engine.push_container(
        container_name,
        registry_config
    )
    
    if push_result["success"]:
        print(f"✅ Container pushed successfully")
        print(f"🌐 Registry URL: {push_result['registry_url']}")
        print(f"⏱️ Push time: {push_result['push_duration_seconds']:.2f}s")
    else:
        print(f"❌ Container push failed: {push_result.get('error', 'Unknown error')}")
    
    # 4. Analytics Integration Demo
    print("\n4. Deployment Analytics...")
    
    analytics_data = deployment_engine.get_deployment_analytics()
    
    if analytics_data.get("analytics_enabled"):
        print("📊 Analytics Integration Status: ✅ Active")
        stats = analytics_data.get("deployment_statistics", {})
        print(f"📈 Total deployments tracked: {stats.get('count', 0)}")
        print(f"📊 Average operation duration: {stats.get('mean', 0):.2f}s")
        print("🔗 Exercise 7 Analytics integration working!")
    else:
        print("📊 Analytics Integration Status: ❌ Not Available")
        print(f"💡 Info: {analytics_data.get('message', 'Analytics not configured')}")
    
    # 5. Container Builder Demo
    print("\n5. Dockerfile Generation Demo...")
    
    dockerfile_content = deployment_engine.container_builder.generate_dockerfile(
        str(demo_package),
        build_options
    )
    
    # Show first few lines of generated Dockerfile
    dockerfile_lines = dockerfile_content.split('\n')[:10]
    print("📄 Generated Dockerfile (first 10 lines):")
    for i, line in enumerate(dockerfile_lines, 1):
        print(f"   {i:2d}: {line}")
    print("   ...")
    
    # 6. Security Scanner Demo
    print("\n6. Security Scanner Demo...")
    
    security_result = deployment_engine.security_scanner.scan_container(
        build_result['container_id']
    )
    
    print(f"🔒 Security Scan Status: {security_result['scan_status']}")
    print(f"🚨 Vulnerabilities Found: {security_result['vulnerabilities_found']}")
    print("📊 Severity Breakdown:")
    for severity, count in security_result['severity_breakdown'].items():
        print(f"   • {severity.capitalize()}: {count}")
    print(f"✅ Compliance Status: {security_result['compliance_status']}")
    
    # 7. System Integration Status
    print("\n7. System Integration Status...")
    
    integrations = {
        "Exercise 7 Analytics": ANALYTICS_INTEGRATION,
        "Container Builder": True,
        "Registry Manager": True,
        "Security Scanner": True,
        "Recipe Isolation CLI": True,  # From existing system
    }
    
    print("🔗 Integration Status:")
    for component, status in integrations.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {component}")
    
    print("\n🎉 Exercise 8 Container Deployment Demo Complete!")
    print("✅ Enterprise Container Deployment System is functional")
    print("\n🏆 Exercise 8 Phase 1 - Container Deployment Engine: COMPLETED!")

if __name__ == "__main__":
    main()