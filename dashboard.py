import pandas as pd
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go

def create_layout(app, df):
    return html.Div(children=[
        html.Title('Controle TAGME Gurumê', id='title'),  # Definindo o título da página

        html.H1(children='Dashboard de Clientes por Base'),

        html.Div([
            html.Label('Selecione a Base:'),
            dcc.Dropdown(
                id='base-dropdown',
                options=[
                    {'label': 'ALL', 'value': 'ALL'},
                    {'label': 'GCOM', 'value': 'GCOM'},
                    {'label': 'TAGME', 'value': 'TAGME'}
                ],
                value='ALL'
            ),
            html.Button("Não Registrados", id="btn-nao-registrados", n_clicks=0)
        ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div(id="output-container-button",
                 children=[],
                 style={'width': '100%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div(id="output-container-graph",
                 children=[],
                 style={'width': '75%', 'display': 'inline-block'}),

        html.Div(id="clientes-gcom-tagme")
    ])

def update_graph(app, df):
    @app.callback(
        Output('output-container-graph', 'children'),
        [Input('base-dropdown', 'value')]
    )
    def display_graph(selected_base):
        # Verificar se a coluna 'Base' existe no DataFrame
        if 'Base' not in df.columns:
            return html.Div([
                html.H4("Erro: Coluna 'Base' não encontrada no DataFrame")
            ])

        if selected_base == 'ALL':
            filtered_df = df
        else:
            filtered_df = df[df['Base'] == selected_base]

        total_por_base = filtered_df['Base'].value_counts()
        bases = total_por_base.index
        totais = total_por_base.values

        # Cores dos gráficos
        colors = ['blue' if base == 'GCOM' else 'orange' for base in bases]

        figure = {
            'data': [
                go.Bar(
                    x=bases,
                    y=totais,
                    text=totais,
                    textposition='auto',
                    marker=dict(color=colors)  # Definir cores das barras
                )
            ],
            'layout': go.Layout(
                title='Total de Clientes por Base',
                xaxis={'title': 'Base'},
                yaxis={'title': 'Total de Clientes'},
                showlegend=False
            )
        }

        return dcc.Graph(
            id='clientes-por-base',
            figure=figure
        )

    @app.callback(
        Output("output-container-button", "children"),
        [Input("btn-nao-registrados", "n_clicks")],
        [State("base-dropdown", "value")]
    )
    def display_nao_registrados(n_clicks, selected_base):
        if n_clicks > 0:
            if selected_base == 'GCOM':
                gcom_clients = set(df[df['Base'] == 'GCOM']['Telefone'])
                tagme_clients = set(df[df['Base'] == 'TAGME']['Telefone'])
                nao_registrados = gcom_clients - tagme_clients
                lista_nao_registrados = html.Ul([html.Li(nome) for nome in df[df['Telefone'].isin(nao_registrados)]['Nome']])
                return lista_nao_registrados
            else:
                return "Selecione a base GCOM para identificar os clientes não registrados."
        return None
    
    @app.callback(
        Output("clientes-gcom-tagme", "children"),
        [Input('base-dropdown', 'value')]
    )
    def display_gcom_tagme_stats(selected_base):
        if selected_base == 'ALL':
            gcom_clients = set(df[df['Base'] == 'GCOM']['Telefone'])
            tagme_clients = set(df[df['Base'] == 'TAGME']['Telefone'])
            common_clients = gcom_clients.intersection(tagme_clients)
            
            return html.Div([
                html.H2('Clientes em GCOM X TAGME', style={'textAlign': 'center'}),
                html.P(f'Clientes em ambas as bases: {len(common_clients)}')
            ])
        else:
            return None
