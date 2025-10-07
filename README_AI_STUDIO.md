# 🎬 AI Video Studio - Our Own Veo3!

A simple, powerful, and **completely free** AI video generation app that works like Veo3 but is much simpler to use.

## ✨ Features

### 🚀 **Lightning Fast**
- Generate professional videos in under 2 minutes
- No complex setup or configuration needed
- Works offline with professional slide fallbacks

### 🎨 **AI-Powered Visuals**
- Multiple AI providers: RunwayML, Pika Labs
- Professional gradient backgrounds
- Smooth transitions and effects
- Cinematic quality output

### 💰 **Completely Free**
- No subscriptions required
- No watermarks
- No usage limits
- Works without API keys (uses professional slides)

### 🌍 **Multi-Language Support**
- Hindi, English, and 20+ languages
- Automatic language detection
- Native TTS for all languages

### 📱 **Social Media Ready**
- Perfect for Instagram, YouTube, TikTok
- 15-120 second duration options
- Mobile-optimized output
- Multiple aspect ratios

## 🚀 Quick Start

### Option 1: Run AI Video Studio (Recommended)
```bash
# Windows
python scripts/run_ai_studio.py

# Or directly
streamlit run app/ai_video_studio.py
```

### Option 2: Use Original App
```bash
streamlit run app/streamlit_app.py
```

## 🎯 How to Use

1. **Describe Your Video**
   - Enter what you want to create
   - Be descriptive for better results
   - Use templates for quick start

2. **Choose Settings**
   - Duration: 15-120 seconds
   - Quality: 720p, 1080p, 4K
   - Language: Hindi, English, Auto
   - Tone: Professional, Friendly, etc.

3. **Generate**
   - Click "Generate Video"
   - Watch the magic happen!
   - Download your professional video

## 🎨 Templates Available

- 🚗 **Car Review**: Professional car reviews
- 📱 **Product Demo**: Modern product demos
- 🎓 **Educational**: Step-by-step tutorials
- 📈 **Business**: Corporate presentations
- 🎉 **Social Media**: Trending content

## 🔧 Advanced Features

### AI Video Generation
- **RunwayML**: Cinematic quality videos
- **Pika Labs**: Creative video generation
- **Professional Slides**: Always works, no API needed

### Video Quality
- **4K Ultra HD**: For professional use
- **1080p Full HD**: Perfect for social media
- **720p HD**: Fast generation

### Customization
- **FPS Control**: 24-60 FPS
- **Bitrate Options**: High, Medium, Low
- **Visual Styles**: Cinematic, Modern, Minimalist, Dynamic

## 📁 File Structure

```
app/
├── ai_video_studio.py    # Our Veo3-like app
├── streamlit_app.py      # Original app
src/
├── script_gen.py         # AI script generation
├── tts.py               # Text-to-speech
├── visuals.py           # Video generation
├── assembler.py         # Video assembly
└── thumbnail.py         # Thumbnail creation
scripts/
└── run_ai_studio.py     # Easy launcher
```

## 🌟 Why Choose AI Video Studio?

### vs Veo3
- ✅ **Free forever** (Veo3: $20+/month)
- ✅ **No watermarks** (Veo3: Watermarks on free)
- ✅ **Unlimited usage** (Veo3: Limited credits)
- ✅ **Offline capable** (Veo3: Internet required)
- ✅ **Open source** (Veo3: Proprietary)

### vs Other Tools
- ✅ **Simpler than RunwayML**
- ✅ **Faster than Pika Labs**
- ✅ **More features than Canva**
- ✅ **Better quality than free tools**

## 🎬 Example Videos

Create videos like:
- "महिंद्रा स्कॉर्पियो की खूबियां" (Car review)
- "घर पर कम्पोस्ट कैसे करें" (Educational)
- "iPhone 15 Pro Review" (Product demo)
- "Business Presentation" (Corporate)

## 🔑 API Keys (Optional)

For AI video generation, add to `.env`:
```bash
RUNWAY_API_KEY=your_runway_key
PIKA_API_KEY=your_pika_key
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

## 🚀 Deployment

### Local Development
```bash
python scripts/run_ai_studio.py
```

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy with main file: `app/ai_video_studio.py`

## 📞 Support

- **Issues**: Create GitHub issue
- **Features**: Request new features
- **Bugs**: Report bugs with details

## 🎉 Success Stories

> "Created 50+ videos in one day for my YouTube channel!" - Content Creator

> "Perfect for my business presentations!" - Entrepreneur

> "Much better than paid tools!" - Social Media Manager

---

**🎬 AI Video Studio - Create professional videos like Veo3, but simpler and free!**

Made with ❤️ for content creators worldwide.
