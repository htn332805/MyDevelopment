# Delta Compression Module Documentation

## Overview

The Delta Compression module provides efficient change tracking and compression capabilities for state data in the persistence framework. It tracks only the differences between states, minimizing storage requirements while maintaining data integrity.

## Key Components

### DeltaRecord

A class representing a delta record with changes and metadata.

```python
record = DeltaRecord(
    timestamp=time.time(),
    changes={"key1": "new_value"},
    removed_keys=["old_key"],
    metadata={"author": "system"}
)
```

#### DeltaRecord Methods

- `to_dict()` - Convert to dictionary representation
- `from_dict(data)` - Create from dictionary representation (class method)

### DeltaCompressor

Engine for delta compression operations.

```python
compressor = DeltaCompressor(
    strategy=DeltaStrategy.AUTO,
    enable_compression=True,
    compression_level=6
)
```

#### DeltaCompressor Methods

- `calculate_delta(old_state, new_state, include_unchanged=False)` - Calculate delta between two states
- `apply_delta(base_state, delta_info)` - Apply delta to a base state
- `create_delta_record(changes, removed_keys, timestamp=None)` - Create delta record from changes
- `merge_deltas(deltas)` - Merge multiple deltas into a single delta
- `serialize_delta(delta)` - Serialize delta record to bytes
- `deserialize_delta(data)` - Deserialize delta record from bytes
- `get_compression_stats()` - Get compression statistics

### DeltaChain

Manages chains of delta records for efficient storage and retrieval.

```python
chain = DeltaChain(
    delta_strategy=DeltaStrategy.AUTO,
    max_chain_length=20,
    enable_rebase=True
)
```

#### DeltaChain Methods

- `add_delta(delta)` - Add a delta to the chain
- `add_state(state, timestamp=None)` - Add a new state by calculating delta
- `get_state_at_index(index)` - Get state at specific index
- `get_current_state()` - Get current (latest) state
- `get_delta_at_index(index)` - Get delta at specific index
- `clear_chain()` - Clear the delta chain
- `rebaseline()` - Set current state as new base state
- `get_chain_metrics()` - Get metrics about the chain

## Strategy Options

The module supports multiple delta strategies through the `DeltaStrategy` enum:

- `BINARY` - Binary diffing (requires bsdiff4)
- `DICT` - Dictionary-based diffing
- `COMPRESS` - Compression without diffing
- `AUTO` - Automatically select best strategy
- `NONE` - No delta compression

## Usage Examples

### Basic Usage

```python
from orchestrator.persistence.delta import DeltaCompressor, DeltaChain
from orchestrator.persistence.core import DeltaStrategy

# Create a delta compressor
compressor = DeltaCompressor(strategy=DeltaStrategy.AUTO)

# Calculate delta between states
old_state = {"key1": "value1", "key2": 42}
new_state = {"key1": "value1", "key3": "new_value"}

delta_info = compressor.calculate_delta(old_state, new_state)
print(f"Changes: {delta_info['changes']}")
print(f"Removed keys: {delta_info['removed_keys']}")

# Apply delta to reconstruct state
reconstructed = compressor.apply_delta(old_state, delta_info)
assert reconstructed == new_state
```

### Using DeltaChain for State History

```python
from orchestrator.persistence.delta import DeltaChain

# Create a delta chain
chain = DeltaChain(max_chain_length=10)

# Add states
chain.add_state({"version": 1, "data": "initial"})
chain.add_state({"version": 2, "data": "updated"})
chain.add_state({"version": 3, "data": "final"})

# Get state history
initial_state = chain.get_state_at_index(0)
current_state = chain.get_current_state()

# Optimize chain
chain.rebaseline()
```

## Performance Considerations

- Use `DeltaStrategy.DICT` for small to medium states with frequent changes
- Use `DeltaStrategy.BINARY` for large states with complex structures
- Adjust `max_chain_length` based on memory constraints and history requirements
- Call `rebaseline()` periodically to prevent chain length issues
- Use compression for network transfer; consider disabling for frequent local operations

## Integration with Other Modules

The Delta Compression module integrates with:

- `core.py` - Uses core enums and utilities
- `snapshot.py` - Delta records power efficient snapshot storage
- `cache.py` - Optimized delta caching improves performance
- `enhanced.py` - Main integration point for the framework
