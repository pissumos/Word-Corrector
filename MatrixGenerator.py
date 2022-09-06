import re
import numpy as np
import ASCIIChecker as asc


def main():
    deletion_matrix = np.zeros((32, 32))
    deletion_file = open("deletion_matrix.txt", "w+")
    insertion_matrix = np.zeros((32, 32))
    insertion_file = open("insertion_matrix.txt", "w+")
    trans_matrix = np.zeros((32, 32))
    trans_file = open("trans_matrix.txt", "w+")
    subs_matrix = np.zeros((32, 32))
    subs_file = open("substitution_matrix.txt", "w+")
    spell_errors_file = open("spell-errors.txt", "r")
    error_lines = spell_errors_file.readlines()
    for line in error_lines:
        colon_index = line.find(":")
        word = line[0:colon_index]
        line = line[colon_index + 2:line.__len__() - 1]
        misspelled = line.split()
        misspelled_count = []
        # get all misspelled versions and counts
        for miss_i in range(0, misspelled.__len__()):
            match = re.match("(\w*)(\*)?(\d*)?(,)?", misspelled[miss_i])
            misspelled[miss_i] = match.group(1)
            if match.group(3):
                misspelled_count.insert(miss_i, match.group(3))
            else:
                misspelled_count.insert(miss_i, 0)
            miss = misspelled[miss_i]
            for i in range(len(word) - 1):
                # check for transposition
                if miss == word[:i] + word[i + 1] + word[i] + word[i + 2:]:
                    first = asc.checkAscii(ord(word[i + 1]))
                    second = asc.checkAscii(ord(word[i]))
                    trans_matrix[first - 97][second - 97] = int(trans_matrix[first - 97][second - 97]) + int(
                        misspelled_count[miss_i])
            for i in range(len(miss)):
                # check for insertion
                if word == miss[:i] + miss[i + 1:]:
                    first = asc.checkAscii(ord(miss[i - 1]))
                    second = asc.checkAscii(ord(miss[i][0]))
                    insertion_matrix[first - 97][second - 97] = int(
                        insertion_matrix[first - 97][second - 97]) + int(
                        misspelled_count[miss_i])
            for i in range(len(word)):
                # check for deletion
                if miss == word[:i] + word[i + 1:]:
                    first = asc.checkAscii(ord(word[i - 1]))
                    second = asc.checkAscii(ord(word[i]))
                    deletion_matrix[first - 97][second - 97] = int(deletion_matrix[first - 97][second - 97]) + int(
                        misspelled_count[miss_i])
                if len(miss) == len(word):
                    # check for subs
                    if word[:i] + word[i + 1:] == miss[:i] + miss[i + 1:]:
                        first = asc.checkAscii(ord(miss[i]))
                        second = asc.checkAscii(ord(word[i]))
                        subs_matrix[first - 97][second - 97] = int(subs_matrix[first - 97][second - 97]) + int(
                            misspelled_count[miss_i])

    total_trans = 0
    total_sub = 0
    total_ins = 0
    total_del = 0
    for i in range(32):
        for j in range(32):
            total_trans += trans_matrix[i][j]
            trans_file.write(str(int(trans_matrix[i][j])) + " ")
            total_sub += subs_matrix[i][j]
            subs_file.write(str(int(subs_matrix[i][j])) + " ")
            total_ins += insertion_matrix[i][j]
            insertion_file.write(str(int(insertion_matrix[i][j])) + " ")
            total_del += deletion_matrix[i][j]
            deletion_file.write(str(int(deletion_matrix[i][j])) + " ")
        insertion_file.write("\n")
        trans_file.write("\n")
        subs_file.write("\n")
        deletion_file.write("\n")
    deletion_file.write(str(int(total_del)))
    insertion_file.write(str(int(total_ins)))
    subs_file.write(str(int(total_sub)))
    trans_file.write(str(int(total_trans)))


if __name__ == '__main__':
    main()
