import random
import sys

# input:
# [python3] [create_test_file.py] [input_file_1_name] [number of sequences input_file_1] [input_file_2_name] [number of sequences input_file_2] [sequence_length]

input_file_1 = sys.argv[1]
input_file_1_num = int(sys.argv[2])  # number of sequences for input file 1
input_file_2 = sys.argv[3]
input_file_2_num = int(sys.argv[4])  # number of sequences for input file 2
sequence_length = int(sys.argv[5])

def extract_and_write_random_lines(file_1, input_1, file_2, input_2, seq_length):
    def get_random_lines(file_path, num_sequences, seq_length):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            sequences = [''.join(random.sample(lines, seq_length)) for _ in range(num_sequences)]
            return [f">{file_path.removesuffix('.fasta')}_sequence_{i}\n{seq}" for i, seq in
                    enumerate(sequences, start=1)]

    lines_from_file_1 = get_random_lines(file_1, input_1, seq_length)
    lines_from_file_2 = get_random_lines(file_2, input_2, seq_length)

    combined_sequences = lines_from_file_1 + lines_from_file_2
    random.shuffle(combined_sequences)  # Shuffling the combined sequences

    output_file_path = f"{input_file_1.removesuffix('.fasta')}_{input_1}_{input_file_2.removesuffix('.fasta')}_{input_2}.fasta"

    with open(output_file_path, 'w') as output_file:
        for seq in combined_sequences:
            output_file.write(seq)

    return "Sequences written to the output file in random order and FASTA format."


print(extract_and_write_random_lines(input_file_1, input_file_1_num, input_file_2, input_file_2_num, sequence_length))
