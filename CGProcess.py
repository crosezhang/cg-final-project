import pandas as pd
import sys
from collections import Counter
import itertools
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import seaborn as sns
from scipy.stats import chi2_contingency
import scipy.stats as stats
import re

# Read command-line arguments
fasta_file = sys.argv[1]
kraken_file = sys.argv[2]
phyloligo_file = sys.argv[3]
output_file = sys.argv[4]


def parse_kraken_output(file_path):
    sequence_taxid_mapping = {}
    table_data = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("C") or line.startswith("U"):
                parts = line.strip().split('\t')
                sequence_id = parts[1]
                tax_id = parts[2]
                sequence_taxid_mapping[sequence_id] = tax_id
            else:
                # Assuming this line is part of the table
                table_data.append(line.strip().split('\t'))

    # Remove header row if it exists in table_data
    if table_data[0][0] == '%':
        table_data.pop(0)

    # Converting table data to DataFrame
    columns = ['%', 'reads', 'taxReads', 'kmers', 'dup', 'cov', 'taxID', 'rank', 'taxName']
    df = pd.DataFrame(table_data, columns=columns)
    return sequence_taxid_mapping, df

sequence_taxid_mapping, kraken_df = parse_kraken_output(kraken_file)

#pre-processing: filling values of rank
kraken_df.loc[(kraken_df['rank'] == 'no rank') & kraken_df['taxName'].str.contains('str'),'rank'] = 'strain'
kraken_df.loc[(kraken_df['rank'] == 'no rank') & kraken_df['taxName'].str.contains('group'),'rank'] = 'kingdom'

kraken_df["cov"] = pd.to_numeric(kraken_df["cov"])

# Sort the DataFrame by rank specificity and coverage
rank_order = ['domain','superkingdom', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species group','species', 'strain', 'no rank']
rank_index = {rank: index for index, rank in enumerate(rank_order)}
kraken_df['rank_index'] = kraken_df['rank'].map(rank_index)

df_sorted = kraken_df.sort_values(by=['rank_index', 'cov'], ascending=[True, False])

#Filtering df to lowest ranks (max rank_index values to identify contaminants)
df_filtered = kraken_df[kraken_df['rank_index'] >= 8]

# Identify the target species based on the highest coverage
df_cov_sorted = df_filtered.sort_values(by='cov', ascending=False)
for index, row in df_cov_sorted.iterrows():
    if row['rank_index'] != 11:
        target_row = row
        break

target_species_name = target_row['taxName']
target_species_id = target_row['taxID']

kraken_contaminants_dict = []
kraken_contaminants = []

# Iterate through the lowest rank dataframe
for index, row in df_filtered.iterrows():
    if row['taxName'] != target_species_name:
        # For each potential contaminant, find the corresponding sequence IDs
        sequence_ids = [seq_id for seq_id, tax_id in sequence_taxid_mapping.items() if str(tax_id) == str(row['taxID'])]
        # Append the contaminant details to the list
        kraken_contaminants_dict.append({'taxName': row['taxName'], 'taxID': row['taxID'], 'sequence_IDs': sequence_ids})
        kraken_contaminants.extend(sequence_ids)
        
# Output the list of contaminants

def calculate_gc_content(sequence):
    gc_count = sum(1 for base in sequence if base in ["G", "C"])
    return gc_count / len(sequence) * 100


def parse_fasta(filename):
    with open(filename, 'r') as file:
        sequences = {}
        sequence_ids = []
        current_seq = ''
        current_id = ''
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if current_id:
                    sequences[current_id] = current_seq
                    sequence_ids.append(current_id)
                current_id = line[1:]
                current_seq = ''
            else:
                current_seq += line
        if current_id:
            sequences[current_id] = current_seq
            sequence_ids.append(current_id)
        return sequences, sequence_ids


sequences, sequence_ids = parse_fasta(fasta_file)

gc_contents = {seq_id: calculate_gc_content(seq) for seq_id, seq in sequences.items()}


def calculate_deviation(gc_content, typical_range):
    if gc_content < typical_range[0]:
        return typical_range[0] - gc_content
    elif gc_content > typical_range[1]:
        return gc_content - typical_range[1]
    else:
        return 0


# Identify sequences with atypical GC content and their deviation
typical_gc_range = (40, 60)  # Adjustable range: currently set to e.coli (prokaryotic) range
atypical_gc_data = [(seq_id, calculate_deviation(gc, typical_gc_range))
                    for seq_id, gc in gc_contents.items()
                    if not (typical_gc_range[0] <= gc <= typical_gc_range[1])]

# Sort the sequences in descending order of deviation
atypical_gc_data.sort(key=lambda x: x[1], reverse=True)

# Extract sorted sequence IDs
sorted_atypical_sequences = [data[0] for data in atypical_gc_data]


def generate_all_kmers(k_size):
    """Generate all possible k-mers for a given size and alphabet."""
    alphabet = ['A', 'T', 'G', 'C']
    return [''.join(kmer) for kmer in itertools.product(alphabet, repeat=k_size)]


def generate_kmer_profile(sequence, all_kmers):
    """Generate a k-mer profile for a given sequence using a fixed set of k-mers."""
    kmer_counts = {kmer: 0 for kmer in all_kmers}
    for i in range(len(sequence) - k_size + 1):
        kmer = sequence[i:i + k_size]
        if kmer in kmer_counts:
            kmer_counts[kmer] += 1
    return list(kmer_counts.values())


def cluster_sequences(kmer_profiles, sequence_ids, k_size, n_clusters=2):
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(kmer_profiles)

    # Scatter plot of the k-mer profiles colored by cluster label
    plt.scatter(np.array(kmer_profiles)[:, 0], np.array(kmer_profiles)[:, 1])
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    plt.title('K-mer Profile Clustering')

    # Annotate each point with its sequence ID
    for i, txt in enumerate(sequence_ids):
        plt.annotate(txt, (np.array(kmer_profiles)[i, 0], np.array(kmer_profiles)[i, 1]))

    plt.show()

    # Map labels to sequence IDs
    labeled_sequences = {sequence_id: label for sequence_id, label in zip(sequence_ids, labels)}

    # Group sequences by cluster
    clusters = {i: [] for i in range(n_clusters)}
    for sequence_id, label in labeled_sequences.items():
        clusters[label].append(sequence_id)

    return labels, clusters


# Generate all possible k-mers
k_size = 6
all_kmers = generate_all_kmers(k_size)

# Generate k-mer profiles for all sequences
kmer_profiles = [generate_kmer_profile(seq, all_kmers) for seq in sequences.values()]
labels = cluster_sequences(kmer_profiles, sequence_ids, k_size=6)


# START OF USE OF PHYLOLIGO

# Load the distance matrix
distance_matrix = np.loadtxt(phyloligo_file)

# Perform clustering
clusterer = KMeans(n_clusters=2)
cluster_labels = clusterer.fit_predict(distance_matrix)

# Perform t-SNE for visualization
perplexity_value = min(30, len(sequences) - 1)
tsne = TSNE(random_state=42, perplexity=perplexity_value)
embedded = tsne.fit_transform(distance_matrix)

# Plot t-SNE results with cluster labels
plt.figure(figsize=(10, 8))
sns.scatterplot(x=embedded[:, 0], y=embedded[:, 1], hue=cluster_labels, palette='bright')
plt.title('t-SNE visualization of clustering')
plt.show()

cluster_counts = Counter(cluster_labels)

# Determine the most common cluster (the cluster with the highest count)
most_common_cluster = cluster_counts.most_common(1)[0][0]

# Identify potential contaminants
# These are sequences whose cluster label is not the most common cluster label
phyloligo_contaminants = [sequence_ids[i] for i, cluster in enumerate(cluster_labels) if cluster != most_common_cluster]

# END OF PHYLOLIGO

def fuzzy_match(seq1, seq2):
    # Create patterns to match whole words
    pattern1 = fr'\b{seq1}\b'
    pattern2 = fr'\b{seq2}\b'
    return re.search(pattern1, seq2) or re.search(pattern2, seq1)


# Convert the lists to sets for efficient operations
phyloligo_set = set(phyloligo_contaminants)
kraken_set = set(kraken_contaminants)

# Initialize a set to store common contaminants
common_contaminants = set()

# Iterate through each pair of sequence IDs
for p_seq in phyloligo_set:
    for k_seq in kraken_set:
        if fuzzy_match(p_seq, k_seq):
            common_contaminants.add(k_seq)

# Contaminant Sequence Count Analysis
phyloligo_count = len(set(phyloligo_contaminants))
kraken_count = len(set(kraken_contaminants))
# Probability Estimation
common_count = len(common_contaminants)
prob_phyloligo_given_kraken = 0 if kraken_count == 0 else common_count / kraken_count
prob_kraken_given_phyloligo = 0 if phyloligo_count == 0 else common_count / phyloligo_count

# Sequence length analysis
phyloligo_lengths = [len(sequences[seq_id]) for seq_id in phyloligo_contaminants if seq_id in sequences]
kraken_lengths = [len(sequences[seq_id]) for seq_id in kraken_contaminants if seq_id in sequences]
# Visualization

# Plotting sequence length distributions
plt.hist(phyloligo_lengths, alpha=0.5, label='PhylOligo')
plt.hist(kraken_lengths, alpha=0.5, label='Kraken')
plt.legend()
plt.title('Sequence Length Distribution')
plt.xlabel('Sequence Length')
plt.ylabel('Frequency')
plt.show()

# Statistical Significance testing
# Create a contingency table
contingency_table = [[phyloligo_count, kraken_count], [len(sequences) - phyloligo_count, len(sequences) - kraken_count]]
chi2, p, dof, ex = chi2_contingency(contingency_table)

# Confidence Interval Calculation for Probability Estimations
confidence = 0.95
phyloligo_interval = stats.norm.interval(confidence, loc=prob_phyloligo_given_kraken,
                                         scale=stats.sem(phyloligo_lengths))
kraken_interval = stats.norm.interval(confidence, loc=prob_kraken_given_phyloligo, scale=stats.sem(kraken_lengths))

with open(output_file, 'w') as f:
    f.write("Kraken Identified Target Species:\n:")
    f.write(f"{target_species_name}\n")
    f.write(f"{df_filtered}\n")

    f.write("Kraken Identified Potential Contaminants:\n")
    f.writelines([f"{cont}\n" for cont in kraken_contaminants])

    f.write("\nPhylOligo Identified Potential Contaminants:\n")
    f.writelines([f"{cont}\n" for cont in phyloligo_contaminants])

    f.write("\nCommon Contaminants (High Confidence):\n")
    f.writelines([f"{cont}\n" for cont in common_contaminants])

    # Additional Analyses
    f.write("\nContaminant Sequence Count Analysis:\n")
    f.write(f"PhylOligo contaminant count: {phyloligo_count}\n")
    f.write(f"Kraken contaminant count: {kraken_count}\n")

    f.write("\nProbability Estimation:\n")
    f.write(f"P(PhylOligo|Kraken): {prob_phyloligo_given_kraken}\n")
    f.write(f"P(Kraken|PhylOligo): {prob_kraken_given_phyloligo}\n")

    f.write("\nChi-Square Test for Statistical Significance:\n")
    f.write(f"Chi-square test p-value: {p}\n")

    f.write("\nConfidence Intervals for Probability Estimations:\n")
    f.write(f"Confidence interval for P(PhylOligo|Kraken): {phyloligo_interval}\n")
    f.write(f"Confidence interval for P(Kraken|PhylOligo): {kraken_interval}\n")
