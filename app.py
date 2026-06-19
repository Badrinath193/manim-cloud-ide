"""
Manim Web Renderer - Streamlit App
Upload or paste Manim code, render, and download the video!
"""
import streamlit as st
import subprocess
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Manim Renderer",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for aesthetics
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
</style>
""", unsafe_allow_html=True)

st.title("🎬 Manim Cloud Renderer")
st.markdown("Write Manim code, render, and download!")

# Default example code
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

# Sidebar for settings
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
    st.markdown("**Instructions:**")
    st.markdown("""
    1. Write/paste Manim code
    2. Click **Render**
    3. Download your video!
    """)

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
        with st.spinner("Rendering... this may take a minute..."):
            # Create temp directory
            with tempfile.TemporaryDirectory() as tmpdir:
                # Write the code to a file
                manim_file = Path(tmpdir) / "scene.py"
                manim_file.write_text(code_input)

                # Extract scene class name
                import re
                match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', code_input)
                if match:
                    scene_name = match.group(1)
                else:
                    scene_name = "Scene"

                # Run manim
                output_dir = Path(tmpdir) / "media"
                cmd = [
                    sys.executable, "-m", "manim",
                    "-ql", str(manim_file), scene_name,
                    "--output_file", "animation",
                    "-v", "ERROR"
                ]

                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        cwd=tmpdir,
                        timeout=300
                    )

                    if result.returncode != 0:
                        st.error("Render failed!")
                        st.code(result.stderr)
                    else:
                        # Find the rendered video
                        videos = list(output_dir.rglob("*.mp4"))

                        if videos:
                            video_path = videos[0]
                            st.markdown('<div class="success-box">✅ Render complete!</div>', unsafe_allow_html=True)

                            # Show video
                            st.video(str(video_path))

                            # Download button
                            with open(video_path, "rb") as f:
                                st.download_button(
                                    label="⬇️ Download Video",
                                    data=f.read(),
                                    file_name=f"{scene_name}.mp4",
                                    mime="video/mp4"
                                )
                        else:
                            st.error("No video file found!")

                except subprocess.TimeoutExpired:
                    st.error("Render timed out! Try lower quality.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("💡 *Tip: Use GitHub Actions for high-quality renders*")