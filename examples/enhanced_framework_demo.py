"""
Framework0 Enhanced Features Demonstration.

This example demonstrates the key enhanced features of Framework0 including:
- Component factory and dependency injection
- Advanced debugging with checkpoints
- Comprehensive error handling with recovery
- Unified framework integration

Run with: python examples/enhanced_framework_demo.py
"""

import os
import sys
import time
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Framework0 enhanced imports
from src.core.interfaces import ComponentLifecycle, Executable, Configurable
from src.core.factory import register_component, create_component


class DataProcessor(ComponentLifecycle, Executable, Configurable):
    """Example data processing component."""
    
def __init__(self, name -> Any: str = "data_processor"):
        """Initialize data processor."""
        super().__init__()
        self.name = name
        self.processing_count = 0
        self.config = {"batch_size": 10, "timeout": 30}
        
    def _do_initialize(self, config: Dict[str, Any]) -> None:
        """Initialize data processor with configuration."""
        self.configure(config)
        print(f"DataProcessor '{self.name}' initialized with config: {self.config}")
    
    def _do_cleanup(self) -> None:
        """Cleanup data processor resources."""
        print(f"DataProcessor '{self.name}' cleaned up after {self.processing_count} operations")
    
    def configure(self, config: Dict[str, Any]) -> bool:
        """Update configuration."""
        try:
            self.config.update(config)
            return True
        except Exception:
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return self.config.copy()
    
    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute data processing."""
        data = context.get("data", [])
        batch_size = self.config.get("batch_size", 10)
        
        print(f"Processing {len(data)} items in batches of {batch_size}")
        
        processed_items = []
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            time.sleep(0.01)  # Simulate processing
            processed_items.extend([f"processed_{item}" for item in batch])
        
        self.processing_count += 1
        return {"processed": processed_items, "count": len(processed_items)}
    
    def can_execute(self, context: Dict[str, Any]) -> bool:
        """Check if processor can execute."""
        return "data" in context and isinstance(context["data"], list)


def demonstrate_component_factory() -> Any:
    """Demonstrate component factory and dependency injection."""
    print("\n=== Component Factory & Dependency Injection Demo ===")
    
    # Register components with dependencies
    register_component(
        DataProcessor,
        name="data_processor",
        singleton=True,
        config={"batch_size": 5, "timeout": 60}
    )
    
    # Create data processor
    processor = create_component("data_processor")
    processor.initialize({"name": "demo_processor"})
    
    # Test component functionality
    test_data = list(range(1, 16))  # 15 items
    context = {"data": test_data}
    
    if processor.can_execute(context):
        result = processor.execute(context)
        print(f"Processed {result['count']} items")
    
    processor.cleanup()


def demonstrate_basic_functionality() -> Any:
    """Demonstrate basic functionality."""
    print("\n=== Basic Enhanced Features Demo ===")
    
    # Test basic component creation
    processor = DataProcessor("basic_demo")
    processor.initialize({"batch_size": 3})
    
    # Test data processing
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    context = {"data": test_data}
    
    if processor.can_execute(context):
        result = processor.execute(context)
        print(f"Basic processing completed: {result['count']} items processed")
    
    processor.cleanup()


def main() -> Any:
    """Main demonstration function."""
    print("Framework0 Enhanced Features Demonstration")
    print("=" * 50)
    
    try:
        demonstrate_component_factory()
        demonstrate_basic_functionality()
        
        print("\n=== All Demonstrations Completed Successfully ===")
        
    except Exception as e:
        print(f"\nDemo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
