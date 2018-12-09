#!/usr/bin/env bash

topology=$(cat "$1")
filtered_topology=$( echo "$topology" | grep -o '^[[:blank:]]*"..@localhost' | sed 's/\"/ /')

for agent in $filtered_topology
do

echo $agent
sudo prosodyctl deluser "$agent"

done

