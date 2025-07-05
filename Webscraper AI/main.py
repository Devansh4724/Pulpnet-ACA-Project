import streamlit as st
from scraper import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama

st.title("AI Webscraper")
url = st.text_input("Enter the website to be scraped: ")
enter = st.button("Scrape Website")

if enter:
    text=st.write("Scraping the website")
    result=scrape_website(url)
    body_content = extract_body_content(result)
    clean_content = clean_body_content(body_content)
    st.session_state.dom_content = clean_content
    with open("processed_data.txt","w",encoding="utf-8") as fobj:
        fobj.write( st.session_state.dom_content)

    with st.expander("View DOM Content"):
        st.text_area("DOM Content",clean_content,height=300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("What do you want to parse?")

if st.button("Parse Content"):
    if parse_description:
        print("Parsing Content")
        dom_chunks = split_dom_content(st.session_state.dom_content)
        result = parse_with_ollama(dom_chunks,parse_description)
        st.write(result)