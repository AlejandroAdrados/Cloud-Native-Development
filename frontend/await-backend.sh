#!/bin/sh

healthendpoint="$1"
echo "await script activated"

until curl -f --connect-timeout 10 "$healthendpoint"; do
  echo "Waiting for backend to be up"
  sleep 7
done

echo "Backend initialized. Configuring backend connections..."
echo "Sleeping for 25 seconds"
sleep 25

cd /usr/src/app
OUTPUTFILE=./outputs.json
if test -f "$OUTPUTFILE"; then
  for s in $(jq -r ".G7T2Stack|to_entries|map(\"\(.key)=\(.value|tostring)\")|.[]" $OUTPUTFILE); do
      echo VITE_$s >> ./.env
  done
fi

echo "Configuration done! Starting server..."
npm run docker-start
