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
    output = chain.run(docs)
    ##print(f"Summary: {output}")
    return output


# review_list = [
#   """Great place for business meetings: I came for a seminar which ran from Monday to Wednesday and also stayed a few
#   extra nights to relax.The rooms and amenities were top notch. Staff was friendly and accommodating.
#   I used the fitness center most mornings and had no trouble despite it being quite small. Unfortunately I had no time
#   to use the spa so I cannot comment on that. I'm short, I would definitely stay here again.""",
#   """Trade show visit: Simple but clean and all amenities necessary for a business stay. Good breakfast for this price
#   range. Staff always cleans tables as guests leave and helpful cheerful front desk staff. Traveled with some foreign
#   guests and they made them very comfortable as well.""",
#   """Business Conference: Check in was quick, which is always a plus. The room I stayed in was clean and well appointed
#   with a radical view of the city. Where they truly shined was the breakout sessions they put together during my
#   conference. The food for said breakouts was tasty as well as thoughtfully and artistically displayed.
#   One breakout had all food floating, on mini boats, around a moat the had made in the common area."""
# ]
#
# preferences = "business traveler"
#
# summarize_review_list(review_list, preferences)
