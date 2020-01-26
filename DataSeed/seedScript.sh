#!/bin/bash

function SeedAll(){
server=$1

echo $server

Seed $server 'emails.json' email/save
Seed $server 'employees.json' employee/save
Seed $server 'locations.json' location/save
Seed $server 'manufacturerImages.json' manufacturerImage/save
Seed $server 'manufacturers.json ' manufacturer/save
Seed $server 'openings.json' opening/save
Seed $server 'products.json' product/save
Seed $server 'realizations.json' realization/save
Seed $server 'realizationTypes.json' realizationType/save
Seed $server 'resources.json' resource/save
Seed $server 'telephones.json' telephone/save
Seed $server 'users.json ' user/register

}

function Seed(){
server=$1
seedPayloadFile=$2
endpoint=$3

data_length=$(jq '. | length' $seedPayloadFile)
for ((x = 0; x < $data_length; x++)); do
    data=$(jq -c ".[$x]" $seedPayloadFile)
    curl -s --insecure --location --request POST  "$server/api/$endpoint" -H 'accept: application/json; charset=utf-8' -H 'Content-Type: application/json-patch+json; charset=utf-8' --data-raw "$data"
done
}