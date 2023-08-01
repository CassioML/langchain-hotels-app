# Hotels LLM Demo

## Setup

Create a `python3.8+` virtualenv and `pip install -r requirements.txt`.

Copy `.env.template` to `.env` and fill the values.

Launch the script to populate the reviews vector table:

```
python -m setup.2-populate-vector-table
```

### Prepare dataset

_Note: these steps are not necessary, their result is checked in the repo for you._

Firstly, you need a virtualenv with `requirements.txt` and `requirements-setup.txt`.

Download `Datafiniti_Hotel_Reviews_Jun19.csv` from [here](https://www.kaggle.com/datasets/datafiniti/hotel-reviews?select=Datafiniti_Hotel_Reviews_Jun19.csv) (unzip if necessary) and put it into `setup/original`.

To clean it:

```
python -m setup.0-clean-csv
```

To calculate embeddings (note: the script has options for incremental and forced recalculation):

```
python -m setup.1-augment-with-embeddings
```

This creates the json file with all embeddings ready to be written to DB (note:
the script admits limiting the number of rows to write with e.g. `-n 100`):

```
python -m setup.2-populate-vector-table
```

Note that this whole section has been run already (time- and token-consuming!),
the json is checked in, and the only necessary step is writing to DB.

### Populate hotel table

The non-embedded hotel data is stored in a separate table. To populate it:

``` 
python -m setup.3-populate-hotel-table.py
```

This script creates the table and loads the non-embedded data from the `hotel_reviews.csv` file into it.

## Running

### API

Launch the API with

```
uvicorn api:app
# (optionally add "--reload")
```

Once you see the `Uvicorn running on http://127.0.0.1:8000` message, try with:

```
curl -XPOST \
  localhost:8000/find_reviews \
  -d '{"review": "At times I actually feared for my life"}' \
  -H 'Content-Type: application/json' | jq

curl -XPOST \
  localhost:8000/summarize_reviews \
  -d '{"review": "I enjoyed a long walk to the city"}' \
  -H 'Content-Type: application/json' | jq

curl -XPOST \
  localhost:8000/find_hotels \
  -d '{"country": "US", "city": "Phoenix"}' \
  -H 'Content-Type: application/json' | jq
```

### Client

In another shell, go to the `client` directory and `npm install`, then
`npm start` and check you browser on `localhost:3000`.

## Experiment

### Notebooks

Additionally, `pip install jupyter==1.0.0`, then `jupyter notebook`.