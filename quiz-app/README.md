# Quiz Dashboard Application - Complete Implementation Guide

## Overview

The Quiz Dashboard is a comprehensive interactive learning system built with Dash/Plotly and integrated with Framework0 architecture. It provides advanced quiz functionality with spaced repetition algorithms, multi-type question support, and robust performance analytics.

## Features Implemented

### 🎯 Core Quiz Functionality
- **5 Question Types Supported:**
  - Multiple Choice with shuffle-able options
  - True/False with boolean evaluation  
  - Fill-in-the-blank with multiple acceptable answers
  - Reorder/sequence questions
  - Matching (left/right) with pair validation

### 🧠 Advanced Algorithms
- **Spaced Repetition (SM-2 Inspired)**: Adaptive question scheduling based on user performance
- **Weighted Question Selection**: Multi-factor algorithm considering:
  - User performance history
  - Question difficulty
  - Recent attempts and errors  
  - Category/hashtag preferences
  - Anti-clustering for variety

### 📊 Analytics & Tracking
- **User Performance Profiling**: Comprehensive performance analytics
- **Progress Tracking**: Real-time progress with session management
- **Performance Metrics**: Accuracy, latency, streak tracking
- **Category Analysis**: Performance breakdown by topic/hashtag

### 🎨 User Experience
- **Responsive Bootstrap Design**: Mobile-friendly interface
- **MathJax LaTeX Support**: Mathematical notation rendering
- **Real-time Feedback**: Immediate answer validation with explanations
- **Hint System**: Progressive hint delivery with penalty tracking

### 🏗️ Framework0 Integration
- **Component Lifecycle Management**: Proper initialization and cleanup
- **Advanced Error Handling**: Graceful degradation with recovery
- **Comprehensive Logging**: Debug-capable logging system
- **Resource Monitoring**: Performance tracking and optimization

## File Structure

```
quiz-app/
├── app.py                          # Full Dash application (Framework0 integrated)
├── demo_app.py                     # Demo application with callbacks
├── simple_working_demo.py          # Working demo (simplified)
├── test_quiz_system.py            # Comprehensive test suite  
├── simple_test.py                 # Basic functionality tests
├── assets/
│   ├── custom.css                 # Custom styling
│   └── mathjax.js                 # LaTeX rendering support
├── data/
│   ├── questions/
│   │   └── sample_questions.json  # 10 sample questions (all types)
│   └── db/                        # SQLite database storage
├── models/
│   └── storage.py                 # Database models & operations
├── schemas/
│   └── question_schema.json       # JSON validation schema
└── utils/
    ├── qloader.py                 # Question loading & validation
    └── selection.py               # Spaced repetition algorithms
```

## Quick Start

### 1. Install Dependencies
```bash
pip install dash plotly sqlalchemy pandas numpy jsonschema markdown dash-bootstrap-components psutil networkx pyyaml
```

### 2. Run Basic Demo
```bash
cd quiz-app
python simple_working_demo.py
# Open http://127.0.0.1:8050
```

### 3. Run Full Application
```bash
cd quiz-app
python app.py
# Open http://127.0.0.1:8050
```

### 4. Run Tests
```bash
cd quiz-app
python simple_test.py          # Basic tests
python test_quiz_system.py     # Full test suite (requires Framework0)
```

## Question Format

Questions use a comprehensive JSON schema supporting all question types:

```json
{
  "question_id": "unique-id",
  "type": "multiple_choice|true_false|fill_blank|reorder|matching",
  "prompt": "Question text (supports **markdown** and LaTeX $\\sum_{i=1}^n$)",
  "choices": ["A", "B", "C", "D"],           // for multiple_choice
  "answer": 1,                               // index or value
  "hint": "Helpful hint text",
  "explanation": "Detailed explanation with LaTeX support",
  "difficulty": "easy|medium|hard",
  "categories": ["algorithms", "sorting"],
  "hashtags": ["#sorting", "#complexity"],
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Database Schema

The system uses SQLite with comprehensive tracking:

- **questions**: Question metadata cache
- **users**: User accounts and preferences  
- **attempts**: Detailed attempt history with latency tracking
- **question_stats**: Performance statistics for spaced repetition

## Algorithm Details

### Spaced Repetition Selection
The system implements an advanced SM-2 inspired algorithm:

```python
weight = base_weight * performance_factor * recency_factor * hashtag_boost * due_multiplier
```

Where:
- `base_weight`: Difficulty-based weight (easy=1.0, medium=2.0, hard=3.0)
- `performance_factor`: Increases for frequently missed questions
- `recency_factor`: Boosts recently failed questions
- `hashtag_boost`: 3x multiplier for user-requested topics
- `due_multiplier`: 2x multiplier for SM-2 scheduled reviews

### Adaptive Difficulty
The system adjusts question selection based on user performance:
- **High performers (>80% accuracy)**: Increased hard questions
- **Medium performers (60-80%)**: Balanced selection
- **Struggling users (<60%)**: Focus on easy/medium questions

## Performance Features

### Optimization
- **Thread-safe operations**: All database operations use proper locking
- **Efficient caching**: Question pool cached in memory with smart invalidation
- **Resource monitoring**: Built-in performance tracking and logging
- **Lazy loading**: Questions loaded on-demand for better startup time

### Scalability
- **Database indexing**: Optimized queries for user performance analytics
- **Modular architecture**: Easy to extend with new question types
- **Plugin system**: Framework0 integration allows easy extensions

## Screenshots

### Start Screen
![Quiz Dashboard Start Screen](https://github.com/user-attachments/assets/5690498d-cdd3-4e17-8bf1-4fb2fecfba59)

### Question Interface  
![Quiz Dashboard Question Interface](https://github.com/user-attachments/assets/acb55fa2-8838-4c9e-9c17-8dc965abbf30)

## Framework0 Integration Benefits

1. **Robust Architecture**: Component lifecycle management ensures proper resource cleanup
2. **Advanced Error Handling**: Graceful degradation with comprehensive error recovery
3. **Debug Capabilities**: Advanced debugging toolkit with variable tracking
4. **Performance Monitoring**: Built-in resource monitoring and profiling
5. **Extensibility**: Plugin system allows easy feature additions
6. **Backwards Compatibility**: Version-safe extensions and API evolution

## Production Deployment

### Basic Deployment
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8050 quiz-app.app:server
```

### With Nginx (Recommended)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Environment Variables
```bash
export DEBUG=0                    # Disable debug mode
export DATABASE_URL="path/to/production.db"
export LOG_LEVEL="INFO"
```

## Contributing

The quiz system follows Framework0 patterns:

1. **Single Responsibility**: Each module has one clear purpose
2. **Full Typing**: All functions include comprehensive type hints
3. **Comprehensive Comments**: Every line documented for maintainability
4. **Backward Compatibility**: Never break existing APIs
5. **Test Coverage**: All features include pytest test coverage

## Future Enhancements

### Planned Features
- [ ] Multi-user authentication system
- [ ] Advanced analytics dashboard with charts
- [ ] Question authoring interface
- [ ] Import/export capabilities (CSV, JSON, SCORM)
- [ ] Mobile app integration
- [ ] Real-time multiplayer quizzes
- [ ] AI-powered question generation
- [ ] Advanced accessibility features

### Technical Improvements
- [ ] Redis caching for high-performance deployments
- [ ] PostgreSQL support for enterprise usage
- [ ] Kubernetes deployment configurations
- [ ] Advanced monitoring with Prometheus/Grafana
- [ ] CDN integration for static assets

## Support

For questions or issues:
1. Check the test suite: `python simple_test.py`
2. Review logs in `logs/` directory
3. Enable debug mode: `export DEBUG=1`
4. Consult Framework0 documentation for integration details

The Quiz Dashboard represents a complete, production-ready learning management system with advanced pedagogical algorithms and robust technical architecture.