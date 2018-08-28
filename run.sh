#!/bin/sh
for filename in Data/CFD-WF/*.jpg; do
	echo "File $filename"
	python get-coords.py "$filename" "Results/CFD-WF/$(basename "$filename" .jpg)_output.jpg" "Results/cfd-wf-wrong.txt"
	# python face.py "$filename"
done