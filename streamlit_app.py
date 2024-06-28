import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

def generate_the_vaca_vaca(q1: str,q2:str) -> list[str]:
    """
    Generate a list of 5 baby names

    Parameters:
    q1 (str): q1
    q2 (str) : q2

    Returns:
    list: list of books to read
    """

    prompt_template_name = PromptTemplate(
        input_variables=['gender', 'q1'],
        template="""= I like the book series {q2} and the book called: {q1}. 
        Suggest the top 5 books I should read based on my q1s.
                     """
                )

    name_chain = LLMChain(llm=llm,
                          prompt=prompt_template_name,
                          output_key='the_vaca_vaca')

    chain = SequentialChain(
        chains=[name_chain],
        input_variables=['q2', 'q1'],
        output_variables=['the_vaca_vaca']
    )

    response = chain({'q2': q2,
                      'q1': q1})
    return response


# main code
st.title('Ayn Book Recommendation Center')

# DO NOT CHANGE BELOW ----
# get open AI key from user
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    
# initialize Open AI
import os
os.environ['OPENAI_API_KEY'] = openai_api_key
llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature = 0.6)

# DO NOT CHANGE ABOVE ----


# ask user for what they want
q2 = st.text_input("Enter the name of your q2: ")
q1 = st.text_input("Enter the name of your q1: ")

# get the answer from LLM
if q2 and q1:
    response = generate_the_vaca_vaca(q2, q1)
    the_vaca_vaca = response['the_vaca_vaca'].strip().split(",")
    st.write("** Top 5 Books to Read **")

    for book in the_vaca_vaca:
        st.write("--", book)
