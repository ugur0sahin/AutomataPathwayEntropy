import json
import numpy as np
import pandas as pd
import plotly.io as pio
from fastdtw import fastdtw
import plotly.graph_objects as go
from scipy.spatial.distance import euclidean

def scalar_euclidean(x, y):
    return abs(x - y)


def calculate_dtw_distance(seq1, seq2):
    distance, _ = fastdtw(seq1, seq2, dist=scalar_euclidean)
    return distance

def draw_change_plot(df):
    fig = go.Figure()

    # Plot the data using Plotly
    fig.add_trace(go.Scatter(y=df[Mutation], mode='lines+markers', name=Mutation,
                             marker=dict(size=10)))
    mean_ls, std_ls = np.mean(df[Mutation]), np.std(df[Mutation])
    # Add title and labels
    fig.update_layout(
        title=f'{Mutation} Plot',
        xaxis_title='Index',
        yaxis_title=Mutation,
        yaxis=dict(range=[mean_ls - std_ls, mean_ls + std_ls])
    )

    # Show the plot
    pio.write_image(fig, f'{Mutation}_plot.png')

sampleState, sampleMutation, sample_isolatedNodes = json.load(open("dbs/ACH-000001_states.json","r")), \
                                                    json.load(open("dbs/ACH-000001_mutated_nodes.json","r")), \
                                                    json.load(open("dbs/ACH-000001_isolated_nodes.json","r"))

Genes= list(sampleState[0].keys())

State_dependGene_activities = dict()
for Gene in Genes:
    Gene_activity_record_temp=list()
    for State in sampleState:
        Gene_activity_record_temp.append(State[Gene])
    State_dependGene_activities[Gene] = Gene_activity_record_temp


if __name__ != '__main__':
    json.dump(State_dependGene_activities, open("dbs/ACH-000001_gene_defined_states.json", "w"))

if __name__ == '__main__':
    dtw_dist_record=dict()
    for Mutation, States in State_dependGene_activities.items():
        pdStateMutation = {Mutation: States}

        df = pd.DataFrame(pdStateMutation)

        mutation_step = 20

        # Calculate the activity level changes before and after the mutation
        changes_before_mutation = [States[i + 1] - States[i] for i in range(10, mutation_step - 1)]
        changes_after_mutation = [States[i + 1] - States[i] for i in
                                  range(mutation_step+10, len(States) - 1)]

        # Calculate the DTW distance between the activity changes before and after the mutation
        dtw_distance = calculate_dtw_distance(changes_before_mutation, changes_after_mutation)
        dtw_dist_record[Mutation] = dtw_distance

print({k: v for k, v in sorted(dtw_dist_record.items(), key=lambda item: item[1], reverse=True)})



