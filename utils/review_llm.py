from typing import List

from langchain import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from utils.ai import get_llm


# TODO should this function go in the ai module?
def summarize_review_list(reviews: List[str], trip_preferences: str) -> str:
    summarizing_llm = get_llm()

    concatenated_reviews = "\n".join(review for review in reviews)
    # print(concatenated_reviews)

    # THE FOLLOWING TO BE MOVED TO A 'prompts' MODULE

    # prompt_template = """ You are an assistant helping travelers choose hotels.
    # Write a very short summary of the following reviews, for someone whose travel preferences are {prefs}:
    # {hotel_reviews}

    # EXAMPLE SUMMARY: The hotel is good, cozy and well furnished, but is noisy and, sometimes, the waiters are impolite.

    # CONCISE SUMMARY: """

    prompt_template = """ You are an assistant helping travelers choose hotels.
    Write a bullet-point summary of the following "input reviews" for someone with the travel profile as given below.
    Do not exceed writing 7 concise bullet points.
    
    Absolutely do not use information other than given in the "input reviews" below.
    
    TRAVELER PROFILE: {prefs}.
    
    INPUT REVIEWS:
    {hotel_reviews}

    EXAMPLE SUMMARY:
        - Good hotel, cozy and well furnished.
        - Sometimes noisy at night.
        - Some of the staff are slightly rude.
        - Weak pressure in the showers and water not always very hot.
        - Kitchen is awesome.

    CONCISE SUMMARY: """

    query_prompt_template = PromptTemplate.from_template(prompt_template)
    populated_prompt = query_prompt_template.format(
        prefs=trip_preferences, hotel_reviews=concatenated_reviews
    )
    print(populated_prompt)

    chain = load_summarize_chain(llm=summarizing_llm, chain_type="stuff")
    docs = [Document(page_content=populated_prompt)]
    return chain.run(docs)
