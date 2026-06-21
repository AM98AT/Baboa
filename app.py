# -*- coding: utf-8 -*-
"""Entry point. The app is split into modules under lib/ — see lib/pages.py for main()."""
import streamlit as st

st.set_page_config(
    page_title="متابعة الصحّة اليومية",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from lib.styles import inject_css
from lib.pages import main

inject_css()
main()
