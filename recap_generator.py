"""
Simple recap generator for manhwa/anime/book titles.
Requires openai, gTTS, moviepy, and requests.
Set OPENAI_API_KEY and UNSPLASH_ACCESS_KEY in environment.
Use `pyinstaller --onefile recap_generator.py` to build a Windows executable.
"""
import os
import requests
import openai
from pathlib import Path
from gtts import gTTS
from moviepy.editor import ImageSequenceClip, AudioFileClip


def fetch_summary(title: str) -> str:
    prompt = (f"Provide a concise recap for '{title}'. "
              "Limit the recap to about three paragraphs.")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"].strip()


def fetch_images(query: str, num_images: int = 5) -> list[str]:
    """Download images from Unsplash and return local file paths."""
    access_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not access_key:
        raise RuntimeError("UNSPLASH_ACCESS_KEY not set")
    url = "https://api.unsplash.com/search/photos"
    params = {"query": query, "per_page": num_images, "client_id": access_key}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    paths = []
    for i, photo in enumerate(data.get("results", [])):
        img_url = photo["urls"]["regular"]
        img_data = requests.get(img_url).content
        path = Path(f"img_{i}.jpg")
        with open(path, "wb") as f:
            f.write(img_data)
        paths.append(str(path))
    return paths


def text_to_speech(text: str, filename: str) -> str:
    tts = gTTS(text)
    tts.save(filename)
    return filename


def create_video(images: list[str], audio_path: str, output: str) -> str:
    clip = ImageSequenceClip(images, fps=1)
    audio = AudioFileClip(audio_path)
    clip = clip.set_audio(audio)
    clip.write_videofile(output, codec="libx264")
    return output


def main() -> None:
    title = input("Enter title: ").strip()
    summary = fetch_summary(title)
    print(summary)
    images = fetch_images(title)
    audio = text_to_speech(summary, "narration.mp3")
    create_video(images, audio, "recap.mp4")
    print("Recap video saved to recap.mp4")


if __name__ == "__main__":
    main()
