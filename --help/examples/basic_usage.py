#!/usr/bin/env python3
"""
Basic Usage Example - IAF0 Framework Integration
================================================
Demonstrates how to use Context, Scriptlet, and Analysis frameworks together.
"""

from orchestrator.context import Context
from scriptlets.framework import BaseScriptlet, register_scriptlet
from src.analysis.framework import BaseAnalyzerV2, AnalysisConfig


@register_scriptlet
class DataProcessor(BaseScriptlet):
    """Example scriptlet for data processing."""
    
    def run(self, input_data=None):
        """Process input data and store results in context."""
        # Get configuration from context
        config = self.context.get("processing.config", {"multiplier": 2})
        
        # Process data
        if input_data:
            result = [x * config.get("multiplier", 2) for x in input_data]
        else:
            result = []
        
        # Store results in context
        self.context.set("processing.result", result, who=self.name)
        self.context.set("processing.count", len(result), who=self.name)
        
        return {"status": "success", "processed": len(result), "result": result}


class CustomAnalyzer(BaseAnalyzerV2):
    """Example analyzer for statistical analysis."""
    
    def analyze(self, data, **kwargs):
        """Analyze data and return comprehensive results."""
        if not data:
            return self._create_result({"error": "No data provided"})
        
        # Perform statistical analysis
        stats = {
            "count": len(data),
            "sum": sum(data),
            "mean": sum(data) / len(data),
            "min": min(data),
            "max": max(data)
        }
        
        # Generate insights
        insights = []
        if stats["mean"] > 10:
            insights.append("Data has high average value")
        if stats["max"] - stats["min"] > 20:
            insights.append("Data has wide range")
        
        return self._create_result({
            "statistics": stats,
            "insights": insights,
            "data_quality": "good" if len(data) > 5 else "limited"
        })


def main():
    """Demonstrate integrated usage of IAF0 frameworks."""
    print("🚀 IAF0 Framework Integration Example")
    
    # 1. Initialize Context
    context = Context()
    context.set("processing.config", {"multiplier": 3}, who="main")
    print("✅ Context initialized")
    
    # 2. Use Scriptlet with Context
    processor = DataProcessor(context=context)
    input_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    result = processor.run(input_data)
    print(f"✅ Scriptlet processed: {result}")
    
    # 3. Get processed data from Context
    processed_data = context.get("processing.result")
    print(f"✅ Retrieved from context: {processed_data}")
    
    # 4. Analyze with Analysis Framework
    config = AnalysisConfig(statistical_precision=2, debug_mode=True)
    analyzer = CustomAnalyzer(config)
    
    analysis_result = analyzer.analyze(processed_data)
    print(f"✅ Analysis complete: {analysis_result.summary}")
    
    # 5. Store analysis in Context
    context.set("analysis.result", analysis_result.data, who="analyzer")
    context.set("analysis.insights", analysis_result.data.get("insights", []), who="analyzer")
    
    # 6. Show Context history
    print("\n📊 Context Change History:")
    history = context.get_history()
    for change in history[-5:]:  # Show last 5 changes
        print(f"  {change.who} set {change.key}: {change.after}")
    
    print("\n🎉 Integration example completed successfully!")


if __name__ == "__main__":
    main()
