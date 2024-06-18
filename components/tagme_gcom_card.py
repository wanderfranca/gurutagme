import dash_html_components as html
import dash_bootstrap_components as dbc

def create_tagme_gcom_card():
    return dbc.Card(
        dbc.CardBody(
            html.Div(id="clientes-gcom-tagme")
        ),
        className="mb-5",
    )