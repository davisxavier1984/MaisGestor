import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import requests
import tempfile
import json

# Função para carregar o estado de envio de emails de um arquivo JSON
def carregar_estado_emails():
    if os.path.exists("emails_enviados.json"):
        with open("emails_enviados.json", "r") as f:
            return json.load(f)
    return {}

# Função para salvar o estado de envio de emails em um arquivo JSON
def salvar_estado_emails(emails_enviados):
    with open("emails_enviados.json", "w") as f:
        json.dump(emails_enviados, f)

# Função para criar uma checkbox para cada município e registrar o envio de email
def registrar_emails_por_municipio(df, emails_enviados):
    st.subheader("Registro de Envio de E-mails por Município")
    for municipio in df['MUNICIPIO'].unique():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(municipio)
        with col2:
            enviado = emails_enviados.get(municipio, False)
            email_enviado = st.checkbox("Email enviado", value=enviado, key=municipio)
            emails_enviados[municipio] = email_enviado
    salvar_estado_emails(emails_enviados)

# Função para mapear estados para os seus respectivos códigos UF
def get_uf_code(state):
    state = state.upper()  # Converte o estado para maiúsculas
    uf_codes = {
        'AC': '12', 'AL': '27', 'AM': '13', 'AP': '16', 'BA': '29', 'CE': '23',
        'DF': '53', 'ES': '32', 'GO': '52', 'MA': '21', 'MG': '31', 'MS': '50',
        'MT': '51', 'PA': '15', 'PB': '25', 'PE': '26', 'PI': '22', 'PR': '41',
        'RJ': '33', 'RN': '24', 'RO': '11', 'RR': '14', 'RS': '43', 'SC': '42',
        'SE': '28', 'SP': '35', 'TO': '17'
    }
    return uf_codes.get(state)

# Função para contar o número de instrumentos não iniciados por estado
def contar_nao_iniciados_por_estado():
    estados = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
    total_nao_iniciados_por_estado = []
    for estado in estados:
        df = load_data_from_state(estado)
        if not df.empty:
            contagem_nao_iniciados = contar_nao_iniciados(df)
            total_nao_iniciados = contagem_nao_iniciados['NaoIniciados'].sum()
            total_nao_iniciados_por_estado.append({'Estado': estado, 'NaoIniciados': total_nao_iniciados})
    return pd.DataFrame(total_nao_iniciados_por_estado)

# Função para criar o gráfico da Situação Nacional
def criar_grafico_situacao_por_estado(df_situacao_estado):
    df_situacao_estado = df_situacao_estado.sort_values(by='NaoIniciados', ascending=False)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.barh(df_situacao_estado['Estado'], df_situacao_estado['NaoIniciados'], color='blue')
    ax.set_xlabel('Estado')
    ax.set_ylabel('Quantidade de Instrumentos Não Iniciados')
    ax.set_title('Situação Nacional - Quantidade de Instrumentos Não Iniciados por Estado')
    st.pyplot(fig)

# Função para formatar as cores da Tabela
def highlight_cells(val):
    if val in ['Aprovado', 'Avaliado', 'Aprovado com Ressalvas']:
        color = 'green'
    elif val in ['Não Iniciado', 'Não Aprovado']:
        color = 'red'
    elif val in ['Em Análise no Conselho de Saúde', 'Em Elaboração', 'Retornado para Ajustes']:
        color = 'yellow'
    else:
        color = ''
    return f'background-color: {color}'

# Função para baixar e renomear o arquivo
def download_and_rename_file(state):
    uf_code = get_uf_code(state)
    if uf_code is None:
        st.error(f"Código da UF para o estado '{state}' não encontrado.")
        return None
    url = f'https://digisusgmp.saude.gov.br/v1.5/transparencia/extracao/csv?uf={uf_code}'
    temp_dir = tempfile.gettempdir()  # Diretório temporário seguro para escrita
    local_file = os.path.join(temp_dir, f'{state}.csv')  # Nome do arquivo no diretório temporário

    try:
        response = requests.get(url)  # Fazer a requisição usando requests
        if response.status_code == 200:
            with open(local_file, 'wb') as f:
                f.write(response.content)  # Escrever o conteúdo baixado no arquivo local
        else:
            st.error(f"Erro ao baixar o arquivo. Código de status: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao baixar o arquivo: {e}")
        return None

    return local_file

# Função para carregar os dados com tratamento de erros
def load_data_from_state(state):
    local_file = download_and_rename_file(state)
    if local_file is None:
        return pd.DataFrame()

    try:
        df = pd.read_csv(local_file, delimiter=';', on_bad_lines='skip')  # Ignorar linhas com erros de tokenização
    except pd.errors.ParserError as e:
        st.error(f"Erro ao ler o arquivo CSV: {e}")
        return pd.DataFrame()
    except FileNotFoundError:
        st.error(f"Arquivo {local_file} não encontrado.")
        return pd.DataFrame()

    if 'REGIAO' not in df.columns:
        st.error(f"A coluna 'REGIAO' não foi encontrada no arquivo {local_file}.")
        return pd.DataFrame()

    df['EXERCICIO'] = df['EXERCICIO'].fillna(0).astype(int).astype(str)
    df.loc[df['SITUACAO'].isnull(), 'SITUACAO'] = 'Não Iniciado'
    df['TIPO_INSTRUMENTO'] = df['TIPO_INSTRUMENTO'].replace({
        'Plano Municipal de Saúde': 'PMS',
        'Programação Anual de Saúde': 'PAS',
        'Plano de Saúde': 'PMS'
    })

    return df

# Função para contar o número de instrumentos não iniciados por município
def contar_nao_iniciados(df):
    df_nao_iniciados = df[df['SITUACAO'] == 'Não Iniciado']
    contagem = df_nao_iniciados.groupby('MUNICIPIO').size().reset_index(name='NaoIniciados')
    return contagem

# Função para gerar a tabela formatada
def gerar_tabela_formatada(df, municipio, regional):
    tabela_municipio = df[(df['MUNICIPIO'] == municipio) & (df['REGIAO'] == regional)]
    if tabela_municipio.empty:
        return pd.DataFrame()
        
    pms_index = tabela_municipio[tabela_municipio['TIPO_INSTRUMENTO'] == 'PMS'].index
    tabela_municipio.loc[tabela_municipio['TIPO_INSTRUMENTO'] == 'Plano de Saúde', 'TIPO_INSTRUMENTO'] = 'PMS'
    
    pms_lines = tabela_municipio[tabela_municipio['TIPO_INSTRUMENTO'] == 'PMS']
    exercicios_lines = tabela_municipio[tabela_municipio['TIPO_INSTRUMENTO'] != 'PMS']
    exercicios_lines = exercicios_lines.sort_values(by=['FASE', 'EXERCICIO'])
    tabela_municipio = pd.concat([pms_lines, exercicios_lines])
    
    tabela_formatada = tabela_municipio.pivot_table(index=['FASE', 'EXERCICIO'],
                                                    columns='TIPO_INSTRUMENTO',
                                                    values='SITUACAO',
                                                    aggfunc=lambda x: x).reset_index()
    tabela_formatada.insert(0, 'REGIONAL', regional)
    tabela_formatada.insert(0, 'MUNICÍPIO', municipio)
    tabela_formatada.fillna('', inplace=True)
    
    if 'Pactuação' in tabela_formatada.columns:
        tabela_formatada.drop(columns=['Pactuação'], inplace=True)
    if 'PMS' not in tabela_formatada.columns:
        tabela_formatada['PMS'] = ''
    if 'PAS' not in tabela_formatada.columns:
        tabela_formatada['PAS'] = ''
        
    colunas_ordem = ['MUNICÍPIO', 'REGIONAL', 'FASE', 'EXERCICIO', 'PMS', 'PAS'] + [col for col in tabela_formatada.columns if col not in ['MUNICÍPIO', 'REGIONAL', 'FASE', 'EXERCICIO', 'PMS', 'PAS']]
    tabela_formatada = tabela_formatada[colunas_ordem]
    return tabela_formatada

# Função para criar uma barra colorida proporcional ao número de instrumentos não iniciados
def criar_escala_colorida(nao_iniciados, max_nao_iniciados):
    proporcao = nao_iniciados / max_nao_iniciados
    cor = f'rgb({int(255 * proporcao)}, {int(255 * (1 - proporcao))}, 0)'
    largura = int(proporcao * 100)
    barra = f"<div style='background-color:{cor}; width:{largura}%; height:10px; display:inline-block;'></div>"
    return barra

# Função para criar o gráfico completo por regional
def criar_grafico_completo(df, regional, max_nao_iniciados):
    municipios_na_regiao = df[df['REGIAO'] == regional]
    contagem_nao_iniciados = contar_nao_iniciados(municipios_na_regiao)
    contagem_nao_iniciados = contagem_nao_iniciados.sort_values(by='NaoIniciados', ascending=False)
    cores = [(1.0, 1 - (nao_iniciados / max_nao_iniciados), 0.0, 1.0) for nao_iniciados in contagem_nao_iniciados['NaoIniciados']]
    fig, ax = plt.subplots(figsize=(10, 8))
    barras = ax.barh(contagem_nao_iniciados['MUNICIPIO'], contagem_nao_iniciados['NaoIniciados'], color=cores)
    ax.set_xlabel('Número de Instrumentos Não Iniciados')
    ax.set_ylabel('Município')
    ax.set_title(f'Instrumentos Não Iniciados na Regional {regional}')
    st.pyplot(fig)

# Função para criar o gráfico para todos os municípios de um estado
def criar_grafico_estado_completo(df):
    contagem_nao_iniciados = contar_nao_iniciados(df)
    contagem_nao_iniciados = contagem_nao_iniciados.sort_values(by='NaoIniciados', ascending=False)
    max_nao_iniciados = contagem_nao_iniciados['NaoIniciados'].max()
    cores = [(1.0, 1 - (nao_iniciados / max_nao_iniciados), 0.0, 1.0) for nao_iniciados in contagem_nao_iniciados['NaoIniciados']]
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.barh(contagem_nao_iniciados['MUNICIPIO'], contagem_nao_iniciados['NaoIniciados'], color=cores)
    ax.set_xlabel('Número de Instrumentos Não Iniciados')
    ax.set_ylabel('Município')
    ax.set_title(f'Instrumentos Não Iniciados por Município no Estado Selecionado')
    st.pyplot(fig)

# Função para contar o número de instrumentos não iniciados por regional
def contar_nao_iniciados_por_regional(df):
    df_nao_iniciados = df[df['SITUACAO'] == 'Não Iniciado']
    contagem = df_nao_iniciados.groupby('REGIAO').size().reset_index(name='NaoIniciados')
    return contagem

def criar_grafico_por_regional(df):
    contagem_nao_iniciados = contar_nao_iniciados_por_regional(df)
    contagem_nao_iniciados = contagem_nao_iniciados.sort_values(by='NaoIniciados', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(contagem_nao_iniciados['REGIAO'], contagem_nao_iniciados['NaoIniciados'], color='blue')
    ax.set_xlabel('Regional')
    ax.set_ylabel('Número de Instrumentos Não Iniciados')
    ax.set_title('Instrumentos Não Iniciados por Regional')
    st.pyplot(fig)

# Função para carregar o estado de emails de um arquivo JSON
def carregar_estado_emails():
    if os.path.exists("emails_enviados.json"):
        with open("emails_enviados.json", "r") as f:
            return json.load(f)
    return {}

# Função para salvar o estado de emails em um arquivo JSON
def salvar_estado_emails(emails_enviados):
    with open("emails_enviados.json", "w") as f:
        json.dump(emails_enviados, f)

# Função para registrar o envio de emails por município
def registrar_emails_por_municipio(df, emails_enviados):
    for municipio in df['MUNICIPIO'].unique():
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            email_enviado = st.checkbox("", value=emails_enviados.get(municipio, False), key=municipio)
            emails_enviados[municipio] = email_enviado
        with col2:
            st.write(municipio)
        with col3:
            st.write(" ")
    salvar_estado_emails(emails_enviados)

def criar_escala_colorida(nao_iniciados, max_nao_iniciados):
    proporcao = nao_iniciados / max_nao_iniciados
    cor = f'rgb({int(255 * proporcao)}, {int(255 * (1 - proporcao))}, 0)'
    largura = int(proporcao * 100)
    barra = f"<div style='background-color:{cor}; width:{largura}%; height:10px; display:inline-block; border-radius:5px;'></div>"
    return barra


# Função principal do Streamlit

# Função para carregar o estado de envio de emails de um arquivo JSON
def carregar_estado_emails():
    if os.path.exists("emails_enviados.json"):
        with open("emails_enviados.json", "r") as f:
            return json.load(f)
    return {}

# Função para salvar o estado de envio de emails em um arquivo JSON
def salvar_estado_emails(emails_enviados):
    with open("emails_enviados.json", "w") as f:
        json.dump(emails_enviados, f)

# Função para criar uma checkbox para cada município e registrar o envio de email
def registrar_emails_por_municipio(df, emails_enviados):
    st.subheader("Registro de Envio de E-mails por Município")
    for municipio in df['MUNICIPIO'].unique():
        col1, col2 = st.columns([1, 4])
        with col1:
            email_enviado = st.checkbox("", value=emails_enviados.get(municipio, False), key=municipio)
            emails_enviados[municipio] = email_enviado
        with col2:
            st.write(municipio)
    salvar_estado_emails(emails_enviados)

# Função para criar a barra colorida
def criar_escala_colorida(nao_iniciados, max_nao_iniciados):
    proporcao = nao_iniciados / max_nao_iniciados
    cor = f'rgb({int(255 * proporcao)}, {int(255 * (1 - proporcao))}, 0)'
    largura = int(proporcao * 100)
    barra = f"<div style='background-color:{cor}; width:{largura}%; height:10px; display:inline-block;'></div>"
    return barra

# Função principal do Streamlit
# Função principal do Streamlit
def main():
    st.image('Logo.png', width=100)
    st.title('Situação do DigiSUS - Módulo Planejamento')
    st.markdown('*As barras correspondem ao número de instrumentos não alimentados no sistema.*')

    # Carrega o estado de emails enviados
    emails_enviados = carregar_estado_emails()

    if 'page' not in st.session_state:
        st.session_state['page'] = 'Análise por Município'

    st.sidebar.title("Selecione a Página")

    estados = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
    estado_selecionado = st.sidebar.selectbox('Selecione o Estado', estados)
    df = load_data_from_state(estado_selecionado)

    if df.empty:
        st.warning("Nenhum dado encontrado para o estado selecionado.")
        return

    if 'REGIAO' not in df.columns:
        st.error(f"O arquivo do estado {estado_selecionado} não contém a coluna 'REGIAO'.")
        return

    st.sidebar.markdown(
        "<p style='color:white; position:fixed; bottom:0; width:50%; text-align:left;'>"
        "Desenvolvido por <b>Davi Xavier</b></p>",
        unsafe_allow_html=True
    )

    if st.sidebar.button('Análise por Município'):
        st.session_state['page'] = 'Análise por Município'
    if st.sidebar.button('Gráfico por Regional'):
        st.session_state['page'] = 'Gráfico por Regional'
    if st.sidebar.button('Gráfico de Todo o Estado'):
        st.session_state['page'] = 'Gráfico de Todo o Estado'
    if st.sidebar.button('Situação Nacional'):
        st.session_state['page'] = 'Situação Nacional'
    if st.sidebar.button('Relatório de E-mails Enviados'):
        st.session_state['page'] = 'Relatório de E-mails Enviados'
    fases = df['FASE'].dropna().unique()
    fases_selecionadas = st.sidebar.multiselect('Selecione as Fases', fases, default=fases)
    instrumentos = df['TIPO_INSTRUMENTO'].dropna().unique()
    instrumentos_selecionados = st.sidebar.multiselect('Selecione os Tipos de Instrumentos', instrumentos, default=instrumentos)

    df = df[df['FASE'].isin(fases_selecionadas)]
    df = df[df['TIPO_INSTRUMENTO'].isin(instrumentos_selecionados)]

    if st.session_state['page'] == 'Análise por Município':
        criterios = st.sidebar.radio("Critério de Classificação", ('Número de Instrumentos Não Iniciados', 'Nome do Município'))
        regionais_validas = df['REGIAO'].dropna().unique()
        regional = st.sidebar.selectbox('Selecione a Regional', regionais_validas)
        municipios_na_regiao = df[df['REGIAO'] == regional]
        contagem_nao_iniciados = contar_nao_iniciados(municipios_na_regiao)

        if criterios == 'Nome do Município':
            contagem_nao_iniciados = contagem_nao_iniciados.sort_values(by='MUNICIPIO')
        else:
            contagem_nao_iniciados = contagem_nao_iniciados.sort_values(by='NaoIniciados', ascending=False)

        max_nao_iniciados = contagem_nao_iniciados['NaoIniciados'].max()

        st.subheader('Municípios')

        for index, row in contagem_nao_iniciados.iterrows():
            municipio = row['MUNICIPIO']
            nao_iniciados = row['NaoIniciados']
            col1, col2 = st.columns([1, 5])
            with col1:
                email_enviado = st.checkbox("", value=emails_enviados.get(municipio, False), key=municipio)
                emails_enviados[municipio] = email_enviado
                                    
            with col2:
                barra_colorida = criar_escala_colorida(nao_iniciados, max_nao_iniciados)
                st.markdown(barra_colorida, unsafe_allow_html=True)

            if st.button(f'{municipio}', key=f'detalhe_{municipio}'):
                tabela_formatada = gerar_tabela_formatada(df, municipio, regional)
                if not tabela_formatada.empty:
                    styled_df = tabela_formatada.style.map(highlight_cells)
                    st.dataframe(styled_df)
                else:
                    st.warning('Nenhum dado encontrado para o município e regional selecionados.')

        salvar_estado_emails(emails_enviados)

    elif st.session_state['page'] == 'Gráfico por Regional':
        regional = st.sidebar.selectbox('Selecione a Regional para o Gráfico', df['REGIAO'].unique())
        max_nao_iniciados = contar_nao_iniciados(df)['NaoIniciados'].max()
        criar_grafico_completo(df, regional, max_nao_iniciados)

    elif st.session_state['page'] == 'Gráfico de Todo o Estado':
        criar_grafico_por_regional(df)

    elif st.session_state['page'] == 'Situação Nacional':
        st.subheader("Quantidade de Instrumentos Não Iniciados por Estado")
        df_situacao_estado = contar_nao_iniciados_por_estado()
        criar_grafico_situacao_por_estado(df_situacao_estado)

    elif st.session_state['page'] == 'Relatório de E-mails Enviados':
        st.subheader("Relatório de Municípios com E-mails Enviados")
        municipios_com_emails = [municipio for municipio, enviado in emails_enviados.items() if enviado]
        
        if municipios_com_emails:
            df_relatorio = df[df['MUNICIPIO'].isin(municipios_com_emails)]
            regionais = df_relatorio['REGIAO'].unique()
            total_geral = 0
            
            for regional in regionais:
                st.markdown(f"### <span style='color:blue'>Regional: {regional}</span>", unsafe_allow_html=True)
                municipios_na_regiao = df_relatorio[df['REGIAO'] == regional]['MUNICIPIO'].unique()
                st.markdown(f"<span style='color:green'>{', '.join(municipios_na_regiao)}</span>", unsafe_allow_html=True)
                total_na_regiao = len(municipios_na_regiao)
                st.markdown(f"<span style='color:red'>Total de municípios na regional {regional}: {total_na_regiao}</span>", unsafe_allow_html=True)
                total_geral += total_na_regiao
            
            st.markdown(f"## <span style='color:purple'>Total geral de municípios com e-mails enviados: {total_geral}</span>", unsafe_allow_html=True)
        else:
            st.warning("Nenhum email enviado ainda.")




if __name__ == '__main__':
    main()
