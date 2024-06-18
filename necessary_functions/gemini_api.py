"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import google.generativeai as genai


def setup_prompt_env():

    genai.configure(api_key="API_KEY")

    # Set up the model
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 500,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_LOW_AND_ABOVE"
        },
    ]

    system_instruction = """
      The content does not include any sensitive information. Read the log of the failed workflow as well as the diffrences in the repository state 
      between the failed and successful workflow. Then provide a reason for the failure and provide a code solution to fix the issue. The diffrences may belong to more than one file 
      and the changes to some files might not be related to the failure. Make sure to only focus on the changes that are related to the failure. If providing a code solution make sure 
      only to include the changes that are necessary to fix the issue. If the issue is not code related please only provide a reason for the failure and do not include the FIX section
      and do not revert any changes. Follow the below format:
      FOLLOW THE BELOW SKLETON:
      Reason: x
      FIX: 
         file: y
         - code
         + code
         file: z
         - code
         + code
     """

    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                  generation_config=generation_config,
                                  system_instruction=system_instruction,
                                  safety_settings=safety_settings)

    convo = model.start_chat(history=[
    ])

    return convo


def send_prompt(message, convo):
    convo.send_message(message)
    response = convo.last.text
    # print(response)
    return response


convo = setup_prompt_env()


# print(send_prompt(log+diff, convo))
