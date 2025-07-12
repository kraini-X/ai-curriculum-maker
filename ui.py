import os
import streamlit as st
from rag_util import extract_text_from_pdf, create_vector_store, get_relevant_chunks
from agents import topic_decomposer, lesson_planner, quiz_generator, resource_recommender, assignment_maker, export_to_pdf

st.set_page_config(page_title="AI Curriculum Planner", layout="wide")


st.title("📚 AI Curriculum Planner")


st.markdown("### 📄 Upload Your Syllabus")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    st.success("✅ File uploaded successfully!")
    os.makedirs("data", exist_ok=True)
    save_path = os.path.join("data", uploaded_file.name)

    if "syllabus_text" not in st.session_state:
        uploaded_file.seek(0)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        syllabus_text = extract_text_from_pdf(save_path)
        st.session_state["syllabus_text"] = syllabus_text

        progress = st.progress(0, text="🔍 Extracting text...")
        progress.progress(30, text="📄 Text extracted. Splitting into chunks...")

        create_vector_store(syllabus_text)
        st.session_state["vector_store_created"] = True

        progress.progress(100, text="✅ Vector store created!")
    else:
        syllabus_text = st.session_state["syllabus_text"]

    with st.expander("📘 Preview Extracted Syllabus Text"):
        st.markdown(syllabus_text[:2000] + "..." if len(syllabus_text) > 2000 else syllabus_text)

    st.success("🎉 Syllabus processed! You can now generate your curriculum.")
    st.divider()


st.markdown("### 🧠 Curriculum Planning")
user_topic = st.text_input("🔎 Enter a topic to generate curriculum (e.g., 'Quantum Mechanics')")

if user_topic:
    if "context" not in st.session_state or st.session_state.get("last_topic") != user_topic:
        with st.spinner("🔍 Retrieving relevant syllabus context..."):
            context = get_relevant_chunks(user_topic, top_k=3)
            st.session_state["context"] = context
            st.session_state["last_topic"] = user_topic
    else:
        context = st.session_state["context"]

    if "weekly_plan" not in st.session_state:
        with st.spinner("🪄 Generating weekly subtopics..."):
            weekly_plan = topic_decomposer(user_topic, context)
            st.session_state["weekly_plan"] = weekly_plan

    st.markdown("#### 📅 Weekly Curriculum Plan")
    with st.expander("📋 View Weekly Plan"):
        st.markdown(st.session_state["weekly_plan"])

    st.divider()

    if st.button("📘 Generate Lesson Plan"):
        with st.spinner("📚 Creating detailed lesson plan..."):
            st.session_state["detailed_plan"] = lesson_planner(st.session_state["weekly_plan"])

        st.markdown("#### 📚 Detailed Lesson Plan")
        with st.expander("📖 View Full Lesson Plan"):
            st.markdown(st.session_state["detailed_plan"])
        st.success("🎓 Curriculum generation complete!")

    if st.button("📝 Generate Quiz"):
        with st.spinner("📝 Creating quiz questions..."):
            st.session_state["quiz"] = quiz_generator(st.session_state["weekly_plan"])

        st.markdown("#### 📝 Quiz Questions")
        with st.expander("📋 View Quiz Questions"):
            st.markdown(st.session_state["quiz"])
        st.success("✅ Quiz generation complete!")

    if st.button("🔗 Resource Recommendations"):
        with st.spinner("🔗 Fetching resource recommendations..."):
            st.session_state["resources"] = resource_recommender(st.session_state["weekly_plan"])

        st.markdown("#### 🔗 Recommended Resources")
        with st.expander("📚 View Recommended Resources"):
            st.markdown(st.session_state["resources"])
        st.success("✅ Resource recommendations complete!")

    if st.button("📝 Generate Assignments"):
        with st.spinner("✏️ Creating student assignments..."):
            st.session_state["assignments"] = assignment_maker(st.session_state["weekly_plan"])

        st.markdown("#### 📝 Weekly Assignments")
        with st.expander("📄 View Assignments"):
            st.markdown(st.session_state["assignments"], unsafe_allow_html=True)
        st.success("📬 Assignments ready!")
st.divider()
st.markdown("### 📤 Export Selected Curriculum Sections")

options = st.multiselect(
    "✅ Select sections to include in the exported PDF",
    ["Weekly Plan", "Lesson Plan", "Quiz", "Resources", "Assignments"]
)

if st.button("⬇️ Export Selected as PDF"):
    html_parts = []

    if "weekly_plan" not in st.session_state:
        st.warning("⚠️ Weekly Plan must be generated before exporting.")
    else:
        for section in options:
            if section == "Weekly Plan":
                html_parts.append(f"<h2>📅 Weekly Plan</h2><div>{st.session_state.weekly_plan.replace('\n', '<br>')}</div>")

            elif section == "Lesson Plan":
                if "detailed_plan" not in st.session_state:
                    with st.spinner("📘 Generating Lesson Plan..."):
                        st.session_state.detailed_plan = lesson_planner(st.session_state.weekly_plan)
                html_parts.append(f"<h2>📘 Lesson Plan</h2><div>{st.session_state.detailed_plan.replace('\n', '<br>')}</div>")

            elif section == "Quiz":
                if "quiz" not in st.session_state:
                    with st.spinner("📝 Generating Quiz..."):
                        st.session_state.quiz = quiz_generator(st.session_state.weekly_plan)
                html_parts.append(f"<h2>🧠 Quiz</h2><div>{st.session_state.quiz.replace('\n', '<br>')}</div>")

            elif section == "Resources":
                if "resources" not in st.session_state:
                    with st.spinner("🔗 Fetching Resources..."):
                        st.session_state.resources = resource_recommender(st.session_state.weekly_plan)
                html_parts.append(f"<h2>🔗 Resources</h2><div>{st.session_state.resources.replace('\n', '<br>')}</div>")

            elif section == "Assignments":
                if "assignments" not in st.session_state:
                    with st.spinner("📝 Creating Assignments..."):
                        st.session_state.assignments = assignment_maker(st.session_state.weekly_plan)
                html_parts.append(f"<h2>📝 Assignments</h2><div>{st.session_state.assignments.replace('\n', '<br>')}</div>")

        if html_parts:
           
            full_html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: "DejaVu Sans", sans-serif;
            line-height: 1.6;
            color: #2c3e50;
        }}
        h1, h2 {{
            color: #1a5276;
        }}
        div {{
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <h1>📚 AI Curriculum Plan</h1>
    {''.join(html_parts)}
</body>
</html>
'''

            pdf_path = export_to_pdf(full_html)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Curriculum PDF",
                    data=f,
                    file_name="Curriculum_Plan.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("⚠️ Please select at least one section to export.")
