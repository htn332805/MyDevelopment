# delta.py - User Manual

## Overview
**File Path:** `isolated_recipe/example_numbers/orchestrator/persistence/delta.py`  
**File Type:** Python Module  
**Last Modified:** 2025-10-04T22:24:24.353392  
**File Size:** 27,701 bytes  

## Description
Delta Compression Module for Enhanced Persistence Framework.

This module provides delta compression capabilities for efficient
data storage and transfer, reducing the storage requirements by
tracking only changes between successive states.

Features:
- Multiple delta compression strategies
- Delta chain management with automatic optimization
- Integrity verification and statistics

## Purpose and Application
This Python module is part of the Framework0 system and provides the following capabilities:

### Key Features
1. **Function: extract_keys_from_delta**
2. **Function: __init__**
3. **Function: __repr__**
4. **Function: to_dict**
5. **Function: from_dict**
6. **Function: __init__**
7. **Function: calculate_delta**
8. **Function: _dict_delta**
9. **Function: _binary_delta**
10. **Function: apply_delta**
11. **Function: create_delta_record**
12. **Function: merge_deltas**
13. **Function: get_compression_stats**
14. **Function: serialize_delta**
15. **Function: deserialize_delta**
16. **Function: __init__**
17. **Function: add_delta**
18. **Function: add_state**
19. **Function: get_state_at_index**
20. **Function: get_current_state**
21. **Function: get_delta_at_index**
22. **Function: clear_chain**
23. **Function: rebaseline**
24. **Function: _optimize_chain**
25. **Function: get_chain_metrics**
26. **Class: DeltaCompressionError (0 methods)**
27. **Class: DeltaRecord (4 methods)**
28. **Class: DeltaCompressor (10 methods)**
29. **Class: DeltaChain (10 methods)**

## Functions (25 total)

### `extract_keys_from_delta`

**Signature:** `extract_keys_from_delta(delta: DeltaRecord) -> Set[str]`  
**Line:** 775  
**Description:** Extract all affected keys from a delta.

Args:
    delta: Delta record to extract keys from
    
Returns:
    Set[str]: Set of all keys affected by this delta

### `__init__`

**Signature:** `__init__(self, timestamp: float, changes: Dict[str, Any], removed_keys: List[str], metadata: Dict[str, Any], compression_ratio: float, size_bytes: int, checksum: str)`  
**Line:** 66  
**Description:** Initialize a delta record.

Args:
    timestamp: When the delta was created
    changes: Key-value changes
    removed_keys: Keys that were removed
    metadata: Additional metadata
    compression_ratio: Compression ratio achieved
    size_bytes: Size in bytes after compression
    checksum: Integrity checksum

### `__repr__`

**Signature:** `__repr__(self) -> str`  
**Line:** 96  
**Description:** String representation of delta record.

### `to_dict`

**Signature:** `to_dict(self) -> Dict[str, Any]`  
**Line:** 102  
**Description:** Convert to dictionary representation.

Returns:
    Dict[str, Any]: Dictionary representation

### `from_dict`

**Signature:** `from_dict(cls, data: Dict[str, Any]) -> 'DeltaRecord'`  
**Line:** 119  
**Description:** Create from dictionary representation.

Args:
    data: Dictionary representation
    
Returns:
    DeltaRecord: Reconstructed delta record

### `__init__`

**Signature:** `__init__(self, strategy: str, enable_compression: bool, compression_level: int)`  
**Line:** 146  
**Description:** Initialize the delta compressor.

Args:
    strategy: Delta compression strategy to use
    enable_compression: Whether to enable compression
    compression_level: Compression level (1-9, higher is more compression)

### `calculate_delta`

**Signature:** `calculate_delta(self, old_state: Dict[str, Any], new_state: Dict[str, Any], include_unchanged: bool) -> Dict[str, Any]`  
**Line:** 175  
**Description:** Calculate delta between two states.

Args:
    old_state: Previous state
    new_state: Current state
    include_unchanged: Whether to include unchanged values
    
Returns:
    Dict[str, Any]: Delta information including changes and removals

### `_dict_delta`

**Signature:** `_dict_delta(self, old_state: Dict[str, Any], new_state: Dict[str, Any], include_unchanged: bool) -> Dict[str, Any]`  
**Line:** 234  
**Description:** Calculate dictionary-based delta.

Args:
    old_state: Previous state dictionary
    new_state: Current state dictionary
    include_unchanged: Whether to include unchanged values
    
Returns:
    Dict[str, Any]: Delta information

### `_binary_delta`

**Signature:** `_binary_delta(self, old_state: Dict[str, Any], new_state: Dict[str, Any]) -> Dict[str, Any]`  
**Line:** 300  
**Description:** Calculate binary delta using bsdiff if available.

Args:
    old_state: Previous state
    new_state: Current state
    
Returns:
    Dict[str, Any]: Delta information

### `apply_delta`

**Signature:** `apply_delta(self, base_state: Dict[str, Any], delta_info: Dict[str, Any]) -> Dict[str, Any]`  
**Line:** 340  
**Description:** Apply delta to a base state to produce new state.

Args:
    base_state: Base state to apply delta to
    delta_info: Delta information from calculate_delta
    
Returns:
    Dict[str, Any]: Updated state
    
Raises:
    DeltaCompressionError: If delta application fails

### `create_delta_record`

**Signature:** `create_delta_record(self, changes: Dict[str, Any], removed_keys: List[str], timestamp: Optional[float]) -> DeltaRecord`  
**Line:** 386  
**Description:** Create compressed delta record from changes.

Args:
    changes: Dictionary of changes
    removed_keys: List of removed keys
    timestamp: Delta creation timestamp (default: current time)
    
Returns:
    DeltaRecord: Compressed delta record

### `merge_deltas`

**Signature:** `merge_deltas(self, deltas: List[DeltaRecord]) -> Optional[DeltaRecord]`  
**Line:** 456  
**Description:** Merge multiple deltas into a single delta.

Args:
    deltas: List of deltas to merge
    
Returns:
    Optional[DeltaRecord]: Merged delta or None if input is empty

### `get_compression_stats`

**Signature:** `get_compression_stats(self) -> Dict[str, Any]`  
**Line:** 498  
**Description:** Get compression statistics.

Returns:
    Dict[str, Any]: Dictionary of compression statistics

### `serialize_delta`

**Signature:** `serialize_delta(self, delta: DeltaRecord) -> bytes`  
**Line:** 506  
**Description:** Serialize delta record to bytes for storage.

Args:
    delta: Delta record to serialize
    
Returns:
    bytes: Serialized delta data

### `deserialize_delta`

**Signature:** `deserialize_delta(self, data: bytes) -> DeltaRecord`  
**Line:** 527  
**Description:** Deserialize delta record from bytes.

Args:
    data: Serialized delta data
    
Returns:
    DeltaRecord: Deserialized delta record

### `__init__`

**Signature:** `__init__(self, delta_strategy: str, max_chain_length: int, enable_rebase: bool)`  
**Line:** 557  
**Description:** Initialize the delta chain manager.

Args:
    delta_strategy: Delta compression strategy
    max_chain_length: Maximum chain length before optimization
    enable_rebase: Whether to enable automatic rebaseline

### `add_delta`

**Signature:** `add_delta(self, delta: DeltaRecord) -> None`  
**Line:** 587  
**Description:** Add a delta to the chain.

Args:
    delta: Delta record to add

### `add_state`

**Signature:** `add_state(self, state: Dict[str, Any], timestamp: Optional[float]) -> DeltaRecord`  
**Line:** 605  
**Description:** Add a new state to the chain by calculating delta from previous state.

Args:
    state: New state to add
    timestamp: Timestamp for the delta (default: current time)
    
Returns:
    DeltaRecord: Created delta record

### `get_state_at_index`

**Signature:** `get_state_at_index(self, index: int) -> Dict[str, Any]`  
**Line:** 655  
**Description:** Get the state at a specific index in the chain.

Args:
    index: Index in the chain (0 is base state)
    
Returns:
    Dict[str, Any]: State at the specified index
    
Raises:
    IndexError: If index is out of range

### `get_current_state`

**Signature:** `get_current_state(self) -> Dict[str, Any]`  
**Line:** 683  
**Description:** Get the current (latest) state in the chain.

Returns:
    Dict[str, Any]: Current state

### `get_delta_at_index`

**Signature:** `get_delta_at_index(self, index: int) -> Optional[DeltaRecord]`  
**Line:** 691  
**Description:** Get a delta record at a specific index in the chain.

Args:
    index: Index in the chain
    
Returns:
    Optional[DeltaRecord]: Delta record or None if index out of range

### `clear_chain`

**Signature:** `clear_chain(self) -> None`  
**Line:** 705  
**Description:** Clear the delta chain.

### `rebaseline`

**Signature:** `rebaseline(self) -> None`  
**Line:** 719  
**Description:** Rebaseline the chain by setting current state as new base state.

### `_optimize_chain`

**Signature:** `_optimize_chain(self) -> None`  
**Line:** 739  
**Description:** Optimize the delta chain by merging deltas.

### `get_chain_metrics`

**Signature:** `get_chain_metrics(self) -> Dict[str, Any]`  
**Line:** 764  
**Description:** Get metrics about the delta chain.

Returns:
    Dict[str, Any]: Dictionary of chain metrics


## Classes (4 total)

### `DeltaCompressionError`

**Line:** 54  
**Inherits from:** PersistenceError  
**Description:** Exception raised when delta compression operations fail.

### `DeltaRecord`

**Line:** 59  
**Description:** Represents a delta record with changes and metadata.

Delta records store the changes between two states, along with
metadata about the delta operation.

**Methods (4 total):**
- `__init__`: Initialize a delta record.

Args:
    timestamp: When the delta was created
    changes: Key-value changes
    removed_keys: Keys that were removed
    metadata: Additional metadata
    compression_ratio: Compression ratio achieved
    size_bytes: Size in bytes after compression
    checksum: Integrity checksum
- `__repr__`: String representation of delta record.
- `to_dict`: Convert to dictionary representation.

Returns:
    Dict[str, Any]: Dictionary representation
- `from_dict`: Create from dictionary representation.

Args:
    data: Dictionary representation
    
Returns:
    DeltaRecord: Reconstructed delta record

### `DeltaCompressor`

**Line:** 139  
**Description:** Delta compression engine for efficient state difference tracking.

This class handles the detection, compression, and management of 
incremental changes between data states.

**Methods (10 total):**
- `__init__`: Initialize the delta compressor.

Args:
    strategy: Delta compression strategy to use
    enable_compression: Whether to enable compression
    compression_level: Compression level (1-9, higher is more compression)
- `calculate_delta`: Calculate delta between two states.

Args:
    old_state: Previous state
    new_state: Current state
    include_unchanged: Whether to include unchanged values
    
Returns:
    Dict[str, Any]: Delta information including changes and removals
- `_dict_delta`: Calculate dictionary-based delta.

Args:
    old_state: Previous state dictionary
    new_state: Current state dictionary
    include_unchanged: Whether to include unchanged values
    
Returns:
    Dict[str, Any]: Delta information
- `_binary_delta`: Calculate binary delta using bsdiff if available.

Args:
    old_state: Previous state
    new_state: Current state
    
Returns:
    Dict[str, Any]: Delta information
- `apply_delta`: Apply delta to a base state to produce new state.

Args:
    base_state: Base state to apply delta to
    delta_info: Delta information from calculate_delta
    
Returns:
    Dict[str, Any]: Updated state
    
Raises:
    DeltaCompressionError: If delta application fails
- `create_delta_record`: Create compressed delta record from changes.

Args:
    changes: Dictionary of changes
    removed_keys: List of removed keys
    timestamp: Delta creation timestamp (default: current time)
    
Returns:
    DeltaRecord: Compressed delta record
- `merge_deltas`: Merge multiple deltas into a single delta.

Args:
    deltas: List of deltas to merge
    
Returns:
    Optional[DeltaRecord]: Merged delta or None if input is empty
- `get_compression_stats`: Get compression statistics.

Returns:
    Dict[str, Any]: Dictionary of compression statistics
- `serialize_delta`: Serialize delta record to bytes for storage.

Args:
    delta: Delta record to serialize
    
Returns:
    bytes: Serialized delta data
- `deserialize_delta`: Deserialize delta record from bytes.

Args:
    data: Serialized delta data
    
Returns:
    DeltaRecord: Deserialized delta record

### `DeltaChain`

**Line:** 550  
**Description:** Manages chains of delta records for efficient storage and retrieval.

This class handles sequences of delta records, including optimization,
rebaseline, and state reconstruction operations.

**Methods (10 total):**
- `__init__`: Initialize the delta chain manager.

Args:
    delta_strategy: Delta compression strategy
    max_chain_length: Maximum chain length before optimization
    enable_rebase: Whether to enable automatic rebaseline
- `add_delta`: Add a delta to the chain.

Args:
    delta: Delta record to add
- `add_state`: Add a new state to the chain by calculating delta from previous state.

Args:
    state: New state to add
    timestamp: Timestamp for the delta (default: current time)
    
Returns:
    DeltaRecord: Created delta record
- `get_state_at_index`: Get the state at a specific index in the chain.

Args:
    index: Index in the chain (0 is base state)
    
Returns:
    Dict[str, Any]: State at the specified index
    
Raises:
    IndexError: If index is out of range
- `get_current_state`: Get the current (latest) state in the chain.

Returns:
    Dict[str, Any]: Current state
- `get_delta_at_index`: Get a delta record at a specific index in the chain.

Args:
    index: Index in the chain
    
Returns:
    Optional[DeltaRecord]: Delta record or None if index out of range
- `clear_chain`: Clear the delta chain.
- `rebaseline`: Rebaseline the chain by setting current state as new base state.
- `_optimize_chain`: Optimize the delta chain by merging deltas.
- `get_chain_metrics`: Get metrics about the delta chain.

Returns:
    Dict[str, Any]: Dictionary of chain metrics


## Usage Examples

```python
# Import the module
from isolated_recipe.example_numbers.orchestrator.persistence.delta import *

# Use module functions and classes as needed
```


## Dependencies

This module requires the following dependencies:

- `bsdiff4`
- `datetime`
- `difflib`
- `enum`
- `functools`
- `gzip`
- `hashlib`
- `json`
- `logging`
- `numpy`
- `orchestrator.persistence.core`
- `os`
- `time`
- `typing`


## Framework Integration

This module is part of the Framework0 system and integrates with:

- **Context Management System** - for unified configuration
- **Recipe Execution Engine** - for workflow orchestration
- **Logging System** - for centralized logging with debug support


---
*Generated on 2025-10-05 21:24:45 by Framework0 Documentation Generator*
