import pandas as pd
from dash import Dash
import dash_bootstrap_components as dbc
from dashboard import create_layout, update_graph

# Caminho do arquivo XLSX
file_path = '0B.xlsx' 

# Carregar os dados
df = pd.read_excel(file_path)

# Adicionar o código do país (55) aos telefones
df['Telefone'] = df['Telefone'].apply(lambda x: '55' + str(x).strip() if pd.notna(x) and not str(x).strip().startswith('55') else str(x).strip())

# Remover linhas duplicadas
df = df.drop_duplicates()

# Inicializar a aplicação Dash com um tema Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Configurar o layout da aplicação
app.layout = create_layout(app, df)

# Configurar os callbacks
update_graph(app, df)

# Executar a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)
