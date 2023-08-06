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

    user_input = st.text_input("You: ")
    if user_input:
        st.session_state.conversation.append(f"You: {user_input}")
        bot_reply = bot_response(user_input)
        st.session_state.conversation.append(f"Bot: {bot_reply}")

        # Display the conversation history
        st.write('\n'.join(st.session_state.conversation))

if __name__ == '__main__':
    main()
