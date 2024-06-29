import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

def generate_the_vaca_vaca(q1: str,q2:str, q3: str,q4:str, q5: str,q6:str,q7:str) -> list[str]:
    """
    Generate a list of 3 recommendations for a trip

    Parameters:
    q1 (str): q1
    q2 (str) : q2
    q3 (str): q3
    q4 (str) : q4
    q5 (str): q5
    q6 (str) : q6
    q7 (str): q7


    Returns:
    list: list of books to read
    """

    prompt_template_name = PromptTemplate(
        input_variables=['q2', 'q1','q3','q4','q5','q6','q7'],
        template="""= I would like to go on vacation. 
        Use these 7 questions and answers to determine 3 places for me to travel to(I live in USA). 
        Write a list of activities that we can do at each of these spots using these questions and answers
        Also write a brief paragraph summarizing the places.
        
        What kind of climate do you prefer for your vacation?: {}
        Are you looking for a beach destination, a city with a warm climate, or a mix of both?: {}
        Do you prefer a vacation spot that is more relaxed and laid-back or one that offers a lot of activities and entertainment?:{}
        Are you interested in exploring cultural and historical sites during your vacation?:{}
        Do you prefer traveling within your own country or are you open to international destinations?:{}
        Do you have a preference for a certain type of accommodation, such as a resort, hotel, vacation rental, or something else?: {}
        Are you interested in a particular region of the USA, such as the East Coast, West Coast, South, or somewhere else?: {}
                     """.format(q1,q2,q3,q4,q5,q6,q7)
                )

    name_chain = LLMChain(llm=llm,
                          prompt=prompt_template_name,
                          output_key='the_vaca_vaca')

    chain = SequentialChain(
        chains=[name_chain],
        input_variables=['q1', 'q2','q3','q4','q5','q6','q7'],
        output_variables=['the_vaca_vaca']
    )

    response = chain({'q1': q1,
                      'q2': q2,
                      'q3': q3,
                      'q4': q4,
                      'q5': q5,
                      'q6': q6,
                      'q7': q7})
    return response


# main code
st.title('Ayn Vacation Recommendation Center')

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
q1 = st.text_input("What kind of climate do you prefer for your vacation?: ")
q2 = st.text_input("Are you looking for a beach destination, a city with a warm climate, or a mix of both?: ")
q3 = st.text_input(" Do you prefer a vacation spot that is more relaxed and laid-back or one that offers a lot of activities and entertainment?: ")
q4 = st.text_input("Are you interested in exploring cultural and historical sites during your vacation?: ")
q5 = st.text_input("Do you prefer traveling within your own country or are you open to international destinations?: ")
q6 = st.selectbox("Do you have a preference for a certain type of accommodation, such as a resort, hotel, vacation rental, or something else?: ",["yes","no"])
q7 = st.text_input("Are you interested in a particular region of the USA, such as the East Coast, West Coast, South, or somewhere else?: ")

#get the answer from LLM
if q2 and q1 and q3 and q4 and q5 and q6 and q7:
    response = generate_the_vaca_vaca(q1, q2,q3,q4,q5,q6,q7)
    the_vaca_vaca = response['the_vaca_vaca']
    st.write("** Top 3 Place to Visit **")
    st.write(the_vaca_vaca)
