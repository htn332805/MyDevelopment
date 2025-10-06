# Framework0 API Reference

## Overview
This document provides a comprehensive API reference for all Python modules in Framework0.

**Generated:** 2025-10-05 21:24:45  
**Total Modules:** 256  

## Modules by Category

### Core (16 modules)

- **example_core_plugin** (`examples/plugins/core/example_core_plugin.py`) - 23 functions, 10 classes
- **core** (`orchestrator/persistence/core.py`) - 27 functions, 8 classes
- **core** (`scriptlets/foundation/logging/core.py`) - 10 functions, 5 classes
- **metrics_core** (`scriptlets/foundation/metrics/metrics_core.py`) - 24 functions, 6 classes
- **error_core** (`scriptlets/foundation/errors/error_core.py`) - 18 functions, 7 classes
- **health_core** (`scriptlets/foundation/health/health_core.py`) - 23 functions, 7 classes
- **trace_logger_v2** (`src/core/trace_logger_v2.py`) - 33 functions, 4 classes
- **logger** (`src/core/logger.py`) - 32 functions, 3 classes
- **core** (`isolated_recipe/example_numbers/orchestrator/persistence/core.py`) - 27 functions, 8 classes
- **logger** (`isolated_recipe/example_numbers/src/core/logger.py`) - 32 functions, 3 classes
- **logger** (`isolated_recipe/example_numbers_minimal/src/core/logger.py`) - 32 functions, 3 classes
- **logger** (`test_results/enhanced_example_isolated/src/core/logger.py`) - 32 functions, 3 classes
- **logger** (`test_results/example_numbers_isolated/src/core/logger.py`) - 32 functions, 3 classes
- **logger** (`test_results/compute_median_isolated/src/core/logger.py`) - 32 functions, 3 classes
- **logger** (`test_results/example_numbers0_isolated/src/core/logger.py`) - 32 functions, 3 classes
- **test_core_functionality** (`tests/test_core_functionality.py`) - 21 functions, 5 classes

### Analysis (5 modules)

- **metrics_analyzers** (`scriptlets/foundation/metrics/metrics_analyzers.py`) - 27 functions, 7 classes
- **baseline_framework_analyzer** (`tools/baseline_framework_analyzer.py`) - 21 functions, 3 classes
- **recipe_dependency_analyzer** (`tools/recipe_dependency_analyzer.py`) - 10 functions, 3 classes
- **test_enhanced_analysis_framework** (`tests/test_enhanced_analysis_framework.py`) - 11 functions, 1 classes
- **test_analysis_framework** (`tests/test_analysis_framework.py`) - 56 functions, 14 classes

### Context (13 modules)

- **enhanced_context_server** (`orchestrator/enhanced_context_server.py`) - 32 functions, 3 classes
- **context_client** (`orchestrator/context_client.py`) - 17 functions, 6 classes
- **context** (`orchestrator/context/context.py`) - 18 functions, 3 classes
- **context-checkpoint** (`orchestrator/context/.ipynb_checkpoints/context-checkpoint.py`) - 9 functions, 1 classes
- **context_client** (`isolated_recipe/example_numbers/orchestrator/context_client.py`) - 17 functions, 6 classes
- **context** (`isolated_recipe/example_numbers/orchestrator/context/context.py`) - 18 functions, 3 classes
- **context-checkpoint** (`isolated_recipe/example_numbers/orchestrator/context/.ipynb_checkpoints/context-checkpoint.py`) - 9 functions, 1 classes
- **context** (`isolated_recipe/example_numbers_minimal/orchestrator/context/context.py`) - 18 functions, 3 classes
- **context** (`test_results/enhanced_example_isolated/orchestrator/context/context.py`) - 18 functions, 3 classes
- **context** (`test_results/example_numbers_isolated/orchestrator/context/context.py`) - 18 functions, 3 classes
- **context** (`test_results/compute_median_isolated/orchestrator/context/context.py`) - 18 functions, 3 classes
- **context** (`test_results/example_numbers0_isolated/orchestrator/context/context.py`) - 18 functions, 3 classes
- **test_enhanced_context_server** (`tests/test_enhanced_context_server.py`) - 29 functions, 5 classes

### Recipe (28 modules)

- **runner** (`orchestrator/runner.py`) - 24 functions, 4 classes
- **recipe_parser** (`orchestrator/recipe_parser.py`) - 4 functions, 0 classes
- **enhanced_recipe_parser** (`orchestrator/enhanced_recipe_parser.py`) - 27 functions, 8 classes
- **recipe_analytics_engine** (`scriptlets/analytics/recipe_analytics_engine.py`) - 41 functions, 7 classes
- **run_recipe** (`isolated_recipe/example_numbers/run_recipe.py`) - 1 functions, 0 classes
- **runner** (`isolated_recipe/example_numbers/orchestrator/runner.py`) - 24 functions, 4 classes
- **recipe_parser** (`isolated_recipe/example_numbers/orchestrator/recipe_parser.py`) - 4 functions, 0 classes
- **run_recipe** (`isolated_recipe/example_numbers_minimal/run_recipe.py`) - 1 functions, 0 classes
- **runner** (`isolated_recipe/example_numbers_minimal/orchestrator/runner.py`) - 24 functions, 4 classes
- **recipe_parser** (`isolated_recipe/example_numbers_minimal/orchestrator/recipe_parser.py`) - 4 functions, 0 classes
- **recipe_portfolio** (`capstone/integration/recipe_portfolio.py`) - 18 functions, 6 classes
- **run_recipe** (`test_results/enhanced_example_isolated/run_recipe.py`) - 1 functions, 0 classes
- **runner** (`test_results/enhanced_example_isolated/orchestrator/runner.py`) - 24 functions, 4 classes
- **recipe_parser** (`test_results/enhanced_example_isolated/orchestrator/recipe_parser.py`) - 4 functions, 0 classes
- **run_recipe** (`test_results/example_numbers_isolated/run_recipe.py`) - 1 functions, 0 classes
- **runner** (`test_results/example_numbers_isolated/orchestrator/runner.py`) - 24 functions, 4 classes
- **recipe_parser** (`test_results/example_numbers_isolated/orchestrator/recipe_parser.py`) - 4 functions, 0 classes
- **run_recipe** (`test_results/compute_median_isolated/run_recipe.py`) - 1 functions, 0 classes
- **runner** (`test_results/compute_median_isolated/orchestrator/runner.py`) - 24 functions, 4 classes
- **recipe_parser** (`test_results/compute_median_isolated/orchestrator/recipe_parser.py`) - 4 functions, 0 classes
- **run_recipe** (`test_results/example_numbers0_isolated/run_recipe.py`) - 1 functions, 0 classes
- **runner** (`test_results/example_numbers0_isolated/orchestrator/runner.py`) - 24 functions, 4 classes
- **recipe_parser** (`test_results/example_numbers0_isolated/orchestrator/recipe_parser.py`) - 4 functions, 0 classes
- **recipe_execution_validator** (`tools/recipe_execution_validator.py`) - 9 functions, 4 classes
- **recipe_isolation_cli** (`tools/recipe_isolation_cli.py`) - 26 functions, 2 classes
- **comprehensive_recipe_test_cli** (`tools/comprehensive_recipe_test_cli.py`) - 11 functions, 1 classes
- **recipe_validation_engine** (`tools/recipe_validation_engine.py`) - 15 functions, 3 classes
- **test_enhanced_recipe_parser** (`tests/test_enhanced_recipe_parser.py`) - 35 functions, 3 classes

### Server (2 modules)

- **server_config** (`server/server_config.py`) - 20 functions, 2 classes
- **test_websocket_performance** (`tests/test_websocket_performance.py`) - 5 functions, 4 classes

### Tools (17 modules)

- **example_tool_plugin** (`examples/plugins/tools/example_tool_plugin.py`) - 25 functions, 9 classes
- **workspace_cleaner_clean** (`tools/workspace_cleaner_clean.py`) - 11 functions, 1 classes
- **workspace_restructurer** (`tools/workspace_restructurer.py`) - 13 functions, 3 classes
- **framework0_manager** (`tools/framework0_manager.py`) - 1 functions, 0 classes
- **post_restructure_validator** (`tools/post_restructure_validator.py`) - 15 functions, 2 classes
- **workspace_cleaner_v2** (`tools/workspace_cleaner_v2.py`) - 16 functions, 3 classes
- **phased_restructurer** (`tools/phased_restructurer.py`) - 15 functions, 1 classes
- **workspace_cleaner** (`tools/workspace_cleaner.py`) - 0 functions, 0 classes
- **documentation_updater** (`tools/documentation_updater.py`) - 18 functions, 1 classes
- **framework_enhancer** (`tools/framework_enhancer.py`) - 18 functions, 3 classes
- **comprehensive_workspace_scanner** (`tools/comprehensive_workspace_scanner.py`) - 18 functions, 3 classes
- **workspace_execution_validator** (`tools/workspace_execution_validator.py`) - 12 functions, 3 classes
- **comprehensive_documentation_generator** (`tools/comprehensive_documentation_generator.py`) - 16 functions, 1 classes
- **framework0_documentation_generator** (`tools/framework0_documentation_generator.py`) - 0 functions, 0 classes
- **framework0_workspace_cleaner** (`tools/framework0_workspace_cleaner.py`) - 15 functions, 2 classes
- **minimal_dependency_resolver** (`tools/minimal_dependency_resolver.py`) - 17 functions, 4 classes
- **baseline_documentation_updater** (`tools/baseline_documentation_updater.py`) - 15 functions, 3 classes

### Tests (33 modules)

- **test_error_framework_integration** (`test_error_framework_integration.py`) - 4 functions, 0 classes
- **test_health_monitoring** (`engine/steps/python/test_health_monitoring.py`) - 10 functions, 2 classes
- **test_logging_framework** (`engine/steps/python/test_logging_framework.py`) - 10 functions, 2 classes
- **test_delta_compression** (`tests/test_delta_compression.py`) - 25 functions, 4 classes
- **test_plugin_integration_quick** (`tests/test_plugin_integration_quick.py`) - 7 functions, 1 classes
- **test_workspace_cleaner_v2** (`tests/test_workspace_cleaner_v2.py`) - 13 functions, 1 classes
- **test_event_system** (`tests/test_event_system.py`) - 33 functions, 6 classes
- **test_plugin_integration** (`tests/test_plugin_integration.py`) - 14 functions, 2 classes
- **test_template_system_corrected** (`tests/test_template_system_corrected.py`) - 23 functions, 8 classes
- **test_async_integration** (`tests/test_async_integration.py`) - 9 functions, 1 classes
- **test_async_load_framework** (`tests/test_async_load_framework.py`) - 9 functions, 5 classes
- **test_configuration_system** (`tests/test_configuration_system.py`) - 37 functions, 7 classes
- **test_plugin_integration_working** (`tests/test_plugin_integration_working.py`) - 10 functions, 1 classes
- **test_simple_validation** (`tests/test_simple_validation.py`) - 4 functions, 0 classes
- **test_foundation_integration** (`tests/test_foundation_integration.py`) - 36 functions, 7 classes
- **test_database_operations** (`tests/test_database_operations.py`) - 17 functions, 2 classes
- **test_template_system** (`tests/test_template_system.py`) - 41 functions, 10 classes
- **test_enhanced_persistence** (`tests/test_enhanced_persistence.py`) - 10 functions, 1 classes
- **test_delta_module** (`tests/test_delta_module.py`) - 0 functions, 0 classes
- **test_realtime_performance** (`tests/test_realtime_performance.py`) - 29 functions, 4 classes
- **test_integration** (`tests/test_integration.py`) - 10 functions, 1 classes
- **test_performance_load** (`tests/test_performance_load.py`) - 25 functions, 3 classes
- **test_framework0_integration** (`tests/test_framework0_integration.py`) - 15 functions, 2 classes
- **test_enhanced_memory_bus** (`tests/test_enhanced_memory_bus.py`) - 27 functions, 6 classes
- **test_performance_metrics** (`tests/test_performance_metrics.py`) - 41 functions, 7 classes
- **test_production_workflow_engine** (`tests/test_production_workflow_engine.py`) - 20 functions, 6 classes
- **test_visualization_system** (`tests/test_visualization_system.py`) - 9 functions, 0 classes
- **test_basic_performance** (`tests/test_basic_performance.py`) - 14 functions, 1 classes
- **integration_test_summary** (`tests/integration_test_summary.py`) - 1 functions, 0 classes
- **test_scriptlet_framework** (`tests/test_scriptlet_framework.py`) - 48 functions, 30 classes
- **test_batch_processing** (`tests/test_batch_processing.py`) - 32 functions, 2 classes
- **test_exercise_7_analytics** (`tests/analytics/test_exercise_7_analytics.py`) - 48 functions, 6 classes
- **test_container_deployment_engine** (`tests/deployment/test_container_deployment_engine.py`) - 23 functions, 6 classes

### Other (142 modules)

- **plugin_registry_demo** (`plugin_registry_demo.py`) - 11 functions, 2 classes
- **cli_demo** (`cli_demo.py`) - 2 functions, 0 classes
- **event_demo** (`event_demo.py`) - 5 functions, 0 classes
- **simple_plugin_demo** (`simple_plugin_demo.py`) - 1 functions, 0 classes
- **template_demo** (`template_demo.py`) - 5 functions, 0 classes
- **plugin_system_demo** (`plugin_system_demo.py`) - 22 functions, 4 classes
- **configuration_demo** (`configuration_demo.py`) - 1 functions, 0 classes
- **exercise_10_complete_integration_demo** (`exercise_10_complete_integration_demo.py`) - 3 functions, 0 classes
- **exercise_11_phase_a_demo** (`exercise_11_phase_a_demo.py`) - 0 functions, 0 classes
- **foundation_integration_demo** (`foundation_integration_demo.py`) - 7 functions, 0 classes
- **exercise_11_phase_b_demo** (`exercise_11_phase_b_demo.py`) - 1 functions, 1 classes
- **missing_module** (`engine/engine/steps/python/missing_module.py`) - 9 functions, 2 classes
- **compute_median** (`engine/orchestrator/scriptlets/python/steps/compute_median.py`) - 9 functions, 2 classes
- **missing_scriptlet** (`engine/scriptlets/missing_scriptlet.py`) - 9 functions, 2 classes
- **compute_numbers** (`engine/steps/python/compute_numbers.py`) - 8 functions, 2 classes
- **compute_numbers_enhanced** (`engine/enhanced_scriptlets/compute_numbers_enhanced.py`) - 9 functions, 2 classes
- **interactive_demo** (`docs/interactive_demo.py`) - 2 functions, 0 classes
- **basic_usage** (`--help/examples/basic_usage.py`) - 3 functions, 2 classes
- **basic_usage** (`--help/backup_pre_cleanup/examples/basic_usage.py`) - 3 functions, 2 classes
- **enhanced_logging_demo** (`examples/enhanced_logging_demo.py`) - 6 functions, 0 classes
- **example_orchestration_plugin** (`examples/plugins/orchestration/example_orchestration_plugin.py`) - 18 functions, 10 classes
- **example_scriptlet_plugin** (`examples/plugins/scriptlets/example_scriptlet_plugin.py`) - 22 functions, 10 classes
- **persistence** (`orchestrator/persistence.py`) - 6 functions, 1 classes
- **dependency_graph** (`orchestrator/dependency_graph.py`) - 7 functions, 1 classes
- **enhanced_memory_bus** (`orchestrator/enhanced_memory_bus.py`) - 51 functions, 6 classes
- **memory_bus** (`orchestrator/memory_bus.py`) - 9 functions, 2 classes
- **persistence** (`orchestrator/context/persistence.py`) - 9 functions, 1 classes
- **version_control** (`orchestrator/context/version_control.py`) - 6 functions, 1 classes
- **db_adapter** (`orchestrator/context/db_adapter.py`) - 13 functions, 2 classes
- **memory_bus** (`orchestrator/context/memory_bus.py`) - 7 functions, 1 classes
- **memory_bus-checkpoint** (`orchestrator/context/.ipynb_checkpoints/memory_bus-checkpoint.py`) - 7 functions, 1 classes
- **__init__-checkpoint** (`orchestrator/context/.ipynb_checkpoints/__init__-checkpoint.py`) - 0 functions, 0 classes
- **snapshot** (`orchestrator/persistence/snapshot.py`) - 30 functions, 5 classes
- **enhanced** (`orchestrator/persistence/enhanced.py`) - 47 functions, 3 classes
- **delta** (`orchestrator/persistence/delta.py`) - 25 functions, 4 classes
- **cache** (`orchestrator/persistence/cache.py`) - 80 functions, 9 classes
- **exercise_8_phase_2_demo** (`FYI/exercise_8_phase_2_demo.py`) - 1 functions, 0 classes
- **EXERCISE_7_COMPLETION_REPORT** (`FYI/EXERCISE_7_COMPLETION_REPORT.py`) - 1 functions, 0 classes
- **exercise_7_demo** (`FYI/exercise_7_demo.py`) - 1 functions, 0 classes
- **exercise_9_phase_1_demo** (`FYI/exercise_9_phase_1_demo.py`) - 0 functions, 0 classes
- **EXERCISE_8_PHASE_1_COMPLETION_REPORT** (`FYI/EXERCISE_8_PHASE_1_COMPLETION_REPORT.py`) - 2 functions, 0 classes
- **exercise_8_demo** (`FYI/exercise_8_demo.py`) - 1 functions, 0 classes
- **performance_metrics** (`scriptlets/performance_metrics.py`) - 9 functions, 2 classes
- **framework** (`scriptlets/framework.py`) - 50 functions, 9 classes
- **analytics_data_models** (`scriptlets/analytics/analytics_data_models.py`) - 56 functions, 14 classes
- **analytics_templates** (`scriptlets/analytics/analytics_templates.py`) - 45 functions, 13 classes
- **analytics_dashboard** (`scriptlets/analytics/analytics_dashboard.py`) - 43 functions, 9 classes
- **api_integration** (`scriptlets/core/api_integration.py`) - 16 functions, 4 classes
- **batch_processing** (`scriptlets/core/batch_processing.py`) - 35 functions, 6 classes
- **data_validation** (`scriptlets/core/data_validation.py`) - 41 functions, 6 classes
- **database_operations** (`scriptlets/core/database_operations.py`) - 30 functions, 3 classes
- **file_processing** (`scriptlets/core/file_processing.py`) - 18 functions, 2 classes
- **template_system** (`scriptlets/extensions/template_system.py`) - 67 functions, 22 classes
- **plugin_interface** (`scriptlets/extensions/plugin_interface.py`) - 22 functions, 9 classes
- **event_system** (`scriptlets/extensions/event_system.py`) - 30 functions, 11 classes
- **configuration_system** (`scriptlets/extensions/configuration_system.py`) - 30 functions, 8 classes
- **cli_system** (`scriptlets/extensions/cli_system.py`) - 55 functions, 16 classes
- **plugin_manager** (`scriptlets/extensions/plugin_manager.py`) - 24 functions, 6 classes
- **plugin_registry** (`scriptlets/extensions/plugin_registry.py`) - 48 functions, 8 classes
- **environment_rollback** (`scriptlets/production_ecosystem/environment_rollback.py`) - 5 functions, 7 classes
- **security_framework** (`scriptlets/production_ecosystem/security_framework.py`) - 46 functions, 13 classes
- **observability_platform** (`scriptlets/production_ecosystem/observability_platform.py`) - 38 functions, 12 classes
- **deployment_engine** (`scriptlets/production_ecosystem/deployment_engine.py`) - 4 functions, 7 classes
- **logging_framework** (`scriptlets/foundation/logging_framework.py`) - 11 functions, 2 classes
- **health_monitoring** (`scriptlets/foundation/health_monitoring.py`) - 14 functions, 2 classes
- **foundation_orchestrator** (`scriptlets/foundation/foundation_orchestrator.py`) - 21 functions, 1 classes
- **foundation_integration_bridge** (`scriptlets/foundation/foundation_integration_bridge.py`) - 28 functions, 3 classes
- **adapters** (`scriptlets/foundation/logging/adapters.py`) - 13 functions, 2 classes
- **formatters** (`scriptlets/foundation/logging/formatters.py`) - 11 functions, 3 classes
- **metrics_collectors** (`scriptlets/foundation/metrics/metrics_collectors.py`) - 36 functions, 4 classes
- **resilience_patterns** (`scriptlets/foundation/errors/resilience_patterns.py`) - 28 functions, 6 classes
- **error_handlers** (`scriptlets/foundation/errors/error_handlers.py`) - 38 functions, 6 classes
- **recovery_strategies** (`scriptlets/foundation/errors/recovery_strategies.py`) - 33 functions, 7 classes
- **error_handling** (`scriptlets/foundation/errors/error_handling.py`) - 20 functions, 1 classes
- **health_checks** (`scriptlets/foundation/health/health_checks.py`) - 14 functions, 4 classes
- **health_reporters** (`scriptlets/foundation/health/health_reporters.py`) - 17 functions, 3 classes
- **production_workflow_engine** (`scriptlets/production/production_workflow_engine.py`) - 6 functions, 6 classes
- **isolation_framework** (`scriptlets/deployment/isolation_framework.py`) - 7 functions, 7 classes
- **container_deployment_engine** (`scriptlets/deployment/container_deployment_engine.py`) - 12 functions, 4 classes
- **dash_integration** (`src/dash_integration.py`) - 16 functions, 2 classes
- **basic_usage** (`src/basic_usage.py`) - 4 functions, 2 classes
- **dash_demo** (`src/dash_demo.py`) - 10 functions, 1 classes
- **integration_demo** (`src/integration_demo.py`) - 9 functions, 1 classes
- **performance_dashboard** (`src/visualization/performance_dashboard.py`) - 25 functions, 5 classes
- **execution_flow** (`src/visualization/execution_flow.py`) - 25 functions, 5 classes
- **timeline_visualizer** (`src/visualization/timeline_visualizer.py`) - 25 functions, 8 classes
- **enhanced_visualizer** (`src/visualization/enhanced_visualizer.py`) - 21 functions, 6 classes
- **request_tracer_v2** (`src/core/request_tracer_v2.py`) - 42 functions, 4 classes
- **plugin_interfaces_v2** (`src/core/plugin_interfaces_v2.py`) - 30 functions, 11 classes
- **plugin_discovery** (`src/core/plugin_discovery.py`) - 19 functions, 8 classes
- **plugin_interfaces** (`src/core/plugin_interfaces.py`) - 44 functions, 12 classes
- **unified_plugin_system_v2** (`src/core/unified_plugin_system_v2.py`) - 12 functions, 8 classes
- **integrated_plugin_discovery** (`src/core/integrated_plugin_discovery.py`) - 10 functions, 5 classes
- **plugin_manager** (`src/core/plugin_manager.py`) - 43 functions, 9 classes
- **unified_plugin_system** (`src/core/unified_plugin_system.py`) - 14 functions, 7 classes
- **plugin_discovery_integration** (`src/core/plugin_discovery_integration.py`) - 10 functions, 3 classes
- **debug_manager** (`src/core/debug_manager.py`) - 32 functions, 3 classes
- **components** (`src/analysis/components.py`) - 19 functions, 4 classes
- **enhanced_components** (`src/analysis/enhanced_components.py`) - 25 functions, 4 classes
- **framework** (`src/analysis/framework.py`) - 18 functions, 4 classes
- **enhanced_framework** (`src/analysis/enhanced_framework.py`) - 22 functions, 5 classes
- **registry** (`src/analysis/registry.py`) - 16 functions, 2 classes
- **dependency_graph** (`isolated_recipe/example_numbers/orchestrator/dependency_graph.py`) - 7 functions, 1 classes
- **persistence** (`isolated_recipe/example_numbers/orchestrator/context/persistence.py`) - 9 functions, 1 classes
- **version_control** (`isolated_recipe/example_numbers/orchestrator/context/version_control.py`) - 6 functions, 1 classes
- **db_adapter** (`isolated_recipe/example_numbers/orchestrator/context/db_adapter.py`) - 13 functions, 2 classes
- **memory_bus** (`isolated_recipe/example_numbers/orchestrator/context/memory_bus.py`) - 7 functions, 1 classes
- **memory_bus-checkpoint** (`isolated_recipe/example_numbers/orchestrator/context/.ipynb_checkpoints/memory_bus-checkpoint.py`) - 7 functions, 1 classes
- **__init__-checkpoint** (`isolated_recipe/example_numbers/orchestrator/context/.ipynb_checkpoints/__init__-checkpoint.py`) - 0 functions, 0 classes
- **snapshot** (`isolated_recipe/example_numbers/orchestrator/persistence/snapshot.py`) - 30 functions, 5 classes
- **enhanced** (`isolated_recipe/example_numbers/orchestrator/persistence/enhanced.py`) - 47 functions, 3 classes
- **delta** (`isolated_recipe/example_numbers/orchestrator/persistence/delta.py`) - 25 functions, 4 classes
- **cache** (`isolated_recipe/example_numbers/orchestrator/persistence/cache.py`) - 80 functions, 9 classes
- **framework** (`isolated_recipe/example_numbers/scriptlets/framework.py`) - 50 functions, 9 classes
- **path_wrapper** (`isolated_recipe/example_numbers_minimal/path_wrapper.py`) - 7 functions, 1 classes
- **compute_numbers** (`isolated_recipe/example_numbers_minimal/engine/steps/python/compute_numbers.py`) - 8 functions, 2 classes
- **framework** (`isolated_recipe/example_numbers_minimal/scriptlets/framework.py`) - 50 functions, 9 classes
- **phase_7_demo** (`capstone/phase_7_demo.py`) - 1 functions, 0 classes
- **capstone_integration** (`capstone/capstone_integration.py`) - 4 functions, 1 classes
- **phase_8_demo** (`capstone/phase_8_demo.py`) - 0 functions, 0 classes
- **phase_3_demo** (`capstone/phase_3_demo.py`) - 6 functions, 2 classes
- **phase_6_demo** (`capstone/phase_6_demo.py`) - 0 functions, 0 classes
- **phase_2_demo** (`capstone/phase_2_demo.py`) - 7 functions, 2 classes
- **phase_4_demo** (`capstone/phase_4_demo.py`) - 7 functions, 1 classes
- **phase_5_demo** (`capstone/phase_5_demo.py`) - 6 functions, 1 classes
- **production_platform** (`capstone/integration/production_platform.py`) - 19 functions, 9 classes
- **container_deployment** (`capstone/integration/container_deployment.py`) - 22 functions, 10 classes
- **workflow_engine** (`capstone/integration/workflow_engine.py`) - 14 functions, 10 classes
- **interactive_demo** (`capstone/integration/interactive_demo.py`) - 7 functions, 4 classes
- **plugin_ecosystem** (`capstone/integration/plugin_ecosystem.py`) - 20 functions, 11 classes
- **analytics_dashboard** (`capstone/integration/analytics_dashboard.py`) - 16 functions, 6 classes
- **path_wrapper** (`test_results/enhanced_example_isolated/path_wrapper.py`) - 7 functions, 1 classes
- **compute_numbers_enhanced** (`test_results/enhanced_example_isolated/engine/enhanced_scriptlets/compute_numbers_enhanced.py`) - 9 functions, 2 classes
- **framework** (`test_results/enhanced_example_isolated/scriptlets/framework.py`) - 50 functions, 9 classes
- **path_wrapper** (`test_results/example_numbers_isolated/path_wrapper.py`) - 7 functions, 1 classes
- **compute_numbers** (`test_results/example_numbers_isolated/engine/steps/python/compute_numbers.py`) - 8 functions, 2 classes
- **framework** (`test_results/example_numbers_isolated/scriptlets/framework.py`) - 50 functions, 9 classes
- **path_wrapper** (`test_results/compute_median_isolated/path_wrapper.py`) - 7 functions, 1 classes
- **compute_median** (`test_results/compute_median_isolated/engine/orchestrator/scriptlets/python/steps/compute_median.py`) - 9 functions, 2 classes
- **framework** (`test_results/compute_median_isolated/scriptlets/framework.py`) - 50 functions, 9 classes
- **path_wrapper** (`test_results/example_numbers0_isolated/path_wrapper.py`) - 7 functions, 1 classes
- **framework** (`test_results/example_numbers0_isolated/scriptlets/framework.py`) - 50 functions, 9 classes

---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
