import numpy as np
import ASCIIChecker as asc
import string
import sys

alphabet = list(string.ascii_lowercase)
subs_matrix = []
trans_matrix = []
deletion_matrix = []
insertion_matrix = []
subs_total = 0
trans_total = 0
deletion_total = 0
insertion_total = 0


def get_counts_matrix(array, txt):
    with open(txt, 'r') as f:
        for line in f:
            if len(line.split()) > 1:
                array.append([int(num) for num in line.split()])
            else:
                return float(line.split()[0])


def get_words_from_dictionary(counts, lines, words):
    for index in range(2, len(lines[2:])):
        line = lines[index].split()
        if len(line) is 2:
            words.insert(index, line[0])
            counts.insert(index, line[1])


def print_correct_word(dictionary_word_counts, dictionary_words, total_count, word, correct_words_file):
    edit_words = []
    edit_ratios = []
    for i in range(len(word)):
        if i is not (len(word) - 1):  # insertion done
            w = word[0:i + 1] + "" + word[i + 2:]
            first = asc.checkAscii(ord(word[i])) - 97
            second = asc.checkAscii(ord(word[i + 1])) - 97
            if dictionary_words.__contains__(w):
                edit_words.append(w)
                edit_ratios.append(float(insertion_matrix[first][second] + 1) / (insertion_total + 32) *
                                   float(dictionary_word_counts[dictionary_words.index(w)]) / total_count)
            first = asc.checkAscii(ord(word[i + 1])) - 97  # trans done
            second = asc.checkAscii(ord(word[i])) - 97
            w = word[0:i] + word[i + 1] + word[i] + word[i + 2:]
            if dictionary_words.__contains__(w):
                edit_words.append(w)
                edit_ratios.append(float(trans_matrix[first][second] + 1) / (trans_total + 32) *
                                   float(dictionary_word_counts[dictionary_words.index(w)]) / total_count)
        for letter in alphabet:
            if letter is not word[i]:  # subs done
                # y typed as x
                w = word[0:i] + letter + word[i + 1:len(word)]
                # first word[i]
                # second letter
                first = asc.checkAscii(ord(word[i])) - 97
                second = asc.checkAscii(ord(letter)) - 97
                if dictionary_words.__contains__(w):
                    edit_words.append(w)
                    edit_ratios.append(float(subs_matrix[first][second] + 1) / (subs_total + 32) *
                                       float(dictionary_word_counts[dictionary_words.index(w)]) / total_count)
            if i == len(word) - 1:
                w = word + letter
                first = asc.checkAscii(ord(word[i])) - 97
                second = asc.checkAscii(ord(letter)) - 97
                if dictionary_words.__contains__(w):
                    edit_words.append(w)  # deletion done
                    edit_ratios.append(float(deletion_matrix[first][second] + 1) / (deletion_total + 32) *
                                       float(dictionary_word_counts[dictionary_words.index(w)]) / total_count)
            else:
                w = word[0:i + 1] + letter + word[i + 1:len(word)]
                first = asc.checkAscii(ord(word[i])) - 97
                second = asc.checkAscii(ord(letter)) - 97
                if dictionary_words.__contains__(w):
                    edit_words.append(w)  # deletion done
                    edit_ratios.append(float(deletion_matrix[first][second] + 1) / (deletion_total + 32) *
                                       float(dictionary_word_counts[dictionary_words.index(w)]) / total_count)
    if len(edit_words) != 0:
        correct_words_file.write(edit_words[edit_ratios.index(np.amax(edit_ratios))] + "\n")
    else:
        correct_words_file.write("\n")


def main():
    global subs_total, trans_total, deletion_total, insertion_total
    dictionary_file = open("dictionary.txt", "r")
    lines = dictionary_file.readlines()
    total_count = float(lines[1])
    dictionary_words = []  # words in the dictionary
    dictionary_word_counts = []  # counts of the words
    get_words_from_dictionary(dictionary_word_counts, lines, dictionary_words)
    subs_total = get_counts_matrix(subs_matrix, "substitution_matrix.txt")
    trans_total = get_counts_matrix(trans_matrix, "trans_matrix.txt")
    deletion_total = get_counts_matrix(deletion_matrix, "deletion_matrix.txt")
    insertion_total = get_counts_matrix(insertion_matrix, "insertion_matrix.txt")

    test_miss = open(sys.argv[1], "r")
    correct_words = open(sys.argv[2], "w+")
    for line in test_miss:
        print_correct_word(dictionary_word_counts, dictionary_words, total_count, line.split()[0], correct_words)


if __name__ == '__main__':
    main()
