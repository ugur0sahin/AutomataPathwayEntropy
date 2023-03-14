import random
import numpy as np
import plotly.graph_objects as go

def form_random_repetetive_matrix(number_of_genes=20,iteration_number=150, repetitve_range=30):
    rand1 = random.randint(1,repetitve_range)
    times = int(iteration_number/rand1) + 1

    motif,matrix = [[random.randint(0, 1) for _ in range(number_of_genes)] for i in range(rand1)], list()
    for i in range(times):
        matrix.extend(motif)

    return np.asarray(matrix)[:iteration_number,:]


def mutated_progressed_matrix(mutation_entry_ls=(18, 25, 50, 65,150, 175,192,215,250,269,325,365,395)):
    # Define the mutation entry numbers and Create a dictionary of matrices with different mutation entry numbers
    matrice_dict = dict()

    for mutation_entry in mutation_entry_ls:
        # Generate a random repetitive matrix with the specified mutation entry number
        matrix = form_random_repetetive_matrix(iteration_number=mutation_entry)

        # Add the matrix to the dictionary with the mutation entry number as the key
        matrice_dict[mutation_entry] = matrix

    return np.concatenate(list(matrice_dict.values())), matrice_dict

def repeat_counter(matrx,bootstrap_number=15):
    number_of_row, count_dict = (matrx.shape)[0], dict()
    for _ in range(bootstrap_number):
        chosen_row = random.randint(0, number_of_row - 1)
        if chosen_row not in count_dict.keys():
             count_dict[chosen_row]= np.count_nonzero(np.all(matrx == matrx[chosen_row], axis=1))

    # Get the values from the dictionary, Calculate the average of the values
    values = count_dict.values()
    average = sum(values) / len(values)

    return average

def plot_delta_progression(x1_wo_names,y1_local,y2_global):
    # Create a figure object
    fig = go.Figure()

    x1 = [str(step)+"thMut"for step in x1_wo_names]
    # Add scatter trace for y1 values with lines+markers mode
    fig.add_trace(go.Scatter(x=x1, y=y1_local, mode='lines+markers', name='Local Rep.',
                             marker=dict(size=10)))

    # Add scatter trace for y2 values with lines+markers mode
    fig.add_trace(go.Scatter(x=x1, y=y2_global, mode='lines+markers', name='Global Rep.',
                             marker=dict(size=10)))

    # Set layout for the plot
    fig.update_layout(title='DeltaChanges of Repetitive Patterns.',
                      xaxis_title='Steps Mutations are Introduced.',
                      yaxis_title='Local/Global Repetitions.',
                      legend_title='Variables')

    # Set x-axis to categorical
    fig.update_xaxes(type='category')

    # Show the plot
    fig.show()

if __name__ == '__main__':
    formed_matrix, matrice_dict = mutated_progressed_matrix()
    x1, y1_local, y2_global = list(matrice_dict.keys()), list(), list()
    for sector in matrice_dict.values():
        y1_local.append(repeat_counter(sector)); y2_global.append(repeat_counter(formed_matrix))
    plot_delta_progression(x1,y1_local,y2_global)