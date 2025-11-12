import asyncio
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv
from tool import fetch_canvas_courses

load_dotenv()

def format_courses(courses):
    """Format course information for the prompt."""
    if not courses:
        return "No courses found."
    
    formatted = f"Here are all your Canvas courses ({len(courses)} total):\n\n"
    
    for i, course in enumerate(courses, 1):
        course_id = course.get("id", "N/A")
        course_name = course.get("name", "N/A")
        course_code = course.get("course_code", "N/A")
        enrollment_term = course.get("enrollment_term_id", "N/A")
        workflow_state = course.get("workflow_state", "N/A")
        
        formatted += f"{i}. Course ID: {course_id}\n"
        formatted += f"   Name: {course_name}\n"
        formatted += f"   Code: {course_code}\n"
        formatted += f"   Term: {enrollment_term}\n"
        formatted += f"   Status: {workflow_state}\n"
        
        # Add course URL if available
        if course.get("html_url"):
            formatted += f"   URL: {course.get('html_url')}\n"
        
        formatted += "\n"
    
    return formatted

async def main():
    # Fetch courses first
    print("Fetching courses from Canvas API...")
    try:
        courses = fetch_canvas_courses()
        print(f"✅ Successfully fetched {len(courses)} courses\n")
        
        # Format course information
        courses_info = format_courses(courses)
        
        # Create enhanced input with course information
        input_prompt = f"""Based on the following Canvas course information, provide a comprehensive summary and analysis:

{courses_info}

Please:
1. Summarize all the courses in a clear, organized format
2. Identify any patterns or groupings (e.g., by term, department, etc.)
3. Provide insights about your course load
4. Suggest any recommendations or observations

Generate a well-structured, informative response."""
        
        # Use Dedalus runner with the enhanced input
        client = AsyncDedalus()
        runner = DedalusRunner(client)

        result = await runner.run(
            input=input_prompt,
            model="openai/gpt-5-mini",
            stream=False
        )

        print("=" * 60)
        print("COMPLETION RESULT:")
        print("=" * 60)
        print(result.final_output)
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())