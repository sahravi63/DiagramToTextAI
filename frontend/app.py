import streamlit as st
import requests

st.title("DiagramToTextAI")

uploaded_file = st.file_uploader("Upload Flowchart / PDF", type=["png", "jpg", "pdf"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    
    try:
        response = requests.post("http://127.0.0.1:8000/process/", files=files)
        response.raise_for_status()  # Raises HTTP error if status code is 4xx/5xx
        
        data = response.json()  # Ensure response is JSON
        
        if "summary" in data:
            st.write("### Summary:")
            st.write(data["summary"])
            
            # Handle file downloads
            for file_type in ["pdf", "docx", "ppt"]:
                if file_type in data:
                    file_url = f"http://127.0.0.1:8000/download/{data[file_type]}"
                    file_response = requests.get(file_url)

                    if file_response.status_code == 200:
                        st.download_button(
                            f"Download {file_type.upper()}",
                            data=file_response.content,
                            file_name=f"summary.{file_type}"
                        )
                    else:
                        st.error(f"Failed to download {file_type.upper()} file.")
        else:
            st.error("No summary generated. Please check the backend.")

    except requests.exceptions.ConnectionError:
        st.error("Error: Unable to connect to the backend. Is FastAPI running?")
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.JSONDecodeError:
        st.error("Error: Received invalid response from the server.")
        st.write(response.text)  # Debugging: Show raw response
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
