import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash import Dash

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/style.css"])


def Sidebar():
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
                    dbc.Button("Não identificados", id="btn-nao-registrados", n_clicks=0, className="btnguruverde")
                ],
                id="sidebar-content",
                className="sidebar",
            )
        ],
        id="sidebar"
    )
