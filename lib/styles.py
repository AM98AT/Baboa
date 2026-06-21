# -*- coding: utf-8 -*-
"""Mobile-first + Arabic right-to-left CSS, injected once at startup."""
import streamlit as st

_CSS = """
<style>
/* whole app right-to-left, Arabic-friendly fonts */
html, body, .stApp, .block-container, [data-testid="stMarkdownContainer"] {
    direction: rtl; text-align: right;
    font-family: "Segoe UI", Tahoma, "Noto Naskh Arabic", "Arial", sans-serif; }
/* hide Streamlit's own top toolbar (it overlaps content on mobile) */
header[data-testid="stHeader"] { display: none; }
/* our own fixed header bar */
.app-header { position: fixed; top: 0; left: 0; right: 0; height: 52px; z-index: 1000;
    background: #1565c0; color: #fff; display: flex; align-items: center;
    justify-content: center; font-size: 1.15rem; font-weight: 700;
    box-shadow: 0 2px 6px rgba(0,0,0,0.25); }
/* tighter padding + readable width on phones; top space clears the fixed header */
.block-container { padding-top: 4.3rem; padding-bottom: 3rem;
    padding-left: 0.8rem; padding-right: 0.8rem; max-width: 640px; }
/* bigger base text for older eyes */
html, body, [class*="css"] { font-size: 17px; }
/* full-width, tall, rounded buttons = easy to tap */
.stButton > button { width: 100%; padding: 0.65rem 0.8rem;
    font-size: 1.05rem; border-radius: 12px; font-weight: 600; }
/* hide menu/footer clutter */
#MainMenu, footer { visibility: hidden; }
/* expander headers larger and easier to tap */
.streamlit-expanderHeader, details summary { font-size: 1.05rem !important; }
/* metric numbers sized so 3 fit on a phone row */
[data-testid="stMetricValue"] { font-size: 1.5rem; }
[data-testid="stMetricLabel"] { font-size: 0.8rem; }
/* keep the chart itself left-to-right so numbers/dates read correctly */
[data-testid="stPlotlyChart"] { direction: ltr; }
/* link styled as a full-width "See details" button */
a.seebtn { display:block; width:100%; box-sizing:border-box; text-align:center;
    background:#1565c0; color:#fff !important; text-decoration:none;
    padding:0.6rem 0.8rem; border-radius:12px; font-weight:700; font-size:1.02rem;
    margin:2px 0 12px 0; }
/* sticky back bar that scrolls with you */
a.backbtn { position:sticky; top:52px; z-index:900; display:block; width:100%;
    box-sizing:border-box; text-align:center; background:#37474f; color:#fff !important;
    text-decoration:none; padding:0.7rem; border-radius:0 0 12px 12px; font-weight:700;
    font-size:1.08rem; margin-bottom:12px; box-shadow:0 2px 6px rgba(0,0,0,0.2); }
/* navigation chips */
a.navchip { display:inline-block; margin:3px; padding:7px 12px; border-radius:18px;
    text-decoration:none; font-weight:600; font-size:0.95rem; }
</style>
"""


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)
