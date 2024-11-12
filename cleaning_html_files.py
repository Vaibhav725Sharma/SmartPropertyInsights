import os
from bs4 import BeautifulSoup

def clean_html_file(input_path, output_path):
    # Load the HTML content
    with open(input_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove all CSS and JavaScript tags
    for tag in soup(["style", "script"]):
        tag.decompose()

    # Save the cleaned HTML to the desired path
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(soup.prettify())

    print(f"Cleaned HTML file saved as '{output_path}'")

def clean_all_html_files(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all the files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".html"):
            input_path = os.path.join(input_folder, filename)
            output_filename = f"cleaned_{filename}"
            output_path = os.path.join(output_folder, output_filename)
            
            # Clean the HTML file and save it
            clean_html_file(input_path, output_path)

# Set paths for input and output folders
input_folder = "C:/Users/acer/Desktop/Smart_Real_State/Scraped Html"
output_folder = "C:/Users/acer/Desktop/Smart_Real_State/Cleaned Html files"

# Clean all HTML files in the input folder and save them to the output folder
clean_all_html_files(input_folder, output_folder)
