mkdir -p ~/.streamlit/
echo "[theme]
primaryColor='#0056d2'
backgroundColor='#f6f6f6'
secondaryBackgroundColor='#efefef'
textColor='#141414'
font = 'sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
