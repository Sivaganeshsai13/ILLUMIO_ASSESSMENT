#CSV Parser and Network Analyzer
##Overview
This project is a CSV parsing tool designed to analyze network-related data, such as tags and port/protocol combinations. It reads from a CSV file and generates useful statistics, which are saved into an output file.

##Features
Tag Counts: Computes how many times each tag appears in the CSV file.
Port/Protocol Combination Counts: Tallies the numberof occurrences for each port/protocol combination.

##Assumptions and Limitations
Log Format: The program only supports the default CSV log format and does not support custom formats.
Version Supported: The script supports Version 2 of the CSV format only.
Input Data: The input CSV file should have three columns: Port, Protocol, and Tag

**ExamplE**:
csv

Port,Protocol,Tag
443,tcp,sv_P2
23,tcp,sv_P1
25,tcp,email

File Naming: The input file must be named lookup.csv, and the output will be written to output.txt. Any other filename will require manual changes to the script.
CSV Headers: The CSV file should contain headers for each column.

Files
lookup.csv: Input CSV file containing the network data.
parser.py: Python script to parse the CSV file and compute the tag counts and port/protocol combination counts.
output.txt: The output file where the results are written, including:
A summary of tag counts.
A list of all port/protocol combinations and their counts.
