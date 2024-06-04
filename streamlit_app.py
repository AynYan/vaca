import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

def generate_baby_names(gender: str,nationality:str) -> list[str]:
    """
    Generate a list of 5 baby names

    Parameters:
    age (str): age of person
    nationailty (str) : nationailty of person

    Returns:
    list: list of peoples' names
    """

    prompt_template_name = PromptTemplate(
        input_variables=['gender', 'nationality'],
        template="""I want to find a name for a {nationality} {age} person. 
                    Suggest top 3 popular names for the baby.
                    Return it as a comma separated list """
                )

    name_chain = LLMChain(llm=llm,
                          prompt=prompt_template_name,
                          output_key='people_names')

    chain = SequentialChain(
        chains=[name_chain],
        input_variables=['age', 'nationality'],
        output_variables=['people_names']
    )

    response = chain({'age': age,
                      'nationality': nationality})
    return response


# main code
st.title('AYn Name Generator')

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

# DO NOT CHANEGE ABOVE ----


# ask user for what they want
age = st.selectbox("Choose an age group",
                             ("0-12","13-21","22-44","45-65","66-89","90-110"))
nationality = st.selectbox("Choose the nationality", 
                                  ("American", "Asian","European","African","South American"))

# get the answer from LLM
if age and nationality:
    response = generate_people_names(age, nationality)
    people_names = response['people_names'].strip().split(",")
    st.write("** Top 3 Baby Names **")

    for name in people_names:
        st.write("--", name)
