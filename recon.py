import subprocess
import os
import time
import threading

# Function to display the landing page
def landing_page():
    text = '''
    
░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░░▒▓██████▓▒░░▒▓████████▓▒░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░    ░▒▓██▓▒░░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓████████▓▒░  ░▒▓██▓▒░  ░▒▓██████▓▒░   
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██▓▒░    ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░ 

                        Subdomain Enumeration Tool v1.0
                  ---------------------------------------------
                  Enter your domain and save location below.
                  Press Ctrl+C to cancel at any time.
                  ---------------------------------------------

                                                                                '''
    print(text)

# Loading animation function
def loading_animation(stop_event):
    symbols = ['|', '/', '-', '\\']
    i = 0
    while not stop_event.is_set():
        print(f"\rRunning... {symbols[i % len(symbols)]}", end="")
        i += 1
        time.sleep(0.1)

# Function to run subdomain enumeration tools and save the output
def enumerate_subdomains(domain, save_location):
    # Ensure the save directory exists
    os.makedirs(save_location, exist_ok=True)

    try:
        # Subfinder
        print("\nStarting subfinder...")
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        loading_thread.start()
        with open(f"{save_location}/subdomain1.txt", "w") as outfile:
            result = subprocess.run(
                ["subfinder", "-d", domain, "-all", "recursive"],
                stdout=outfile,
                stderr=subprocess.PIPE,
                text=True
            )
        stop_event.set()
        loading_thread.join()
        if result.returncode == 0:
            print(f"\rsubfinder completed successfully. Output saved to {save_location}/subdomain1.txt.")
        else:
            print(f"\rsubfinder failed with status: {result.returncode}. Error: {result.stderr.strip()}")

        # Assetfinder
        print("\nStarting assetfinder...")
        stop_event = threading.Event()
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
        if result.returncode == 0:
            print(f"\rassetfinder completed successfully. Output saved to {save_location}/subdomain2.txt.")
        else:
            print(f"\rassetfinder failed with status: {result.returncode}. Error: {result.stderr.strip()}")

        # Spyhunt
        print("\nStarting spyhunt...")
        stop_event = threading.Event()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
        loading_thread.start()
        spyhunt_dir = os.path.expanduser("~/spyhunt/")
        venv_activate = os.path.join(spyhunt_dir, "venv/bin/activate")
        spyhunt_script = os.path.join(spyhunt_dir, "spyhunt.py")
        result = subprocess.run(
            f"cd {spyhunt_dir} && source {venv_activate} && python3 {spyhunt_script} -s {domain} --save {save_location}/subdomain3.txt",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stop_event.set()
        loading_thread.join()
        if result.returncode == 0:
            print(f"\rspyhunt completed successfully. Output saved to {save_location}/subdomain3.txt.")
        else:
            print(f"\rspyhunt failed with status: {result.returncode}. Error: {result.stderr.strip()}")

    except Exception as e:
        print(f"\rError running subdomain tools: {str(e)}")

# Main function to handle user input and orchestrate the process
def main():
    import sys
    try:
        # Display the landing page
        landing_page()
        
        # Get user inputs
        domain = input("Enter the domain: ").strip()
        save_location = input("Enter the save location (default ./results/): ").strip() or "./results/"
        
        # Validate domain (basic check)
        if not domain or "." not in domain:
            print("Invalid domain. Please enter a valid domain.")
            return
        
        # Run the subdomain enumeration
        enumerate_subdomains(domain, save_location)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Please try again.")
        return

# Entry point of the script
if __name__ == "__main__":
    main()