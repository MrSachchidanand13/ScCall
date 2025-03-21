from flask import Flask, render_template, request, jsonify
from functools import lru_cache
import json

app = Flask(__name__)

@lru_cache(maxsize=1)
def load_students_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file).get('students', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/students', methods=['GET'])
def get_students():
    query = request.args.get('q', '').lower()
    page = int(request.args.get('page', 1))
    per_page = 20  # Load 20 students at a time
    
    students_data = load_students_data()
    start = (page - 1) * per_page
    end = start + per_page
    
    if not query:
        paginated_students = students_data[start:end]
        has_more = end < len(students_data)
        return jsonify({'students': paginated_students, 'has_more': has_more})
    
    filtered_students = []
    for student in students_data:
        name = student.get('Name', '').lower()
        primary = student.get('Primary Mobile', '')
        secondary = student.get('Secondary Mobile', '')
        admission = student.get('Admission No', '').lower()
        
        if (query in name or 
            query in primary or 
            query in secondary or 
            query in admission or
            any(query in str(value).lower() for value in student.values())):
            filtered_students.append(student)
    
    paginated_students = filtered_students[start:end]
    has_more = end < len(filtered_students)
    return jsonify({'students': paginated_students, 'has_more': has_more})

if __name__ == '__main__':
    app.run(debug=True)