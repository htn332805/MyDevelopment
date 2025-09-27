import sys

# Open the file
with open('src/core/decorators_v2.py', 'r') as f:
    lines = f.readlines()

# Print specific lines with line numbers
problem_lines = [161, 213, 275, 340, 385, 433, 480, 530]
for line_num in problem_lines:
    print(f"Line {line_num}: {lines[line_num-1].strip()}")
    print(f"Line {line_num+1}: {lines[line_num].strip()}")
    print("---")