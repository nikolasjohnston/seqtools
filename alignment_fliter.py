#!/usr/bin/env python
## This script takes an alignment FASTA file as input and filters sequences based on "N" values and gap ("-") percentage.
## The user specifies the maximum percentages for filtering. Outputs include a filtered outfile, a list of sequences removed, and a summary CSV file.

import argparse
import os
import csv
from Bio import SeqIO

def generate_output_filenames(input_file):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_filtered.fasta"
    filtered_out_file = f"{base_name}_filtered_out.fasta"
    summary_file = f"{base_name}_summary.txt"
    csv_file = f"{base_name}_filtered_status.csv"
    return output_file, filtered_out_file, summary_file, csv_file

def filter_sequences(input_file, max_n_percentage, max_gap_percentage):
    output_file, filtered_out_file, summary_file, csv_file = generate_output_filenames(input_file)

    with open(input_file, 'r') as infile:
        with open(output_file, 'w') as outfile:
            with open(filtered_out_file, 'w') as filtered_outfile:
                with open(summary_file, 'w') as summaryfile:
                    with open(csv_file, 'w', newline='') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow(['Sample', 'Status', 'N Percentage', 'Gap Percentage', 'Reason'])  # CSV header

                        for record in SeqIO.parse(infile, 'fasta'):
                            sequence_name = record.id
                            sequence = str(record.seq)
                            n_count = sequence.count('N')
                            gap_count = sequence.count('-')
                            n_percentage = (n_count / len(sequence)) * 100
                            gap_percentage = (gap_count / len(sequence)) * 100

                            print(f'Sequence: {sequence_name}, N Percentage: {n_percentage:.2f}, Gap Percentage: {gap_percentage:.2f}')

                            if n_percentage <= max_n_percentage and gap_percentage <= max_gap_percentage:
                                SeqIO.write(record, outfile, 'fasta')
                                csv_writer.writerow([sequence_name, 'Kept', f'{n_percentage:.2f}%', f'{gap_percentage:.2f}%', ''])
                            else:
                                SeqIO.write(record, filtered_outfile, 'fasta')
                                summaryfile.write(f'{sequence_name}\n')
                                reason = []
                                if n_percentage > max_n_percentage:
                                    reason.append('N')
                                if gap_percentage > max_gap_percentage:
                                    reason.append('Gap')
                                csv_writer.writerow([sequence_name, 'Removed', f'{n_percentage:.2f}%', f'{gap_percentage:.2f}%', ', '.join(reason)])

def main():
    parser = argparse.ArgumentParser(description='Filter sequences based on N and gap percentages.')
    parser.add_argument('input_file', help='Input FASTA file')
    parser.add_argument('max_n_percentage', type=float, help='Maximum percentage of N values')
    parser.add_argument('max_gap_percentage', type=float, help='Maximum percentage of gap (-) values')

    args = parser.parse_args()

    filter_sequences(args.input_file, args.max_n_percentage, args.max_gap_percentage)

if __name__ == '__main__':
    main()
