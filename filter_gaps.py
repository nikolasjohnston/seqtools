#!/usr/bin/env python

import argparse
from Bio import SeqIO

def filter_sequences(input_file, output_file, filtered_out_file, max_n_percentage):
    
     # Open fileS for reading AND WRITING
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile, open(filtered_out_file, 'w') as filtered_outfile:
     
       # Iterate through each sequence record in the input file
        for record in SeqIO.parse(infile, 'fasta'):
          
           # Get the sequence and calculate the percentage of N values
            sequence = str(record.seq)
            n_count = sequence.count('-')
            n_percentage = (n_count / len(sequence)) * 100
            
             # Check if the sequence meets the criteria
            if n_percentage <= max_n_percentage:
                 # Write the record to the output file
                SeqIO.write(record, outfile, 'fasta')
            else:
                # Write the record to the filtered-out file
                SeqIO.write(record, filtered_outfile, 'fasta')

def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Filter sequences based on N percentage.')
    parser.add_argument('input_file', help='Input FASTA file')
    parser.add_argument('output_file', help='Output FASTA file')
    parser.add_argument('filtered_out_file', help='File to save filtered out sequences')
    parser.add_argument('max_n_percentage', type=float, help='Maximum percentage of N values')

     # Parse command-line arguments
    args = parser.parse_args()

    # Call the function to filter sequences
    filter_sequences(args.input_file, args.output_file, args.filtered_out_file, args.max_n_percentage)

if __name__ == '__main__':
    main()
