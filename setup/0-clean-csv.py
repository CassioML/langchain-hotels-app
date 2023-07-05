import pandas as pd
import hashlib

if __name__ == '__main__':

    raw_csv = pd.read_csv('setup/original/Datafiniti_Hotel_Reviews_Jun19.csv')
    chosen_columns = pd.DataFrame(raw_csv, columns=['id','reviews.date', 'city', 'country', 'name', 'reviews.rating', 'reviews.text', 'reviews.title', 'reviews.username'])

    rename_map = {
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

    def hotel_id(row):
        desc = '/'.join([row['hotel_name'], row['hotel_city'], row['hotel_country']])
        return hashlib.md5(desc.encode()).hexdigest()[:8]

    DISCARDABLE_ENDING = '... More'
    def clean_review_text(row):
        text = row['text']
        if text[-len(DISCARDABLE_ENDING):] == DISCARDABLE_ENDING:
            return text[:-len(DISCARDABLE_ENDING)]
        else:
            return text


    renamed_csv['hotel_id'] = renamed_csv.apply(hotel_id, axis=1)
    renamed_csv['text'] = renamed_csv.apply(clean_review_text, axis=1)

    file_name = 'setup/hotel_reviews.csv'
    renamed_csv.to_csv(file_name)

    print(f'Saved to {file_name}')
