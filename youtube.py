from pyrogram import Client, filters
from pytube import YouTube
import os

Api_Id=9126459
Api_Hash='238c912d48a9ec0d0e8b05738f358ffc'
YOUR_BOT_TOKEN='6391184772:AAE2Ifo8hO-M2hm8NYDB4XKBzfQoZbiaSR0'
bot = Client("youtube_bot",Api_Id,Api_Hash,bot_token=YOUR_BOT_TOKEN)



# Dictionary to keep track of user state
user_states = {}

# Handle the /start command
@bot.on_message(filters.command("start"))
def start_command(client, message):
    user_states[message.from_user.id] = {}
    message.reply_text("Welcome to the YouTube downloader bot! Send me a YouTube video URL to download.")

# Handle messages containing a YouTube URL
@bot.on_message(filters.regex(r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+"))
def handle_youtube_url(client, message):
    url = message.text

    try:
        youtube_video = YouTube(url)
        
        # Get available video streams
        video_streams = youtube_video.streams.filter(file_extension="mp4")
        
        # Create a list of available resolutions
        resolutions = [f"{index + 1}. {stream.resolution} - {stream.abr}" for index, stream in enumerate(video_streams)]
        
        # Display the available resolutions to the user
        resolution_text = "\n".join([f"{resolution}" for resolution in resolutions])
        user_states[message.from_user.id]["video_streams"] = video_streams
        message.reply_text(f"Choose a resolution:\n{resolution_text}")

    except Exception as e:
        message.reply_text(f"Error: {str(e)}")

# Handle resolution choice
@bot.on_message(filters.regex(r"\d+"))
def handle_resolution_choice(client, message):
    try:
        choice = int(message.text)
        selected_stream = user_states[message.from_user.id]["video_streams"][choice - 1]

        # Download the video
        selected_stream.download()

        # Send the downloaded video to the user
        with open(selected_stream.default_filename, "rb") as video_file:
            bot.send_video(message.chat.id, video_file, caption="Here is your downloaded video!")

        # Delete the downloaded video file
        os.remove(selected_stream.default_filename)

    except Exception as e:
        message.reply_text(f"Error: {str(e)}")

# Start the bot
bot.run()
