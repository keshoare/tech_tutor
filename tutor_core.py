import os
from groq import Groq
from config import Config
from spellchecker import SpellChecker
from colorama import Fore, Style, init

init(autoreset=True)

class SmartTechTutor:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.spell = SpellChecker()
        
        # ✅ FIX: Load technical words into spell checker whitelist
        technical_words = [
            'roadmap', 'machinelearning', 'machine', 'learning', 'tensorflow', 
            'pytorch', 'numpy', 'pandas', 'sklearn', 'matplotlib', 'keras',
            'api', 'json', 'http', 'https', 'github', 'python', 'javascript',
            'typescript', 'react', 'nodejs', 'docker', 'kubernetes', 'aws',
            'azure', 'gcp', 'sql', 'nosql', 'mongodb', 'postgresql', 'redis',
            'nginx', 'linux', 'backend', 'frontend', 'devops', 'git', 'ml',
            'ai', 'dl', 'nlp', 'cnn', 'rnn', 'lstm', 'gan', 'transformer',
            'bert', 'gpt', 'llm', 'rest', 'graphql', 'websocket', 'tcp',
            'udp', 'ip', 'dns', 'cuda', 'gpu', 'tpu', 'epoch', 'batch',
            'gradient', 'optimizer', 'loss', 'accuracy', 'precision', 'recall'
        ]
        self.spell.word_frequency.load_words(technical_words)
        
        self.chat_history = []
        self.last_response = ""
        
        self.system_prompt = """
You are the 'Smart Tech Tutor', a world-class expert in Computer Science and Programming.

RULES:
1. CODE QUALITY: Generate optimized, clean, production-ready code.
2. COMPLEXITY: NEVER show Time/Space Complexity unless user EXPLICITLY asks.
3. EXPLANATION: If user asks for explanation, break it down step-by-step.
4. ROADMAPS: If user asks for roadmap, provide structured learning path.
5. TONE: Professional, educational, concise.

FORMAT:
- Use Markdown for code blocks.
- Do NOT add complexity analysis unless requested.
- For roadmaps, use clear sections with bullet points.
"""

    def correct_spelling(self, text):
        """Basic spell correction for non-code text."""
        # Skip spell check for commands or code-like text
        if text.startswith('/'):
            return text
        if any(char in text for char in ['{', ';', 'def ', 'import ', 'class ', '=>']):
            return text
        
        words = text.split()
        corrected_words = []
        
        # ✅ FIX: Get the dictionary as a set for lookup
        known_words = set(self.spell.word_frequency.dictionary.keys())
        
        for word in words:
            # Keep words with special characters, numbers, or very short
            if len(word) < 3 or not word.isalpha():
                corrected_words.append(word)
            # ✅ FIX: Check against known_words set (not method)
            elif word.lower() in known_words:
                corrected_words.append(word)
            else:
                correction = self.spell.correction(word)
                corrected_words.append(correction if correction else word)
        
        return " ".join(corrected_words)

    def _user_wants_complexity(self, user_input: str) -> bool:
        """Detect if user is asking for complexity analysis."""
        complexity_keywords = [
            "complexity", "time complexity", "space complexity", 
            "big o", "o(n)", "o(1)", "analyze", "efficiency", 
            "performance", "how efficient", "runtime", "big-o"
        ]
        user_lower = user_input.lower()
        return any(keyword in user_lower for keyword in complexity_keywords)

    def get_stream_response(self, user_input):
        """Stream response from Groq API."""
        # Skip spell check for commands
        if user_input.startswith('/'):
            cleaned_input = user_input
        else:
            cleaned_input = self.correct_spelling(user_input)
        
        if cleaned_input != user_input and not user_input.startswith('/'):
            print(f"{Fore.YELLOW}[Tutor] I noticed some typos. I corrected them to: '{cleaned_input}'{Style.RESET_ALL}\n")

        # Add complexity note only if user asks for it
        if self._user_wants_complexity(user_input):
            cleaned_input += "\n\n[NOTE: Please include Time and Space Complexity analysis at the end.]"

        self.chat_history.append({"role": "user", "content": cleaned_input})

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.chat_history
        ]

        try:
            completion = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=messages,
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS,
                stream=True
            )

            full_response = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            self.chat_history.append({"role": "assistant", "content": full_response})
            self.last_response = full_response

        except Exception as e:
            yield f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}"

    def save_code_to_file(self, code_content, suggested_name="solution.py"):
        """Save generated code to file."""
        filename = input(f"{Fore.CYAN}Enter filename to save (default: {suggested_name}): {Style.RESET_ALL}") or suggested_name
        filepath = os.path.join(Config.SAVE_DIR, filename)
        
        if "```" in code_content:
            parts = code_content.split("```")
            code_to_save = parts[1] if len(parts) > 1 else code_content
            if "\n" in code_to_save:
                code_to_save = code_to_save.split("\n", 1)[1]
        else:
            code_to_save = code_content

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code_to_save)
        
        print(f"{Fore.GREEN}✅ Code successfully saved to: {filepath}{Style.RESET_ALL}")

    def switch_model(self, model_name: str):
        """Switch AI models."""
        valid_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
        if model_name in valid_models:
            Config.MODEL_NAME = model_name
            print(f"{Fore.GREEN}✅ Model switched to: {model_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Invalid model. Choose from: {valid_models}{Style.RESET_ALL}")
