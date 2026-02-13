import streamlit as st
import os
import smtplib
import zipfile
import yt_dlp
from pydub import AudioSegment
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# ---------- 1. SECURE EMAIL CREDENTIALS ----------
try:
    SENDER_EMAIL = st.secrets["GMAIL_ID"]
    SENDER_PASSWORD = st.secrets["GMAIL_PASS"]
except:
    SENDER_EMAIL = ""
    SENDER_PASSWORD = ""

# ---------- 2. DOWNLOAD + CUT + MERGE ----------
def process_mashup(singer, n, y, output_filename="mashup.mp3"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': 'temp_%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    downloaded_files = []
    search_query = f"ytsearch{n}:{singer}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(search_query, download=True)
            if 'entries' in info:
                for entry in info['entries']:
                    downloaded_files.append(f"temp_{entry['id']}.mp3")
        except Exception as e:
            st.error(f"Download Error: {e}")
            return None

    if not downloaded_files:
        st.error("No files downloaded.")
        return None

    merged = AudioSegment.empty()

    for file in downloaded_files:
        try:
            audio = AudioSegment.from_mp3(file)
            clipped = audio[:y * 1000]  # convert sec to ms
            merged += clipped
        except:
            continue

    merged.export(output_filename, format="mp3")

    # cleanup temp files
    for file in downloaded_files:
        if os.path.exists(file):
            os.remove(file)

    return output_filename

# ---------- 3. ZIP FUNCTION ----------
def create_zip(mp3_filename):
    zip_filename = mp3_filename.replace(".mp3", ".zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(mp3_filename)
    return zip_filename

# ---------- 4. EMAIL FUNCTION ----------
def send_email(receiver_email, zip_file):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = "Your Mashup is Ready 🎵"

    msg.attach(MIMEText("Hi,\n\nYour mashup file is attached.\n\nRegards.", 'plain'))

    with open(zip_file, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={zip_file}',
        )
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
    server.quit()

# ---------- 5. STREAMLIT UI ----------
st.title("🎵 Mashup Generator")

singer = st.text_input("Singer Name")
num_videos = st.number_input("Number of Videos", min_value=11, value=11)
duration = st.number_input("Duration (seconds)", min_value=21, value=21)
email_id = st.text_input("Receiver Email")

if st.button("Generate Mashup"):
    if not SENDER_EMAIL:
        st.error("Secrets missing! Add GMAIL_ID and GMAIL_PASS in Streamlit Cloud.")
    elif not singer or not email_id:
        st.error("Please fill all fields.")
    else:
        with st.spinner("Processing... please wait ⏳"):
            output_file = process_mashup(singer, num_videos, duration)

        if output_file:
            zip_file = create_zip(output_file)
            try:
                send_email(email_id, zip_file)
                st.success(f"✅ Email sent successfully to {email_id}")
            except Exception as e:
                st.error(f"Email failed: {e}")

            with open(zip_file, "rb") as fp:
                st.download_button("Download Zip File", fp, file_name=zip_file)