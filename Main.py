import pandas as pd
import streamlit as st
from datetime import datetime
from pyUFbr.baseuf import ufbr
from unidecode import unidecode

st.sidebar.image('logo_maisgestor.png')

# Lista de estados com códigos e siglas
estados_codigos = {
    'ACRE': '12', 'ALAGOAS': '27', 'AMAPA': '16', 'AMAZONAS': '13', 'BAHIA': '29', 'CEARA': '23', 
    'DISTRITO FEDERAL': '53', 'ESPIRITO SANTO': '32', 'GOIAS': '52', 'MARANHAO': '21', 'MATO GROSSO': '51', 
    'MATO GROSSO DO SUL': '50', 'MINAS GERAIS': '31', 'PARA': '15', 'PARAIBA': '25', 'PARANA': '41', 
    'PERNAMBUCO': '26', 'PIAUI': '22', 'RIO DE JANEIRO': '33', 'RIO GRANDE DO NORTE': '24', 'RIO GRANDE DO SUL': '43', 
    'RONDONIA': '11', 'RORAIMA': '14', 'SANTA CATARINA': '42', 'SAO PAULO': '35', 'SERGIPE': '28', 'TOCANTINS': '17'
}
estados_siglas = {
    'ACRE': 'AC', 'ALAGOAS': 'AL', 'AMAPA': 'AP', 'AMAZONAS': 'AM', 'BAHIA': 'BA', 'CEARA': 'CE', 
    'DISTRITO FEDERAL': 'DF', 'ESPIRITO SANTO': 'ES', 'GOIAS': 'GO', 'MARANHAO': 'MA', 'MATO GROSSO': 'MT', 
    'MATO GROSSO DO SUL': 'MS', 'MINAS GERAIS': 'MG', 'PARA': 'PA', 'PARAIBA': 'PB', 'PARANA': 'PR', 
    'PERNAMBUCO': 'PE', 'PIAUI': 'PI', 'RIO DE JANEIRO': 'RJ', 'RIO GRANDE DO NORTE': 'RN', 'RIO GRANDE DO SUL': 'RS', 
    'RONDONIA': 'RO', 'RORAIMA': 'RR', 'SANTA CATARINA': 'SC', 'SAO PAULO': 'SP', 'SERGIPE': 'SE', 'TOCANTINS': 'TO'
}

# Dicionário para mapear siglas aos nomes completos
siglas_para_estados = {v: k for k, v in estados_siglas.items()}

# Adicionar seletor de estado
estado_selecionado = st.sidebar.selectbox('Selecione o estado:', list(estados_codigos.keys()))

# Obter o código e a sigla do estado selecionado
codigo_estado = estados_codigos[estado_selecionado]
sigla_estado = estados_siglas[estado_selecionado]
nome_estado = siglas_para_estados[sigla_estado]

# Função para selecionar os municípios com base no código do estado (pyUFbr)
def obter_municipios(codigo_estado):
    municipios = ufbr.list_cidades(codigo=codigo_estado)
    municipios_sem_acentos = [unidecode(municipio) for municipio in municipios]
    return municipios_sem_acentos

# Obter a lista de municípios com base no estado selecionado
municipios = obter_municipios(codigo_estado)
municipio_selecionado = st.sidebar.selectbox('Selecione o município:', municipios)

# Carregar os arquivos CSV em DataFrames
DatasEnvio = pd.read_csv('DatasEnvio.csv', encoding='utf-8-sig')
SIA = pd.read_csv('EnvioSIA.csv', encoding='utf-8-sig')
SIH = pd.read_csv('EnvioSIH.csv', encoding='utf-8-sig')
CNES = pd.read_csv('EnvioCNES.csv', encoding='utf-8-sig')

# Remover uma coluna específica pelo índice do DataFrame DatasEnvio, se presente
if 'Observação' in DatasEnvio.columns:
    DatasEnvio = DatasEnvio.drop(columns=['Observação'])

# Filtrar os dados de SIA, SIH e CNES com base no estado e município selecionado
SIA_filtrado = SIA[(SIA['UF'] == sigla_estado) & (SIA['Nome'].apply(unidecode) == unidecode(municipio_selecionado))]
SIH_filtrado = SIH[(SIH['UF'] == sigla_estado) & (SIH['Nome do Município'].apply(unidecode) == unidecode(municipio_selecionado))]
CNES_filtrado = CNES[(CNES['UF'] == nome_estado) & (CNES['Municipio'].apply(unidecode) == unidecode(municipio_selecionado))]

# Função para analisar os dados de CNES
def analisar_envio_cnes(df_envio, sistema):
    df_datas = DatasEnvio[DatasEnvio['Sistema'] == sistema]
    competencia_atual = df_datas['Competência'].iloc[-1]
    
    competencias_atrasadas = []
    
    # Verificar se as competências enviadas estão em dia
    for competencia in df_envio['Competência'].unique():
        if competencia != '/' and competencia != competencia_atual:
            competencias_atrasadas.append(competencia)

    if competencias_atrasadas:
        competencias_atrasadas_str = ', '.join(competencias_atrasadas)
        return f":x: Competências em atraso para {sistema}: **{competencias_atrasadas_str}**."
    else:
        return f":white_check_mark: Todas as competências para {sistema} estão em dia."

# Função para comparar os envios com as datas de envio para SIA e SIH
def comparar_envio_com_datasenvio(df_envio, sistema, nome_coluna):
    df_datas = DatasEnvio[DatasEnvio['Sistema'] == sistema]
    competencia_atual = df_datas['Competência'].iloc[-1]
    
    competencias_atrasadas = []
    total_envios = df_envio[df_envio.columns[-2]].sum()
    total_competencias = len(df_envio)

    for coluna in df_envio.columns:
        if coluna != competencia_atual and coluna not in ['Nome', 'Nome do Município', 'Municipio', 'UF', 'Soma', 'Percentual de Envio']:
            if df_envio[coluna].eq(0).any():
                competencias_atrasadas.append(coluna)

    percentual_envio = df_envio['Percentual de Envio'].mean() if total_competencias > 0 else 0

    if competencias_atrasadas:
        competencias_atrasadas_str = ', '.join(competencias_atrasadas)
        return f":x: Competências em atraso para {sistema}: **{competencias_atrasadas_str}**. {total_envios} competências enviadas. **{percentual_envio:.2f}%** de envio realizado."
    else:
        return f":white_check_mark: Todas as competências enviadas para {sistema} estão em dia. {total_envios} competências enviadas. **{percentual_envio:.2f}%** de envio realizado."

# Obter a data atual do sistema (apenas data, sem tempo)
data_atual = datetime.now().date()

# Função para verificar se a competência está no intervalo
def verificar_competencia_aberta(data_inicial, data_final):
    return data_inicial.date() <= data_atual <= data_final.date()

# Aplicar verificação e destacar linhas
DatasEnvio['Competência Aberta'] = DatasEnvio.apply(
    lambda row: 'Sim' if verificar_competencia_aberta(pd.to_datetime(row['Data Início'], dayfirst=True), pd.to_datetime(row['Data Fim'], dayfirst=True)) else 'Não',
    axis=1
)

# Atualizar o DataFrame com a formatação e a mensagem
def formatar_linhas(row):
    if row['Competência Aberta'] == 'Sim':
        return ['color: limegreen'] * len(row)
    else:
        return ['color: red'] * len(row)

# Adicionar barra lateral
st.sidebar.title('Opções de Visualização')
visualizacao = st.sidebar.radio('Escolha o tipo de visualização:', ('Resumida', 'Detalhada'), index=0)

# Mostrar DataFrame de Datas de Envio com destaque para as competências abertas apenas na visualização detalhada
if visualizacao == 'Detalhada':
    st.subheader(':calendar: **Datas do Transmissor**')
    
    # Aplicar verificação e destacar linhas
    st.dataframe(DatasEnvio.style.apply(
        lambda x: ['color: green' if x['Competência Aberta'] == 'Sim' else 'color: red' for _ in range(len(DatasEnvio.columns))],
        axis=1
    ), use_container_width=True)

    st.divider()

    # Exibir envio SIA com formatação e mensagem
    st.subheader(':clipboard: **Envio SIA**')
    mensagem_sia = comparar_envio_com_datasenvio(SIA_filtrado, 'SIASUS', 'Nome')
    st.markdown(mensagem_sia)
    st.dataframe(SIA_filtrado, use_container_width=True)
    st.divider()

    # Exibir envio SIH com formatação e mensagem
    st.subheader(':clipboard: **Envio SIH**')
    mensagem_sih = comparar_envio_com_datasenvio(SIH_filtrado, 'SIHD', 'Nome do Município')
    st.markdown(mensagem_sih)
    st.dataframe(SIH_filtrado, use_container_width=True)
    st.divider()

    # Exibir envio CNES com formatação e mensagem (usando análise separada)
    st.subheader(':clipboard: **Envio CNES**')
    mensagem_cnes = analisar_envio_cnes(CNES_filtrado, 'CNES')
    st.markdown(mensagem_cnes)
    st.dataframe(CNES_filtrado, use_container_width=True)

else:
    st.header(':blue[**Atenção Especializada**] :green[Envio dos Sistemas]')
    st.write("### Visualização Resumida")
    
    # Colocar mensagem de competência aberta
    if any(DatasEnvio['Competência Aberta'] == 'Sim'):
        sistemas_abertos = DatasEnvio[DatasEnvio['Competência Aberta'] == 'Sim'][['Sistema', 'Competência']]
        mensagem_sistemas = ', '.join([f"{row['Sistema']} {row['Competência']}" for _, row in sistemas_abertos.iterrows()])
        st.success(f'Há competências abertas no momento para os sistemas: {mensagem_sistemas}')
    
    # Adicionar os status dos sistemas na visualização resumida
    mensagem_sia = comparar_envio_com_datasenvio(SIA_filtrado, 'SIASUS', 'Nome')
    st.markdown(mensagem_sia)
    
    mensagem_sih = comparar_envio_com_datasenvio(SIH_filtrado, 'SIHD', 'Nome do Município')
    st.markdown(mensagem_sih)
    
    mensagem_cnes = analisar_envio_cnes(CNES_filtrado, 'CNES')
    st.markdown(mensagem_cnes)
