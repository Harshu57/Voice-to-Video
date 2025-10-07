from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import streamlit as st

from src.config import CONFIG
from src.logging_utils import setup_logger
from src.transcribe import transcribe_audio
from src.script_gen import generate_script
from src.tts import synthesize_speech
from src.visuals import generate_visuals
from src.assembler import assemble_video
from src.thumbnail import create_thumbnail

logger = setup_logger(__name__)

st.set_page_config(page_title="Voice → Video Studio", layout="wide")

st.title("Voice → Video Studio")

# Session state containers
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "segments" not in st.session_state:
    st.session_state.segments = []
if "storyboard" not in st.session_state:
    st.session_state.storyboard = None
if "scene_audios" not in st.session_state:
    st.session_state.scene_audios = []
if "scene_videos" not in st.session_state:
    st.session_state.scene_videos = []
if "final_video" not in st.session_state:
    st.session_state.final_video = None

# --- Auto Mode ---
with st.expander("Auto Mode (Topic → Hindi video)", expanded=True):
    topic = st.text_input("Topic (e.g., घर पर कम्पोस्ट कैसे करें) ")
    auto_tone = st.selectbox("Tone", ["friendly", "conversational", "educational", "humorous", "serious"], index=0, key="auto_tone")
    auto_target = st.slider("Target duration (sec)", 30, 600, 90, 10, key="auto_target")
    if st.button("Auto-create Hindi video"):
        if not topic.strip():
            st.error("Please enter a topic.")
        else:
            with st.spinner("Creating Hindi storyboard..."):
                # Use topic as input, request Hindi by passing language='hi'
                sb = generate_script(topic.strip(), tone=auto_tone, target_duration_sec=auto_target, language="hi")
                st.session_state.storyboard = sb
            with st.spinner("Synthesizing Hindi voice-over..."):
                audios = synthesize_speech(st.session_state.storyboard.get("scenes", []), voice=(CONFIG.openai_tts_voice or ""), speed=1.0)
                st.session_state.scene_audios = audios
            with st.spinner("Creating visuals..."):
                vids = generate_visuals(st.session_state.storyboard.get("scenes", []), style="animated slides")
                st.session_state.scene_videos = vids
            with st.spinner("Assembling final video..."):
                output_video_path = os.path.join("outputs", "final", "final_video.mp4")
                subs = [s.get("on_screen_text") or s.get("script_text") or "" for s in st.session_state.storyboard.get("scenes", [])]
                out = assemble_video(st.session_state.scene_videos, st.session_state.scene_audios, subs, output_video_path)
                st.session_state.final_video = out
                thumb_path = os.path.join("outputs", "final", "thumbnail.jpg")
                create_thumbnail(st.session_state.storyboard.get("title", "Video"), thumb_path)
            st.success("Auto Mode complete! Scroll down to preview/download.")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("1) Audio input")
    uploaded = st.file_uploader("Upload audio (wav/mp3/m4a)", type=["wav", "mp3", "m4a"]) 

    lang = st.selectbox("Language (auto by default)", ["auto", "en", "hi", "ur"]) 
    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            if uploaded is None:
                st.error("Please upload an audio file.")
            else:
                os.makedirs(".tmp", exist_ok=True)
                audio_path = os.path.join(".tmp", uploaded.name)
                with open(audio_path, "wb") as f:
                    f.write(uploaded.read())
                result = transcribe_audio(audio_path, None if lang == "auto" else lang)
                st.session_state.transcript = result.get("transcript", "")
                st.session_state.segments = result.get("segments", [])
                st.success("Transcription complete.")

with col_right:
    st.subheader("2) Transcript and storyboard")
    raw = st.text_area("Transcript (editable)", st.session_state.transcript, height=200)
    st.session_state.transcript = raw
    tone = st.selectbox("Tone", ["conversational", "friendly", "educational", "humorous", "serious"])
    target_sec = st.slider("Target duration (sec)", 30, 600, 90, 10)
    if st.button("Generate storyboard"):
        with st.spinner("Generating storyboard via GPT or fallback..."):
            sb = generate_script(st.session_state.transcript, tone=tone, target_duration_sec=target_sec)
            st.session_state.storyboard = sb
            st.success("Storyboard generated.")
    if st.session_state.storyboard:
        st.write("Storyboard JSON (editable):")
        sb_json = st.text_area("", json.dumps(st.session_state.storyboard, ensure_ascii=False, indent=2), height=350)
        try:
            st.session_state.storyboard = json.loads(sb_json)
        except Exception:
            st.warning("Invalid JSON; keeping previous storyboard.")

st.markdown("---")

col3, col4 = st.columns([1, 1])

with col3:
    st.subheader("3) Voice-over")
    voice = st.text_input("Voice (provider specific)", value=(CONFIG.openai_tts_voice or "Rachel"))
    speed = st.slider("Speech speed", 0.5, 2.0, 1.0, 0.1)
    if st.button("Generate voice-over"):
        if not st.session_state.storyboard:
            st.error("Generate a storyboard first.")
        else:
            with st.spinner("Synthesizing speech..."):
                audios = synthesize_speech(st.session_state.storyboard.get("scenes", []), voice=voice, speed=speed)
                st.session_state.scene_audios = audios
                st.success(f"Generated {len(audios)} audio files.")

with col4:
    st.subheader("4) Visuals")
    style = st.selectbox("Visual style", ["animated slides", "avatar", "stock footage"])
    if st.button("Generate visuals"):
        if not st.session_state.storyboard:
            st.error("Generate a storyboard first.")
        else:
            with st.spinner("Creating visuals..."):
                vids = generate_visuals(st.session_state.storyboard.get("scenes", []), style=style)
                st.session_state.scene_videos = vids
                st.success(f"Generated {len(vids)} visual clips.")

st.markdown("---")

st.subheader("5) Assemble video")
output_video_path = os.path.join("outputs", "final", "final_video.mp4")
thumb_path = os.path.join("outputs", "final", "thumbnail.jpg")

if st.button("Assemble"):
    if not st.session_state.scene_videos or not st.session_state.scene_audios:
        st.error("Generate audio and visuals first.")
    else:
        with st.spinner("Assembling final video..."):
            subs = [s.get("on_screen_text") or s.get("script_text") or "" for s in st.session_state.storyboard.get("scenes", [])]
            out = assemble_video(st.session_state.scene_videos, st.session_state.scene_audios, subs, output_video_path)
            st.session_state.final_video = out
            create_thumbnail(st.session_state.storyboard.get("title", "Video"), thumb_path)
            st.success("Assembly complete.")

if st.session_state.final_video and os.path.exists(st.session_state.final_video):
    st.video(st.session_state.final_video)
    with open(st.session_state.final_video, "rb") as f:
        st.download_button("Download MP4", data=f, file_name="final_video.mp4", mime="video/mp4")

st.markdown("---")

with st.expander("Optional: Upload to YouTube"):
    from src.youtube_upload import upload_to_youtube

    yt_title = st.text_input("Title", value=(st.session_state.storyboard or {}).get("title", ""))
    yt_desc = st.text_area("Description", value=(st.session_state.storyboard or {}).get("description", ""))
    yt_tags = st.text_input("Tags (comma separated)", value=",")
    privacy = st.selectbox("Privacy", ["public", "unlisted", "private"])
    if st.button("Upload"):
        if not st.session_state.final_video:
            st.error("Assemble a video first.")
        else:
            st.info("YouTube upload not implemented in this demo. See src/youtube_upload.py.")
