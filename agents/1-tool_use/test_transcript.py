#!/usr/bin/env python3

from youtube_transcript_api import YouTubeTranscriptApi
import re

def fetch_youtube_transcript(url: str) -> str:
    """
    Extract transcript with timestamps from a YouTube video URL and format it for LLM consumption
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Formatted transcript with timestamps, where each entry is on a new line
             in the format: "[MM:SS] Text"
    """
    # Extract video ID from URL
    video_id_pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    video_id_match = re.search(video_id_pattern, url)
    
    if not video_id_match:
        raise ValueError("Invalid YouTube URL")
    
    video_id = video_id_match.group(1)
    
    try:
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        
        # Format each entry with timestamp and text
        formatted_entries = []
        for snippet in fetched_transcript:
            # Convert seconds to MM:SS format
            minutes = int(snippet.start // 60)
            seconds = int(snippet.start % 60)
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            
            formatted_entry = f"{timestamp} {snippet.text}"
            formatted_entries.append(formatted_entry)
        
        # Join all entries with newlines
        return "\n".join(formatted_entries)
    
    except Exception as e:
        raise Exception(f"Error fetching transcript: {str(e)}")

# Test with a well-known video that has transcripts
if __name__ == "__main__":
    # Test with a sample URL (this is just an example - use any YouTube video with transcripts)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Never Gonna Give You Up
    try:
        result = fetch_youtube_transcript(test_url)
        print("Success! First 200 characters of transcript:")
        print(result[:200])
        print("...")
    except Exception as e:
        print(f"Error: {e}")
