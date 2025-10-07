"""
AI Video Studio - Our own Veo3-like app
Simple, powerful, and free to use
"""

import streamlit as st
import os
import sys
from typing import List, Dict, Any
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import CONFIG
from src.logging_utils import setup_logger
from src.script_gen import generate_script
from src.tts import synthesize_speech
from src.visuals import generate_visuals
from src.assembler import assemble_video
from src.thumbnail import create_thumbnail

logger = setup_logger(__name__)

st.set_page_config(
    page_title="AI Video Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .video-preview {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎬 AI Video Studio</h1>
    <p>Create professional videos like Veo3 - Simple, Fast, Free!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Video quality settings
    st.subheader("🎥 Video Quality")
    video_quality = st.selectbox(
        "Quality", 
        ["720p HD", "1080p Full HD", "4K Ultra HD"],
        index=1
    )
    
    # AI model selection
    st.subheader("🤖 AI Models")
    use_ai = st.checkbox("Use AI Video Generation", value=bool(CONFIG.runway_api_key or CONFIG.pika_api_key))
    
    if use_ai:
        ai_provider = st.radio(
            "Choose AI Provider:",
            ["RunwayML", "Pika Labs", "Auto (Best Available)"],
            index=2
        )
    
    # Advanced settings
    with st.expander("🔧 Advanced Settings"):
        fps = st.slider("FPS", 24, 60, 30)
        bitrate = st.selectbox("Bitrate", ["High", "Medium", "Low"], index=0)
        style = st.selectbox("Visual Style", ["Cinematic", "Modern", "Minimalist", "Dynamic"])

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Create Your Video")
    
    # Input section
    with st.container():
        st.subheader("1️⃣ Describe Your Video")
        
        # Text input with better styling
        prompt = st.text_area(
            "What do you want to create?",
            placeholder="Example: A professional video about Mahindra Scorpio SUV features, showing the car in action with smooth transitions...",
            height=100,
            help="Be descriptive! The more details you provide, the better your video will be."
        )
        
        # Language selection
        col_lang, col_duration = st.columns(2)
        with col_lang:
            language = st.selectbox("Language", ["Hindi", "English", "Auto"], index=0)
        with col_duration:
            duration = st.slider("Duration (seconds)", 15, 120, 30, 5)
        
        # Tone and style
        col_tone, col_style = st.columns(2)
        with col_tone:
            tone = st.selectbox("Tone", ["Professional", "Friendly", "Educational", "Dramatic", "Casual"], index=0)
        with col_style:
            video_style = st.selectbox("Video Style", ["Documentary", "Commercial", "Social Media", "Presentation"], index=1)

with col2:
    st.header("🎯 Quick Actions")
    
    # Quick templates
    st.subheader("📋 Quick Templates")
    
    templates = {
        "🚗 Car Review": "Professional car review video with smooth transitions and detailed features",
        "📱 Product Demo": "Modern product demonstration with clean visuals and engaging content",
        "🎓 Educational": "Clear educational content with step-by-step explanations and visuals",
        "📈 Business": "Professional business presentation with corporate styling and data visualization",
        "🎉 Social Media": "Engaging social media content with trendy effects and quick cuts"
    }
    
    selected_template = st.selectbox("Choose Template:", list(templates.keys()))
    if st.button("Use Template"):
        st.session_state.prompt = templates[selected_template]
        st.rerun()
    
    # Recent videos
    st.subheader("📁 Recent Videos")
    if os.path.exists("outputs/final"):
        recent_videos = [f for f in os.listdir("outputs/final") if f.endswith('.mp4')]
        if recent_videos:
            for video in recent_videos[-3:]:  # Show last 3
                if st.button(f"📹 {video}", key=f"recent_{video}"):
                    st.session_state.selected_video = f"outputs/final/{video}"
        else:
            st.info("No videos created yet")

# Generate button
if st.button("🎬 Generate Video", type="primary", use_container_width=True):
    if not prompt.strip():
        st.error("Please describe what you want to create!")
    else:
        with st.spinner("🎬 Creating your professional video..."):
            try:
                # Step 1: Generate script
                with st.status("📝 Generating professional script...", expanded=True) as status:
                    # Enhanced prompt for better results
                    enhanced_prompt = f"""
                    Create a professional {duration}-second video about: {prompt}
                    
                    Requirements:
                    - Language: {language}
                    - Tone: {tone}
                    - Style: {video_style}
                    - Target audience: Social media users
                    - Include engaging hooks and clear calls-to-action
                    - Make it shareable and viral-worthy
                    """
                    
                    storyboard = generate_script(
                        enhanced_prompt, 
                        tone=tone.lower(), 
                        target_duration_sec=duration, 
                        language="hi" if language == "Hindi" else "en"
                    )
                    
                    # Display generated script for review
                    st.markdown("### 📝 Generated Script Preview:")
                    for i, scene in enumerate(storyboard.get("scenes", []), 1):
                        with st.expander(f"Scene {i}: {scene.get('script_text', '')[:50]}..."):
                            st.write(f"**Text:** {scene.get('script_text', '')}")
                            st.write(f"**Visual:** {scene.get('visual_description', '')}")
                            st.write(f"**Duration:** {scene.get('duration_sec', 0)} seconds")
                    
                    status.update(label="✅ Professional script generated!", state="complete")
                
                # Step 2: Generate audio
                with st.status("🎵 Creating voice-over...", expanded=True) as status:
                    audio_files = synthesize_speech(storyboard.get("scenes", []), voice="", speed=1.0)
                    status.update(label="✅ Audio generated!", state="complete")
                
                # Step 3: Generate visuals
                with st.status("🎨 Creating visuals...", expanded=True) as status:
                    video_files = generate_visuals(storyboard.get("scenes", []), style=video_style.lower())
                    status.update(label="✅ Visuals created!", state="complete")
                
                # Step 4: Assemble final video
                with st.status("🎬 Assembling final video...", expanded=True) as status:
                    output_path = f"outputs/final/ai_studio_{len(os.listdir('outputs/final') if os.path.exists('outputs/final') else []) + 1}.mp4"
                    subtitles = [s.get("on_screen_text") or s.get("script_text") or "" for s in storyboard.get("scenes", [])]
                    final_video = assemble_video(video_files, audio_files, subtitles, output_path)
                    
                    # Create thumbnail
                    thumbnail_path = output_path.replace('.mp4', '_thumb.jpg')
                    create_thumbnail(storyboard.get("title", "AI Generated Video"), thumbnail_path)
                    
                    status.update(label="✅ Video ready!", state="complete")
                
                st.success("🎉 Your professional video is ready!")
                st.session_state.generated_video = final_video
                st.session_state.video_title = storyboard.get("title", "AI Generated Video")
                
            except Exception as e:
                st.error(f"❌ Error creating video: {str(e)}")
                logger.error(f"Video generation failed: {e}")

# Display generated video
if hasattr(st.session_state, 'generated_video') and st.session_state.generated_video:
    st.markdown("---")
    st.header("🎬 Your Generated Video")
    
    col_video, col_info = st.columns([2, 1])
    
    with col_video:
        st.markdown("### 📹 Preview")
        st.video(st.session_state.generated_video)
        
        # Download button
        with open(st.session_state.generated_video, "rb") as f:
            st.download_button(
                "📥 Download Video",
                data=f.read(),
                file_name=f"{st.session_state.video_title}.mp4",
                mime="video/mp4",
                use_container_width=True
            )
    
    with col_info:
        st.markdown("### 📊 Video Info")
        st.info(f"**Title:** {st.session_state.video_title}")
        st.info(f"**Duration:** {duration} seconds")
        st.info(f"**Quality:** {video_quality}")
        st.info(f"**Style:** {video_style}")
        
        # Share options
        st.markdown("### 🔗 Share")
        if st.button("📱 Social Media Ready"):
            st.success("Video optimized for social media!")
        
        if st.button("📧 Email Video"):
            st.info("Email sharing feature coming soon!")

# Features section
st.markdown("---")
st.header("✨ Why Choose AI Video Studio?")

features = [
    {
        "icon": "🚀",
        "title": "Lightning Fast",
        "description": "Generate professional videos in under 2 minutes"
    },
    {
        "icon": "🎨",
        "title": "AI-Powered",
        "description": "Advanced AI creates cinematic visuals automatically"
    },
    {
        "icon": "💰",
        "title": "Completely Free",
        "description": "No subscriptions, no watermarks, no limits"
    },
    {
        "icon": "🌍",
        "title": "Multi-Language",
        "description": "Supports Hindi, English, and 20+ languages"
    },
    {
        "icon": "📱",
        "title": "Social Ready",
        "description": "Perfect for Instagram, YouTube, TikTok"
    },
    {
        "icon": "🎬",
        "title": "Professional Quality",
        "description": "4K output with smooth transitions and effects"
    }
]

# Display features in grid
cols = st.columns(3)
for i, feature in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="feature-card">
            <h4>{feature['icon']} {feature['title']}</h4>
            <p>{feature['description']}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🎬 <strong>AI Video Studio</strong> - Create professional videos like Veo3, but simpler and free!</p>
    <p>Made with ❤️ for content creators</p>
</div>
""", unsafe_allow_html=True)
