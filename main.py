from tutor_core import SmartTechTutor
from config import Config
from colorama import Fore, Style, init

init(autoreset=True)

def print_banner():
    print(Fore.BLUE + """
    ╔══════════════════════════════════════════════════════════╗
    ║            SMART TECH TUTOR (CLI EDITION) 🤖           
    ║      Powered by Groq AI | Backend: Qwen Senior Dev       ║
    ╚══════════════════════════════════════════════════════════╝
    """ + Style.RESET_ALL)

def print_help():
    print(Fore.CYAN + """
    ════════════════ COMMANDS ════════════════
    /fast            → Switch to FAST model (8B)
    /smart           → Switch to SMART model (70B)
    /model           → Show current model
    /save            → Save last code to file
    /help            → Show this help menu
    /clear           → Clear chat history
    /roadmap [topic] → Get learning roadmap for topic
    exit             → Quit the tutor
    ═══════════════════════════════════════════
    """ + Style.RESET_ALL)

def main():
    tutor = SmartTechTutor()
    print_banner()
    print_help()
    
    while True:
        try:
            user_input = input(f"{Fore.GREEN}You:{Style.RESET_ALL} ").strip()

            if not user_input:
                continue

            # Exit command
            if user_input.lower() == 'exit':
                print(f"{Fore.RED}Shutting down Smart Tech Tutor...{Style.RESET_ALL}")
                break
            
            # Help command
            if user_input.lower() == '/help':
                print_help()
                continue
            
            # ✅ MODEL SWITCH: Exact match only (no extra text)
            if user_input.lower() == '/fast':
                tutor.switch_model("llama-3.1-8b-instant")
                print(f"{Fore.YELLOW}Now ask your question:{Style.RESET_ALL}")
                continue
            
            if user_input.lower() == '/smart':
                tutor.switch_model("llama-3.3-70b-versatile")
                print(f"{Fore.YELLOW}Now ask your question:{Style.RESET_ALL}")
                continue
            
            # Show current model
            if user_input.lower() == '/model':
                print(f"{Fore.CYAN}Current model: {Config.MODEL_NAME}{Style.RESET_ALL}")
                continue
            
            # Save command
            if user_input.lower() == '/save':
                if tutor.last_response:
                    tutor.save_code_to_file(tutor.last_response)
                else:
                    print(f"{Fore.YELLOW}No code generated yet to save.{Style.RESET_ALL}")
                continue
            
            # Clear chat history
            if user_input.lower() == '/clear':
                tutor.chat_history = []
                print(f"{Fore.GREEN}✅ Chat history cleared.{Style.RESET_ALL}")
                continue
            
            # ✅ ROADMAP COMMAND
            if user_input.lower().startswith('/roadmap'):
                topic = user_input.replace('/roadmap', '').strip()
                if topic:
                    user_input = f"Create a detailed learning roadmap for {topic}. Include: 1) Prerequisites 2) Topics in order 3) Resources 4) Timeline 5) Projects"
                else:
                    print(f"{Fore.YELLOW}Please specify a topic. Example: /roadmap machine learning{Style.RESET_ALL}")
                    continue

            # Get AI Response (Streaming)
            print(f"{Fore.CYAN}Tutor:{Style.RESET_ALL} ", end='')
            
            for chunk in tutor.get_stream_response(user_input):
                print(chunk, end='', flush=True)
            
            print("\n" + "-"*50 + "\n")

        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Interrupted by user. Exiting.{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()  # Print full error for debugging

if __name__ == "__main__":
    main()
