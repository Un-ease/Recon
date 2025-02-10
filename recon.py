import subprocess
import os
import time
import threading

# Function to display the landing page
def landing_page():
    text = '''
    
	\033[31m░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░░▒▓██████▓▒░░▒▓████████▓▒░▒▓████████▓▒░ 	\033[31m
	\033[31m░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░        	\033[31m
	\033[31m░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░    ░▒▓██▓▒░░▒▓█▓▒░        	\033[31m
	\033[31m░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓████████▓▒░  ░▒▓██▓▒░  ░▒▓██████▓▒░   	\033[31m
	\033[31m░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██▓▒░    ░▒▓█▓▒░        	\033[31m
	\033[31m░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        	\033[31m
 	\033[31m░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░ 	\033[31m

	\033[31m             Subdomain Enumeration Tool v1.1 - Anij Gurung	\033[31m
	\033[31m              ---------------------------------------------	\033[31m
	\033[31m                Enter your domain and save location below.	\033[31m
	\033[31m                 Press Ctrl+C to cancel at any time.	\033[31m
	\033[31m              ---------------------------------------------	\033[31m

                                                                                '''
    print(text)

# Loading animation function
def loading_animation(stop_event):
    symbols = ['|', '/', '-', '\\']
    i = 0
    while not stop_event.is_set():
        print(f"\rRunning... {symbols[i % len(symbols)]}", end="", flush=True)
        i += 1
        time.sleep(0.1)
    print("\r" + " " * 50, end="\r")  # Clear line after stopping

# Function to run subdomain enumeration tools and save the output
def enumerate_subdomains(domain, save_location):
    os.makedirs(save_location, exist_ok=True)  # Ensure the save directory exists

    try:
        # Subfinder
        print("\nStarting subfinder...")
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        loading_thread.start()
        with open(f"{save_location}/subdomain1.txt", "w") as outfile:
            result = subprocess.run(
                ["subfinder", "-d", domain, "-all"],
                stdout=outfile,
                stderr=subprocess.PIPE,
                text=True
            )
        stop_event.set()
        loading_thread.join()
        print(f"\rsubfinder {'completed successfully' if result.returncode == 0 else 'failed'}. Output saved to {save_location}/subdomain1.txt.")

        # Assetfinder
        print("\nStarting assetfinder...")
        stop_event.clear()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        loading_thread.start()
        with open(f"{save_location}/subdomain2.txt", "w") as outfile:
            result = subprocess.run(
                ["assetfinder", "--subs-only", domain],
                stdout=outfile,
                stderr=subprocess.PIPE,
                text=True
            )
        stop_event.set()
        loading_thread.join()
        print(f"\rassetfinder {'completed successfully' if result.returncode == 0 else 'failed'}. Output saved to {save_location}/subdomain2.txt.")

        # Spyhunt
        print("\nStarting spyhunt...")
        stop_event.clear()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        loading_thread.start()
        spyhunt_dir = os.path.expanduser("~/spyhunt/")
        venv_activate = os.path.join(spyhunt_dir, "venv/bin/activate")
        spyhunt_script = os.path.join(spyhunt_dir, "spyhunt.py")
        spyhunt_command = f"cd {spyhunt_dir} && . {venv_activate} && python3 {spyhunt_script} -s {domain} --save {save_location}/subdomain3.txt"
        result = subprocess.run(
            ["bash", "-c", spyhunt_command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stop_event.set()
        loading_thread.join()
        print(f"\rspyhunt {'completed successfully' if result.returncode == 0 else 'failed'}. Output saved to {save_location}/subdomain3.txt.")

        print("\nMerging and sorting subdomains...")
        subprocess.run(
            ["sort", "-u",
             f"{save_location}/subdomain1.txt",
             f"{save_location}/subdomain2.txt",
             f"{save_location}/subdomain3.txt",
             "-o", f"{save_location}/domain.txt"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print(f"\n✅ Unique subdomains saved in {save_location}/domain.txt")

    except Exception as e:
        print(f"\rError running subdomain tools: {str(e)}")

# Main function to handle user input and orchestrate the process
def main():
    import sys
    try:
        landing_page()  # Display the landing page
        
        domain = input("Enter the domain: ").strip()
        save_location = input("Enter the save location (default ./results/): ").strip() or "./results/"
        
        # Validate domain (basic check)
        if not domain or "." not in domain:
            print("Invalid domain. Please enter a valid domain.")
            return
        
        save_location = os.path.abspath(save_location)  # Convert to absolute path
        
        enumerate_subdomains(domain, save_location)  # Run subdomain enumeration

    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Please try again.")
        sys.exit(1)

# Entry point of the script
if __name__ == "__main__":
    main()
