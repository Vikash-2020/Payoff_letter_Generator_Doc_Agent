functions_desc = [  
    {  
        "name": "perform_similarity_search",  
        "description": "Finds and extracts information from a document that best matches the transformed query using a similarity search algorithm.",  
        "parameters": {  
            "type": "object",  
            "properties": {  
                "transformed_query": {  
                    "type": "string",  
                    "description": "The refined query augmented with keywords and concepts from a predefined schema to improve the accuracy of the similarity search."  
                }  
            },  
            "required": ["transformed_query"]  
        },  
        "returns": {  
            "type": "string",  
            "description": "The extracted information from the document that corresponds to the transformed query. If no match is found, a response indicating no results will be returned."  
        }  
    },  
    {  
        "name": "update_response",  
        "description": "Appends extracted data to a local file named 'data.txt' to persistently store the results of the data extraction process.",  
        "parameters": {  
            "type": "object",  
            "properties": {  
                "extracted_data": {  
                    "type": "string",  
                    "description": "The information extracted from the similarity search (without conversational text) that needs to be recorded in the file. Ex: 'Sponsor Name: J.H. Whitney Capital Partners, LLC'"  
                }  
            },  
            "required": ["extracted_data"]  
        },  
        "returns": {  
            "type": "string",  
            "description": "A status message indicating the outcome of the file operation. Returns 'Success' if the data was appended without issues, or 'Failed' if an error occurred."  
        }  
    }  
]  


# functions =[  
#     {  
#         "name": "perform_similarity_search",  
#         "description": "Utilizes a similarity search algorithm to find and extract information from a Note Purchase and Guarantee Agreement document that best matches the transformed query. This function is essential for the Document Agent's capability to process and retrieve specific details from the document in response to user inquiries.",  
#         "parameters": {  
#             "type": "object",  
#             "properties": {  
#                 "transformed_query": {  
#                     "type": "string",  
#                     "description": "The refined query that has been augmented with pertinent keywords and concepts from the predefined schema, specifically tailored to enhance the accuracy of the similarity search within the document vector store."  
#                 }  
#             },  
#             "required": ["transformed_query"]  
#         },  
#         "returns": {  
#             "type": "string",  
#             "description": "The output is a string that encapsulates the information extracted from the document that most accurately corresponds to the transformed query. If no relevant match is found, the function will return a response indicating the lack of results."
#         }  
#     },
#     {  
#         "name": "update_response",  
#         "description": "Appends the extracted data to a local text file named 'data.txt', storing the results of the data extraction process. This function is used to persistently save the information that has been retrieved through the similarity search, ensuring that it can be accessed or referenced later.",  
#         "parameters": {  
#             "type": "object",  
#             "properties": {  
#                 "extracted_data": {  
#                     "type": "string",  
#                     "description": "The string containing the information that was extracted from the similarity search and needs to be recorded into the file."  
#                 }  
#             },  
#             "required": ["extracted_data"]  
#         },  
#         "returns": {  
#             "type": "string",  
#             "description": "A status message indicating the outcome of the file operation. Returns 'Success' if the data was appended to the file without any issues, or 'Failed' if an error occurred during the process."  
#         }  
#     }

# ]  