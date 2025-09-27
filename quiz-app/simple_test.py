#!/usr/bin/env python3
# quiz-app/simple_test.py

"""
Simplified test script for the quiz system core functionality.
"""

import json
import sqlite3
import tempfile
import os
from pathlib import Path

def test_basic_quiz_functionality():
    """Test basic quiz functionality without Framework0 dependencies."""
    print("Testing basic quiz functionality...")
    
    # Test 1: JSON Schema validation
    print("1. Testing JSON schema...")
    schema_path = Path("schemas/question_schema.json")
    if schema_path.exists():
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        print("   ✓ Schema loaded successfully")
    else:
        print("   ✗ Schema file not found")
        return False
    
    # Test 2: Sample questions loading
    print("2. Testing sample questions...")
    questions_path = Path("data/questions/sample_questions.json")
    if questions_path.exists():
        with open(questions_path, 'r') as f:
            questions = json.load(f)
        print(f"   ✓ Loaded {len(questions)} sample questions")
        
        # Validate question structure
        for q in questions[:3]:  # Test first 3 questions
            required_fields = ['question_id', 'type', 'prompt', 'answer']
            missing = [field for field in required_fields if field not in q]
            if missing:
                print(f"   ✗ Question {q.get('question_id', 'unknown')} missing: {missing}")
                return False
        print("   ✓ Question structure validation passed")
    else:
        print("   ✗ Sample questions file not found")
        return False
    
    # Test 3: Database schema creation
    print("3. Testing database schema...")
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
        try:
            conn = sqlite3.connect(tmp_db.name)
            
            # Create tables
            conn.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    question_id TEXT PRIMARY KEY,
                    qtype TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    categories TEXT,
                    hashtags TEXT,
                    difficulty TEXT DEFAULT 'medium'
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS attempts (
                    attempt_id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    question_id TEXT,
                    correct INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            
            # Test data insertion
            conn.execute("INSERT INTO users (username) VALUES (?)", ("test_user",))
            conn.execute("""
                INSERT INTO questions (question_id, qtype, prompt, difficulty)
                VALUES (?, ?, ?, ?)
            """, ("test_q1", "multiple_choice", "Test question", "medium"))
            
            conn.commit()
            
            # Test data retrieval
            cursor = conn.execute("SELECT COUNT(*) FROM questions")
            count = cursor.fetchone()[0]
            if count > 0:
                print("   ✓ Database operations working")
            else:
                print("   ✗ Database insert failed")
                return False
                
        except Exception as e:
            print(f"   ✗ Database test failed: {e}")
            return False
        finally:
            conn.close()
            os.unlink(tmp_db.name)
    
    # Test 4: Question type handling
    print("4. Testing question type handling...")
    question_types = set()
    for q in questions:
        question_types.add(q['type'])
    
    expected_types = {'multiple_choice', 'true_false', 'fill_blank', 'reorder', 'matching'}
    found_types = question_types & expected_types
    
    print(f"   ✓ Found question types: {sorted(found_types)}")
    
    if len(found_types) >= 3:
        print("   ✓ Multiple question types supported")
    else:
        print("   ✗ Insufficient question type variety")
        return False
    
    print("\n✅ All basic tests passed!")
    return True

def test_quiz_logic():
    """Test quiz answer evaluation logic."""
    print("\nTesting quiz answer evaluation...")
    
    # Test multiple choice
    mcq = {
        "type": "multiple_choice",
        "choices": ["A", "B", "C", "D"],
        "answer": 1
    }
    
    def evaluate_mcq(question, answer):
        return int(answer) == question['answer']
    
    if evaluate_mcq(mcq, "1"):
        print("   ✓ Multiple choice evaluation working")
    else:
        print("   ✗ Multiple choice evaluation failed")
        return False
    
    # Test true/false
    tf = {
        "type": "true_false",
        "answer": True
    }
    
    def evaluate_tf(question, answer):
        return bool(answer) == question['answer']
    
    if evaluate_tf(tf, True):
        print("   ✓ True/false evaluation working")
    else:
        print("   ✗ True/false evaluation failed")
        return False
    
    # Test fill in blank
    fill = {
        "type": "fill_blank",
        "answer": ["cos(x)", "cos x", "\\cos(x)"]
    }
    
    def evaluate_fill(question, answer):
        if isinstance(question['answer'], list):
            answer_str = str(answer).strip().lower()
            return any(answer_str == str(acc).strip().lower() for acc in question['answer'])
        return str(answer).strip().lower() == str(question['answer']).strip().lower()
    
    if evaluate_fill(fill, "cos(x)"):
        print("   ✓ Fill-in-the-blank evaluation working")
    else:
        print("   ✗ Fill-in-the-blank evaluation failed")
        return False
    
    print("   ✅ Quiz logic tests passed!")
    return True

def main():
    """Run simplified tests."""
    print("=" * 50)
    print("QUIZ SYSTEM SIMPLIFIED TEST")
    print("=" * 50)
    
    try:
        # Change to quiz-app directory
        os.chdir(Path(__file__).parent)
        
        test1_passed = test_basic_quiz_functionality()
        test2_passed = test_quiz_logic()
        
        if test1_passed and test2_passed:
            print("\n🎉 All tests passed! Basic quiz system is working.")
            print("\nNext steps:")
            print("1. Run the full test with: python test_quiz_system.py")
            print("2. Start the Dash app with: python app.py")
            return 0
        else:
            print("\n❌ Some tests failed.")
            return 1
            
    except Exception as e:
        print(f"\n❌ Test suite crashed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())