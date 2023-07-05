# Internal draft notes

## Input data preparation

Third and largest data set from [here](https://www.kaggle.com/datasets/datafiniti/hotel-reviews?select=Datafiniti_Hotel_Reviews_Jun19.csv)

Two-stage data import:

1. csv to some filtered cleaned format
2. augmented with embedding, ready to import into Astra

### How-to

Use `requirements-setup.txt` in addition to the app-only requirements.

download the file, make the csv into the cleaned one
(discard useless columns, our column names, hotel_id)

Get OpenAI embeddings for the title+text of each review (a pre-made task,
but easy to reproduce also partially for learning).

