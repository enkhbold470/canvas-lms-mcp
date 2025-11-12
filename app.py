from flask import Flask, render_template, request, jsonify
from tool import fetch_canvas_courses, fetch_canvas_assignments, fetch_canvas_grades
from datetime import datetime
import os
import asyncio
from dedalus_labs import AsyncDedalus, DedalusRunner

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Main dashboard showing courses, assignments, homework, and grades."""
    try:
        # Fetch all data
        courses = fetch_canvas_courses()
        assignments = fetch_canvas_assignments()
        grades = fetch_canvas_grades()
        
        # Process assignments - separate homework from other assignments
        homework = []
        other_assignments = []
        
        for assignment in assignments:
            assignment_type = assignment.get("submission_types", [])
            due_date = assignment.get("due_at")
            
            # Format due date
            if due_date:
                try:
                    dt = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
                    assignment["due_date_formatted"] = dt.strftime("%B %d, %Y at %I:%M %p")
                    assignment["due_date_iso"] = dt.isoformat()
                except:
                    assignment["due_date_formatted"] = due_date
                    assignment["due_date_iso"] = due_date
            
            # Categorize as homework or assignment
            if "online_upload" in assignment_type or "online_text_entry" in assignment_type:
                homework.append(assignment)
            else:
                other_assignments.append(assignment)
        
        # Process grades
        processed_grades = []
        for grade_data in grades:
            enrollment = grade_data.get("enrollment", {})
            course_name = grade_data.get("course_name", "Unknown")
            course_id = grade_data.get("course_id")
            
            current_score = enrollment.get("grades", {}).get("current_score")
            final_score = enrollment.get("grades", {}).get("final_score")
            
            processed_grades.append({
                "course_id": course_id,
                "course_name": course_name,
                "current_score": current_score,
                "final_score": final_score,
                "computed_current_score": enrollment.get("grades", {}).get("computed_current_score"),
                "computed_final_score": enrollment.get("grades", {}).get("computed_final_score")
            })
        
        return render_template('dashboard.html',
                             courses=courses,
                             homework=homework,
                             assignments=other_assignments,
                             grades=processed_grades)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/api/ai-companion', methods=['POST'])
def ai_companion():
    """Handle AI companion chat requests."""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get context about courses, assignments, etc.
        try:
            courses = fetch_canvas_courses()
            assignments = fetch_canvas_assignments()
            grades = fetch_canvas_grades()
            
            context = f"""You are an AI assistant helping a student with their Canvas LMS courses.

Student's Courses ({len(courses)} total):
"""
            for course in courses[:5]:  # Limit to first 5 for context
                context += f"- {course.get('name', 'Unknown')} (ID: {course.get('id')})\n"
            
            context += f"\nTotal Assignments: {len(assignments)}\n"
            context += f"Total Courses with Grades: {len(grades)}\n\n"
            
            enhanced_prompt = f"""{context}

Student Question: {user_message}

Please provide a helpful, friendly response. You can help with:
- Questions about their courses
- Assignment due dates and details
- Grade information
- Study tips and academic advice
- General Canvas LMS questions

Be concise but helpful."""
        except:
            enhanced_prompt = user_message
        
        # Use Dedalus runner for AI response
        async def get_ai_response():
            client = AsyncDedalus()
            runner = DedalusRunner(client)
            result = await runner.run(
                input=enhanced_prompt,
                model="openai/gpt-4o",
                stream=False
            )
            return result.final_output
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ai_response = loop.run_until_complete(get_ai_response())
        loop.close()
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

