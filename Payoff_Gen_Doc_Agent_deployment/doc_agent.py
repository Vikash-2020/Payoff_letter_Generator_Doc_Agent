# Importing Dependencies
from openai import AzureOpenAI
from prompts import doc_agent_system_prompt
from app_secrets import gpt_4t_azure_endpoint, gpt_4t_azure_api_key, gpt_4t_model, gpt_4t_azure_api_version
from info_retriever import extract_detail
from tools_description import functions_desc

# Setting up AzureOpenAI Environment
client = AzureOpenAI(
    api_version= gpt_4t_azure_api_version,
    api_key=gpt_4t_azure_api_key,
    base_url= gpt_4t_azure_endpoint
)



def perform_similarity_search(transformed_query: str) -> str:
    response = extract_detail(query=transformed_query)

    return response



def update_response(extracted_data):  
    try:  
        # Open the text file in append mode or create it if it doesn't exist  
        with open('extracted_data.txt', 'a') as file:  
            # Write the extracted_data to the file followed by a newline character  
            file.write(extracted_data + '\n')  
        # If everything went well, return "Success"  
        return "Success"  
    except Exception as e:  
        # If an error occurred during the file operation, return "Failed"  
        print(f"An error occurred: {e}")  
        return "Failed"  



# Defining the tools or functions

functions = functions_desc

# get completions

def get_completion(messages=None, func=None, function_call="auto",
                   temperature=0, max_tokens=1000, top_p=1, frequency_penalty=0,
                   presence_penalty=0, stop=None):
    # Set default values if parameters are not provided
    messages = messages or []
    functions = func or []
    
    # Make API call with provided parameters
    response = client.chat.completions.create(
        messages= messages,
        model=gpt_4t_model,
        functions=func,
        function_call=function_call,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop
    )
    print(response.choices[0].message.content)
    return response.choices[0].message


def get_answer(chat_history,search_query):
    message  = chat_history.copy()
    message.append({"role": "user", "content": f"Details extraction query:\n{search_query}"})
    # print(message)
    print("Generating First Response")
    # think = st.empty()
    response = get_completion(messages= message, func= functions)
    # print(response)

    while True:
        print("In Iteration...")
        if response.function_call:

            response.content = "null"
            message.append(response)
            function_name = response.function_call.name
            
            if function_name == "perform_similarity_search":
                print("Searching Vector Store")

                function_response =  perform_similarity_search(response.function_call.arguments)

                # print(type(function_response))
                # print(function_response)

                print(f"{response.function_call.arguments}")

                message.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_response,
                    }
                )
                # print(message)

                print("generating response after function call")
                response = get_completion(messages= message, func= functions)
                # print(response)
                continue

            elif function_name == "update_response":
                print("Updating Response Dict")
                # print(function_response)


                function_response =  update_response(response.function_call.arguments)

                return "Success"
        else:
            message.append({"role": "user", "content": "Please call function to extract and response_update."})
            response = get_completion(messages= message, func= functions)





def get_extracted_data(file_path = 'extracted_data.txt'):
    
    # Initialize a variable to store the text  
    file_text = ''  
    
    # Open the text file and read its contents  
    try:  
        # with open(file_path, 'r', encoding='utf-8') as file:  
        with open(file_path, 'r') as file:  
            file_text = file.read()
        return file_text  
    except FileNotFoundError:  
        print(f"The file at {file_path} was not found.")  
    except Exception as e:  
        print(f"An error occurred while reading the file: {e}")  



def execute_doc_agent(doc_schema):
    
    query_list = ["Extract Date of “Agreement”", "Extract name of (the “Initial Issuer”)", "Extract name of (the “Surviving Issuer”)", "Extract name of (the “Holdings”) entity", "[Sponsor Name]", "[The Sponsor address with the attention of person name] (From Notices section)", "[The Obligor address with the attention of person name] (From Notices section)", "Extract section number of Expenses; Indemnification; Limitation of Liability section?","Extract Governing Law section","Extract date of Maturity from Authorization of Notes section", "Extract date of Maturity", "Extract section number of Optional Prepayments section."]

    for query in query_list:
        extracted_details = get_extracted_data()

        chat_history = [{"role":"system","content": doc_agent_system_prompt},{"role": "user", "content": f"Additional Information for more context, use this to add relevant section or titles name to the query for better similarity search.\nThis is the Note Purchase and Guarantee Agreement Document Schema:\n----------\n{doc_schema}\n----------\nExtracted Details:\n----------\n{extracted_details}\n----------\n"},{"role": "assistant", "content": "Thank you for sharing the document schema and extracted data."}]

        status = get_answer(chat_history,query)
        print(status)




    # for key, value in details_dict.items(): 
    #     extracted_details = get_extracted_data()

    #     chat_history = [{"role":"system","content": doc_agent_system_prompt},{"role": "user", "content": f"Additional Information for more context, use this to add relevant section or titles name to the query for better similarity search.\nThis is the Note Purchase and Guarantee Agreement Document Schema:\n----------\n{doc_schema}\n----------\nExtracted Details:\n----------\n{extracted_details}\n----------\n"},{"role": "assistant", "content": "Thank you for sharing the document schema and extracted data."}]
     
    #     search_query = f"\nQ: {value}\n{key}"
    #     status = get_answer(chat_history,search_query)
    #     print(status)
    # print("extraction completed...")


def test_doc_agent(query):
    extracted_details = get_extracted_data()
    doc_schema = get_extracted_data("document_schema.txt")

    chat_history = [{"role":"system","content": doc_agent_system_prompt},{"role": "user", "content": f"Additional Information for more context, use this to add relevant section or titles name to the query for better similarity search.\nThis is the Note Purchase and Guarantee Agreement Document Schema:\n----------\n{doc_schema}\n----------\nExtracted Details:\n----------\n{extracted_details}\n----------\n"},{"role": "assistant", "content": "Thank you for sharing the document schema and extracted data."}]    

    status = get_answer(chat_history,query)
    print(status)



# doc_schema = get_extracted_data("document_schema.txt")

# execute_doc_agent(doc_schema)


# test_doc_agent("The Sponsor address with the attention of person name. (From Notices section)")
# test_doc_agent()

# test_doc_agent("Extract Date of “Agreement”")
# test_doc_agent("Extract name of (the “Initial Issuer”)")
# test_doc_agent("Extract name of (the “Surviving Issuer”)")
# test_doc_agent("[Sponsor Name]")
# test_doc_agent("[The Sponsor address with the attention of person name] (From 12.9 Notices section)")
# test_doc_agent("[The Obligor address with the attention of person name] (From 12.9 Notices section)")
# test_doc_agent("Extract section number of Expenses; Indemnification; Limitation of Liability section?")

# {"extracted_data":"Date of the Note Purchase and Guarantee Agreement: September 14, 2017"}
# {"extracted_data":"Initial Issuer: JHW ACP Acquisition, Inc."}
# {"extracted_data":"Surviving Issuer: Accupac, Inc."}
# {"extracted_data":"Sponsor Name: J.H. Whitney Capital Partners, LLC"}
# {"extracted_data":"Sponsor Address: 130 Main Street, New Canaan, CT 06840. Attention: Robert Williams, Ann Kim Chung, Bharath Ganesan."}
# {"extracted_data":"Obligor Address: 1501 Industrial Boulevard, P.O. Box 200, Mainland, PA 19451. Attention: Bruce Wright, Chief Financial Officer."}
# {"extracted_data":"Section number for Expenses; Indemnification; Limitation of Liability: 12.2"}












# test_doc_agent("Extract name of (the “Initial Issuer”) from SECTION 1. DEFINITIONS; INTERPRETATION")
# test_doc_agent("Extract name of (“Holdings”), from SECTION 1. DEFINITIONS; INTERPRETATION")
# test_doc_agent("Extract name of (the “Surviving Issuer”) from SECTION 1. DEFINITIONS; INTERPRETATION")
# test_doc_agent("Maturity date or Due date (from section 2.1 Authorization of Note)")


# test_doc_agent("Can you provide the names of the parties responsible for the execution and delivery of this Agreement, as mentioned in the statement where it's indicated that the parties' duly authorized officers have caused the Agreement to be executed and delivered on the date first set forth above? (From Signature Page to NPGA)")
# test_doc_agent("Search 'The parties hereto have caused this Agreement to be duly executed and delivered by their duly authorized officers as of the date first set forth above.' and then Extract [Signature Page to NPGA]")




# test_doc_agent("Find name of section where this is mentioned '2:00 p.m., prevailing New York, New York time'")
# test_doc_agent("Section 12: Payment obligations must be credited by [Time, location or timezone]")




