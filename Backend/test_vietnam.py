from tiktokvoice import tts, available_voices
from video import generate_subtitles
from moviepy.editor import AudioFileClip

def check_vietnamese_support():
    # Check if Vietnamese voice is available
    vietnamese_voice = "vi_female_x"  # Replace with actual Vietnamese voice option if available
    if vietnamese_voice in available_voices():
        print("Vietnamese voice is supported.")
    else:
        print("Vietnamese voice is not supported.")

    # Test TTS with Vietnamese text
    test_text = "Xin chào, đây là một bài kiểm tra."
    try:
        tts(test_text, vietnamese_voice, filename="../temp/test_vietnamese.mp3")
        print("TTS supports Vietnamese text.")
    except Exception as e:
        print(f"TTS does not support Vietnamese text. Error: {e}")

    # Test subtitle generation with Vietnamese text
    try:
        generate_subtitles(audio_path="../temp/test_vietnamese.mp3",
                           sentences=[test_text],
                           audio_clips=[AudioFileClip("../temp/test_vietnamese.mp3")],
                           voice="vi")
        print("Subtitle generation supports Vietnamese text.")
    except Exception as e:
        print(f"Subtitle generation does not support Vietnamese text. Error: {e}")


# Call this function to check Vietnamese support
check_vietnamese_support()
