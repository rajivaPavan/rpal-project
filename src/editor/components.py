import streamlit as st

__flag_names = {
    None: "Output",
    "-ast": "AST",
    "-st": "ST",
}

out_format  = lambda x: __flag_names[x]

def switches():
    switch = st.radio(
        "Select output format:",
        [None, "-ast", "-st"],
        format_func=out_format,
        horizontal=True,
        label_visibility="collapsed",
    )
    return switch
