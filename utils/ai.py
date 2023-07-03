import os
from dotenv import find_dotenv, load_dotenv

import langchain
from langchain.llms import OpenAI
from langchain.cache import CassandraCache

dotenv_file = find_dotenv('.env')
load_dotenv(dotenv_file)

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

llm = OpenAI(openai_api_key=OPENAI_API_KEY)


def enable_llm_cache(session, keyspace):
    langchain.llm_cache = CassandraCache(
        session=session,
        keyspace=keyspace,    
    )


def capitalize(s):
    return s.upper()


def get_answer(question):
    return llm(question).strip()


if __name__ == '__main__':
    cap = 'Capitalize me'
    print(capitalize(cap))
