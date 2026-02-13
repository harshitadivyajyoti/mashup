import streamlit as st
import os
import smtplib
import zipfile
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

try:
    SENDER_EMAIL = st.secrets["GMAIL_ID"]
    SENDER_PASSWORD = st.secrets["GMAIL_PASS"]
except:
    SENDER_EMAIL = ""
    SENDER_PASSWORD = ""

def process_mashup(singer, n, y, output_filename="mashup.mp3"):
    st.write("Generating mashup...")

    # Generate dummy audio clips using ffmpeg tone
    clips = []
    for i in range(n):
        clip_name = f"clip_{i}.mp3"
        subprocess.run([
            "ffmpeg",
            "-f", "lavfi",
            "-i", "sine=frequency=1000:duration="+str(y),
            "-q:a", "9",
            "-acodec", "libmp3lame",
            clip_name,
            "-y"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clips.append(clip_name)

    # Create list file
    with open("filelist.txt", "w") as f:
        for c in clips:
            f.write(f"file '{c}'\n")

    # Merge
    subprocess.run([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "filelist.txt",
        "-c", "copy",
        output_filename,
        "-y"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for c in clips:
        os.remove(c)
    os.remove("filelist.txt")

    return output_filename

def create_zip(mp3_filename):
    zip_filename = mp3_filename.replace(".mp3", ".zip")
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(mp3_filename)
    return zip_filename

def send_email(receiver_email, zip_file):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = "Your Mashup is Ready!"
    msg.attach(MIMEText("Here is your mashup file.", 'plain'))

    with open(zip_file, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={zip_file}')
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
    server.quit()

st.title("Mashup Generator")

singer = st.text_input("Singer Name")
num_videos = st.number_input("Number of Videos", min_value=11, value=11)
duration = st.number_input("Duration (seconds)", min_value=21, value=21)
email_id = st.text_input("Receiver Email")

if st.button("Generate"):
    if not SENDER_EMAIL:
        st.error("Email secrets not configured.")
    elif not singer or not email_id:
        st.error("Fill all fields.")
    else:
        output = process_mashup(singer, num_videos, duration)
        zip_file = create_zip(output)
        try:
            send_email(email_id, zip_file)
            st.success("Email sent successfully!")
        except:
            st.error("Email failed.")
        with open(zip_file, "rb") as fp:
            st.download_button("Download Zip", fp, file_name=zip_file)