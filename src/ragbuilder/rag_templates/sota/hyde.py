code="""from langchain_community.llms import Ollama
from langchain_community.document_loaders import *
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from operator import itemgetter
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain.retrievers import MergerRetriever
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain.chains import LLMChain, HypotheticalDocumentEmbedder

def rag_pipeline():
    try:
        def format_docs(docs):
            return "\\n".join(doc.page_content for doc in docs) 
        
        llm = Ollama(model='llama3.1:latest',base_url='BASE_URL')
        
        {loader_class}
        
        embedding = OllamaEmbeddings(model='mxbai-embed-large:latest',base_url='BASE_URL')

        hyde_embedding = HypotheticalDocumentEmbedder.from_llm(llm,
                                                   embedding,
                                                   prompt_key="web_search"
                                                   )
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=1600, chunk_overlap=200)
        splits=splitter.split_documents(docs)
        c=Chroma.from_documents(documents=splits, embedding=hyde_embedding, collection_name='testindex-ragbuilder',)
        retrievers=[]
        retriever=c.as_retriever(search_type='similarity', search_kwargs={'k': 5})
        retrievers.append(retriever)
        retriever=MergerRetriever(retrievers=retrievers)
        prompt = hub.pull("rlm/rag-prompt")
        rag_chain = (
            RunnableParallel(context=retriever, question=RunnablePassthrough())
                .assign(context=itemgetter("context") | RunnableLambda(format_docs))
                .assign(answer=prompt | llm | StrOutputParser())
                .pick(["answer", "context"]))
        return rag_chain
    except Exception as e:
        print(f"An error occurred: {e}")"""

# from langchain_community.llms import Ollama
# from langchain_community.document_loaders import *
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from operator import itemgetter
# from langchain import hub
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
# from langchain.retrievers import MergerRetriever
# from langchain.retrievers.document_compressors import DocumentCompressorPipeline
# from langchain.chains import LLMChain, HypotheticalDocumentEmbedder
# from langchain.text_splitter import MarkdownHeaderTextSplitter

# def rag_pipeline():
#     try:
#         def format_docs(docs):
#             return "\\n".join(doc.page_content for doc in docs) 
        
#         llm = Ollama(model='llama3.1:latest',base_url='http://localhost:11434')
#         loader = WebBaseLoader('https://en.wikipedia.org/wiki/Kerala?action=raw')
#         # loader = WebBaseLoader('https://ashwinaravind.github.io/')

#         documents = loader.load()
#         # splitter = RecursiveCharacterTextSplitter(chunk_size=1600, chunk_overlap=200)
#         # documents=splitter.split_documents(documents)
#         headers_to_split_on = [
#             ("#", "Header 1"),
#             ("##", "Header 2"),
#             ("###", "Header 3"),
#         ]
#         markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
#         splits=markdown_splitter.split_text(documents[0].page_content)
        
#         embedding = OllamaEmbeddings(model='mxbai-embed-large:latest',base_url='http://localhost:11434')

#         hyde_embedding = HypotheticalDocumentEmbedder.from_llm(llm,
#                                                    embedding,
#                                                    prompt_key="web_search"
#                                                    )
        
#         splitter = RecursiveCharacterTextSplitter(chunk_size=1600, chunk_overlap=200)
#         splits=splitter.split_documents(documents)
#         c=Chroma.from_documents(documents=splits, embedding=hyde_embedding, collection_name='testindex-ragbuilder',)
#         retrievers=[]
#         retriever=c.as_retriever(search_type='similarity', search_kwargs={'k': 5})
#         retrievers.append(retriever)
#         retriever=MergerRetriever(retrievers=retrievers)
#         prompt = hub.pull("rlm/rag-prompt")
#         rag_chain = (
#             RunnableParallel(context=retriever, question=RunnablePassthrough())
#                 .assign(context=itemgetter("context") | RunnableLambda(format_docs))
#                 .assign(answer=prompt | llm | StrOutputParser())
#                 .pick(["answer", "context"]))
#         print(rag_chain.invoke("Where is kerala?"))
#     except Exception as e:
#         print(f"An error occurred: {e}")

# print('hyde')
# rag_pipeline()