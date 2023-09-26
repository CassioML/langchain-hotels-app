# Hotels LLM Demo

## Setup

Create a `python3.8+` virtualenv and `pip install -r requirements.txt`.

Copy `.env.template` to `.env` and fill the values.

Launch the script to populate the reviews vector table:

```
python -m setup.2-populate-vector-table
```

### (optional) Prepare dataset

_Note: these steps are not necessary, their result is checked in the repo for you._

Firstly, you need a virtualenv with `requirements.txt` and `requirements-setup.txt`.

Download `Datafiniti_Hotel_Reviews_Jun19.csv` from [here](https://www.kaggle.com/datasets/datafiniti/hotel-reviews?select=Datafiniti_Hotel_Reviews_Jun19.csv) (unzip if necessary) and put it into `setup/original`.

To refine it into its "cleaned" version for later use:

```
python -m setup.0-clean-csv
```

To calculate embeddings (note: the script has options for incremental and forced recalculation):

```
python -m setup.1-augment-with-embeddings
```

This creates the json file with all embeddings ready to be written to DB.

Note that this whole section has been run already (time- and token-consuming!),
the json is checked in, and the only necessary step is writing to DB.

### Create/populate review vector table

Insertion of reviews in the review _vector_ table:

```
python -m setup.2-populate-review-vector-table
```

### Create/populate hotel and city tables

The non-embedded hotel data is stored in a separate table. To populate it:

``` 
python -m setup.3-populate-hotels-and-cities-table
```

This script creates the table and loads the non-embedded data from the `hotel_reviews.csv` file into it.

### Create/populate users table

```
python -m setup.4-create-users-table
```

### Create/populate review (non-vector) table

This table is used for other non-vector operations:

```
python -m setup.5-populate-reviews-table
```

## Running

### API

Launch the API with

```
uvicorn api:app
# (optionally add "--reload")
```

Once you see the `Uvicorn running on [address:port]` message, the API is up.

### Client

In another shell, go to the `client` directory and `npm install`, then
`npm start` and check you browser on `localhost:3000`.
