import asyncio
import os
import httpx
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

# def add(a: int, b: int) -> int:
#     """Add two numbers."""
#     return a + b

# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b

def get_canvas_headers():
    """Get Canvas API headers."""
    api_key = os.getenv("CANVAS_API_KEY")
    base_url = os.getenv("CANVAS_BASE_URL")
    
    if not api_key:
        raise ValueError("CANVAS_API_KEY environment variable is not set")
    if not base_url:
        raise ValueError("CANVAS_BASE_URL environment variable is not set")
    
    base_url = base_url.rstrip("/")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    return base_url, headers

def fetch_canvas_courses() -> List[Dict[str, Any]]:
    """Fetch available courses from Canvas LMS using API key and base URL."""
    base_url, headers = get_canvas_headers()
    url = f"{base_url}/api/v1/courses"
    
    with httpx.Client() as client:
        response = client.get(url, headers=headers, params={"enrollment_state": "active"})
        response.raise_for_status()
        courses = response.json()
        return courses

def fetch_canvas_assignments(course_id: int = None) -> List[Dict[str, Any]]:
    """Fetch assignments from Canvas. If course_id is None, fetches all assignments."""
    base_url, headers = get_canvas_headers()
    
    if course_id:
        url = f"{base_url}/api/v1/courses/{course_id}/assignments"
    else:
        # Fetch assignments from all courses
        url = f"{base_url}/api/v1/users/self/todo"
        # Actually, we need to get all courses first, then get assignments
        courses = fetch_canvas_courses()
        all_assignments = []
        
        with httpx.Client() as client:
            for course in courses:
                course_id = course.get("id")
                if course_id:
                    try:
                        course_url = f"{base_url}/api/v1/courses/{course_id}/assignments"
                        response = client.get(course_url, headers=headers)
                        response.raise_for_status()
                        assignments = response.json()
                        for assignment in assignments:
                            assignment["course_name"] = course.get("name", "Unknown")
                            assignment["course_id"] = course_id
                        all_assignments.extend(assignments)
                    except:
                        continue
        
        return all_assignments
    
    with httpx.Client() as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        assignments = response.json()
        return assignments

def fetch_canvas_grades(course_id: int = None) -> List[Dict[str, Any]]:
    """Fetch grades from Canvas. If course_id is None, fetches grades from all courses."""
    base_url, headers = get_canvas_headers()
    
    if course_id:
        url = f"{base_url}/api/v1/courses/{course_id}/enrollments"
    else:
        # Fetch grades from all courses
        courses = fetch_canvas_courses()
        all_grades = []
        
        with httpx.Client() as client:
            for course in courses:
                course_id = course.get("id")
                if course_id:
                    try:
                        enrollments_url = f"{base_url}/api/v1/courses/{course_id}/enrollments"
                        response = client.get(enrollments_url, headers=headers, params={"type": "StudentEnrollment"})
                        response.raise_for_status()
                        enrollments = response.json()
                        
                        # Get assignments for this course to match with grades
                        assignments_url = f"{base_url}/api/v1/courses/{course_id}/assignments"
                        assignments_response = client.get(assignments_url, headers=headers)
                        assignments = assignments_response.json() if assignments_response.status_code == 200 else []
                        
                        for enrollment in enrollments:
                            if enrollment.get("user_id"):
                                grade_data = {
                                    "course_id": course_id,
                                    "course_name": course.get("name", "Unknown"),
                                    "enrollment": enrollment,
                                    "assignments": assignments
                                }
                                all_grades.append(grade_data)
                    except:
                        continue
        
        return all_grades
    
    with httpx.Client() as client:
        response = client.get(url, headers=headers, params={"type": "StudentEnrollment"})
        response.raise_for_status()
        enrollments = response.json()
        return enrollments

def test_api_directly():
    """Test the Canvas API directly without using the runner."""
    print("=" * 60)
    print("Testing Canvas API directly...")
    print("=" * 60)
    
    try:
        courses = fetch_canvas_courses()
        print(f"✅ API call successful! Found {len(courses)} courses.")
        print("\nCourses:")
        for i, course in enumerate(courses[:5], 1):  # Show first 5 courses
            course_name = course.get("name", "N/A")
            course_id = course.get("id", "N/A")
            print(f"  {i}. [{course_id}] {course_name}")
        
        if len(courses) > 5:
            print(f"  ... and {len(courses) - 5} more courses")
        
        return True
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return False
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP error: {e.response.status_code} - {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return False

async def test_with_runner():
    """Test the Canvas API using Dedalus runner."""
    print("\n" + "=" * 60)
    print("Testing with Dedalus Runner...")
    print("=" * 60)
    
    try:
        client = AsyncDedalus()
        runner = DedalusRunner(client)

        result = await runner.run(
            input="Fetch and display all available Canvas courses", 
            model="openai/gpt-5-mini", 
            tools=[fetch_canvas_courses]
        )

        print(f"\n✅ Runner test successful!")
        print(f"\nResult:\n{result.final_output}")
        return True
    except Exception as e:
        print(f"❌ Runner error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    # Test API directly first
    api_success = test_api_directly()
    
    # Only test with runner if API test passed
    if api_success:
        asyncio.run(test_with_runner())
    else:
        print("\n⚠️  Skipping runner test due to API failure.")

if __name__ == "__main__":
    main()