import json
import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go



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

    for Mutation, States in State_dependGene_activities.items():
        pdStateMutation = {Mutation: States}
        df = pd.DataFrame(pdStateMutation)
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

