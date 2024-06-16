import os    
import streamlit as st
import time
from pathlib import Path
from SchemaExtractor.schema_extractor import extract_document_schema, extract_signature_page_data
from LDA_KOR_metadata_extraction.LDA_metadata_extract import process_documents

DOC_PATH = "./documents"
VECTOR_STORE_PATH = "./vector_store"

def save_uploaded_file(uploaded_file, target_dir):  
    """Save the uploaded file to the target directory."""  
    try:  
        # Create the target directory if it doesn't already exist  
        os.makedirs(target_dir, exist_ok=True)  
          
        # Construct the full path to save the file  
        file_path = os.path.join(target_dir, uploaded_file.name)  
          
        # Write the uploaded file to the file system  
        with open(file_path, "wb") as f:  
            f.write(uploaded_file.getbuffer())  
        return True  
    except Exception as e:  
        print(e)  
        return False  


# Streamlit UI layout       
st.title('Document Uploader')    
    
# Single file uploader that allows multiple files    
uploaded_files = st.file_uploader("Upload documents", accept_multiple_files=True, disabled=False)    
    
# Submit button for the form    
submit_button = st.button(label='Upload Documents', disabled=False)    
    
# If the user submits the form    
if submit_button and uploaded_files:    
    # Display a generating message  
    with st.spinner('Saving uploaded documents...'):  
        success = False  
        for uploaded_file in uploaded_files:  
            saved = save_uploaded_file(uploaded_file, "documents")
            success = success or saved  # If at least one file is saved successfully, success will be True  
          
        # If any document was saved successfully, show success message    
        if success:  
            st.success('Documents uploaded successfully!')

        else:  
            st.error('No documents to upload. Please upload at least one document.')

else:  
    if submit_button:  # If the button was clicked but no files were uploaded  
        st.error('No documents to upload. Please upload at least one document.')
        

if st.button(label="Generate"):
    st.write("Payoff Letter generation will take time please wait...")

    st.write("extracting document Schema...")

    start_time = time.time()
    doc_schema, toc_range = extract_document_schema(DOC_PATH)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"extract_document_schema executed in {execution_time:.4f} seconds.")
    st.write(f"extract_document_schema executed in {execution_time:.4f} seconds.")


    st.write("extracting Signature Page data...")

    start_time = time.time()
    spd , spd_range = extract_signature_page_data(DOC_PATH)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"extract_signature_page_data executed in {execution_time:.4f} seconds.")
    st.write(f"extract_signature_page_data executed in {execution_time:.4f} seconds.")

    # toc_range = [1,5]
    st.write("extracting metadata and creating vector index...")
    start_time = time.time()
    process_documents(doc_folder=DOC_PATH, storage_base_folder= VECTOR_STORE_PATH, toc_range= toc_range)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"process_documents executed in {execution_time:.4f} seconds.")
    st.write(f"process_documents executed in {execution_time:.4f} seconds.")
    
    # from doc_agent import execute_doc_agent, get_extracted_data


    # doc_schema = get_extracted_data("document_schema.txt")

    # execute_doc_agent(doc_schema)

    # exit()



    # # st.write("extraction and indexing completed...")
    # sections = []


    # for section, usage in get_section_generator():
    #     with open('generated_payoff_letter.txt', 'a') as file:  
    #         file.write(f"{section}\n\n")
    #     sections.append(section)
    #     st.write(section)
    #     st.sidebar.write(usage)
    
    # print("------------------------------")
    # print(f"Total Iterations: {ITERATION_COUNT}")
    # print(f"Total Prompt token: {PROMPT_TOKENS}")
    # print(f"Total Completion token: {COMPLETION_TOKENS}")
    # print(f"Total tokens used: {TOTAL_TOKENS}")
    # print(f"`get_section` func executed in {EXECUTION_TIME} seconds.")
    # print("------------------------------")
    # # st.write(status)

    # # Join the sections using "\n\n" and store into a variable  
    # full_text = "\n\n".join(sections)  
  
    # # Provide a button to download the content  
    # btn = st.download_button(  
    #     label="Download Letter",  
    #     data=full_text,  
    #     file_name="generated_payoff_letter.txt",  
    #     mime="text/plain"  
    # )  

  
# Run the app with `streamlit run your_script.py`
