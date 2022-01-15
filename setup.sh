mkdir -p ~/.streamlit/
echo "[theme]
base='light'
primaryColor=’#080808’
secondaryBackgroundColor=’#e6d8a7’
textColor='#292103'
font = ‘sans serif’
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml