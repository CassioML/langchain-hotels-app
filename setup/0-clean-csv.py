import uuid
import pandas as pd
from setup.setup_constants import HOTEL_REVIEW_FILE_NAME, RAW_REVIEW_SOURCE_FILE_NAME

# Script that cleans up the raw CSV data and stores it in a new CSV:
#  - Picks only the columns of interest.
#  - Cleans up trailing truncation marker from truncated reviews.
#  - Assigns a synthetic, unique review_id because the original dataset does not contain one.
#
# The resulting CSV file will be used as the review data in subsequent setup steps.

if __name__ == '__main__':

    raw_csv = pd.read_csv(RAW_REVIEW_SOURCE_FILE_NAME)
    chosen_columns = pd.DataFrame(raw_csv, columns=['id','reviews.date', 'city', 'country', 'name', 'reviews.rating', 'reviews.text', 'reviews.title', 'reviews.username'])

    rename_map = {
        'id': 'hotel_id',
        'reviews.date': 'date',
        'city': 'hotel_city',
        'country': 'hotel_country',
        'name': 'hotel_name',
        'reviews.rating': 'rating',
        'reviews.text': 'text',
        'reviews.title': 'title',
        'reviews.username': 'username',
    }
    renamed_csv = chosen_columns.rename(columns=rename_map)

    DISCARDABLE_ENDING_WITH_SPACE = '... More'
    DISCARDABLE_ENDING_WITHOUT_SPACE = '...More'

    def clean_review_text(row):
        text0 = row['text']
        #
        if text0.find(DISCARDABLE_ENDING_WITH_SPACE) > -1:
            text1 = text0[:text0.find(DISCARDABLE_ENDING_WITH_SPACE)]
        else:
            text1 = text0
        #
        if text1.find(DISCARDABLE_ENDING_WITHOUT_SPACE) > -1:
            text2 = text1[:text1.find(DISCARDABLE_ENDING_WITHOUT_SPACE)]
        else:
            text2 = text1
        #
        return text2

    def review_id(row):
        return uuid.uuid4().hex

    renamed_csv['id'] = renamed_csv.apply(review_id, axis=1)
    renamed_csv['text'] = renamed_csv.apply(clean_review_text, axis=1)

    file_name = HOTEL_REVIEW_FILE_NAME
    renamed_csv.to_csv(file_name)

    print(f'Saved to {file_name}')
