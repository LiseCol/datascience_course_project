def remote_css(url):
    st.markdown('<style src="{}"></style>'.format(url), unsafe_allow_html=True)
