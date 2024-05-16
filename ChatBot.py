import streamlit as st
import openai

# Fetch api key for openai - personal account
openai.api_key = st.secrets["apikey"]

# OpenAI function
def get_response(message):
    try:
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages = [{"role": "user", "content": message}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"


st.title('Basico Assistant')
st.write('The Basico assistant will help you with any queries regarding our company, feel free to chat at any time :)')

user_input = st.text_input('You:', '')
response_placeholder = st.empty()

# Submit button
if st.button('Send'):
    if user_input:
        response = get_response(user_input)
        response_placeholder.write(f"Bot: {response}")
    else:
        response_placeholder.write('Your message goes here :)')

# Test - Remove me
apikey = st.secrets["apikey"]
st.write(f"API key is {apikey}")

st.write("""
## Next Steps
1. Integrate OpenAI API to generate responses.
2. Implement cosine similarity search for improved response matching.
3. Enhance the UI with conversation history.
""")