import subprocess
import os

def landing_page():
    text ='''
    
░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░░▒▓██████▓▒░░▒▓████████▓▒░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░    ░▒▓██▓▒░░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓████████▓▒░  ░▒▓██▓▒░  ░▒▓██████▓▒░   
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██▓▒░    ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░ 
                                                                                
                                                                                '''
    print(text)

# List of subdomain enumeration tools and their configurations

# Function to run subdomain enumeration tools and save the output
def enumerate_subdomains(domain, save_location):
    # Ensure the save directory exists
    os.makedirs(save_location, exist_ok=True)

    # List of tools and their commands
    tools = [
        ("subfinder", ["subfinder", "-d", domain, "-all", "recursive"]),
        ("assetfinder", ["assetfinder", "--subs-only", domain]),
        ("spyhunt", ["python3", "spyhunt.py", "-s", domain, "--save"])
    ]

    try:
        for tool_name, command in tools:
            print(f"Running {tool_name}...")
            
            if tool_name == "spyhunt":
                # Special handling for spyhunt
                spyhunt_dir = os.path.expanduser("~/spyhunt/")
                venv_activate = os.path.join(spyhunt_dir, "venv/bin/activate")
                spyhunt_script = os.path.join(spyhunt_dir, "spyhunt.py")
                
                # Change directory, activate venv, and run the script
                result = subprocess.run(
                    f"cd {spyhunt_dir} && source {venv_activate} && python3 {spyhunt_script} -s {domain} --save {save_location}/subdomain3.txt",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                # Run other tools normally
                with open(f"{save_location}/{tool_name}_output.txt", "w") as outfile:
                    result = subprocess.run(
                        command,
                        stdout=outfile,
                        stderr=subprocess.PIPE,
                        text=True
                    )

            # Check the result of the subprocess
            if result.returncode == 0:
                print(f"{tool_name} completed successfully.")
            else:
                print(f"{tool_name} failed with status: {result.returncode}")
                print(f"Error: {result.stderr}")

    except Exception as e:
        print(f"Error running subdomain tools: {str(e)}")

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