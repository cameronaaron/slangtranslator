import os
import tkinter as tk
from tkinter import messagebox
import logging
import openai

# Set up logging
logging.basicConfig(filename='translator.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Load OpenAI API key from environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')

def create_conversation_message(role, content):
    """Create a message object for a conversation."""
    return {"role": role, "content": content}

def translate_to_standard_english(conversation):
    """Translate slang or vernacular language to standard English using OpenAI API."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].message['content']
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return "An error occurred while processing your request."

def validate_user_input(user_input):
    """Validate user input and return an error message if input is invalid."""
    if user_input.strip() == "":
        return "Input cannot be empty. Please enter a valid message."
    return None

def update_output_text_widget(output_text_widget, text):
    """Update the output text widget with the translated text."""
    output_text_widget.delete("1.0", "end")
    output_text_widget.insert("end", text)

def create_conversation_object(user_input):
    """Create a conversation object for the OpenAI API."""
    return [
        create_conversation_message("system", "You are a helpful assistant that translates slang or vernacular language into standard English. Your main task is to provide clear, easy-to-understand translations. You should also try to give context where necessary to make the translations as useful as possible."),
        create_conversation_message("user", user_input)
    ]

def call_openai_api(conversation):
    """Call the OpenAI API to translate slang to standard English."""
    return translate_to_standard_english(conversation)

def handle_translate_button_click(input_text_widget, output_text_widget):
    """Handle the click event for the translate button."""
    # Get user input from input_text widget
    user_input = input_text_widget.get("1.0", "end-1c")

    # Validate user input
    error_message = validate_user_input(user_input)
    if error_message is not None:
        messagebox.showerror("Input Error", error_message)
        return

    # Create conversation object for OpenAI API
    conversation = create_conversation_object(user_input)

    # Call OpenAI API to translate slang to standard English
    response = call_openai_api(conversation)

    # Update output_text widget with translated text
    update_output_text_widget(output_text_widget, response)

def create_input_text_widget(main_window):
    """Create the input text widget."""
    input_text_widget = tk.Text(main_window, height=10)
    return input_text_widget

def create_output_text_widget(main_window):
    """Create the output text widget."""
    output_text_widget = tk.Text(main_window, height=10)
    return output_text_widget

def create_translate_button(main_window, input_text_widget, output_text_widget):
    """Create the translate button."""
    translate_button = tk.Button(main_window, text="Translate", command=lambda: handle_translate_button_click(input_text_widget, output_text_widget))
    return translate_button

def pack_gui_elements(input_label, input_text_widget, output_label, output_text_widget, translate_button):
    """Pack the GUI elements."""
    input_label.pack()
    input_text_widget.pack()
    output_label.pack()
    output_text_widget.pack()
    translate_button.pack()

def create_main_window():
    """Create the main window and GUI elements."""
    # Create main window
    main_window = tk.Tk()
    main_window.title("Slang Translator")

    # Create GUI elements
    input_label = tk.Label(main_window, text="Enter slang or vernacular text:")
    output_label = tk.Label(main_window, text="Standard English translation:")
    input_text_widget = create_input_text_widget(main_window)
    output_text_widget = create_output_text_widget(main_window)
    translate_button = create_translate_button(main_window, input_text_widget, output_text_widget)
    pack_gui_elements(input_label, input_text_widget, output_label, output_text_widget, translate_button)

    return main_window

def run():
    """Create main window and run the main loop."""
    # Create main window and GUI elements
    main_window = create_main_window()

    # Run the main loop
    main_window.mainloop()

if __name__ == "__main__":
    run()