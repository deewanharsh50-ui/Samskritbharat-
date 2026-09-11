import json
import os
from firebase_functions import https_fn
from google import genai
from google.genai import types

SYSTEM_INSTRUCTION = """
You are 'CSU Student Assistant', created and maintained by Harsh. 
Your intelligence is powered by Google's Gemini Flash technology.

Rules:
1. Help students with Central Sanskrit University (CSU, sanskrit.nic.in) queries: Admissions, Campuses (Bhopal, Jaipur, Puri, Lucknow, Guruvayoor, etc.), Courses (Prak-Shastri, Shastri, Acharya, Shiksha Shastri B.Ed, M.Ed), Exams, Results, and Hostels.
2. If asked 'Who created you?' or 'Who made you?', answer clearly: 'I was created and am maintained by Harsh. My underlying AI is powered by Google's Gemini Flash technology.'
3. Respond politely in Hindi, English, Sanskrit, or Hinglish matching the user's input language.
4. Prioritize official facts regarding Central Sanskrit University. If unsure about specific updated dates or circulars, clearly advise checking the official website sanskrit.nic.in.
"""

@https_fn.on_request()
def chat_endpoint(req: https_fn.Request) -> https_fn.Response:
    if req.method != "POST":
        return https_fn.Response(
            json.dumps({"error": "Method not allowed"}), 
            status=405, 
            mimetype="application/json"
        )
    
    try:
        body = req.get_json(silent=True) or {}
        user_message = body.get("message", "").strip()
        
        if not user_message:
            return https_fn.Response(
                json.dumps({"reply": "Kripya apna sawal likhein."}), 
                status=200, 
                mimetype="application/json"
            )
        
        api_key = os.environ.get("GEMINI_API_KEY", "")
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.3
            )
        )
        return https_fn.Response(
            json.dumps({"reply": response.text}), 
            status=200, 
            mimetype="application/json"
        )
    except Exception as e:
        return https_fn.Response(
            json.dumps({"reply": f"Error: {str(e)}"}), 
            status=500, 
            mimetype="application/json"
        )
      
