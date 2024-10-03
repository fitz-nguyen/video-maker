import json
import logging
import os
from uuid import uuid4

from dotenv import load_dotenv
from gtts import gTTS
from moviepy.config import change_settings
from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    VideoFileClip,
    concatenate_audioclips,
)
from search import search_for_stock_videos
from termcolor import colored
from utils import check_env_vars, choose_random_song, clean_dir, fetch_songs
from video import combine_videos, generate_subtitles, generate_video, save_video
from youtube import upload_video

# Load environment variables
load_dotenv("../.env")
# Check if all required environment variables are set
# This must happen before importing video which uses API keys without checking
check_env_vars()


AMOUNT_OF_STOCK_VIDEOS = 5
GENERATING = False
change_settings({"IMAGEMAGICK_BINARY": os.getenv("IMAGEMAGICK_BINARY")})


def generate_video_from_files(
    voice="vi",  # Change default to Vietnamese
    n_threads=2,
    subtitles_position="bottom",
    text_color="#FFFFFF",
    use_music=False,
    songs_zip_url=None
):
    try:
        # Read script from file
        with open("data/script.txt", "r") as file:
            script = file.read()

        # Read search terms from file
        with open("data/search_terms.json", "r") as file:
            search_terms = json.load(file)

 # Set global variable
        global GENERATING
        GENERATING = True

        # Clean
        clean_dir("../temp/")
        clean_dir("../subtitles/")

        # Download songs
        if use_music:
            # Downloads a ZIP file containing popular TikTok Songs
            if songs_zip_url:
                fetch_songs(songs_zip_url)
            else:
                # Default to a ZIP file containing popular TikTok Songs
                fetch_songs("https://filebin.net/2avx134kdibc4c3q/drive-download-20240209T180019Z-001.zip")

        if not GENERATING:
            raise Exception("Video generation was cancelled.")

        voice_prefix = voice[:2]

        if not voice:
            print(colored("[!] No voice was selected. Defaulting to \"en_us_001\"", "yellow"))
            voice = "en_us_001"
            voice_prefix = voice[:2]

        # Search for a video of the given search term
        video_urls = []

        # Defines how many results it should query and search through
        it = 15

        # Defines the minimum duration of each clip
        min_dur = 10

        # Loop through all search terms,
        # and search for a video of the given search term
        for search_term in search_terms:
            if not GENERATING:
                raise Exception("Video generation was cancelled.")
            found_urls = search_for_stock_videos(
                search_term, os.getenv("PEXELS_API_KEY"), it, min_dur
            )
            # Check for duplicates
            for url in found_urls:
                if url not in video_urls:
                    video_urls.append(url)
                    break

        # Check if video_urls is empty
        if not video_urls:
            print(colored("[-] No videos found to download.", "red"))
            raise Exception("No videos found to download.")

        # Define video_paths
        video_paths = []

        # Let user know
        print(colored(f"[+] Downloading {len(video_urls)} videos...", "blue"))

        # Save the videos
        for video_url in video_urls:
            if not GENERATING:
                raise Exception("Video generation was cancelled.")
            try:
                saved_video_path = save_video(video_url)
                video_paths.append(saved_video_path)
            except Exception:
                print(colored(f"[-] Could not download video: {video_url}", "red"))

        # Let user know
        print(colored("[+] Videos downloaded!", "green"))

        # Let user know
        print(colored("[+] Script generated!\n", "green"))

        if not GENERATING:
            raise Exception("Video generation was cancelled.")
        # Split script into sentences
        sentences = script.split(". ")

        # Remove empty strings
        sentences = list(filter(lambda x: x != "", sentences))
        paths = []

        # Generate TTS for every sentence
        for sentence in sentences:
            if not GENERATING:
                raise Exception("Video generation was cancelled.")
            current_tts_path = f"../temp/{uuid4()}.mp3"
            tts = gTTS(text=sentence, lang=voice)
            tts.save(current_tts_path)
            audio_clip = AudioFileClip(current_tts_path)
            paths.append(audio_clip)

        # Combine all TTS files using moviepy
        final_audio = concatenate_audioclips(paths)
        tts_path = f"../temp/{uuid4()}.mp3"
        final_audio.write_audiofile(tts_path)

        try:
            subtitles_path = generate_subtitles(audio_path=tts_path, sentences=sentences, audio_clips=paths, voice=voice_prefix)
        except Exception as e:
            print(colored(f"[-] Error generating subtitles: {e}", "red"))
            subtitles_path = None

        # Concatenate videos
        temp_audio = AudioFileClip(tts_path)
        combined_video_path = combine_videos(video_paths, temp_audio.duration, 5, n_threads or 2)

        # Put everything together
        try:
            final_video_path = generate_video(combined_video_path, tts_path, subtitles_path,
                                              n_threads or 2, subtitles_position, text_color or "#FFFF00")
            if final_video_path is None:
                raise Exception("generate_video() returned None")
        except Exception as e:
            print(colored(f"[-] Error generating final video: {e}", "red"))
            raise  # Re-raise the exception to stop execution

        # Check if final_video_path exists before proceeding
        if not os.path.exists(f"../temp/{final_video_path}"):
            raise FileNotFoundError(f"Final video file not found: ../temp/{final_video_path}")

        video_clip = VideoFileClip(f"../temp/{final_video_path}")
        if use_music:
            # Select a random song
            song_path = choose_random_song()

            # Add song to video at 30% volume using moviepy
            original_duration = video_clip.duration
            original_audio = video_clip.audio
            song_clip = AudioFileClip(song_path).set_fps(44100)

            # Set the volume of the song to 10% of the original volume
            song_clip = song_clip.volumex(0.1).set_fps(44100)

            # Add the song to the video
            comp_audio = CompositeAudioClip([original_audio, song_clip])
            video_clip = video_clip.set_audio(comp_audio)
            video_clip = video_clip.set_fps(30)
            video_clip = video_clip.set_duration(original_duration)
            video_clip.write_videofile(f"../{final_video_path}", threads=n_threads or 1)
        else:
            video_clip.write_videofile(f"../{final_video_path}", threads=n_threads or 1)

        # Let user know
        print(colored(f"[+] Video generated: {final_video_path}!", "green"))

        # Stop FFMPEG processes
        if os.name == "nt":
            # Windows
            os.system("taskkill /f /im ffmpeg.exe")
        else:
            # Other OS
            os.system("pkill -f ffmpeg")

        GENERATING = False

        print(colored(f"[+] Video generated: {final_video_path}!", "green"))
        return final_video_path

    except Exception as err:
        logging.exception(err)
        print(colored(f"[-] Error: {str(err)}", "red"))
        raise


# Example usage
if __name__ == "__main__":
    try:
        output_path = generate_video_from_files()
        print(f"Video generated successfully: {output_path}")
    except Exception as e:
        print(f"Error generating video: {str(e)}")
