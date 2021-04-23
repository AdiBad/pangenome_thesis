#!/bin/bash
mkdir -p "temp"
for i in *.zip; do
	unzip "$i" "summary.txt" -d "temp"
	mv "temp/summary.txt" "$(basename "$i" .zip)_summary.txt"
done
