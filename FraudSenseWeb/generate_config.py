import json

def generate_config():
    config_data = {}

    print("Welcome to the Config.js Generator!")

    # Collect user input for configuration
    config_data['BASE_URL'] = input("Enter the API Base URL: ")

    # Ensure the BASE_URL starts with http or https
    if not config_data['BASE_URL'].startswith(('http://', 'https://')):
        config_data['BASE_URL'] = 'http://' + config_data['BASE_URL']

    # Write the configuration to config.js
    with open('config.js', 'w') as config_file:
        config_file.write(f'export const BASE_URL = "{config_data["BASE_URL"]}";\n')

    print("config.js has been generated successfully!")

if __name__ == "__main__":
    generate_config()