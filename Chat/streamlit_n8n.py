
"""
import requests
url = 'http://localhost:5678/webhook-test/1cfaa5e6-51cb-4b26-979c-335699c5fa21'
myobj = {
"query":"Who has the largest salary?",
"data":[
	["id","name","salary","days worked"],
	[1,"Sean",1500,30],
	[2,"Jane",2000,25],
	[3,"Tim",4000,90]
]
}
x = requests.post(url, data = myobj)
print(x.text)
"""

import streamlit as st
import requests
import json

# --- Configuration ---
# Replace with the actual URL of your API endpoint
API_ENDPOINT = "https://chr1st3ll3.app.n8n.cloud/webhook/1cfaa5e6-51cb-4b26-979c-335699c5fa21"



#API_ENDPOINT = "http://localhost:5678/webhook-test/streamlit-test"

# Set the page title and layout
st.set_page_config(
	page_title="Streamlit POST Client",
	layout="centered"
)

## Main Application Logic
st.title("Streamlit Query Sender 🚀")
st.markdown("Enter your query and press 'Send Query' to submit it via **HTTP POST** to a server.")

# --- Input Text Box ---
# The text_area widget is good for multi-line input
query_input = st.text_area(
	"Your Query:",
	key="query_box",
	placeholder="Type your question or data here..."
)

# --- Send Button Logic ---
if st.button("Send Query 📤"):
	if query_input:
		st.info(f"Sending query to **{API_ENDPOINT}**...")

		# 1. Prepare the Data
		# Format the data payload as a dictionary
		
		payload = {
		"query":query_input,
		"data":[
			["id","name","salary","days worked"],
			[1,"Sean",1500,30],
			[2,"Jane",2000,25],
			[3,"Tim",4000,90]
		]
		}

		try:
			# 2. Make the POST Request
			# Set headers for JSON content
			headers = {
				"Content-Type": "application/json"
			}
			response = requests.post(API_ENDPOINT, json=payload, headers=headers)
			
			# 3. Handle the Response
			if response.status_code == 200:
				st.success("✅ **Success!** Query sent and response received.")
				st.subheader("Server Response:")
				
				# Try to display the response body nicely
				try:
					response_json = response.json()
					#st.json(response_json) # Display JSON data
					st.html(response_json[0]['data'])
				except requests.exceptions.JSONDecodeError:
					st.text(response.text) # Display raw text if not JSON
				
				st.caption(f"HTTP Status Code: {response.status_code}")
				
			else:
				st.error(f"❌ **Error!** Failed to send query.")
				st.warning(f"HTTP Status Code: {response.status_code}")
				st.text("Response Body:")
				st.code(response.text, language="text")

		except requests.exceptions.ConnectionError:
			st.error("🔌 **Connection Error:** Could not reach the server.")
			st.warning(f"Please ensure the server is running at **{API_ENDPOINT}**.")
		except requests.exceptions.RequestException as e:
			st.error(f"⚠️ **An unexpected error occurred** during the request: {e}")
			
	else:
		st.warning("Please enter a query before sending. 🤔")

# --- Footer/Information ---
st.markdown(
	"""
---
*Note: This application requires a running server at the specified `API_ENDPOINT` to successfully receive the POST request.*
"""
)
