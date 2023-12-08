import random


def generate_genomic_sequence(length):
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choice(nucleotides) for _ in range(length))


def write_sequence_to_file(filename, sequence, line_length=70):

    with open(filename, 'w') as file:
        file.write(f">XX.XX Random Genomic Sequence\n")
        for i in range(0, len(sequence), line_length):
            file.write(sequence[i:i + line_length] + '\n')


sequence_length = 4725 * 70  # 4725 lines of 70 characters each
genomic_sequence = generate_genomic_sequence(sequence_length)
write_sequence_to_file('random_genomic_sequence.fasta', genomic_sequence)
