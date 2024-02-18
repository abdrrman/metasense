from termcolor import colored
import os
import ast
from time import sleep
from tqdm import tqdm
import json

from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain_community.document_loaders import UnstructuredFileLoader, UnstructuredHTMLLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser


import prompts


class Chains:
    client = "Alogia"
    
    @classmethod
    def setLlm(
        cls,
        model="gpt-3.5-turbo-16k",
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        temperature=0.0,
        openai_api_base=None,
        has_gpt4=False,
        persistent_db_path="./chroma_db",
        service_documents_root = "/home/melih/Downloads/Alogia english/Alogia english/Alogia services",
        embedding_model_name = "all-MiniLM-L6-v2",
        services_json_path = "service2link.json",
    ):
        cls.openai_api_key=openai_api_key
        cls.temperature=temperature
        cls.openai_api_base=openai_api_base
        cls.has_gpt4=has_gpt4
        cls.llm = ChatOpenAI(
            model=model,
            openai_api_key=openai_api_key,
            temperature=temperature,
            openai_api_base=openai_api_base
        )
        cls.model = model
        cls.embedding_model = HuggingFaceEmbeddings(model_name = embedding_model_name)
        cls.persistent_db_path = persistent_db_path
        if os.path.exists(persistent_db_path):
            cls.db = Chroma(persist_directory = persistent_db_path, embedding_function=cls.embedding_model)
        else:
            cls.db = None
        cls.service_documents_root = service_documents_root
        cls.initializeRAGModel()
        cls.initServiceLinks(services_json_path)

    @classmethod
    def initServiceLinks(cls, services_json_path):
        with open(services_json_path, "r") as f:
            data = json.load(f)
            cls.services_json = "\n".join([service+":"+link for service,link in data.items()])
    @classmethod
    def initializeRAGModel(cls):
        prompt = ChatPromptTemplate.from_template(prompts.rag.template)
        if os.path.exists(cls.persistent_db_path):
            db = Chroma(persist_directory = cls.persistent_db_path, embedding_function=cls.embedding_model)
            retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})
            cls.rag_chain = (
                {"context": retriever,  "question": RunnablePassthrough()} 
                | prompt 
                | cls.llm
                | StrOutputParser() 
            )
            print("RAG Model automatically initialized.")
            return
        print("RAG Model is being initialized...")
        docs = []
        for filename in tqdm(os.listdir(cls.service_documents_root)):
            path = os.path.join(cls.service_documents_root, filename)
            loader = UnstructuredHTMLLoader(path)
            docs.extend(loader.load())
        db = Chroma.from_documents(docs, cls.embedding_model, persist_directory=cls.persistent_db_path)
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 6})
        cls.rag_chain = (
            {"context": retriever,  "question": RunnablePassthrough()} 
            | prompt 
            | cls.llm
            | StrOutputParser() 
        )
        print("RAG Model has been succesfully initialized.")
    
    @classmethod
    def getModel(cls, change=False, temperature=0, change_model="gpt-4-0613"):
        if change and cls.has_gpt4:
            return ChatOpenAI(
                model=change_model,
                openai_api_key=cls.openai_api_key,
                temperature=temperature,
                openai_api_base=cls.openai_api_base
        )
        
        if temperature > 0:
            return ChatOpenAI(
                model=cls.model,
                openai_api_key=cls.openai_api_key,
                temperature=temperature,
                openai_api_base=cls.openai_api_base
        )
        
        return cls.llm
        
    @classmethod
    def setModel(cls, model):
        cls.model = model

    @classmethod
    def getChain(cls, system_template="", human_template="", change=False, change_model="gpt-4-0613", temperature=0, **kwargs):
        prompts = []
        if system_template:
            prompts.append(SystemMessagePromptTemplate.from_template(system_template))
        if human_template:
            prompts.append(HumanMessagePromptTemplate.from_template(human_template))
        chat_prompt = ChatPromptTemplate.from_messages(prompts)
        return LLMChain(llm=cls.getModel(change=change, temperature=temperature, change_model=change_model), prompt=chat_prompt).run(**kwargs)
    
    @classmethod
    def rag(cls, question):
        print(colored("RAG is being invoked...","green"))
        return cls.rag_chain.invoke(question)
    
    @classmethod
    def intro(cls, doc_path):
        loader = UnstructuredFileLoader(doc_path)
        docs = loader.load()
        document = "\n".join([doc.page_content for doc in docs])
        return cls.getChain(
            system_template=prompts.intro.system_template,
            human_template=prompts.intro.human_template,
            document=document,
            client=cls.client
        )
        
    @classmethod
    def generateQuestion(cls, history=""):
        return cls.getChain(
            system_template=prompts.generate_question.system_template,
            human_template=prompts.generate_question.human_template,
            history=history
        )
    
    @classmethod
    def eliminateServices(cls, doc, question, response):
        res =  cls.getChain(
            system_template=prompts.eliminate_services.system_template,
            human_template=prompts.eliminate_services.human_template,
            doc=doc,
            question=question,
            response=response
        )
        return ast.literal_eval(res)  
    
    @classmethod
    def giveAdvice(cls, doc, history):
        print(colored("Advice is being invoked...","red"))
        return cls.getChain(
            system_template=prompts.give_advice.system_template,
            human_template=prompts.give_advice.human_template,
            doc=doc,
            history=history
        )
        
    @classmethod
    def useAdvice(cls, history, advice, temperature=0):
        res = cls.getChain(
            system_template=prompts.use_advice.system_template,
            human_template=prompts.use_advice.human_template,
            temperature=temperature,
            history=history,
            advice=advice
        )
        # find the last : and return the string after it
        last_colon_index = res.rfind(":")
        return res[last_colon_index + 1:].strip()
    
    @classmethod
    def shouldAsk(cls, history):
        return cls.getChain(
            system_template=prompts.decide.system_template,
            human_template=prompts.decide.human_template,
            history=history
        ) == "yes"
    
    @classmethod
    def link(cls, message):
        return cls.getChain(
            system_template=prompts.link.system_template,
            human_template=prompts.link.human_template,
            services_json=cls.services_json,
            message=message
        )
        
    @classmethod
    def googleTranslate(cls, text, lang="en"):
        detection = cls.translator.detect(text)
        original_lang = detection.lang
        if original_lang == lang:
            return text, original_lang

        # Translate to the language
        translation = cls.translator.translate(text, dest=lang)
        return translation.text, original_lang
    
    @classmethod
    def translate(cls, text, lang="english"):
        res = cls.getChain(
            system_template=prompts.translate.system_template,
            human_template=prompts.translate.human_template,
            text=text,
            lang=lang
        )
        print(res)
        res_json = ast.literal_eval(res)  
        return res_json["translation"], res_json["source_language"]
        
    @classmethod
    def reply(cls, doc, history, advice="", lang="en"):
        temperature = 0.2 if advice else 0
        should_ask = cls.shouldAsk(history)
        put_link = len(advice) == 0
        if not advice:
            if should_ask:
                question = cls.generateQuestion(history)
                print(colored(question,"green"))
                advice = cls.rag(question)
            else:
                advice = cls.giveAdvice(doc, history)
                
        print(colored(advice,"red"))
        print("temperature:", temperature)
        res = cls.useAdvice(history, advice, temperature)
        if put_link:
            res = cls.link(res)
        translated_res, _ = cls.translate(res, lang)
        return res, translated_res
        