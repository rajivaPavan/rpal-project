# app.py
import streamlit as st
import editor.guides
from editor.components import switches
from interpreter import Interpreter
import io
import sys

def intepret(code , switch, output_area):
    # Create interpreter instance and run the code
    interpreter = Interpreter(code, switch)
    # Save old stdout
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    # Run interpreter
    interpreter.interpret()

    # Get output and restore stdout
    output = new_stdout.getvalue()
    sys.stdout = old_stdout

    # Display in Streamlit
    output_area.write(output)

def main():
    st.set_page_config(page_title="RPAL Interpreter", page_icon="🐍", layout="wide")

    st.title("RPAL Interpreter")

    # Add radio buttons for switches
    switch_col, space_col, button_col = st.columns(
        [2, 4, 1],
        gap="large",
        vertical_alignment="bottom"
    )
    with switch_col:
        switch = switches()
    with button_col:
        run_button = st.button("Run")

    # Create 3:1 layout for code and output
    code_col, output_col = st.columns([3, 1])

    # Create a text area for code input in left column
    with code_col:
        code = st.text_area("Enter your RPAL code:", height=400)

    # Output display area in right column
    with output_col:
        st.write("Output:")
        output = st.container(border=True, height=400)

    # Add a button to run the code
    if run_button:
        if code:
            try:
                intepret(code, switch, output)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter some code first!")





if __name__ == "__main__":
    main()
