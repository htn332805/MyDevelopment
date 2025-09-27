# Quiz Dashboard - Complete Interactive Learning Platform

## Overview

The Quiz Dashboard is a comprehensive interactive learning platform built on Framework0's enhanced architecture. It implements advanced pedagogical algorithms, multi-type question support, and sophisticated user progress tracking with spaced repetition scheduling.

## Key Features

### 🧠 Advanced Learning Algorithms
- **Spaced Repetition (SM-2)**: Implements the SuperMemo-2 algorithm with custom enhancements
- **Adaptive Difficulty**: Dynamic question selection based on user performance patterns
- **Anti-Clustering**: Prevents similar questions from appearing consecutively
- **Weighted Selection**: Multi-factor algorithm considering performance, recency, hashtags, and difficulty

### 📝 Multi-Type Question Support
- **Multiple Choice**: Radio button selection with shuffleable options
- **True/False**: Boolean validation with clear UI indicators
- **Fill-in-the-Blank**: Multiple acceptable answers with LaTeX support
- **Reorder/Sequence**: Drag-and-drop interface for ordering tasks
- **Matching Pairs**: Left/right pair validation with visual feedback

### 📊 Comprehensive Analytics
- **User Progress Tracking**: Individual performance metrics and learning curves
- **Mastery Level Calculation**: Sophisticated algorithm based on accuracy, consistency, and repetition
- **Performance Analytics**: Aggregated statistics with difficulty distribution analysis
- **Learning Streaks**: Motivation tracking with daily engagement monitoring

### 🔧 Technical Architecture
- **Thread-Safe Database**: SQLite operations with connection pooling and WAL mode
- **JSON Schema Validation**: Strict question format validation with detailed error reporting
- **MathJax Integration**: Full LaTeX mathematical notation support
- **Bootstrap Responsive UI**: Mobile-friendly design with custom styling
- **RESTful API**: Complete API for quiz operations and data access

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Framework0 dependencies
- Flask web framework
- SQLite database support

### Quick Start

1. **Install Dependencies**
   ```bash
   cd /home/runner/work/MyDevelopment/MyDevelopment
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python run_quiz_dashboard.py --init-sample-data --debug
   ```

3. **Access the Dashboard**
   - Open your browser to `http://localhost:5000`
   - Choose Student or Instructor role
   - Start learning or creating content

### Command Line Options

```bash
python run_quiz_dashboard.py [OPTIONS]

Options:
  --host HOST              Host address to bind to (default: 127.0.0.1)
  --port PORT              Port to listen on (default: 5000)
  --debug                  Enable debug mode
  --database PATH          Database file path (default: quiz_dashboard.db)
  --init-sample-data       Initialize with sample questions
```

## Question Format Specification

### Multiple Choice Questions
```json
{
  "type": "multiple_choice",
  "title": "Question Title",
  "content": "Question text with optional $LaTeX$ support",
  "explanation": "Detailed explanation for learning",
  "difficulty": 3,
  "estimated_time": 60,
  "hashtags": ["topic1", "topic2"],
  "options": [
    {"id": "a", "text": "Option A"},
    {"id": "b", "text": "Option B"}
  ],
  "correct_answer": "a",
  "shuffle_options": true
}
```

### True/False Questions
```json
{
  "type": "true_false",
  "title": "Statement Validation",
  "content": "Statement to be evaluated",
  "correct_answer": true,
  "explanation": "Why this is true/false"
}
```

### Fill-in-the-Blank Questions
```json
{
  "type": "fill_in_blank",
  "title": "Complete the Code",
  "content": "Complete: _____(\"Hello World\")",
  "acceptable_answers": ["print", "print()"],
  "case_sensitive": false
}
```

### Reorder/Sequence Questions
```json
{
  "type": "reorder_sequence",
  "title": "Sort the Steps",
  "content": "Arrange in correct order:",
  "items": [
    {"id": "step1", "text": "First step"},
    {"id": "step2", "text": "Second step"}
  ],
  "correct_order": ["step1", "step2"],
  "partial_credit": true
}
```

### Matching Pairs Questions
```json
{
  "type": "matching_pairs",
  "title": "Match Items",
  "content": "Connect related items:",
  "left_items": [{"id": "left1", "text": "Item A"}],
  "right_items": [{"id": "right1", "text": "Match A"}],
  "correct_matches": [
    {"left_id": "left1", "right_id": "right1"}
  ]
}
```

## API Documentation

### Question Management
- `GET /api/questions/search` - Search questions with filters
- `POST /api/questions/validate` - Validate question format
- `GET /api/questions/{id}` - Get specific question

### User Progress
- `GET /api/user/{id}/progress` - Get user statistics
- `GET /api/quiz/recommendations/{id}` - Get personalized recommendations

### Quiz Sessions
- `POST /quiz/start` - Start new quiz session
- `GET /quiz/{session}/question` - Get next question
- `POST /quiz/{session}/submit` - Submit answer
- `POST /quiz/{session}/complete` - Complete session

## Database Schema

The application uses a comprehensive SQLite schema with the following key tables:

- **users**: User accounts and profiles
- **questions**: Question content with flexible JSON data
- **quiz_sessions**: Individual quiz-taking sessions
- **quiz_attempts**: Detailed attempt tracking
- **user_progress**: Spaced repetition and mastery data
- **question_tags**: Flexible tagging system
- **performance_analytics**: Aggregated statistics

## Spaced Repetition Algorithm

The SM-2 implementation includes:

- **Easiness Factor**: Dynamic adjustment (1.3 - 4.0)
- **Interval Calculation**: Exponential spacing based on performance
- **Performance Scoring**: 0-5 scale incorporating time and confidence
- **Mastery Tracking**: Comprehensive proficiency measurement

## Web Interface

### Student Dashboard
- Personal progress overview
- Quiz session configuration
- Recommended questions based on SR algorithm
- Learning streak tracking
- Performance analytics

### Instructor Dashboard  
- Question creation and management
- Bulk question import
- Student analytics
- Content organization tools

### Quiz Interface
- Responsive question display
- Interactive answer interfaces for all question types
- Real-time progress tracking
- Detailed feedback with explanations
- MathJax rendering for mathematical content

## Testing

Run the comprehensive test suite:

```bash
python -m pytest tests/test_quiz_dashboard.py -v
```

Test coverage includes:
- Database operations and thread safety
- Question validation and CRUD operations
- Spaced repetition algorithms
- Web application endpoints
- Integration workflows

## Customization

### Adding Question Types
1. Extend `QuestionType` enum in `models.py`
2. Add schema validation in `question_manager.py`
3. Implement UI rendering in quiz interface templates
4. Add evaluation logic in `web_app.py`

### Modifying SM-2 Parameters
Configure spaced repetition in `spaced_repetition.py`:
```python
SM2Parameters(
    initial_easiness=2.5,
    min_easiness=1.3,
    max_easiness=4.0,
    # ... other parameters
)
```

### Custom Styling
Modify Bootstrap theme in `templates/base.html` or add custom CSS files.

## Performance Considerations

- Database connection pooling for concurrent access
- Efficient indexing on frequently queried fields
- JSON field optimization for question data
- WAL mode for improved concurrent writes
- Memory-efficient question selection algorithms

## Security Features

- Input validation and sanitization
- SQL injection prevention
- XSS protection in templates
- Session management
- Error handling without information disclosure

## Framework0 Integration

Built on Framework0's enhanced architecture:
- Comprehensive logging system
- Error handling with graceful degradation
- Component lifecycle management
- Event-driven architecture
- Plugin system compatibility

## Contributing

Follow Framework0 development standards:
- Maintain backward compatibility
- Add comprehensive tests
- Include inline documentation
- Use type hints throughout
- Follow PEP 8 style guidelines

## License

This Quiz Dashboard implementation is part of the Framework0 project and follows the same licensing terms.

---

**Built with Framework0 Enhanced Architecture**  
*Spaced Repetition • Adaptive Learning • Performance Analytics*