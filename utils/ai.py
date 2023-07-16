import os
from dotenv import find_dotenv, load_dotenv

import langchain
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.cache import CassandraCache

LLM_PROVIDER = 'OpenAI'

dotenv_file = find_dotenv('.env')
load_dotenv(dotenv_file)

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

EMBEDDING_DIMENSION = 1536

llm = None
embeddings = None


def get_llm():
    global llm
    if llm is None:
        llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    #
    return llm


def get_embeddings():
    global embeddings
    if embeddings is None:
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    #
    return embeddings


def enable_llm_cache(session, keyspace):
    langchain.llm_cache = CassandraCache(
        session=session,
        keyspace=keyspace,    
    )


def capitalize(s):
    return s.upper()


def get_answer(question):
    answering_llm = get_llm()
    return answering_llm(question).strip()


if __name__ == '__main__':
    cap = 'Capitalize me'
    print(capitalize(cap))
