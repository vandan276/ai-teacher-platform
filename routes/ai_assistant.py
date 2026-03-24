from flask import Blueprint, request, jsonify, session
from app import mysql
from utils.decorators import login_required
import google.generativeai as genai
import os

ai_assistant_bp = Blueprint('ai_assistant', __name__)

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

@ai_assistant_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.json
    user_message = data.get('message', '')
    user_name = session.get('name', 'Teacher')
    
    try:
        # Create a prompt with context
        prompt = f"""
        You are an AI Teacher Assistant for an upskilling platform called "AI Upskill".
        The user's name is {user_name}.
        Your goal is to help teachers learn about AI in education, modules, assessments, and badges.
        Be encouraging, professional, and concise.
        
        User: {user_message}
        AI Assistant:"""
        
        response = model.generate_content(prompt)
        ai_response = response.text.strip()
        
    except Exception as e:
        print(f"DEBUG: Gemini Error: {e}")
        # Fallback to enhanced rule-based logic if Gemini fails
        message = user_message.lower()
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, title FROM modules")
        all_modules = cur.fetchall()
        
        matched_module = None
        for m in all_modules:
            if m['title'].lower() in message:
                matched_module = m
                break
                
        if matched_module:
            ai_response = f"I found a module related to your query: '{matched_module['title']}'. You can start it from your dashboard!"
        elif 'badge' in message or 'point' in message:
            ai_response = "You can earn points by passing assessments. Badges like 'Quick Starter' are awarded for module completions."
        else:
            ai_response = f"Hello {user_name}! I'm having a little trouble connecting to my brain right now, but I can help with modules and assessments. Ask me anything!"
        cur.close()
        
    return jsonify({
        'response': ai_response,
        'status': 'success'
    })
