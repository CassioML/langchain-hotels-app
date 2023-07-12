# Hotels LLM Demo

## Setup

Create a `python3.8+` virtualenv and `pip install -r requirements.txt`.

Copy `.env.template` to `.env` and fill the values.

### Prepare dataset

Preliminarly, you need a virtualenv with `requirements.txt` and `requirements-setup.txt`.

Download `Datafiniti_Hotel_Reviews_Jun19.csv` from [here](https://www.kaggle.com/datasets/datafiniti/hotel-reviews?select=Datafiniti_Hotel_Reviews_Jun19.csv) (unzip if necessary) and put it into `setup/original`.

To clean it:

```
python -m setup.0-clean-csv
```

To calculate embeddings (note: the script has options for incremental and force recalculation):

```
python -m setup.1-augment-with-embeddings
```

## Running

`uvicorn api:app`

`curl ...`

## Experiment

### Notebooks

Additionally, `pip install jupyter==1.0.0`, then `jupyter notebook`.