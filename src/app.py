import streamlit as st
import io
import sys
from editor.components import *
from interpreter import Interpreter

def interpret_code(code):
    interpreter = Interpreter(code)
    interpreter.interpret()
    return {
        None: interpreter.get_result(None),
        "-ast": interpreter.get_result("-ast"),
        "-st": interpreter.get_result("-st"),
    }

def main():
    st.set_page_config(page_title="RPAL Interpreter", page_icon="🐍", layout="wide")
    st.title("RPAL Interpreter")

    # Add a sidebar with a link to your GitHub repository
    st.sidebar.title("About")
    st.sidebar.markdown(
        """
        This tool allows you to interpret RPAL code directly in your browser.
        [View on GitHub](https://github.com/rajivaPavan/rpal-project)
        """
    )

    # State to hold code and results
    if "results" not in st.session_state:
        st.session_state["results"] = None
        st.session_state["last_code"] = ""

    # Create a layout for input and output
    code_col, output_col = st.columns([2, 1])

    # Code input
    with code_col:
        code = st.text_area("Enter your RPAL code:", height=400)
        run_button = st.button("Run")

    # Output and format toggle
    with output_col:
        switch = switches()
        output_area = st.empty()

    # Handle "Run" button click
    if run_button:
        if code:
            try:
                # Interpret the code and save results in session state
                st.session_state["results"] = interpret_code(code)
                st.session_state["last_code"] = code
                st.success("Code executed successfully! Toggle output formats to view.")
            except Exception as e:
                st.session_state["results"] = None
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Enter your RPAL code first 👀")

    # Display output based on selected format
    if st.session_state["results"] is not None:
        output = st.session_state["results"].get(switch, "")
        output_area.caption(out_format(switch))
        output_area.text_area("", output, height=400, disabled=True, label_visibility="collapsed")
    elif st.session_state["last_code"] != code:
        st.info("Run the code to see output.")

if __name__ == "__main__":
    main()
