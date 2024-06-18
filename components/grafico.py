import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc

def create_graph(df):
    # Verificar se a coluna 'Base' existe no DataFrame
    if 'Base' not in df.columns:
        return html.Div([
            html.H4("Erro: Coluna 'Base' não encontrada no DataFrame")
        ])

    total_por_base = df['Base'].value_counts()
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
