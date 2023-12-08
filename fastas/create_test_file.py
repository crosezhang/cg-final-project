import random
import sys

input_file_1_path = sys.argv[1]
input_file_1_num = sys.argv[2]  # number of sequences for input file 1
input_file_2_path = sys.argv[3]
input_file_2_num = sys.argv[4]  # number of sequences for input file 2
output_file_path = sys.argv[5]


def extract_and_write_random_lines(input_file_1, input_1, input_file_2, input_2, output_file_path):
    def get_random_lines(file_path, num_sequences, sequence_length):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            sequences = [''.join(random.sample(lines, sequence_length)) for _ in range(num_sequences)]
            return [f">{file_path.removesuffix('.fasta')}_Sequence_{i}\n{seq}" for i, seq in
                    enumerate(sequences, start=1)]

    input_1 = int(input_1)
    input_2 = int(input_2)
    sequence_length = 6

    lines_from_file_1 = get_random_lines(input_file_1, input_1, sequence_length)
    lines_from_file_2 = get_random_lines(input_file_2, input_2, sequence_length)

    combined_sequences = lines_from_file_1 + lines_from_file_2
    random.shuffle(combined_sequences)  # Shuffling the combined sequences

    with open(output_file_path, 'w') as output_file:
        for seq in combined_sequences:
            output_file.write(seq + "\n")

    return "Random sequences written to the output file in random order and FASTA format."


print(extract_and_write_random_lines(input_file_1_path, input_file_1_num, input_file_2_path, input_file_2_num,
                                     output_file_path))
