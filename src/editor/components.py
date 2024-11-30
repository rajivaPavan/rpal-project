import streamlit as st

def switches():
    flag_names = {
        None: "Output",
        "-ast": "AST",
        "-st": "ST",
    }
    switch = st.radio(
        "Select output format:",
        [None, "-ast", "-st"],
        format_func= lambda x: flag_names[x],
        horizontal=True
    )
    return switch
