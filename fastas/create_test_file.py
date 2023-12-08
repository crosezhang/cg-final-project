import os
import random
import sys

input_file_1 = sys.argv[1]
input_file_1_num = int(sys.argv[2])
input_file_2 = sys.argv[3]
input_file_2_num = int(sys.argv[4])
sequence_length = int(sys.argv[5])


def extract_and_write(file_1, input_1, file_2, input_2, seq_length):
    def get_random_lines(file_path, num_sequences, seq_length):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            selected_lines = []
            for seq_num in range(num_sequences):
                start_index = random.randint(0, max(0, len(lines) - seq_length))
                selected_seq = lines[start_index:start_index + seq_length]
                sequence = ''.join(selected_seq)
                file_label = os.path.basename(file_path).removesuffix('.fasta')
                sequence_label = f"{file_label}_Sequence{seq_num + 1}_Lines_{start_index + 1}_to_{start_index + seq_length}"
                selected_lines.append(f">{sequence_label}\n{sequence}")
            return selected_lines

    lines_from_file_1 = get_random_lines(file_1, input_1, seq_length)
    lines_from_file_2 = get_random_lines(file_2, input_2, seq_length)

    combined_sequences = lines_from_file_1 + lines_from_file_2
    random.shuffle(combined_sequences)

    file_1_name = os.path.basename(file_1).removesuffix('.fasta')
    file_2_name = os.path.basename(file_2).removesuffix('.fasta')
    output_file_path = f"{file_1_name}_{input_1}_{file_2_name}_{input_2}.fasta"

    with open(output_file_path, 'w') as output_file:
        for seq in combined_sequences:
            output_file.write(seq)

    return f"Sequences written to {output_file_path} in random order and FASTA format."


print(extract_and_write(input_file_1, input_file_1_num, input_file_2, input_file_2_num, sequence_length))
