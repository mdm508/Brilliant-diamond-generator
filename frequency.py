from collections import Counter
import jieba

jieba.set_dictionary('dict.txt.big')

def get_word_frequencies(input_file):
    word_frequencies = Counter()

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Tokenize the line using jieba
            words = jieba.lcut(line, cut_all=False)
            word_frequencies.update(words)

    return word_frequencies

def line_frequency(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return Counter(lines)

def sentence_score(sentence, word_freq, line_freq, line_weight=0.7):
    # Tokenize the sentence using jieba
    words = jieba.lcut(sentence, cut_all=False)
    # Calculate the word score based on word frequencies
    word_score = sum(word_freq.get(word, 0) for word in words)

    word_density = word_score / len(words) if len(words) > 0 else 0
    # Calculate the overall score as a weighted combination of word density and line score
    overall_score = (1 - line_weight) * word_density + line_weight * line_freq
    return overall_score

def assign_scores(output_file, word_frequencies, line_frequencies):
    sentence_scores = []
    for line, frequency in line_frequencies.items():
        # Calculate the score for each sentence
        score = sentence_score(line, word_frequencies, frequency)
        sentence_scores.append((line, score))

    # Sort sentences by score in descending order
    sentence_scores.sort(key=lambda x: x[1], reverse=True)

    with open(output_file, 'w', encoding='utf-8') as out_file:
        for sentence, score in sentence_scores:
            out_file.write(f"{sentence.strip()}\t{score}\n")


# Input and output file paths
input_file = "out.txt"  # Your output file containing Chinese text
output_file = "sentences_with_scores_unique.txt"  # Output file with sentences and their scores

# Get word frequencies and line frequencies
word_frequencies = get_word_frequencies(input_file)
line_frequencies = line_frequency(input_file)

# Assign scores to sentences and save to the output file
assign_scores(output_file, word_frequencies, line_frequencies)
