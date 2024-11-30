# app.py
import streamlit as st
from interpreter import Interpreter
import io
import sys

def intepret(code , switch) :
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
    st.write(output)


def main():
    st.title("RPAL Interpreter")

    # Create a text area for code input
    code = st.text_area("Enter your RPAL code:", height=200)

    # Add radio buttons for switches
    switch = st.radio(
        "Select output type:",
        [None, "-ast", "-st"],
        format_func=lambda x: "Default output" if x is None else x
    )

    # Add a button to run the code
    if st.button("Run"):
        if code:
            try:
                intepret(code, switch)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter some code first!")

    # Add examples section
    with st.expander("Example Programs"):
        st.markdown("""
        **1. Hello World**
        ```
        'Hello World'
        ```

        **2. Simple Arithmetic**
        ```
        let sum = 2 + 3 in sum
        ```

        **3. Function Definition**
        ```
        let f x = x + 1 in f 3
        ```

        **4. Recursion**
        ```
        let fact = fn n.
            n eq 0 -> 1
            | n * fact (n-1)
        in fact 5
        ```

        **5. Tuple Construction**
        ```
        let t = (1,2,3) in t
        ```
        """)

    # Add documentation section
    with st.expander("RPAL Language Guide"):
        st.markdown("""
        ### Basic Syntax
        - Comments start with //
        - Strings are enclosed in single quotes
        - Basic arithmetic operators: +, -, *, /, **
        - Boolean operators: and, or, not
        - Comparison operators: eq, ne, gr, ge, ls, le

        ### Variable Declaration
        ```
        let x = value in expression
        ```

        ### Function Definition
        ```
        let f x = expression in f arg
        // or
        let f = fn x.expression in f arg
        ```

        ### Conditional Expression
        ```
        condition -> expression1 | expression2
        ```

        ### List Operations
        ```
        Order, Conc, Stem, Stern
        ```

        ### Built-in Functions
        - Print: Prints values
        - Order: Returns length of tuple
        - Conc: Concatenates strings
        - ItoS: Converts integer to string
        """)

if __name__ == "__main__":
    main()
