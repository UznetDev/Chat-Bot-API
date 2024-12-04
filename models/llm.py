import os
import uuid
import json
from data.config import VECTOR_STORAGE_DIR, METADATA_FILE
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from openai import OpenAI



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
        """
        PDF faylni vektorga aylantirish va saqlash

        :param pdf_path: PDF faylning to'liq yo'li
        :param document_name: Dokumentning nomi (ixtiyoriy)
        :return: Yaratilgan vektorstore uchun unikal identifikator
        """
        # Agar document_name ko'rsatilmagan bo'lsa, faylning nomini olish
        if not document_name:
            document_name = os.path.basename(pdf_path)

        # Unikal identifikator yaratish
        doc_id = str(uuid.uuid4())

        # PDF faylni yuklab olish
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        # Matnga bo'lish
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)

        # Vektorlarni Chroma vectorstore ga saqlash
        persist_directory = os.path.join(VECTOR_STORAGE_DIR, doc_id)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small", 
                                           api_key=api_key)
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory=persist_directory
        )

        # Metadata saqlash
        self.documents_metadata[doc_id] = {
            "name": document_name,
            "path": pdf_path,
            "vectors_path": persist_directory
        }
        self.save_metadata()

        print(f"Dokument muvaffaqiyatli qo'shildi: {document_name}")
        return doc_id

    def list_documents(self) -> List[Dict]:
        """Barcha saqlangan dokumentlarni ro'yxatini olish"""
        return list(self.documents_metadata.values())

    def get_document_retriever(self, doc_id: str, api_key: str):
        """
        Belgilangan dokumentning retrieverini olish

        :param doc_id: Dokumentning unikal identifikatiri
        :return: Chroma vectorstore retriever
        """
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

    def query_document(self, doc_id: str, query: str, api_key: str):
        """
        Belgilangan dokumentga savol berish

        :param doc_id: Dokumentning unikal identifikatiri
        :param query: Savol matni
        :return: Javob matni
        """
        # Retriever olish
        retriever = self.get_document_retriever(doc_id, api_key=api_key)

        # LLM modelini sozlash
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=api_key,
            temperature=0.3
        )

        # Retrieval QA zanjirini yaratish
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever
        )

        # Savolga javob olish
        return qa_chain.run(query)
    
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
        
    def get_answer(self, prompt, api_key: str, model_data: dict):
        print(prompt)
        try:
            if model_data['type'] == 'chat':
                return self.open_ai_chat(model_data['name'], prompt, api_key)
            elif model_data['type'] == 'rag_model':
                res = self.query_document(doc_id=model_data['doc_id'], query="hi", api_key=api_key)
                print(res)
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