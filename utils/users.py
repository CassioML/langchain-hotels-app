import json

from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

from utils.db import get_session, get_keyspace
from common_constants import USERS_TABLE_NAME

from utils.models import UserProfile
from utils.ai import get_llm

# TODO: prepare statements and cache them


def read_user_preferences(user_id):
    session = get_session()
    keyspace = get_keyspace()

    user_row = session.execute(
        f"SELECT base_preferences, additional_preferences FROM {keyspace}.{USERS_TABLE_NAME} WHERE id=%s",
        (user_id,),
    ).one()
    if user_row:
        # TODO return instance of UserProfile class instead of the two separate fields
        # return json.loads(user_row.base_preferences), user_row.additional_preferences
        return UserProfile(
            base_preferences=json.loads(user_row.base_preferences),
            additional_preferences=user_row.additional_preferences,
        )
    else:
        return {}


def write_user_profile(user_id, base_preferences, additional_preferences):
    session = get_session()
    keyspace = get_keyspace()

    session.execute(
        f"INSERT INTO {keyspace}.{USERS_TABLE_NAME} (id, base_preferences, additional_preferences) VALUES (%s, %s, %s);",
        (user_id, json.dumps(base_preferences), additional_preferences),
    )


def update_user_desc(user_id, base_preferences, additional_preferences):
    import time

    print("Updating automated travel preferences for user ", user_id)
    # time.sleep(2)  # instead of an LLM or something
    # fake_desc = ", ".join(
    #     "%s=%s" % (k.upper(), "yes" if v else "no") for k, v in base_preferences.items()
    # )

    summarizing_llm = get_llm()

    base_profile = ", ".join(
        "%s=%s" % (k.upper(), "yes" if v else "no") for k, v in base_preferences.items()
    )
    full_profile = ", ".join([base_profile, additional_preferences])

    prompt_template = """
    Summarize the following user's travel profile. This summary will be user to search for hotels that this user 
    may like.
    
    Keep it concise and clear. Use two or three short sentences and a neutral tone. Write in first person. 
    Only use the information provided in the user's travel profile.
    
    Only use the example summaries to understand the style of the summary. Do not use the information in the example 
    summaries when summarizing the current user's travel profile. 
    
    EXAMPLE SUMMARY: I travel with my family and enjoy going to zoos and adventure parks. I am interested in 
    family-friendly hotels with cots.
    
    EXAMPLE SUMMARY: I am a business traveller who values convenient business facilities and close proximity to 
    transportation and sightseeing options. I am not interested in family activities, theme parks or 
    kid-friendly amenities.
    
    USER'S TRAVEL PROFILE:
    {travel_profile}
    
    CONCISE SUMMARY:
    """

    query_prompt_template = PromptTemplate.from_template(prompt_template)
    populated_prompt = query_prompt_template.format(travel_profile=full_profile)
    print("Travel profile summary prompt:\n", populated_prompt)
    # TODO temporary just for testing
    travel_profile_summary = full_profile
    chain = load_summarize_chain(llm=summarizing_llm, chain_type="stuff")
    docs = [Document(page_content=populated_prompt)]
    travel_profile_summary = chain.run(docs)

    print("Travel profile summary:\n", travel_profile_summary)

    # write:
    session = get_session()
    keyspace = get_keyspace()

    session.execute(
        f"INSERT INTO {keyspace}.{USERS_TABLE_NAME} (id, travel_profile_summary) VALUES (%s, %s);",
        (user_id, travel_profile_summary),
    )
