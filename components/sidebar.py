import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

def Sidebar(bases, lojas):
    lojas_options = [{'label': 'TODAS', 'value': 'ALL'}] + [{'label': str(loja), 'value': str(loja)} for loja in lojas if isinstance(loja, str) and loja.strip()]
    
    return html.Div(
        [
            html.Div(
                [
                    html.H4("Filtros", className="text-left"),
                    html.Hr(),
                    html.Label('Selecione a Base:'),
                    dcc.Dropdown(
                        id='base-dropdown',
                        options=[
                            {'label': 'TODAS', 'value': 'ALL'},
                            {'label': 'GCOM', 'value': 'GCOM'},
                            {'label': 'TAGME', 'value': 'TAGME'}
                        ],
                        value='ALL'
                    ),
                    html.Label('Selecione a Loja:'),
                    dcc.Dropdown(
                        id='loja-dropdown',
                        options=lojas_options,
                        value='ALL'
                    ),
                    dbc.Button("Não identificados", id="btn-nao-registrados", n_clicks=0, className="btnguruverde")
                ],
                id="sidebar-content",
                className="sidebar",
            )
        ],
        id="sidebar"
    )
    lojas_options = [{'label': 'TODAS', 'value': 'ALL'}] + [{'label': loja, 'value': loja} for loja in lojas if loja.strip()]
    
    return html.Div(
        [
            html.Div(
                [
                    html.H4("Filtros", className="text-left"),
                    html.Hr(),
                    html.Label('Selecione a Base:'),
                    dcc.Dropdown(
                        id='base-dropdown',
                        options=[
                            {'label': 'TODAS', 'value': 'ALL'},
                            {'label': 'GCOM', 'value': 'GCOM'},
                            {'label': 'TAGME', 'value': 'TAGME'}
                        ],
                        value='ALL'
                    ),
                    html.Label('Selecione a Loja:'),
                    dcc.Dropdown(
                        id='loja-dropdown',
                        options=lojas_options,
                        value='ALL'
                    ),
                    dbc.Button("Não identificados", id="btn-nao-registrados", n_clicks=0, className="btnguruverde")
                ],
                id="sidebar-content",
                className="sidebar",
            )
        ],
        id="sidebar"
    )
    # Filtrar valores de texto
    lojas_options = [{'label': str(loja), 'value': str(loja)} for loja in lojas if isinstance(loja, str) and loja.strip()]
    # Definir o valor padrão como 'ALL' se houver mais de uma loja
    default_value = 'ALL' if len(lojas_options) > 1 else (lojas_options[0]['value'] if lojas_options else None)
    
    return html.Div(
        [
            html.Div(
                [
                    html.H4("Filtros", className="text-left"),
                    html.Hr(),
                    html.Label('Selecione a Base:'),
                    dcc.Dropdown(
                        id='base-dropdown',
                        options=[
                            {'label': 'TODAS', 'value': 'ALL'},
                            {'label': 'GCOM', 'value': 'GCOM'},
                            {'label': 'TAGME', 'value': 'TAGME'}
                        ],
                        value='ALL'
                    ),
                    html.Label('Selecione a Loja:'),
                    dcc.Dropdown(
                        id='loja-dropdown',
                        options=lojas_options,
                        value=default_value
                    ),
                    dbc.Button("Não identificados", id="btn-nao-registrados", n_clicks=0, className="btnguruverde")
                ],
                id="sidebar-content",
                className="sidebar",
            )
        ],
        id="sidebar"
    )
