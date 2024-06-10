import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

def generate_books_to_read(favorite_book: str,favorite_book_series:str) -> list[str]:
    """
    Generate a list of 5 baby names

    Parameters:
    favorite_book (str): favorite singular book
    favorite_book_series (str) : 1st favorite book series

    Returns:
    list: list of books to read
    """

    prompt_template_name = PromptTemplate(
        input_variables=['gender', 'favorite_book'],
        template="""= I like the book series {favorite_book_series} and the book called: {favorite_book}. 
        Suggest the top 5 books I should read based on my favorite books.
                     """
                )

    name_chain = LLMChain(llm=llm,
                          prompt=prompt_template_name,
                          output_key='books_to_read')

    chain = SequentialChain(
        chains=[name_chain],
        input_variables=['favorite_book_series', 'favorite_book'],
        output_variables=['books_to_read']
    )

    response = chain({'favorite_book_series': favorite_book_series,
                      'favorite_book': favorite_book})
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

# DO NOT CHANGE ABOVE ----


# ask user for what they want
favorite_book_series = st.text_input("Enter the name of your favorite book series: ")
favorite_book = st.text_input("Enter the name of your favorite book: ")

# get the answer from LLM
if favorite_book_series and favorite_book:
    response = generate_books_to_read(favorite_book_series, favorite_book)
    people_names = response['books_to_read'].strip().split(",")
    st.write("** Top 5 Books to Read **")

    for book in books_to_read:
        st.write("--", book)
