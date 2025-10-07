# Voice-to-Video (Record speech → auto-create full video)

A modular Python application with a Streamlit UI that records or ingests audio, transcribes speech to text, generates a structured video script via GPT, synthesizes voice-over, creates visuals (APIs or slide fallback), assembles a synchronized video with subtitles and thumbnail, and optionally uploads to YouTube.

## Quick start

```bash
# Windows PowerShell (recommended)
python -m venv .\.venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Copy env template and set your keys (optional for paid providers)
copy .env.example .env

# Run the app
streamlit run app/streamlit_app.py
```

If you have no API keys, the app runs using local fallbacks (mock STT, local TTS, slide visuals) for an end-to-end demo.

## Repo layout

```
app/
  streamlit_app.py
src/
  __init__.py
  config.py
  logging_utils.py
  transcribe.py
  script_gen.py
  tts.py
  visuals.py
  assembler.py
  thumbnail.py
  youtube_upload.py
tests/
  __init__.py
  test_transcribe.py
  test_script_gen.py
  test_tts.py
  test_visuals.py
  test_assembler.py
  test_thumbnail.py
  test_e2e_mocked.py
assets/
  demo/
    sample_transcript.txt
scripts/
  demo_e2e_mock.py
requirements.txt
.env.example
README.md
```

## Environment variables

- OPENAI_API_KEY: OpenAI API key (GPT, Whisper). Optional.
- OPENAI_TTS_VOICE (optional): Default voice name for OpenAI TTS.
- ELEVENLABS_API_KEY (optional): ElevenLabs TTS.
- PEXELS_API_KEY (optional): Stock image fallback.
- PIKA_API_KEY / RUNWAY_API_KEY / KAIBER_API_KEY (optional): Video clip generation.
- YOUTUBE_CLIENT_SECRET_FILE (optional): Path to OAuth2 client secrets JSON.
- MAX_VIDEO_MINUTES (optional): Default 10.
- DEBUG (optional): true for verbose logs.
- HTTP_TIMEOUT_SECONDS, RETRY_MAX_ATTEMPTS, RETRY_BACKOFF_SECONDS: network tuning.

## Architecture (text diagram)

```
[Audio Ingest]
   ├─ Mic record (Streamlit) / Upload file
   └─> src/transcribe.transcribe_audio()  → transcript + segments
                      │
                      v
           src/script_gen.generate_script()  → storyboard JSON
                      │                      (title, scenes, metadata)
                      ├─> user edits in UI → (updated storyboard)
                      v
              src/tts.synthesize_speech()  → scene audio files
                      │
                      v
           src/visuals.generate_visuals()  → scene video/image clips
                      │
                      v
src/assembler.assemble_video() + subtitles + thumbnail → final MP4
                      │
                      └─> Optional: src/youtube_upload.upload_to_youtube()
```

## Streamlit usage

- Start the app, record or upload audio.
- Transcribe, review transcript, generate storyboard (editable JSON), then TTS and visuals.
- Assemble to produce MP4, preview in-app, download, optional YouTube upload (placeholder).

## Script generation prompts

System prompt:
```
You are a helpful assistant that converts user speech transcripts into a concise, scene-by-scene video storyboard. Output JSON with keys: title, scenes[], thumbnail_idea, description, tags, title_options. Each scene must have duration_sec, script_text, visual_description, on_screen_text. Ensure language matches the transcript language. Return ONLY minified JSON.
```
User prompt template:
```
Please turn the following transcript into a video storyboard with 3–6 scenes.
Tone: {tone}
Target duration (sec): {target_duration_sec}
Transcript language (auto-detected): {language}
Transcript:
"""
{transcript}
"""
```

## Tests

```bash
pytest -q
```

- Unit tests mock external APIs and favor local fallbacks.
- E2E mock demonstrates the full pipeline without paid APIs.

## Demo script

```bash
python scripts/demo_e2e_mock.py
```

This creates outputs in `outputs/` using the fallback providers.

## Troubleshooting

- FFmpeg not found: Install FFmpeg and add to PATH.
- Microphone issues: use Chrome/Edge and allow mic permission, or upload a file.
- Rate limits: external calls use retries with backoff; check logs.

## Cost notes

Paid usage only when API keys are configured for OpenAI/ElevenLabs/video generation providers.
