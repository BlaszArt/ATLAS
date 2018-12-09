#!/usr/bin/env bash

topology=$(cat "$1")
filtered_topology=$( echo "$topology" | grep -o '^[[:blank:]]*"..@localhost' | sed 's/\"/ /')

for agent in $filtered_topology
do

sudo prosodyctl deluser "$agent"

done

