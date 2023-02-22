import random
import numpy as np

def form_random_repetetive_matrix(number_of_genes=20,iteration_number=150, repetitve_range=30):
    rand1 = random.randint(1,repetitve_range)
    times = int(iteration_number/rand1) + 1

    motif,matrix = [[random.randint(0, 1) for _ in range(number_of_genes)] for i in range(rand1)], list()
    for i in range(times):
        matrix.extend(motif)

    return np.asarray(matrix)[:iteration_number,:]


def repeat_counter(matrx):
    number_of_row, count_dict = (matrx.shape)[0], dict()
    for _ in range(15):
        chosen_row = random.randint(0, number_of_row - 1)
        if chosen_row not in count_dict.keys():
             count_dict[chosen_row]= np.count_nonzero(np.all(matrx == matrx[chosen_row], axis=1))

    # Get the values from the dictionary, Calculate the average of the values
    values = count_dict.values()
    average = sum(values) / len(values)

    return average

if __name__ == '__main__':
    matrix = form_random_repetetive_matrix()
    print(repeat_counter(matrix))