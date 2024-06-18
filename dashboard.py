from click import group
import pandas as pd
import plotly.graph_objs as go
import dash_html_components as html
import dash_bootstrap_components as dbc
import base64
import os
import datetime
import io

from dash import dcc, html, Input, Output, State, callback
from components.sidebar import Sidebar
from components.grafico import create_graph
from dash import dash_table
from dash.exceptions import PreventUpdate

def create_layout(app, create_graph, bases, lojas):
    sidebar = Sidebar(bases, lojas)

    # Card para o gráfico de Total de Clientes por Base
    graph_card = dbc.Card(
        dbc.CardBody(
            html.Div([
                html.H5("Total de Clientes por Base", className="card-title text-center"),
                html.Div(id="output-container-graph")
            ])
        ),
        className="mb-5",
        style={'background-color': 'white'}, 
    )

    # Card informações de Clientes na TAGME X GCOM
    tagme_gcom_card = dbc.Card(
        dbc.CardBody(
            html.Div(id="clientes-gcom-tagme")
        ),
        className="mb-5",
    )

    # Card clientes não registrados
    not_registered_card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Clientes Não Registrados", className="card-title text-center"),
                html.Div(id="output-container-not-registered")
            ]
        ),
        className="mb-5",
    )

    content = html.Div(id="page-content", children=[
        dbc.Row([
            dbc.Col(graph_card, width=5, className="mt-2"),
            dbc.Col(tagme_gcom_card, width=3),
        ], align="center"),

        dbc.Row([
            dbc.Col(not_registered_card, width=12)
        ], align="center"),

        dbc.Row([
            dbc.Col(id="output-container-button", width=12),
        ], align="center", className="my-4"),

        dbc.Row([
            dbc.Col(
                dbc.Button(
                    "Exportar para Excel",
                    id="export-excel-button",
                    color="primary",
                    className="mr-2 btnguruverde",
                    style={'display': 'none'}  # Ocultar inicialmente o botão de exportação
                ),
                width=12
            )
        ])
    ])

    return dbc.Container(fluid=True, children=[
        dbc.Row([
            dbc.Col(sidebar, id="sidebar-col", width=2),
            dbc.Col(content, id="content-col", width=10),
        ])
    ])

def update_graph(app, df):
    @app.callback(
        [Output('output-container-graph', 'children'),
         Output('clientes-gcom-tagme', 'children')],
        [Input('base-dropdown', 'value'),
         Input('loja-dropdown', 'value')]
    )
    def display_graph_and_stats(selected_base, selected_loja):
        # Verificar se as colunas 'Base' e 'Loja' existem no DataFrame
        if 'Base' not in df.columns or 'Loja' not in df.columns:
            return html.Div([
                html.H4("Erro: Coluna 'Base' ou 'Loja' não encontrada no DataFrame")
            ]), None

        # Filtrar o DataFrame de acordo com a base e a loja selecionadas
        filtered_df = df.copy()
        if selected_base != 'ALL':
            filtered_df = filtered_df[filtered_df['Base'] == selected_base]
        if selected_loja != 'ALL':
            filtered_df = filtered_df[filtered_df['Loja'] == selected_loja]

        # Calcular o total de clientes por base
        total_por_base = filtered_df['Base'].value_counts()
        bases = total_por_base.index
        totais = total_por_base.values

        # Cores dos gráficos
        colors = ['blue' if base == 'GCOM' else 'orange' for base in bases]

        # Gerar o gráfico
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

        graph = dcc.Graph(
            id='clientes-por-base',
            figure=figure
        )

        # Calcular estatísticas para o card TAGME X GCOM
        if 'TAGME' in filtered_df['Base'].unique():
            # Remover espaços em branco extras e converter para string para padronizar o formato do telefone
            filtered_df['Telefone'] = filtered_df['Telefone'].astype(str).str.strip()
            
            # Remover os registros com valores nulos na coluna 'Telefone'
            filtered_df_cleaned = filtered_df.dropna(subset=['Telefone'])
            
            # Agrupar os dados
            grouped_data = filtered_df_cleaned.groupby(['Telefone', 'Base']).size().unstack(fill_value=0)
            
            if 'GCOM' in grouped_data.columns:
                common_clients = grouped_data[(grouped_data['GCOM'] > 0) & (grouped_data['TAGME'] > 0)]
                
                # Total do agrupamento
                total_common_clients = common_clients.shape[0]
                
                # Total de clientes na base TAGME
                total_tagme_clients = filtered_df[filtered_df['Base'] == 'TAGME']['Telefone'].nunique()
                
                # Percentual de clientes em comum em relação ao total de clientes na base TAGME
                percentual_comum = (total_common_clients / total_tagme_clients) * 100 if total_tagme_clients > 0 else 0
                
                tagme_gcom_stats = html.Div([
                    html.H5('TAGME X GCOM', style={'textAlign': 'center'}),
                    html.P(f'Total de clientes identificados: {total_common_clients} | {percentual_comum:.2f}%', style={'textAlign': 'center'}),
                ])
            else:
                tagme_gcom_stats = html.Div([
                    html.H5('TAGME X GCOM', style={'textAlign': 'center'}),
                    html.P('Comparação de Dados entre GCOM X TAGME não identificados no filtro ou a loja ainda não realizou nenhuma identifi', style={'textAlign': 'center'}),
                ])
        else:
            tagme_gcom_stats = html.Div([
                html.H5('TAGME X GCOM', style={'textAlign': 'center'}),
                html.P('Nenhum cliente identificado na base TAGME para os filtros aplicados.', style={'textAlign': 'center'}),
            ])

        return graph, tagme_gcom_stats

    @app.callback(
        Output("output-container-button", "children"),
        [Input("btn-nao-registrados", "n_clicks")],
        [State("base-dropdown", "value"), State("loja-dropdown", "value")]
    )
    def display_nao_registrados(n_clicks, selected_base, selected_loja):
        if n_clicks > 0:
            if selected_base == 'TAGME':
                # Filtrar o DataFrame com base nos filtros selecionados
                filtered_df = df.copy()
                if selected_loja != 'ALL':
                    filtered_df = filtered_df[filtered_df['Loja'] == selected_loja]

                gcom_clients = set(filtered_df[filtered_df['Base'] == 'GCOM']['Telefone'])
                tagme_clients = set(filtered_df[filtered_df['Base'] == 'TAGME']['Telefone'])
                mesa_clients = set(filtered_df[filtered_df['MesaComanda'].notna()]['Telefone'])
                nao_registrados = gcom_clients - tagme_clients - mesa_clients
                
                lista_nao_registrados = html.Ul([html.Li(nome) for nome in filtered_df[filtered_df['Telefone'].isin(nao_registrados)]['Nome']])
            else:
                return "Selecione a base TAGME para identificar os clientes não registrados."
        return None

    @app.callback(
        Output("output-container-not-registered", "children"),
        [Input("btn-nao-registrados", "n_clicks")],
        [State("base-dropdown", "value"), State("loja-dropdown", "value")]
    )
    def display_nao_registrados_table(n_clicks, selected_base, selected_loja):
        if n_clicks > 0:
            if selected_base == 'TAGME':
                # Filtrar o DataFrame com base nos filtros selecionados
                filtered_df = df.copy()
                if selected_loja != 'ALL':
                    filtered_df = filtered_df[filtered_df['Loja'] == selected_loja]

                gcom_clients = set(filtered_df[filtered_df['Base'] == 'GCOM']['Telefone'])
                tagme_clients = set(filtered_df[filtered_df['Base'] == 'TAGME']['Telefone'])
                
                # Encontrar os clientes da TAGME que não estão na base GCOM
                nao_registrados = tagme_clients - gcom_clients
                
                # Filtrar o DataFrame para obter os dados dos clientes não registrados
                df_nao_registrados = filtered_df[filtered_df['Telefone'].isin(nao_registrados)]
                
                return generate_table(df_nao_registrados)
            else:
                return "Selecione a base TAGME para identificar os clientes não registrados."
        return None

    def display_gcom_tagme_stats(selected_base):
        if selected_base == 'ALL':
            # Remover espaços em branco extras e converter para string para padronizar o formato do telefone
            df['Telefone'] = df['Telefone'].astype(str).str.strip()
            
            # Remover os registros com valores nulos na coluna 'Telefone'
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
                html.H2('Clientes na TAGME X GCOM', style={'textAlign': 'center'}),
                html.P(f'Total de clientes identificados: {total_common_clients} | {percentual_comum:.2f}%'),
            ])
        else:
            return {'display': 'none'}

    @app.callback(
        Output("export-excel-button", "href"),
        [Input("table", "data")],
        prevent_initial_call=True
    )
    def export_to_excel(data):
        if not data:
            raise PreventUpdate

        dataframe = pd.DataFrame(data)
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        dataframe.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()
        output.seek(0)
        excel_data = base64.b64encode(output.read()).decode()

        # Nome do arquivo
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        filename = f"export_clientes_n_regis_{now}.xlsx"

        # Diretório de relatórios
        reports_dir = "relatorios"

        # Crie o diretório, se ele não existir
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)

        # Caminho do arquivo completo
        file_path = os.path.join(reports_dir, filename)

        # Salve o arquivo Excel no caminho especificado
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(excel_data))

        return f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{excel_data}"

    def generate_table(dataframe):
        return dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in dataframe.columns],
            data=dataframe.to_dict('records'),
            page_size=50,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
        )
