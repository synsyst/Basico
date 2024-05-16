import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# Fetch api key for openai - personal account
Client = OpenAI(api_key = st.secrets["apikey"])

# OpenAI function
def get_response(message):
    try:
        response = Client.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages = [
                {"role": "system", "content": "You're a professional and helpful assistant in the company Basico"},
                {"role": "user", "content": message}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


st.title('Basico Assistant')
st.write('The Basico assistant will help you with any queries regarding our company, feel free to chat at any time :)')

# Embed JavaScript to listen for Enter key press and click the send button
# so far this javascript listener doesn't really work as intended
components.html("""
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            var input = document.querySelector('input[type="text"]');
            input.addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    event.preventDefault();
                    document.querySelector('button[type="button"]').click();
                }
            });
        });
    </script>
""")


user_input = st.text_input('You:', '')
response_placeholder = st.empty()

# Submit button
if st.button('Send'):
    if user_input:
        response = get_response(user_input)
        response_placeholder.write(f"Assistant: {response}")
    else:
        response_placeholder.write('Please provide a query to receive a response :)')

st.write("""
## Scope Extensions
* Implement cosine similarity search for improved response matching. - more extensive that anticipated, learnings: standalone embedding script to reduce api cost, cosine-similarity match with user query, and then submitting query + any found contextual data
* Enhance the UI with conversation history.
* Clear input field after query submission
* Make enter key activate Send key
""")