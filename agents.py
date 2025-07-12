from groq import Groq
import os
from dotenv import load_dotenv
import pdfkit

import tempfile


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)
print("🔑 Loaded API Key:", api_key)

def topic_decomposer(topic, context):
    prompt = f"""
You are a helpful academic assistant. Based on the following syllabus context, decompose the topic "{topic}" into weekly subtopics. Return it as a numbered list.

### Syllabus Context:
{context}
"""
    response=client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful academic assistant."},
            {"role": "user", "content": prompt}]
            ,temperature=0.5
    )
    return response.choices[0].message.content.strip()
    
def lesson_planner(weekly_subtopics):
    prompt = f"""
You are an academic assistant helping to plan lessons for university-level instruction.

Given the following list of weekly subtopics, generate a detailed weekly lesson plan. For **each week**, include:

- A brief summary of what will be covered
- 3–5 **learning objectives**
- 3–5 **key concepts**
- Suggested **daily breakdown** (e.g., Day 1: ..., Day 2: ...)
- At least one **in-class activity** or discussion idea

### Weekly Subtopics:
{weekly_subtopics}

Return the full curriculum in a clean, markdown-style format.
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful academic assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()


def quiz_generator(lesson_plan):
    prompt= f"""
you are an assistant capable of generating quizzes and questions for testing students understanding.Generate 5 questions for each day of the lesson plan provided. Each question should be clear, concise, and test the key concepts covered that day. Include a mix of question types like mcq,short answer,long answer of 1,3 and 5 mark each.Provide atleast 10 questions from each day of the lesson plan.
### Lesson Plan:
# {lesson_plan}
# Return the quiz in a clean, markdown-style format.
# """ 
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful academic assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5

    )
    return response.choices[0].message.content.strip()

def resource_recommender(weekly_plan):
    prompt = f"""
You are an academic assistant. Based on the following weekly curriculum plan, suggest 2 high-quality resources for each week:
- 1 video or online lecture (preferably YouTube or MOOC)
- 1 article or book reference

Only use publicly available resources (no paywalls).
### Weekly Curriculum Plan:
{weekly_plan}

Return the suggestions in this format:

Week X:
- 🎥 Video: [Title] - [URL]
- 📖 Reading: [Title or Chapter] - [Source or Author]
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful academic assistant recommending learning resources."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )
    return response.choices[0].message.content.strip()


def assignment_maker(weekly_subtopics):
    prompt = f"""
You are an academic curriculum assistant. Based on the following weekly subtopics, create thoughtful, real-world assignments to reinforce the topics.

Each assignment should include:
- Title
- Objective (what the student will learn)
- Instructions (step-by-step)
- Deliverables
- (Optional) A simple grading rubric

Generate 1–2 assignments per week. Be creative and align tasks with higher-order thinking skills.

### Weekly Subtopics:
{weekly_subtopics}

Return the output in markdown format, organized week by week.
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful academic assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()




PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

def export_to_pdf(html_content):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdfkit.from_string(html_content, tmp_file.name, configuration=PDFKIT_CONFIG)
        return tmp_file.name