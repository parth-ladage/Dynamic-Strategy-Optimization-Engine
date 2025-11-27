import google.generativeai as genai
import os

# --- CONFIGURATION ---
# Get your free key from: https://aistudio.google.com/
# Best practice: Use os.getenv("GEMINI_API_KEY") and set it in your terminal
API_KEY = os.getenv("GEMINI_API_KEY") 

genai.configure(api_key=API_KEY)

def ask_gemini_engineer(user_question, strategy_context):
    """
    Sends the user's question + the calculated strategy to Gemini.
    """
    try:
        # 1. Construct the "System Prompt"
        system_instruction = f"""
        You are an expert Formula 1 Race Engineer (like Peter Bonnington 'Bono' or Gianpiero Lambiase 'GP').
        You are talking to the Race Strategist.
        
        CURRENT RACE DATA:
        - Recommended Strategy: {strategy_context.get('recommended', {}).get('name')}
        - Predicted Race Time: {strategy_context.get('recommended', {}).get('total_time')} seconds
        - Alternative Strategy: {strategy_context.get('alternatives', [{}])[1].get('name')}
        
        User Question: "{user_question}"
        
        INSTRUCTIONS:
        - Answer the question briefly (2-3 sentences max).
        - Use F1 terminology (undercut, degradation, pit window, box box).
        - Be confident and professional.
        - If the user asks about the data, explain why the recommended strategy is faster.
        """
        
        # 2. Call Gemini with Robust Fallback Chain
        # UPDATED: Using the specific models available to your key (2.5 Flash, 2.0 Flash)
        model_names = [
            # 'gemini-2.5-flash',
            # 'models/gemini-2.5-flash',
            # 'gemini-2.0-flash',
            # 'models/gemini-2.0-flash',
            'gemini-pro-latest',
            # 'models/gemini-pro-latest'
        ]
        
        response = None
        last_error = None
        
        for model_name in model_names:
            try:
                # Try to initialize and generate
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(system_instruction)
                
                if response:
                    print(f"✅ Success using model: {model_name}")
                    break # If successful, stop trying
            except Exception as e:
                print(f"⚠️ {model_name} failed: {str(e)}")
                last_error = e
                continue
        
        if response:
            return response.text
        else:
            # 3. DIAGNOSTIC: If all fail, return the available models to the UI
            # This helps you see exactly what your API key supports without checking terminal logs
            available_models = []
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        available_models.append(m.name)
            except Exception as e:
                available_models.append(f"List error: {str(e)}")

            models_str = ", ".join(available_models)
            return f"Radio Check... Connection unstable. Your available models: [{models_str}]. (Last Error: {str(last_error)})"
        
    except Exception as e:
        return f"Radio Check... I didn't copy that. (Error: {str(e)})"