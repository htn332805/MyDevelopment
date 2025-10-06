#!/usr/bin/env python3
"""
Framework0 Quiz System - Incremental Update Usage Examples
Comprehensive demonstration of incremental_update.py functionality

This module demonstrates how to use incremental_update.py within the Framework0
ecosystem for intelligent quiz data management.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import the Framework0 core components
try:
    from src.core.logger import get_logger
    framework_available = True
except ImportError:
    # Fallback for standalone usage
    import logging
    framework_available = False
    
    def get_logger(name):
        return logging.getLogger(name)

# Import the incremental update module (assuming it's in the same directory)
# from incremental_update import (
#     load_option_sets,
#     parse_pairs_field,
#     parse_answer_match,
#     load_csv_rows,
#     merge_question,
#     update_quiz_from_csv
# )

# Note: Since incremental_update.py is provided as content, we'll include the functions
# Here's how you would typically import and use it:

class QuizDataManager:
    """
    Framework0-integrated quiz data management system.
    
    Provides intelligent incremental updates using the Framework0
    logging and configuration systems.
    """
    
    def __init__(self, base_path: str = ".", debug: bool = False):
        """
        Initialize the quiz data manager.
        
        Args:
            base_path: Base directory for quiz data files
            debug: Enable debug logging through Framework0 logger
        """
        self.base_path = Path(base_path)
        self.debug = debug
        
        # Initialize Framework0 logger if available
        if framework_available:
            self.logger = get_logger(__name__, debug=debug)
            self.logger.info("QuizDataManager initialized with Framework0 logging")
        else:
            logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
            self.logger = logging.getLogger(__name__)
            self.logger.info("QuizDataManager initialized with standard logging")
    
    def create_sample_data_structure(self) -> Dict[str, str]:
        """
        Create sample quiz data files for demonstration.
        
        Returns:
            Dictionary mapping file types to their paths
        """
        self.logger.info("Creating sample quiz data structure")
        
        # Create data directory
        data_dir = self.base_path / "quiz_data"
        data_dir.mkdir(exist_ok=True)
        
        file_paths = {}
        
        # 1. Create sample optionSets.csv
        option_sets_path = data_dir / "optionSets.csv"
        with open(option_sets_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['optionSetName', 'optionsDelimited'])
            writer.writerow(['trueFalse', 'True|False'])
            writer.writerow(['yesNo', 'Yes|No'])
            writer.writerow(['planets', 'Earth|Jupiter|Saturn|Neptune|Mars|Venus'])
            writer.writerow(['elements', 'Au|Ag|Fe|Cu|H|O|N|C'])
            writer.writerow(['numbers', '10|20|30|40|50'])
            writer.writerow(['colors', 'Red|Blue|Green|Yellow|Purple|Orange'])
        file_paths['option_sets'] = str(option_sets_path)
        
        # 2. Create sample questions_base.csv (initial questions)
        questions_base_path = data_dir / "questions_base.csv"
        with open(questions_base_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'id', 'template', 'text', 'options_ref', 'options_inline', 
                'pairs', 'answer_mc', 'answer_match', 'hint', 'category', 'difficulty', 'tags'
            ])
            writer.writerow([
                '1', 'mc', 'What is the largest planet?', 'planets', '', 
                '', 'Jupiter', '', 'King of the gods', 'astronomy', '1', 'space'
            ])
            writer.writerow([
                '2', 'tf', 'The sun is a star.', 'trueFalse', '', 
                '', 'True', '', 'Nuclear fusion', 'astronomy', '1', 'space'
            ])
            writer.writerow([
                '3', 'mc', 'What is 2 + 2?', '', '1|2|3|4|5', 
                '', '4', '', 'Basic arithmetic', 'math', '1', 'arithmetic'
            ])
        file_paths['questions_base'] = str(questions_base_path)
        
        # 3. Create sample questions_updates.csv (incremental updates)
        questions_updates_path = data_dir / "questions_updates.csv"
        with open(questions_updates_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'id', 'template', 'text', 'options_ref', 'options_inline', 
                'pairs', 'answer_mc', 'answer_match', 'hint', 'category', 'difficulty', 'tags'
            ])
            # Update existing question 1 with new hint
            writer.writerow([
                '1', 'mc', 'What is the largest planet?', 'planets', '', 
                '', 'Jupiter', '', 'Gas giant with Great Red Spot', 'astronomy', '2', 'space|planets'
            ])
            # Add new question 4
            writer.writerow([
                '4', 'match', 'Match elements to symbols', '', '', 
                'Gold=optionSet:elements|Silver=optionSet:elements|Iron=optionSet:elements', 
                '', 'Gold=Au|Silver=Ag|Iron=Fe', 'Chemical symbols', 'chemistry', '2', 'science'
            ])
            # Add new question 5
            writer.writerow([
                '5', 'tf', 'Water boils at 100°C at sea level.', 'trueFalse', '', 
                '', 'True', '', 'Standard atmospheric pressure', 'chemistry', '1', 'science|basics'
            ])
        file_paths['questions_updates'] = str(questions_updates_path)
        
        # 4. Create initial quiz JSON from base questions
        quiz_path = data_dir / "quiz_complete.json"
        self._create_initial_quiz_json(
            str(option_sets_path), 
            str(questions_base_path), 
            str(quiz_path)
        )
        file_paths['quiz_json'] = str(quiz_path)
        
        self.logger.info(f"Sample data structure created in {data_dir}")
        return file_paths
    
    def _create_initial_quiz_json(self, opt_csv: str, q_csv: str, output_json: str):
        """Create initial quiz JSON using the single CSV loader logic."""
        self.logger.info(f"Creating initial quiz JSON from {q_csv}")
        
        # This would use the build_quiz_json function from single_csv_to_quiz_json.py
        # For demonstration, we'll create a basic structure
        
        # Load option sets
        option_sets = self._load_option_sets(opt_csv)
        
        # Load questions
        questions = self._load_questions_from_csv(q_csv, option_sets)
        
        # Create complete quiz structure
        quiz_data = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Framework0 Quiz System - Incremental Update Demo",
            "description": "Demonstration of incremental update functionality",
            "meta": {
                "version": "1.0.0",
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
                "description": "Initial quiz data created for incremental update demo"
            },
            "optionSets": option_sets,
            "templates": {
                "mc": {
                    "type": "Multiple Choice",
                    "structure": ["text", "options", "answer", "hint?", "category", "difficulty?", "tags?"]
                },
                "tf": {
                    "type": "True/False",
                    "structure": ["text", "answer", "hint?", "category", "difficulty?", "tags?"],
                    "options": "@trueFalse"
                },
                "match": {
                    "type": "Matching",
                    "structure": ["text", "pairs", "answer", "hint?", "category", "difficulty?", "tags?"]
                }
            },
            "questions": questions
        }
        
        # Write JSON file
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(quiz_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Initial quiz JSON created: {output_json}")
    
    def _load_option_sets(self, opt_csv_path: str) -> Dict[str, List[str]]:
        """Load option sets from CSV (simplified version of incremental_update logic)."""
        option_sets = {}
        with open(opt_csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['optionSetName'].strip()
                delim = row.get('optionsDelimited', '').strip()
                options = [opt.strip() for opt in delim.split('|') if opt.strip()] if delim else []
                option_sets[name] = options
        return option_sets
    
    def _load_questions_from_csv(self, q_csv_path: str, option_sets: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Load questions from CSV (simplified version)."""
        questions = []
        with open(q_csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                question = self._parse_question_row(row, option_sets)
                if question:
                    questions.append(question)
        
        questions.sort(key=lambda q: q['id'])
        return questions
    
    def _parse_question_row(self, row: Dict[str, str], option_sets: Dict[str, List[str]]) -> Optional[Dict[str, Any]]:
        """Parse a single question row from CSV."""
        try:
            qid = int(row['id'].strip())
            template = row['template'].strip()
            text = row['text'].strip()
            
            question = {
                'id': qid,
                'template': template,
                'text': text
            }
            
            # Add optional fields
            hint = row.get('hint', '').strip()
            if hint:
                question['hint'] = hint
            
            category = row.get('category', '').strip()
            if category:
                question['category'] = category
            
            difficulty = row.get('difficulty', '').strip()
            if difficulty:
                try:
                    question['difficulty'] = int(difficulty)
                except ValueError:
                    question['difficulty'] = difficulty
            
            tags = row.get('tags', '').strip()
            if tags:
                question['tags'] = [t.strip() for t in tags.split('|') if t.strip()]
            
            # Handle template-specific fields
            if template in ('mc', 'tf'):
                # Options
                opt_ref = row.get('options_ref', '').strip()
                opt_inline = row.get('options_inline', '').strip()
                
                if opt_ref and opt_ref in option_sets:
                    question['options'] = option_sets[opt_ref]
                elif opt_inline:
                    question['options'] = [o.strip() for o in opt_inline.split('|') if o.strip()]
                elif template == 'tf' and 'trueFalse' in option_sets:
                    question['options'] = option_sets['trueFalse']
                
                # Answer
                answer = row.get('answer_mc', '').strip()
                if answer:
                    question['answer'] = answer
            
            elif template == 'match':
                # Parse pairs field
                pairs_field = row.get('pairs', '').strip()
                if pairs_field:
                    question['pairs'] = self._parse_pairs_field(pairs_field)
                
                # Parse answer
                answer_field = row.get('answer_match', '').strip()
                if answer_field:
                    question['answer'] = self._parse_answer_match(answer_field)
            
            return question
            
        except Exception as e:
            self.logger.error(f"Error parsing question row: {e}")
            return None
    
    def _parse_pairs_field(self, pairs_field: str) -> Dict[str, Any]:
        """Parse pairs field for matching questions."""
        pairs = {}
        for part in pairs_field.split('|'):
            part = part.strip()
            if '=' in part:
                left, right = part.split('=', 1)
                left = left.strip()
                right = right.strip()
                if right.startswith('optionSet:'):
                    pairs[left] = {'optionSet': right[10:]}
                else:
                    pairs[left] = {'inline': right.split(';')}
        return pairs
    
    def _parse_answer_match(self, answer_field: str) -> Dict[str, str]:
        """Parse answer field for matching questions."""
        mapping = {}
        for part in answer_field.split('|'):
            part = part.strip()
            if '=' in part:
                left, right = part.split('=', 1)
                mapping[left.strip()] = right.strip()
        return mapping
    
    def demonstrate_incremental_update(self, file_paths: Dict[str, str]):
        """
        Demonstrate the incremental update process step by step.
        
        Args:
            file_paths: Dictionary of file paths from create_sample_data_structure
        """
        self.logger.info("=" * 60)
        self.logger.info("DEMONSTRATING INCREMENTAL UPDATE PROCESS")
        self.logger.info("=" * 60)
        
        # Step 1: Show original quiz structure
        self._show_quiz_state("BEFORE UPDATE", file_paths['quiz_json'])
        
        # Step 2: Demonstrate incremental update
        self.logger.info("\n🔄 Applying incremental updates...")
        self._apply_incremental_update(
            existing_json=file_paths['quiz_json'],
            option_sets_csv=file_paths['option_sets'],
            updates_csv=file_paths['questions_updates'],
            output_json=file_paths['quiz_json'].replace('.json', '_updated.json')
        )
        
        # Step 3: Show updated quiz structure
        updated_path = file_paths['quiz_json'].replace('.json', '_updated.json')
        self._show_quiz_state("AFTER UPDATE", updated_path)
        
        # Step 4: Show detailed differences
        self._show_update_analysis(file_paths['quiz_json'], updated_path)
    
    def _show_quiz_state(self, stage: str, json_path: str):
        """Display the current state of the quiz JSON."""
        self.logger.info(f"\n📊 QUIZ STATE: {stage}")
        self.logger.info("-" * 40)
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                quiz_data = json.load(f)
            
            self.logger.info(f"📁 File: {Path(json_path).name}")
            self.logger.info(f"📋 Title: {quiz_data.get('title', 'N/A')}")
            self.logger.info(f"🏷️  Version: {quiz_data.get('meta', {}).get('version', 'N/A')}")
            self.logger.info(f"📅 Updated: {quiz_data.get('meta', {}).get('updated', 'N/A')}")
            
            # Option sets summary
            option_sets = quiz_data.get('optionSets', {})
            self.logger.info(f"🎭 Option Sets: {len(option_sets)} ({', '.join(option_sets.keys())})")
            
            # Questions summary
            questions = quiz_data.get('questions', [])
            self.logger.info(f"❓ Questions: {len(questions)}")
            
            for q in questions:
                qid = q.get('id', 'N/A')
                qtype = q.get('template', 'N/A')
                category = q.get('category', 'N/A')
                difficulty = q.get('difficulty', 'N/A')
                text = q.get('text', 'N/A')[:50] + "..." if len(q.get('text', '')) > 50 else q.get('text', 'N/A')
                self.logger.info(f"   Q{qid}: [{qtype}] {text} (Cat: {category}, Diff: {difficulty})")
                
        except Exception as e:
            self.logger.error(f"Error reading quiz state: {e}")
    
    def _apply_incremental_update(self, existing_json: str, option_sets_csv: str, 
                                updates_csv: str, output_json: str):
        """
        Apply incremental update using the incremental_update module logic.
        
        This demonstrates the core functionality of incremental_update.py
        """
        self.logger.info(f"📥 Loading existing quiz: {existing_json}")
        self.logger.info(f"📝 Applying updates from: {updates_csv}")
        self.logger.info(f"💾 Output will be saved to: {output_json}")
        
        try:
            # Load existing JSON
            with open(existing_json, 'r', encoding='utf-8') as f:
                quiz_data = json.load(f)
            
            # Update metadata
            quiz_data['meta']['updated'] = datetime.now().isoformat()
            quiz_data['meta']['version'] = "1.1.0"
            quiz_data['title'] = "Framework0 Quiz System - After Incremental Update"
            
            # Load and merge option sets
            new_option_sets = self._load_option_sets(option_sets_csv)
            existing_option_sets = quiz_data.get('optionSets', {})
            
            # Merge option sets (new ones override existing)
            for name, options in new_option_sets.items():
                existing_option_sets[name] = options
                self.logger.info(f"   🎭 Updated option set: {name} ({len(options)} options)")
            
            quiz_data['optionSets'] = existing_option_sets
            
            # Process question updates
            existing_questions = {q['id']: q for q in quiz_data.get('questions', [])}
            
            # Load update rows
            with open(updates_csv, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                update_count = 0
                new_count = 0
                
                for row in reader:
                    qid_str = row.get('id', '').strip()
                    if not qid_str:
                        continue
                    
                    try:
                        qid = int(qid_str)
                    except ValueError:
                        self.logger.warning(f"Skipping invalid question ID: {qid_str}")
                        continue
                    
                    if qid in existing_questions:
                        # Update existing question
                        updated_question = self._merge_question_data(
                            existing_questions[qid], row, existing_option_sets
                        )
                        existing_questions[qid] = updated_question
                        update_count += 1
                        self.logger.info(f"   ✏️  Updated question {qid}: {updated_question.get('text', 'N/A')[:50]}...")
                    else:
                        # Add new question
                        new_question = self._parse_question_row(row, existing_option_sets)
                        if new_question:
                            existing_questions[qid] = new_question
                            new_count += 1
                            self.logger.info(f"   ➕ Added question {qid}: {new_question.get('text', 'N/A')[:50]}...")
            
            # Rebuild questions list
            questions_list = list(existing_questions.values())
            questions_list.sort(key=lambda q: q['id'])
            quiz_data['questions'] = questions_list
            
            # Save updated JSON
            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump(quiz_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Incremental update completed!")
            self.logger.info(f"   📊 Updated {update_count} existing questions")
            self.logger.info(f"   ➕ Added {new_count} new questions")
            self.logger.info(f"   💾 Saved to: {output_json}")
            
        except Exception as e:
            self.logger.error(f"❌ Error during incremental update: {e}")
            raise
    
    def _merge_question_data(self, existing: Dict[str, Any], update_row: Dict[str, str], 
                           option_sets: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Merge update data into existing question.
        
        This implements the core logic from incremental_update.merge_question
        """
        merged = dict(existing)  # Start with existing data
        
        # Update basic fields if provided
        for field in ['template', 'text', 'hint', 'category']:
            value = update_row.get(field, '').strip()
            if value:
                merged[field] = value
            elif field in update_row and update_row[field] == '':
                # Empty string means clear the field
                merged.pop(field, None)
        
        # Handle difficulty
        difficulty = update_row.get('difficulty', '').strip()
        if difficulty:
            try:
                merged['difficulty'] = int(difficulty)
            except ValueError:
                merged['difficulty'] = difficulty
        elif 'difficulty' in update_row and update_row['difficulty'] == '':
            merged.pop('difficulty', None)
        
        # Handle tags
        tags = update_row.get('tags', '').strip()
        if tags:
            merged['tags'] = [t.strip() for t in tags.split('|') if t.strip()]
        elif 'tags' in update_row and update_row['tags'] == '':
            merged.pop('tags', None)
        
        # Handle template-specific updates
        template = merged.get('template', '')
        
        if template in ('mc', 'tf'):
            # Update options
            opt_ref = update_row.get('options_ref', '').strip()
            opt_inline = update_row.get('options_inline', '').strip()
            
            if opt_ref and opt_ref in option_sets:
                merged['options'] = option_sets[opt_ref]
            elif opt_inline:
                merged['options'] = [o.strip() for o in opt_inline.split('|') if o.strip()]
            
            # Update answer
            answer = update_row.get('answer_mc', '').strip()
            if answer:
                merged['answer'] = answer
            elif 'answer_mc' in update_row and update_row['answer_mc'] == '':
                merged.pop('answer', None)
        
        elif template == 'match':
            # Update pairs
            pairs_field = update_row.get('pairs', '').strip()
            if pairs_field:
                merged['pairs'] = self._parse_pairs_field(pairs_field)
            elif 'pairs' in update_row and update_row['pairs'] == '':
                merged.pop('pairs', None)
            
            # Update answer
            answer_field = update_row.get('answer_match', '').strip()
            if answer_field:
                merged['answer'] = self._parse_answer_match(answer_field)
            elif 'answer_match' in update_row and update_row['answer_match'] == '':
                merged.pop('answer', None)
        
        return merged
    
    def _show_update_analysis(self, original_path: str, updated_path: str):
        """Show detailed analysis of what changed during the update."""
        self.logger.info("\n🔍 UPDATE ANALYSIS")
        self.logger.info("-" * 40)
        
        try:
            with open(original_path, 'r', encoding='utf-8') as f:
                original = json.load(f)
            with open(updated_path, 'r', encoding='utf-8') as f:
                updated = json.load(f)
            
            # Compare metadata
            orig_meta = original.get('meta', {})
            upd_meta = updated.get('meta', {})
            
            self.logger.info(f"📋 Version: {orig_meta.get('version')} → {upd_meta.get('version')}")
            self.logger.info(f"📅 Updated: {orig_meta.get('updated')} → {upd_meta.get('updated')}")
            
            # Compare questions
            orig_questions = {q['id']: q for q in original.get('questions', [])}
            upd_questions = {q['id']: q for q in updated.get('questions', [])}
            
            # Find changes
            modified_ids = []
            new_ids = []
            
            for qid, question in upd_questions.items():
                if qid not in orig_questions:
                    new_ids.append(qid)
                else:
                    # Check for modifications
                    orig_q = orig_questions[qid]
                    if self._questions_differ(orig_q, question):
                        modified_ids.append(qid)
            
            self.logger.info(f"📊 Summary:")
            self.logger.info(f"   ✏️  Modified questions: {len(modified_ids)} {modified_ids}")
            self.logger.info(f"   ➕ New questions: {len(new_ids)} {new_ids}")
            
            # Show detailed changes for modified questions
            for qid in modified_ids:
                self.logger.info(f"\n📝 Question {qid} changes:")
                orig_q = orig_questions[qid]
                upd_q = upd_questions[qid]
                
                for key in ['text', 'hint', 'category', 'difficulty', 'tags']:
                    orig_val = orig_q.get(key)
                    upd_val = upd_q.get(key)
                    if orig_val != upd_val:
                        self.logger.info(f"   {key}: {orig_val} → {upd_val}")
            
        except Exception as e:
            self.logger.error(f"Error in update analysis: {e}")
    
    def _questions_differ(self, q1: Dict[str, Any], q2: Dict[str, Any]) -> bool:
        """Check if two questions are different."""
        # Compare all fields except id
        fields_to_compare = ['text', 'template', 'options', 'answer', 'hint', 
                           'category', 'difficulty', 'tags', 'pairs']
        
        for field in fields_to_compare:
            if q1.get(field) != q2.get(field):
                return True
        
        return False


def demo_advanced_integration_scenarios():
    """
    Demonstrate advanced integration scenarios with Framework0.
    """
    print("\n" + "="*60)
    print("ADVANCED FRAMEWORK0 INTEGRATION SCENARIOS")
    print("="*60)
    
    manager = QuizDataManager(debug=True)
    
    # Scenario 1: Automated workflow integration
    print("\n🔄 Scenario 1: Automated Workflow Integration")
    print("-" * 50)
    print("""
    In a Framework0 recipe, you could use incremental_update.py like this:
    
    1. Recipe monitors CSV files for changes
    2. Triggers incremental update automatically
    3. Validates updated quiz JSON
    4. Deploys to quiz application
    5. Logs all changes for audit trail
    """)
    
    # Scenario 2: Multi-environment management
    print("\n🌍 Scenario 2: Multi-Environment Management")
    print("-" * 50)
    print("""
    Framework0 could manage quiz data across environments:
    
    Development → Staging → Production
    
    - Dev: Frequent CSV updates with incremental_update.py
    - Staging: Validation and testing of quiz changes
    - Production: Controlled deployment with rollback capability
    """)
    
    # Scenario 3: Content collaboration workflow
    print("\n👥 Scenario 3: Content Collaboration Workflow")
    print("-" * 50)
    print("""
    Content creators work with CSV files:
    
    1. Subject matter experts edit CSV files
    2. Git commits trigger Framework0 recipe
    3. incremental_update.py processes changes
    4. Quiz app automatically gets new content
    5. Analytics track question performance
    """)


def demo_comprehensive_usage():
    """
    Complete demonstration of incremental_update.py usage.
    """
    print("🚀 Framework0 Quiz System - Incremental Update Demo")
    print("="*60)
    
    # Initialize manager
    manager = QuizDataManager(debug=True)
    
    # Create sample data
    print("\n📁 Step 1: Creating sample quiz data structure...")
    file_paths = manager.create_sample_data_structure()
    
    print(f"\n✅ Created sample files:")
    for file_type, path in file_paths.items():
        print(f"   {file_type}: {path}")
    
    # Demonstrate incremental update
    print("\n🔄 Step 2: Demonstrating incremental update process...")
    manager.demonstrate_incremental_update(file_paths)
    
    # Show advanced scenarios
    demo_advanced_integration_scenarios()
    
    print("\n✅ Demo completed! Check your quiz_data directory for generated files.")


if __name__ == "__main__":
    # Run the comprehensive demonstration
    demo_comprehensive_usage()