from langchain import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from utils.ai import get_llm


# TODO should this function go in the ai module?
def summarize_review_list(reviews: list[str], trip_preferences: str) -> str:
    summarizing_llm = get_llm()

    concatenated_reviews = "\n".join(review for review in reviews)
    # print(concatenated_reviews)

    prompt_template = """ You are an assistant helping travelers choose hotels.
    Write a two-paragraph summary of the following reviews, for someone whose travel preferences are {prefs}:
    {hotel_reviews}

    CONCISE SUMMARY: """

    query_prompt_template = PromptTemplate.from_template(prompt_template)
    populated_prompt = query_prompt_template.format(prefs=trip_preferences, hotel_reviews=concatenated_reviews)
    print(populated_prompt)

    chain = load_summarize_chain(llm=summarizing_llm, chain_type="stuff")
    docs = [Document(page_content=populated_prompt)]
    return chain.run(docs)

