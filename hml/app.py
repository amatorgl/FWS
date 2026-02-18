import streamlit as st

# Set the title of the app
st.title('My Streamlit App')

# Add a header
st.header('Welcome to my Streamlit app!')

# Create a text input field
user_input = st.text_input('Enter some text:')

# Display the input back to the user
if user_input:
    st.write(f'You entered: {user_input}')