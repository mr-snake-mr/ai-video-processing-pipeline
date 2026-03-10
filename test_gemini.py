from google import genai

API_KEY = "AIzaSyDln_5FLdhFmxDKN5A1u3LmokDaNaUmGHc"

def find_hook(transcript_text):
    client = genai.Client(api_key=API_KEY)

    prompt = f"""
You are a professional short-form content editor.

From this transcript, choose the most engaging 30 to 60 second self-contained segment.
Return ONLY in this format:
START: MM:SS
END: MM:SS

Transcript:
{transcript_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print(response.text)


if __name__ == "__main__":
    sample_text = """
Hello there! Are you a brand looking for creators to collab with?
Well then look no further because I am ready.
Your product is safe on my channel because I will promote it appropriately.
So what are you waiting for, brands? Give me money.
"""

    find_hook(sample_text)