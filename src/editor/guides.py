import streamlit as st

def examples():
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
def documentation():
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
