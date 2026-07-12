import os
import streamlit as st
from researcher_agent import run_researcher
from planner_agent import run_planner

os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]

st.title("✈️ AI Travel Planning Agent")

origin = st.text_input("Your location", placeholder="e.g. Delhi, India")
destination = st.text_input("Destination", placeholder="e.g. Paris, France")

if st.button("Plan my trip"):
    if origin and destination:
        with st.spinner("Researching... this takes 2-3 minutes"):
            findings = run_researcher(origin, destination, verbose=False)
            report = run_planner(origin, destination, findings, verbose=False)
        st.markdown(report)
    else:
        st.warning("Please enter both location and destination")