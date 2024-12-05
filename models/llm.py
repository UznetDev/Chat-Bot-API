import os
import uuid
import json
import replicate
from data.config import VECTOR_STORAGE_DIR, METADATA_FILE
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from openai import OpenAI
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from data.config import REPLICATE_API_TOKEN





class LLM:
    class Config:
        protected_namespaces = ()
    def __init__(self):
        os.makedirs(VECTOR_STORAGE_DIR, exist_ok=True)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        self.load_metadata()

    def load_metadata(self):
        """Dokumentlar metadata faylini yuklash"""
        if os.path.exists(METADATA_FILE):
            with open(METADATA_FILE, 'r') as f:
                self.documents_metadata = json.load(f)
        else:
            self.documents_metadata = {}

    def save_metadata(self):
        """Dokumentlar metadata faylini saqlash"""
        with open(METADATA_FILE, 'w') as f:
            json.dump(self.documents_metadata, f, indent=4)

    def add_document(self, pdf_path: str, api_key: str, document_name: str = None):
        if not document_name:
            document_name = os.path.basename(pdf_path)
        doc_id = str(uuid.uuid4())
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        persist_directory = os.path.join(VECTOR_STORAGE_DIR, doc_id)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small", 
                                           api_key=api_key)
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory=persist_directory
        )
        self.documents_metadata[doc_id] = {
            "name": document_name,
            "path": pdf_path,
            "vectors_path": persist_directory
        }
        self.save_metadata()

        print(f"Dokument muvaffaqiyatli qo'shildi: {document_name}")
        return doc_id

    def list_documents(self) -> List[Dict]:
        return list(self.documents_metadata.values())

    def get_document_retriever(self, doc_id: str, api_key: str):
        if doc_id not in self.documents_metadata:
            raise ValueError(f"Dokument ID {doc_id} topilmadi")

        persist_directory = self.documents_metadata[doc_id]['vectors_path']
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small", 
                                           api_key=api_key)
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )

        return vectorstore.as_retriever(search_kwargs={"k": 3})

    def query_document(self, doc_id: str, query: str, api_key: str, system: str):

        retriever = self.get_document_retriever(doc_id, api_key=api_key)
        

        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=api_key,
            temperature=0.3
        )

        system_prompt = (
            f"{system}\n"
            "Context: {context}")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        
        chain = create_retrieval_chain(retriever, question_answer_chain)
        print(prompt)


        res = chain.invoke({"input": query})
        return res['answer']

        # return qa_chain.run(query)
    
    def open_ai_chat(self,model: str, prompt: str, api_key: int):
        try:
            self.client = OpenAI(api_key=api_key)
            response = self.client.chat.completions.create(
                model=model,
                messages=prompt
            )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            return f"Error: {str(e)}"
        
    def get_answer(self, prompt, api_key: str, model_data: dict, query: str):
        print(prompt)
        try:
            if model_data['type'] == 'chat':
                return self.open_ai_chat(model_data['name'], prompt, api_key)
            elif model_data['type'] == 'rag_model':
                res = self.query_document(doc_id=model_data['doc_id'], query=query, api_key=api_key, system=model_data['system'])
                return res
            elif model_data['type'] == 'llama':
                res = self.generate_llama2_response(query, prompt)
                return res
            else:
                return "Invalid model type"
        except Exception as err:
            print(err)
            return str(err)

    def create_promts(self, promt: str, prompt_history):

        try:
            promts = []
            for i in prompt_history:
                p = {"role": i["role"], "content": i["content"]}
                promts.append(p)
            promts.append({"role": "user", "content": promt})
            return promts
        except Exception as e:
            print(e)
            return f"Error: {str(e)}"
        except Exception as e:
            print(e)
            return f"Error: {str(e)}"
        

    def generate_llama2_response(self, prompt_input, chat_history: list):
        string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
        print(string_dialogue)
        replicate.Client(api_token="r8_C4BxWGLYucjJSmwBkVVpwePhiTq2tkl03gUaF")
        for dict_message in chat_history:
            if dict_message["role"] == "user":
                string_dialogue += "User: " + dict_message["content"] + "\n\n"
            else:
                string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
        
        output = replicate.run('a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea', 
                            input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                    "temperature":0.5, "top_p":0.5, "max_length":200, "repetition_penalty":1})
        full_response = ''
        for item in output:
            full_response += item
        print(full_response)
        return full_response