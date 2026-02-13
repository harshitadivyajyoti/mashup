# mashup
Under the course Predictive Analytics Using Statistics
# Mashup Generator Web Application

## Author
Harshita Divyajyoti  
Roll No: 102317208  

---

## Project Overview

This project generates an audio mashup using YouTube videos of a given singer.

The application allows users to:
- Enter singer name
- Specify number of videos
- Set clip duration
- Generate a mashup
- Download the mashup as ZIP
- Receive it via email

---

## Project Structure

```
mashup/
│
├── app.py        → Deployment-safe version (Cloud version)
├── app1.py       → Full YouTube implementation (Local version)
├── requirements.txt
├── packages.txt
├── README.md
```

---

## Deployed Version (Streamlit Cloud)

The deployed version avoids direct YouTube scraping due to cloud IP restrictions.

Instead:
- Audio clips are generated using FFmpeg
- Mashup is created
- ZIP file is generated
- Email functionality works

Live App:
https://mashup-gc2szsd3bax2keejbbye6l.streamlit.app/

---

## Running Full Version Locally (With YouTube)

### 1. Clone Repository

```
git clone <your-repo-link>
cd mashup
```

### 2. Install Requirements

```
pip install -r requirements.txt
```

### 3. Install FFmpeg

Download and install FFmpeg from:
https://ffmpeg.org/download.html

Ensure FFmpeg is added to system PATH.

### 4. Run Application

```
streamlit run app1.py
```

This version:
- Downloads YouTube videos
- Extracts audio
- Creates mashup
- Sends email
- Provides ZIP download

---

## Dependencies

- streamlit
- yt-dlp (local version)
- ffmpeg
- smtplib
- zipfile

---

## Important Note

YouTube scraping may fail on cloud platforms due to IP restrictions.  
Therefore, a deployment-safe version is provided separately.

---

## Features

- Dynamic mashup generation
- Email delivery system
- Streamlit-based user interface
- FFmpeg-based audio processing
- Cloud deployment support

---

## Technologies Used

- Python
- Streamlit
- yt-dlp
- FFmpeg
- SMTP (Gmail)
- ZipFile module

---

## Email Configuration

Email credentials are stored securely using Streamlit Secrets in deployment.

---

## Conclusion

This project demonstrates:
- Web application deployment
- Audio processing automation
- Email integration
- Handling real-world API restrictions
- Version separation for local and cloud environments
<img width="1124" height="825" alt="image" src="https://github.com/user-attachments/assets/d2b13a86-76e8-43e3-ae7d-234d7b6bc54d" />
