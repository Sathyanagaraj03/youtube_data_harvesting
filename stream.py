import streamlit as st
def main():
    st.title("Youtube Data Harvesting!!")

    # HTML code for styling
    html_code = """
    <style>
        .input-container {
            margin-bottom: 20px;
        }
        .button-container {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
        }
        .button:hover {
            background-color: #45a049;
        }
        .dropdown-container {
            margin-bottom: 20px;
        }
    </style>
    """

    # Display HTML code for styling
    st.markdown(html_code, unsafe_allow_html=True)

    # User input for channel ID
    channel_id = st.text_input("Enter YouTube Channel ID:", value="UC_x5XG1OV2P6uZZ5FSM9Ttw")

    # Dropdown menu for selecting an option
    option = st.selectbox("Select an option:", ("Option 1", "Option 2", "Option 3"))

    # Button 1 to process channel ID
    if st.button("Process Channel ID", key="process_button"):
        process_channel(channel_id)

    # Button 2 to perform an action based on the selected option
    if st.button("Perform Action", key="action_button"):
        perform_action(option)

def process_channel(channel_id):
    # Process channel ID logic here
    st.write(f"Processing channel ID: {channel_id}")

def perform_action(option):
    # Perform action based on selected option
    st.write(f"Performing action for: {option}")


if __name__ == "__main__":
    main()
