from app.classification import classify_document

sample_text = """
Lecture 4: Introduction to Operating Systems 
Today we will cover process scheduling, including round-robin 
and priority-based scheduling algorithms. Key definitions: 
a process is a program in execution...
"""

result = classify_document(sample_text)
print(result)