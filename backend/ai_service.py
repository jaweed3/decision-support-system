import os
import google.generativeai as genai
import json

class AIService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    async def extract_requirements(self, user_query: str):
        if not self.model:
            return None
            
        prompt = f"""
        Extract laptop requirements from this user query: "{user_query}"
        Return ONLY a JSON object with these keys:
        - budget_max (float or null)
        - min_ram (int or null)
        - min_ssd (int or null)
        - primary_use (string: 'gaming', 'office', 'design', 'student', or 'general')
        - condition_preference (string: 'new', 'used', or 'both')
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Simple JSON extraction from response text
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            return json.loads(text)
        except Exception as e:
            print(f"AI Extraction Error: {e}")
            return None

    async def get_recommendation_summary(self, laptop_data: dict, user_context: str):
        if not self.model:
            return "AI Consultant is offline. Here is your best match based on the data."

        prompt = f"""
        User context: {user_context}
        Best Match Laptop: {laptop_data['model_name']} ({laptop_data['brand']})
        Specs: RAM {laptop_data['ram_gb']}GB, SSD {laptop_data['ssd_gb']}GB, Price {laptop_data['price']}
        
        Provide a short, professional, and meyakinkan (convincing) explanation why this laptop 
        is the perfect choice for the user's needs. Speak as a tech expert.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error getting AI summary: {e}"

ai_service = AIService()
