import os
from groq import Groq
from config import Config
from spellchecker import SpellChecker
from colorama import Fore, Style, init

# Initialize Colorama for CLI
init(autoreset=True)

class SmartTechTutor:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.spell = SpellChecker()
        self.chat_history = []
        
        # System Prompt: Defines the Persona and Constraints
        self.system_prompt = """
        You are the 'Smart Tech Tutor', a world-class expert in Computer Science and Programming.
        Your capabilities include Python, C, C++, Java, JavaScript, and more.

        RULES FOR EVERY RESPONSE:
        1. CODE QUALITY: Generate optimized, clean, and production-ready code.
        2. COMPLEXITY ANALYSIS: ONLY provide Time/Space Complexity if the user EXPLICITLY asks for it (e.g., "what's the complexity", "analyze this code", "explain time complexity").
        3. EXPLANATION: If the user asks for explanation, break it down step-by-step.
        4. CORRECTION: If the user's prompt has typos regarding technical terms, correct them silently and proceed.
        5. FILE CREATION: If the code is substantial, suggest a filename and extension.
        6. TONE: Professional, educational, and concise.

        FORMAT:
        - Use Markdown for code blocks.
        - Do NOT append complexity analysis unless requested.
        - If complexity IS requested, format it clearly at the end:
        **Complexity Analysis:**
        * Time Complexity: O(...)
        * Space Complexity: O(...)
        """
    
# Lines 35-46: switch_model method
    def switch_model(self, model_name: str):
        """
        Dynamically switch AI models based on task complexity.
        Available: 'llama-3.3-70b-versatile', 'llama-3.1-8b-instant'
        """
        valid_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
        if model_name in valid_models:
            Config.MODEL_NAME = model_name
            print(f"{Fore.GREEN}✅ Model switched to: {model_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Invalid model. Choose from: {valid_models}{Style.RESET_ALL}")


    def correct_spelling(self, text):
        """
        Basic spell correction for non-code text.
        Note: We do not correct code snippets, only natural language queries.
        """
        # Simple heuristic: only correct if text looks like a sentence, not code
        if '{' in text or ';' in text or 'def ' in text:
            return text # Likely code, skip spell check
        
        words = text.split()
        corrected_words = []
        for word in words:
            # Ignore technical symbols or very short words
            if len(word) < 3 or not word.isalpha():
                corrected_words.append(word)
            else:
                correction = self.spell.correction(word)
                corrected_words.append(correction if correction else word)
        return " ".join(corrected_words)

    def get_response(self, user_input):
        # 1. Pre-processing: Spell Check
        cleaned_input = self.correct_spelling(user_input)
        
        if cleaned_input != user_input:
            print(f"{Fore.YELLOW}[Tutor] I noticed some typos. I corrected them to: '{cleaned_input}'{Style.RESET_ALL}\n")

        # 2. Update History
        self.chat_history.append({"role": "user", "content": cleaned_input})

        # 3. Prepare Messages for Groq
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.chat_history
        ]

        try:
            # 4. Call Groq API
            completion = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=messages,
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS
            )

            bot_response = completion.choices[0].message.content

            # 5. Update History with Bot Response
            self.chat_history.append({"role": "assistant", "content": bot_response})

            return bot_response

        except Exception as e:
            return f"{Fore.RED}Error connecting to AI Engine: {str(e)}{Style.RESET_ALL}"

    def save_code_to_file(self, code_content, suggested_name="solution.py"):
        """
        Utility to save generated code to the local file system.
        """
        filename = input(f"{Fore.CYAN}Enter filename to save (default: {suggested_name}): {Style.RESET_ALL}") or suggested_name
        filepath = os.path.join(Config.SAVE_DIR, filename)
        
        # Extract code block if markdown is present
        if "```" in code_content:
            parts = code_content.split("```")
            # Usually the code is in the second part (index 1)
            code_to_save = parts[1] if len(parts) > 1 else code_content
            # Remove language identifier if present (e.g., python\n)
            if "\n" in code_to_save:
                code_to_save = code_to_save.split("\n", 1)[1]
        else:
            code_to_save = code_content

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code_to_save)
        
        print(f"{Fore.GREEN}✅ Code successfully saved to: {filepath}{Style.RESET_ALL}")