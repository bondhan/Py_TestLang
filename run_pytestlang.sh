#!/bin/sh

while getopts w: option
do
case "${option}"
in
w) WORKER_NUM=${OPTARG};;
esac
done

if [ -z "$WORKER_NUM" ]
then
WORKER_NUM=10
fi

#echo "Running with worker number = " $WORKER_NUM
#exit 1

# source ../env/bin/activate

cd ./src/apiserver/
gunicorn -w $WORKER_NUM -b $LISTEN_ADDR:5000 main_api_server:app_apiserver &

cd ../iso_client/
gunicorn -w $WORKER_NUM main_iso_client:app_isoclient -b $LISTEN_ADDR:8080 &

cd ../iso_server/
python3.7 main_iso_server.py
