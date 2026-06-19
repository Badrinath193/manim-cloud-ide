"""
Manim Cloud Renderer - Uses GitHub Actions for rendering
Write code, trigger render on GitHub, download the video!
"""
import streamlit as st
import requests
import time
import os
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Manim Cloud Renderer",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    .stTextArea textarea {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
    }
    .stButton button {
        background: linear-gradient(90deg, #e94560, #0f3460);
        color: white;
        border: none;
    }
    h1, h2, h3 {
        color: #e94560 !important;
    }
    .success-box {
        padding: 1rem;
        background: rgba(233, 69, 96, 0.1);
        border-left: 4px solid #e94560;
        border-radius: 0.5rem;
    }
    .info-box {
        padding: 1rem;
        background: rgba(0, 123, 255, 0.1);
        border-left: 4px solid #007bff;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Manim Cloud Renderer")
st.markdown("Write Manim code → GitHub Actions renders it → Download!")

# Default example
DEFAULT_CODE = '''from manim import *

class CircleToSquare(Scene):
    def construct(self):
        circle = Circle(fill_opacity=0.5, color=BLUE)
        circle.shift(LEFT * 2)

        square = Square(fill_opacity=0.5, color=ORANGE)
        square.shift(RIGHT * 2)

        circle_label = Text("Circle", font_size=36).next_to(circle, DOWN)
        square_label = Text("Square", font_size=36).next_to(square, DOWN)

        self.play(Write(circle), Write(circle_label))
        self.wait(0.5)

        self.play(
            Transform(circle.copy().set_color(ORANGE), square),
            circle.animate.set_opacity(0),
            circle_label.animate.next_to(square, DOWN),
            Write(square_label),
            run_time=2
        )

        self.play(Rotate(square, angle=TAU), run_time=2)

        message = Text("Manim in the Cloud!", font_size=48, color=GOLD)
        message.to_edge(UP, buff=0.5)
        self.play(Write(message), run_time=1.5)

        self.wait(2)
'''

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    quality = st.selectbox(
        "Quality",
        ["l (720p)", "m (1080p)", "h (1440p)", "k (4K)"],
        index=0
    )
    quality_map = {"l (720p)": "l", "m (1080p)": "m", "h (1440p)": "h", "k (4K)": "k"}
    quality_flag = quality_map[quality]

    st.markdown("---")
    st.markdown("**How it works:**")
    st.markdown("""
    1. Write your Manim code
    2. Click **Render**
    3. Code is pushed to GitHub
    4. GitHub Actions renders it
    5. Download the video!
    """)
    st.markdown("---")
    st.markdown("**Status:** Check [Actions](https://github.com/Badrinath193/manim-cloud-ide/actions) tab")

# Session state for tracking
if 'render_id' not in st.session_state:
    st.session_state.render_id = None
if 'video_url' not in st.session_state:
    st.session_state.video_url = None

# Main content
code_input = st.text_area(
    "📝 Manim Code",
    value=DEFAULT_CODE,
    height=400,
    placeholder="Paste your Manim code here..."
)

col1, col2 = st.columns([1, 4])
with col1:
    render_btn = st.button("🎬 Render", type="primary")

if render_btn:
    if not code_input.strip():
        st.error("Please enter some Manim code!")
    else:
        with st.spinner("Pushing code to GitHub..."):
            # Write code to file
            with open("temp_scene.py", "w") as f:
                f.write(code_input)

            # Git add, commit, push
            os.system('git add temp_scene.py')
            os.system('git commit -m "Render request"')
            os.system('git push origin main')

            st.success("✅ Code pushed to GitHub!")
            st.info("🚀 GitHub Actions is rendering... Check the Actions tab!")

            st.markdown("""
            <div class="info-box">
            <b>Next steps:</b><br>
            1. Go to <a href="https://github.com/Badrinath193/manim-cloud-ide/actions" target="_blank">GitHub Actions</a><br>
            2. Wait for the workflow to complete<br>
            3. Download from "Artifacts"
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# Alternative: Show how to use GitHub Actions directly
st.markdown("### 📋 Alternative: Use GitHub Actions Directly")

st.markdown("""
1. Go to **[manim-cloud-ide/actions](https://github.com/Badrinath193/manim-cloud-ide/actions)**
2. Click **"Render Manim"** workflow
3. Click **"Run workflow"**
4. Wait for completion
5. Download from **Artifacts** ( expires in 7 days)
""")

# Show last commit info
st.markdown("### 📊 Repository Status")
try:
    import subprocess
    result = subprocess.run(['git', 'log', '-1', '--oneline'], capture_output=True, text=True, cwd='.')
    if result.returncode == 0 and result.stdout:
        st.markdown(f"Last commit: `{result.stdout.strip()}`")
except:
    pass