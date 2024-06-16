import pandas as pd
import plotly.graph_objs as go
import dash_html_components as html
import dash_bootstrap_components as dbc

def create_layout(app, df):
    sidebar = Sidebar()

   # Card para o gráfico de Total de Clientes por Base
    graph_card = dbc.Card(
        dbc.CardBody(
            html.Div([
                html.H5("Total de Clientes por Base", className="card-title text-center"),
                html.Div(id="output-container-graph")
            ])
        ),
        className="mb-5",
        style={'background-color': 'white'},  # Define o fundo do card como transparente
    )

    # Card para as informações de Clientes na TAGME X GCOM
    tagme_gcom_card = dbc.Card(
        dbc.CardBody(
            html.Div(id="clientes-gcom-tagme")
        ),
        className="mb-5",
    )

    content = html.Div(id="page-content", children=[
        dbc.Row([
            dbc.Col(graph_card, width=5, className="mt-2"),
            dbc.Col(tagme_gcom_card, width=3),
        ], align="center"),
        
        dbc.Row([
            dbc.Col(id="output-container-button", width=12),
        ], align="center", className="my-4"),
    ])

    return dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col(sidebar, id="sidebar-col", width=3),
            dbc.Col(content, id="content-col", width=9),
        ])
    ])

def update_graph(app, df):
    @app.callback(
        Output('output-container-graph', 'children'),
        [Input('base-dropdown', 'value')]
    )
    def display_graph(selected_base):
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

        colors = ['blue' if base == 'GCOM' else 'orange' for base in bases]

        figure = {
            'data': [
                go.Bar(
                    x=bases,
                    y=totais,
                    text=totais,
                    textposition='auto',
                    marker=dict(color=colors)
                )
            ],
            'layout': go.Layout(
                xaxis={'title': 'Base'},
                yaxis={'title': 'Total de Clientes'},
                showlegend=False,
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)'
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

    @app.callback(
        Output("clientes-gcom-tagme", "children"),
        [Input('base-dropdown', 'value')]
    )
    def display_gcom_tagme_stats(selected_base):
        if selected_base == 'ALL':
            # Remover espaços em branco extras e converter para string para padronizar o formato do telefone
            df['Telefone'] = df['Telefone'].astype(str).str.strip()
            df_cleaned = df.dropna(subset=['Telefone'])
            
            # Agrupar os dados
            grouped_data = df_cleaned.groupby(['Telefone', 'Base']).size().unstack(fill_value=0)
            
            common_clients = grouped_data[(grouped_data['GCOM'] > 0) & (grouped_data['TAGME'] > 0)]
            
            # Total do agrupamento
            total_common_clients = common_clients.shape[0]
            
            # Total de clientes na base TAGME
            total_tagme_clients = df[df['Base'] == 'TAGME']['Telefone'].nunique()
            
            # Percentual de clientes em comum em relação ao total de clientes na base TAGME
            percentual_comum = (total_common_clients / total_tagme_clients) * 100
            
            return html.Div([
                html.H5('Clientes na TAGME X GCOM', style={'textAlign': 'center'}),
                html.P(f'Total de clientes identificados: {total_common_clients} | {percentual_comum:.2f}%'),
            ])
        else:
            return None
