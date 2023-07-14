import uuid
import pandas as pd
from setup_constants import HOTEL_REVIEW_FILE_NAME

if __name__ == '__main__':

    raw_csv = pd.read_csv('setup/original/Datafiniti_Hotel_Reviews_Jun19.csv')
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

    DISCARDABLE_ENDING = '... More'
    def clean_review_text(row):
        text = row['text']
        if text[-len(DISCARDABLE_ENDING):] == DISCARDABLE_ENDING:
            return text[:-len(DISCARDABLE_ENDING)]
        else:
            return text

    def review_id(row):
        return uuid.uuid4().hex

    renamed_csv['id'] = renamed_csv.apply(review_id, axis=1)
    renamed_csv['text'] = renamed_csv.apply(clean_review_text, axis=1)

    file_name = HOTEL_REVIEW_FILE_NAME
    renamed_csv.to_csv(file_name)

    print(f'Saved to {file_name}')
