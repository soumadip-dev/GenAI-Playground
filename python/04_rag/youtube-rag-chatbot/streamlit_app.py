import streamlit as st

from main import run_pipeline

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="YouTube AI Research Assistant",
    page_icon="🎥",
    layout="centered",
)


# =========================================
# UI
# =========================================

st.title("🎥 YouTube AI Research Assistant")

st.write("Enter a YouTube video URL and ask a question " "about its transcript.")

youtube_url = st.text_input(
    "YouTube URL",
    placeholder="https://youtu.be/7aEAS5E5vjg",
)

question = st.text_area(
    "Your Question",
    placeholder="What is the cost of time?",
    height=100,
)

ask_button = st.button(
    "Ask Question",
    type="primary",
    use_container_width=True,
)


# =========================================
# RUN PIPELINE
# =========================================

if ask_button:
    if not youtube_url.strip():
        st.error("Please enter a YouTube URL.")

    elif not question.strip():
        st.error("Please enter a question.")

    else:
        try:
            with st.spinner("Processing transcript and generating answer..."):
                answer = run_pipeline(
                    youtube_url=youtube_url.strip(),
                    question=question.strip(),
                )

            st.subheader("Answer")
            st.write(answer)

        except ValueError as error:
            st.error(str(error))

        except Exception as error:
            st.error(f"Something went wrong: {error}")
