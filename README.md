# 🎤 InterviewAce
### AI-powered mock interviews for students & fresh grads — powered by Amazon Nova

Built for the **Amazon Nova AI Hackathon** | Category: Voice AI

---

## 🎯 What is InterviewAce?

InterviewAce is a free AI-powered mock interview coach that helps students and fresh graduates prepare for job interviews. Most students can't afford human interview coaching — InterviewAce solves that by providing a personalized, intelligent interviewer available 24/7.

---

## ✨ Features

- 📄 **Resume-aware questions** — paste your resume and Nova tailors every question to your actual experience
- 🎚️ **Difficulty levels** — Easy, Medium, or Hard
- 💬 **Real-time feedback** — Nova gives coaching feedback after every answer
- 🎙️ **Voice input** — speak your answers using the mic button
- 🔊 **Text-to-speech** — hear the interviewer's questions read aloud
- 🎯 **Role-specific** — works for any job role

---

## 🛠️ Tech Stack

- **AI Model:** Amazon Nova Lite via AWS Bedrock
- **Frontend:** Streamlit
- **Voice:** SpeechRecognition + pyttsx3
- **Cloud:** AWS (Bedrock, IAM)
- **Language:** Python

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/snehanair-486/interview-ace.git
cd interview-ace
```

### 2. Install dependencies
```bash
pip install boto3 streamlit SpeechRecognition pyttsx3 awscli
```

If pyaudio fails:
```bash
pip install pipwin
pipwin install pyaudio
```

### 3. Configure AWS
```bash
aws configure
```
Enter your Access Key, Secret Key, region `us-east-1`, format `json`.
Make sure your IAM user has **AmazonBedrockFullAccess** attached.

### 4. Run
```bash
streamlit run app.py
```
Opens at `http://localhost:8501` 🎉
