import streamlit as st

st.title('Basico Assistant')
st.write('The Basico assistant will help you with any queries regarding our company, feel free to chat at any time :)')

user_input = st.text_input('You:', '')
response_placeholder = st.empty()

# Submit button
if st.button('Send'):
    response_placeholder.write('Bot: [response will appear here]')

st.write("""
## Next Steps
1. Integrate OpenAI API to generate responses.
2. Implement cosine similarity search for improved response matching.
3. Enhance the UI with conversation history.
""")