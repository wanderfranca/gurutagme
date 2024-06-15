import pandas as pd
from dash import Dash
from dashboard import create_layout, update_graph

# arquivo XLSX
file_path = '0B.xlsx' 

# Carregar os dados
df = pd.read_excel(file_path)

# Add 55 nos telefones
df['Telefone'] = df['Telefone'].apply(lambda x: '55' + str(x) if pd.notna(x) and not str(x).startswith('55') else x)

# Remover linhas duplicadas
df = df.drop_duplicates()

app = Dash(__name__)

# Configurar o layout da aplicação
app.layout = create_layout(app, df)

# Configurar os callbacks
update_graph(app, df)

# Executar a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)
