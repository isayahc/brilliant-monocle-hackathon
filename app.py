import streamlit as st

# Simple function to handle the bot response
def bot_response(user_input):
    # You can add more complex logic here
    if "hello" in user_input.lower():
        return "Hello! How can I help you today?"
    else:
        return "I'm sorry, I don't understand that. Can you please rephrase?"

# Main app
def main():
    st.title('My Simple Chatbot')

    # Initialize the session state for conversation history
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Display the conversation history
    for message in st.session_state.conversation:
        sender, text = message.split(': ', 1)
        if sender == "You":
            st.markdown(f"<div style='text-align: left; color: blue;'>{sender}: {text}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: right; color: green;'>{sender}: {text}</div>", unsafe_allow_html=True)

    user_input = st.text_input("You: ")
    if user_input:
        st.session_state.conversation.append(f"You: {user_input}")
        bot_reply = bot_response(user_input)
        st.session_state.conversation.append(f"Bot: {bot_reply}")

if __name__ == '__main__':
    main()
