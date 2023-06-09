from dotenv import load_dotenv
import streamlit as st

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

def main():
    load_dotenv()
    # print(os.getenv('OPENAI_API_KEY'))
    st.set_page_config(page_title="Ask Your PDF")
    st.header("Ask for your PDF")

    # Uplaod a file
    pdf_user = st.file_uploader("Upload Your PDF :", type="pdf")

    # Extract the text
    if pdf_user is not None:
        pdf_reader = PdfReader(pdf_user)
        extracted_data = ""
        for page in pdf_reader.pages:
            extracted_data += page.extract_text()
        
        # split into chunks
        extracted_text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len
        )

        data_chunks = extracted_text_splitter.split_text(extracted_data)

        # Create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(data_chunks, embeddings)

        # Show user input
        input_que = st.text_input("Ask Your Question about your PDF: ")
        if input_que:
            sementic_search = knowledge_base.similarity_search(input_que)
            chain = load_qa_chain(OpenAI(), chain_type="stuff")
            response = chain.run(input_documents=sementic_search, question=input_que)         

if __name__ == '__main__':
    main()