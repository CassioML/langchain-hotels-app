#!/bin/bash

REPO_HOME="/workspace/langchain-hotels-app"

# source /home/gitpod/.astra/cli/astra-init.sh
clear
echo    "=========================="

ASTRA_TOKEN="$(${REPO_HOME}/scripts/read_and_output_nonempty_secret.sh "Enter your Astra 'DB Admin' Token")";
echo -e "\nOK"
echo -e "ASTRA_DB_APPLICATION_TOKEN=\"${ASTRA_TOKEN}\"\n" > .env

DATABASE_ID=""
while [ -z "${DATABASE_ID}" ]; do
  echo -n "Enter your Database ID: "
  read DATABASE_ID
done
echo -e "\nOK"
echo -e "ASTRA_DB_ID=\"${DATABASE_ID}\"\n" >> .env

echo -n "(Optional) Enter your Keyspace: "
read KEYSPACE
echo -e "\nOK"
if [ ! -z "${KEYSPACE}" ]; then
  echo -e "ASTRA_DB_KEYSPACE=\"${KEYSPACE}\"\n" >> .env
fi

${REPO_HOME}/scripts/ingest_openai_key.sh ${REPO_HOME}/.env

cd ${REPO_HOME}
pip install -r requirements.txt

# provision DB (i.e. all necessary steps in sequence)
python -m setup.2-populate-review-vector-table
python -m setup.3-populate-hotels-and-cities-table
python -m setup.4-create-users-table
python -m setup.5-populate-reviews-table

# friendly message to user
CLIENT_URL=$(gp url 3000)
echo -e "\n\n** AFTER THE API IS UP YOU CAN OPEN THE CLIENT IN A NEW TAB:\n    ${CLIENT_URL}\n\n";

# start the actual api
uvicorn api:app
