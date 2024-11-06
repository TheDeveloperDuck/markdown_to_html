# Library to convert Markdown to HTML
import markdown
# System-specific functions and parameters
import sys  
# Logging library to record events and errors
import logging  
# For handling file paths
from pathlib import Path
# OS module to interact with the operating system
import os


# Directories for logs and output files
LOG_DIR = "script_logs"
OUTPUT_DIR = "output_html"
LOG_FILE = f"{LOG_DIR}/markdown_to_html.log"

# Ensure the log and output directories exist, creating them if necessary
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set up logging configuration
logging.basicConfig(
    # Log file to record events
    filename="markdown_to_html.log",
    # Set level to INFO to capture general information and errors
    level=logging.INFO, 
    # Log message format
    format="%(asctime)s - %(levelname)s - %(message)s",  
)

# Default file names for HTML and CSS templates if not provided
DEFAULT_HTML_TEMPLATE = "template.html"
DEFAULT_CSS_TEMPLATE = "style.css"

def markdown_to_html(md_file: str, html_template_file: str, css_template_file: str) -> str:
    """
    Convert a Markdown file to HTML using a given HTML template and CSS template.

    Parameters:
    - md_file: Path to the Markdown file
    - html_template_file: Path to the HTML template file containing placeholders
    - css_template_file: Path to the CSS template file with styling information
    
    Returns:
    - A string containing the final HTML output with embedded CSS and content
    """
    
    # Try to read the markdown content from the given file
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()  # Read the entire Markdown file content as a string
        logging.info(f"Successfully read Markdown file '{md_file}'")
    except FileNotFoundError:  # If the file is not found, handle the error gracefully
        logging.error(f"Markdown file '{md_file}' not found.")
        sys.exit(1)  # Exit the program with an error code

    # Convert the Markdown content to HTML
    html_content = markdown.markdown(md_content)  # Convert the Markdown text to HTML using markdown library
    logging.info("Converted Markdown to HTML content")

    # Try to read the CSS content from the given file
    try:
        with open(css_template_file, 'r', encoding='utf-8') as f:
            css_content = f.read()  # Read the entire CSS file content as a string
        logging.info(f"Successfully read CSS template file '{css_template_file}'")
    except FileNotFoundError:  # If the CSS file is not found, handle the error
        logging.error(f"CSS template file '{css_template_file}' not found.")
        sys.exit(1)  # Exit the program with an error code

    # Try to read the HTML template content from the given file
    try:
        with open(html_template_file, 'r', encoding='utf-8') as f:
            html_template = f.read()  # Read the entire HTML template file as a string
        logging.info(f"Successfully read HTML template file '{html_template_file}'")
    except FileNotFoundError:  # If the HTML template file is not found, handle the error
        logging.error(f"HTML template file '{html_template_file}' not found.")
        sys.exit(1)  # Exit the program with an error code

    # Insert the CSS content into the HTML template at the {{ css }} placeholder
    final_html = html_template.replace("{{ css }}", f"<style>{css_content}</style>")
    
    # Insert the converted HTML content into the HTML template at the {{ content }} placeholder
    final_html = final_html.replace("{{ content }}", html_content)
    
    logging.info("Successfully combined HTML content and templates")
    
    # Return the final HTML content as a string
    return final_html

# Main entry point of the script
if __name__ == "__main__":
    # Check if the script is run with at least 1 argument (Markdown file path)
    if len(sys.argv) < 2:
        logging.error("Insufficient arguments. At least the Markdown file must be provided.")
        print("Usage: python markdown_to_html.py <markdown_file> [html_template_file] [css_template_file]")
        sys.exit(1)  # Exit if the correct number of arguments is not provided

    # Assign command-line arguments to respective variables
    md_file = sys.argv[1]  # Markdown file path
    html_template_file = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_HTML_TEMPLATE  # HTML template file path or default
    css_template_file = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_CSS_TEMPLATE  # CSS template file path or default
    
    # Log which templates are being used
    logging.info(f"Using HTML template: '{html_template_file}'")
    logging.info(f"Using CSS template: '{css_template_file}'")
    
    # Generate the final HTML content by calling the markdown_to_html function
    html_output = markdown_to_html(md_file, html_template_file, css_template_file)
    
    # Define the output HTML file path, changing the extension of the Markdown file to .html and saving in OUTPUT_DIR
    output_file = Path(OUTPUT_DIR) / Path(md_file).with_suffix(".html").name
    
    # Write the final HTML content to the output file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_output)  # Save the HTML content in the specified output file
        logging.info(f"Converted HTML saved to '{output_file}'")
    except IOError as e:  # Catch any IO errors while writing to the file
        logging.error(f"Failed to write output HTML file '{output_file}': {e}")
        sys.exit(1)  # Exit the program with an error code
    
    # Print a confirmation message with the path of the generated HTML file
    print(f"Converted HTML saved to '{output_file}'")