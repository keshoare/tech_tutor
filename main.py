from tutor_core import SmartTechTutor
from colorama import Fore, Style, init

init(autoreset=True)

def print_banner():
    print(Fore.BLUE + """
    ╔══════════════════════════════════════════════════════════╗
    ║           🤖 SMART TECH TUTOR (CLI EDITION) 🤖           ║
    ║      Powered by Groq AI | Backend: Qwen Senior Dev       ║
    ╚══════════════════════════════════════════════════════════╝
    """ + Style.RESET_ALL)

def main():
    tutor = SmartTechTutor()
    print_banner()
    
    print(f"{Fore.YELLOW}Instructions:{Style.RESET_ALL}")
    print("- Type your coding question.")
    print("- Type 'save' after a code generation to save the last output to a file.")
    print("- Type 'exit' to quit.\n")

    last_response = ""

    while True:
        try:
            user_input = input(f"{Fore.GREEN}You:{Style.RESET_ALL} ").strip()

            if not user_input:
                continue
            if user_input.lower().startswith('switch_model '):
                model = user_input.split(' ', 1)[1]
                tutor.switch_model(model)
                continue
            if user_input.lower() == 'exit':
                print(f"{Fore.RED}Shutting down Smart Tech Tutor...{Style.RESET_ALL}")
                break
            
            if user_input.lower() == 'save':
                if last_response:
                    tutor.save_code_to_file(last_response)
                else:
                    print(f"{Fore.YELLOW}No code generated yet to save.{Style.RESET_ALL}")
                continue

            # Get AI Response
            print(f"{Fore.CYAN}Tutor is thinking...{Style.RESET_ALL}")
            response = tutor.get_response(user_input)
            last_response = response
            
            # Print Response
            print(f"\n{Fore.BLUE}Tutor:{Style.RESET_ALL}")
            print(response)
            print("\n" + "-"*50 + "\n")

        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Interrupted by user. Exiting.{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()