#=============================================== PARTE 1 ===============================================

import streamlit as st
import requests
import json
import pandas as pd
from pyUFbr.baseuf import ufbr
from requests.exceptions import RequestException

# Nome do arquivo JSON para armazenar os dados
DATA_FILE = "data.json"

def style_metric_cards(
    background_color: str = "#f5f5f5",
    border_size_px: int = 1,
    border_color: str = "#f39c12",
    border_radius_px: int = 5,
    border_left_color: str = "#003366",
    box_shadow: bool = True,
) -> None:
    """Define o estilo dos cartões de métricas."""
    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58,59,69,.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container{{
                padding-top: 1rem;
            }}
            .card {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                border-radius: {border_radius_px}px;
                padding: 5px;
                text-align: center;
                margin-bottom: 5px;
                {box_shadow_str}
            }}
            .card-title {{
                font-size: 0.7rem;
                font-weight: bold;
                margin-bottom: 0.2rem;
                color: #2c3e50;
            }}
            .card-value {{
                font-size: 1.5rem;
                color: {border_left_color};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def metric_card(label: str, value: str | int | float) -> None:
    """Cria um cartão estilizado para exibir uma métrica."""
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">{label}</div>
            <div class="card-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def consultar_api(codigo_ibge: str, competencia: str) -> dict | None:
    """Consulta a API de financiamento da saúde e salva os dados em um arquivo JSON com indentação."""

    st.session_state['competencia'] = competencia

    url = "https://relatorioaps-prd.saude.gov.br/financiamento/pagamento"
    params = {
        "unidadeGeografica": "MUNICIPIO",
        "coUf": codigo_ibge[:2],
        "coMunicipio": codigo_ibge[:6],
        "nuParcelaInicio": competencia,
        "nuParcelaFim": competencia,
        "tipoRelatorio": "COMPLETO"
    }

    try:
        # Remover verify=False e tratar o erro de certificado se ocorrer
        response = requests.get(url, params=params, headers={"Accept": "application/json"}, verify=False)
        response.raise_for_status()
        dados = response.json()

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

        return dados
    except RequestException as e:
        st.error(f"Erro na consulta à API: {e}")
        # Aqui você pode adicionar um tratamento mais específico, como:
        # if isinstance(e, requests.exceptions.SSLError):
        #     st.error("Erro de certificado SSL. Verifique a configuração do servidor.")
        return None

def main():
    st.set_page_config(page_title="Financiamento da Atenção Primária")

    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.image('logo_colorida_mg.png', width=200)

    st.title("Calculadora PAP")
    style_metric_cards()

    with st.expander("🔍 Parâmetros de Consulta", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            estados = ufbr.list_uf
            uf_selecionada = st.selectbox("Selecione um Estado", options=estados)
        with col2:
            competencia = st.text_input("Competência (AAAAMM)", st.session_state.get('competencia', "202501"))

        if uf_selecionada:
            municipios = ufbr.list_cidades(uf_selecionada)
            municipio_selecionado = st.selectbox("Selecione um Município", options=municipios)

            if municipio_selecionado:
                try:
                    codigo_ibge = str(int(float(ufbr.get_cidade(municipio_selecionado).codigo)))[:-1]
                except AttributeError:
                    st.error("Erro ao obter código IBGE do município")
                    return

    if st.button("Consultar"):
        if not (uf_selecionada and municipio_selecionado and competencia):
            st.error("Por favor, preencha todos os campos de consulta.")
            return

        dados = consultar_api(codigo_ibge, competencia)
        st.session_state['dados'] = dados

    if 'dados' in st.session_state:
        dados = st.session_state['dados']
        st.subheader("Informações Gerais")
        dados_pagamentos = dados.get("pagamentos", [])
        if dados_pagamentos:
            df = pd.DataFrame(dados_pagamentos)
            populacao = df['qtPopulacao'].iloc[0] if 'qtPopulacao' in df.columns else 0
            ano_referencia = df['nuAnoRefPopulacaoIbge'].iloc[0] if 'nuAnoRefPopulacaoIbge' in df.columns else 0
            ied = df['dsFaixaIndiceEquidadeEsfEap'].iloc[0] if 'dsFaixaIndiceEquidadeEsfEap' in df.columns else "Não informado"

            st.session_state['ied'] = ied
            st.session_state['populacao'] = populacao

            cols_info = st.columns(3)
            with cols_info[0]:
                metric_card("População IBGE", f"{populacao:,}".replace(",", "."))
            with cols_info[1]:
                metric_card("Ano Referência Populacional", ano_referencia)
            with cols_info[2]:
                metric_card("Índice de Equidade", ied)

        else:
            st.error("Nenhum dado encontrado para os parâmetros informados.")

if __name__ == "__main__":
    main()

#=============================================== PARTE 2 ===============================================

# Carrega a configuração do config.json
with open("config.json", "r", encoding="utf-8") as f:
    config_data = json.load(f)

# Carrega os dados da API do data.json (atualizado pela parte1.py)
with open("data.json", "r", encoding="utf-8") as f:
    api_data = json.load(f)

# Mantenha os dados de config.json separados
data = config_data["data"]
updated_categories = config_data["updated_categories"]
subcategories = config_data["subcategories"]
quality_values = config_data["quality_values"]
fixed_component_values = config_data["fixed_component_values"]
service_to_plan = config_data["service_to_plan"] # Carregando service_to_plan

# CSS para estilizar os campos (pode ser movido para um arquivo .css separado)
CSS = """
<style>
div[data-testid="stVerticalBlock"] > div:first-child {
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 5px;
}

div[data-testid="stVerticalBlock"] > div:nth-child(2) {
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    margin-bottom: 5px;
}

div[data-testid="stVerticalBlock"] > div:last-child {
    padding: 10px;
    border-radius: 5px;
    text-align: right;
    margin-bottom: 5px;
}

.result-value {
    font-weight: bold;
}
</style>
"""

def format_currency(value: float | str) -> str:
    """Formata um número como moeda brasileira."""
    if value == 'Sem cálculo':
        return value
    if isinstance(value, str):
        value = float(value.replace('R$ ', '').replace('.', '').replace(',', '.'))
    return "R$ {:,.2f}".format(value).replace(",", "v").replace(".", ",").replace("v", ".")

def get_estrato(populacao: int) -> str:
    """Retorna o estrato com base na população."""
    if populacao <= 20000:
        return "1"
    elif populacao <= 50000:
        return "2"
    elif populacao <= 100000:
        return "3"
    else:
        return "4"

# Aplicar CSS
st.markdown(CSS, unsafe_allow_html=True)

#=============================================== PARTE 3 ===============================================

# Carregando dados do config.json e data.json
with open("config.json", "r", encoding="utf-8") as f:
    config_data = json.load(f)

with open("data.json", "r", encoding="utf-8") as f:
    api_data = json.load(f)

data = config_data["data"]
updated_categories = config_data["updated_categories"]
subcategories = config_data["subcategories"]
quality_values = config_data["quality_values"]
fixed_component_values = config_data["fixed_component_values"]
service_to_plan = config_data["service_to_plan"]
implantacao_values = config_data["implantacao_values"]

selected_services: dict[str, int] = {}
edited_values: dict[str, float] = {}  # Dicionário para armazenar valores editados
# Dicionário para armazenar valores de implantação editados
edited_implantacao_values: dict[str, float] = {}
# Dicionário para armazenar quantidades de implantação editadas
edited_implantacao_quantity: dict[str, int] = {}

# Use st.expander for each category and create unique keys
for category, services in updated_categories.items():
    with st.expander(category):
        if category == 'Saúde Bucal':
            for subcategory, sub_services in subcategories.items():
                st.markdown(f"##### {subcategory}")
                for service in sub_services:

                    # --- Campos normais ---
                    unique_key = f"{category}_{subcategory}_{service}"
                    unique_key_value = f"{category}_{subcategory}_{service}_value"
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        quantity = st.number_input(f'{service} (Quantidade)', min_value=0, value=0, key=unique_key)
                        selected_services[service] = quantity

                    with col2:
                        # Buscar valor do data.json (resumosPlanosOrcamentarios)
                        initial_value = "R$ 0,00"

                        # *** Buscar valor do config.json ***
                        if service in data and data[service]['valor'] != 'Sem cálculo':
                            initial_value = data[service]['valor']
                        # *** Fim da modificação ***

                        value = st.text_input(f"Valor {service}", value=initial_value, key=unique_key_value)
                        # Armazenar valor editado, se houver
                        if value != initial_value:
                            try:
                                edited_values[service] = float(
                                    value.replace('R$ ', '').replace('.', '').replace(',', '.'))
                            except ValueError:
                                st.error(f"Valor inválido para {service}. Insira um número válido.")
                                edited_values[service] = 0.0
                        else:
                            if service in edited_values:
                                del edited_values[service]

                    with col3:
                        if value != 'Sem cálculo':
                            try:
                                total_value = float(
                                    value.replace('R$ ', '').replace('.', '').replace(',', '.')) * quantity
                            except ValueError:
                                total_value = 0
                        else:
                            total_value = 0
                        st.text_input(f"Subtotal {service}", value=format_currency(total_value), key=f"{unique_key}_total",
                                      disabled=True)

        else:
            for service in services:
                # --- Campos normais ---
                unique_key = f"{category}_{service}"
                unique_key_value = f"{category}_{service}_value"
                col1, col2, col3 = st.columns(3)

                with col1:
                    quantity = st.number_input(f'{service} (Quantidade)', min_value=0, value=0, key=unique_key)
                    selected_services[service] = quantity

                with col2:
                    # Buscar valor do data.json (resumosPlanosOrcamentarios) ou do fixed_component_values se for eSF, eAP 30h ou eAP 20h
                    initial_value = "R$ 0,00"
                    if service in ["eSF", "eAP 30h", "eAP 20h"]:
                        populacao = st.session_state.get('populacao', 0)
                        estrato = get_estrato(populacao)
                        if estrato in fixed_component_values:
                            initial_value = fixed_component_values[estrato][service]
                    else:
                        # *** Buscar valor do config.json ***
                        if service in data and data[service]['valor'] != 'Sem cálculo':
                            initial_value = data[service]['valor']
                        # *** Fim da modificação ***

                    value = st.text_input(f"Valor {service}", value=initial_value, key=unique_key_value)
                    # Armazenar valor editado, se houver
                    if value != initial_value:
                        try:
                            edited_values[service] = float(
                                value.replace('R$ ', '').replace('.', '').replace(',', '.'))
                        except ValueError:
                            st.error(f"Valor inválido para {service}. Insira um número válido.")
                            edited_values[service] = 0.0
                    else:
                        if service in edited_values:
                            del edited_values[service]

                with col3:
                    if value != 'Sem cálculo':
                        try:
                            total_value = float(
                                value.replace('R$ ', '').replace('.', '').replace(',', '.')) * quantity
                        except ValueError:
                            total_value = 0
                    else:
                        total_value = 0
                    st.text_input(f"Subtotal {service}", value=format_currency(total_value), key=f"{unique_key}_total",
                                  disabled=True)

                # --- Campos de implantação (eSF, eAP e eMulti) ---

                if service in ["eSF", "eAP 30h", "eAP 20h", "eMULTI Ampl.", "eMULTI Compl.", "eMULTI Estrat."]:
                    if 'implantacao_campos' not in st.session_state:
                        st.session_state['implantacao_campos'] = {}
                    if category not in st.session_state['implantacao_campos']:
                        # Agora é um dicionário para armazenar as chaves únicas
                        st.session_state['implantacao_campos'][category] = {}

                    # Chaves únicas para os campos de implantação, verificando duplicidade da categoria
                    if category in service:
                        key_q = f"{service}_implantacao_q_quantidade"
                        key_v = f"{service}_implantacao_valor"
                        key_s = f"{service}_implantacao_subtotal"
                    else:
                        key_q = f"{category}_{service}_implantacao_q_quantidade"
                        key_v = f"{category}_{service}_implantacao_valor"
                        key_s = f"{category}_{service}_implantacao_subtotal"

                    # Armazenar as chaves no dicionário
                    st.session_state['implantacao_campos'][category][key_q] = ''
                    st.session_state['implantacao_campos'][category][key_v] = ''
                    st.session_state['implantacao_campos'][category][key_s] = ''

        # Divisor e campos de implantação após os campos normais
        # A lógica agora só é executada se a categoria tiver campos de implantação
        if 'implantacao_campos' in st.session_state and category in st.session_state['implantacao_campos']:
            st.divider()
            st.markdown(f"###### Implantação")

            for key_q in list(st.session_state['implantacao_campos'][category].keys()):
                if key_q.endswith('_quantidade'):
                    service = key_q.split('_')[1] # Obter o nome do serviço a partir da chave
                    key_v = key_q.replace('_q_quantidade', '_valor')
                    key_s = key_q.replace('_q_quantidade', '_subtotal')

                    # --- Campos de implantação (eSF, eAP e eMulti) ---
                    col1_imp, col2_imp, col3_imp = st.columns(3)

                    with col1_imp:
                        # Quantidade de implantação
                        quantity_implantacao = st.number_input(f'{service} (Quantidade)', min_value=0, value=0,
                                                              key=key_q)
                        edited_implantacao_quantity[service] = quantity_implantacao

                    with col2_imp:
                        # Valor de implantação
                        # *** Buscar valor do implantacao_values, tratando eMulti ***
                        initial_implantacao_value = "R$ 0,00"
                        if service in implantacao_values:
                            initial_implantacao_value = implantacao_values[service]
                        elif service == "eMULTI Ampl.":
                            initial_implantacao_value = implantacao_values["eMulti Ampliada"]
                        elif service == "eMULTI Compl.":
                            initial_implantacao_value = implantacao_values["eMulti Complementar"]
                        elif service == "eMULTI Estrat.":
                            initial_implantacao_value = implantacao_values["eMulti Estratégica"]
                        # *** Fim da modificação ***

                        implantacao_value = st.text_input(f"Valor", value=initial_implantacao_value,
                                                          key=key_v)
                        # Armazenar valor de implantação editado, se houver
                        if implantacao_value != initial_implantacao_value:
                            try:
                                edited_implantacao_values[service] = float(
                                    implantacao_value.replace('R$ ', '').replace('.', '').replace(',', '.'))
                            except ValueError:
                                st.error(
                                    f"Valor de implantação inválido para {service}. Insira um número válido.")
                                edited_implantacao_values[service] = 0.0
                        else:
                            if service in edited_implantacao_values:
                                del edited_implantacao_values[service]

                    with col3_imp:
                        if implantacao_value != 'Sem cálculo':
                            try:
                                total_implantacao = float(
                                    implantacao_value.replace('R$ ', '').replace('.', '').replace(',',
                                                                                                '.')) * quantity_implantacao
                            except ValueError:
                                total_implantacao = 0
                        else:
                            total_implantacao = 0
                        st.text_input(f"Subtotal", value=format_currency(total_implantacao),
                                      key=key_s, disabled=True)

# Nova linha para os dropdowns e botão
col_classificacao, col_vinculo = st.columns([1, 1])

with col_classificacao:
    Classificacao = st.selectbox("Considerar Qualidade", options=['Regular', 'Suficiente', 'Bom', 'Ótimo'], index=2)

with col_vinculo:
    Vinculo = st.selectbox("Vínculo e Acompanhamento Territorial", options=['Regular', 'Suficiente', 'Bom', 'Ótimo'], index=2)

calcular_button = st.button('Calcular', use_container_width=True)

#=============================================== PARTE 4 ===============================================


# Carregando dados do config.json e data.json
with open("config.json", "r", encoding="utf-8") as f:
    config_data = json.load(f)

with open("data.json", "r", encoding="utf-8") as f:
    api_data = json.load(f)

data = config_data["data"]
updated_categories = config_data["updated_categories"]
subcategories = config_data["subcategories"]
quality_values = config_data["quality_values"]
fixed_component_values = config_data["fixed_component_values"]
service_to_plan = config_data["service_to_plan"]
implantacao_values = config_data["implantacao_values"]

if calcular_button:  # Usa a variável calcular_button da Parte 3
    if all(q == 0 for q in selected_services.values()):
        st.error("Por favor, selecione pelo menos um serviço para calcular.")
    else:
        st.header("Valores do Novo Cofinanciamento")

        # COMPONENTE 01 - COMPONENTE FIXO
        st.subheader("Componente I - Componente Fixo")
        fixed_table: list[list[str | int | float]] = []

        # Construindo a tabela do componente fixo
        for service in ["eSF", "eAP 30h", "eAP 20h"]:
            quantity = selected_services.get(service, 0)
            if quantity > 0:
                # Buscar valor editado, senão buscar no fixed_component_values com base no estrato
                if service in edited_values:
                    valor = edited_values[service]
                else:
                    populacao = st.session_state.get('populacao', 0)
                    estrato = get_estrato(populacao)
                    if estrato in fixed_component_values:
                        valor = float(fixed_component_values[estrato][service].replace('R$ ', '').replace('.', '').replace(',', '.'))
                    else:
                        valor = 0

                total_value = valor * quantity
                fixed_table.append([service, format_currency(valor), quantity, format_currency(total_value)])

        # Adicionar linhas para implantação de eSF, eAP, eMulti (agrupadas após os serviços)
        for service in ["eSF", "eAP 30h", "eAP 20h", "eMULTI Ampl.", "eMULTI Compl.", "eMULTI Estrat."]:
            if selected_services.get(service, 0) > 0:
                if service in edited_implantacao_values:
                    valor_implantacao = edited_implantacao_values[service]
                else:
                    if service in implantacao_values:
                        valor_implantacao = float(implantacao_values.get(service, "R$ 0,00").replace('R$ ', '').replace('.', '').replace(',', '.'))
                    elif service == "eMULTI Ampl.":
                        valor_implantacao = float(implantacao_values.get("eMulti Ampliada", "R$ 0,00").replace('R$ ', '').replace('.', '').replace(',', '.'))
                    elif service == "eMULTI Compl.":
                        valor_implantacao = float(implantacao_values.get("eMulti Complementar", "R$ 0,00").replace('R$ ', '').replace('.', '').replace(',', '.'))
                    elif service == "eMULTI Estrat.":
                        valor_implantacao = float(implantacao_values.get("eMulti Estratégica", "R$ 0,00").replace('R$ ', '').replace('.', '').replace(',', '.'))
                    else:
                        valor_implantacao = 0

                if service in edited_implantacao_quantity:
                    quantity_implantacao = edited_implantacao_quantity[service]
                else:
                    quantity_implantacao = 0

                total_implantacao = valor_implantacao * quantity_implantacao
                fixed_table.append([f"{service} (Implantação)", format_currency(valor_implantacao), quantity_implantacao, format_currency(total_implantacao)])

        fixed_df = pd.DataFrame(fixed_table, columns=['Serviço', 'Valor Unitário', 'Quantidade', 'Valor Total'])

        # Adicionar linha de total à tabela do componente fixo
        total_fixed_value = sum(
            float(str(val).replace('R$ ', '').replace('.', '').replace(',', '.'))
            for val in fixed_df['Valor Total']
        )
        total_fixed_row = pd.DataFrame({
            'Serviço': ['Total'],
            'Valor Unitário': [''],
            'Quantidade': [''],
            'Valor Total': [format_currency(total_fixed_value)]
        })
        fixed_df = pd.concat([fixed_df, total_fixed_row], ignore_index=True)

        st.table(fixed_df)

        # COMPONENTE 02 - VÍNCULO E ACOMPANHAMENTO TERRITORIAL.
        st.subheader("Componente II - Vínculo e Acompanhamento Territorial")
        vinculo_table: list[list[str | int | float]] = []

        # Valores do componente de vínculo e acompanhamento
        vinculo_values: dict[str, dict[str, float]] = {
            'eSF': {'Ótimo': 8000, 'Bom': 6000, 'Suficiente': 4000, 'Regular': 2000},
            'eAP 30h': {'Ótimo': 4000, 'Bom': 3000, 'Suficiente': 2000, 'Regular': 1000},
            'eAP 20h': {'Ótimo': 3000, 'Bom': 2250, 'Suficiente': 1500, 'Regular': 750},
        }

        # Construindo a tabela de vínculo e acompanhamento
        for service, quality_levels in vinculo_values.items():
            if Vinculo in quality_levels:
                quantity = selected_services.get(service, 0)
                if quantity > 0:
                    if service in edited_values:
                        value = edited_values[service]
                    else:
                        value = quality_levels[Vinculo]
                    total_value = value * quantity
                    vinculo_table.append([service, Vinculo, format_currency(value), quantity, format_currency(total_value)])

        vinculo_df = pd.DataFrame(vinculo_table, columns=['Serviço', 'Qualidade', 'Valor Unitário', 'Quantidade', 'Valor Total'])

        # Adicionar linha de total à tabela de vínculo e acompanhamento
        total_vinculo_value = sum(
            float(str(val).replace('R$ ', '').replace('.', '').replace(',', '.'))
            for val in vinculo_df['Valor Total']
        )
        total_vinculo_row = pd.DataFrame({
            'Serviço': ['Total'],
            'Qualidade': [''],
            'Valor Unitário': [''],
            'Quantidade': [''],
            'Valor Total': [format_currency(total_vinculo_value)]
        })
        vinculo_df = pd.concat([vinculo_df, total_vinculo_row], ignore_index=True)

        st.table(vinculo_df)

        # COMPONENTE 03 - QUALIDADE
        st.subheader("Componente III - Qualidade")
        quality_table: list[list[str | int | float]] = []

        # Construindo a tabela de qualidade
        for service, quality_levels in quality_values.items():
            if Classificacao in quality_levels:
                quantity = selected_services.get(service, 0)
                if quantity > 0:
                    if service in edited_values:
                        value = edited_values[service]
                    else:
                        value = quality_levels[Classificacao]
                    total_value = value * quantity
                    quality_table.append([service, Classificacao, format_currency(value), quantity, format_currency(total_value)])

        quality_df = pd.DataFrame(quality_table, columns=['Serviço', 'Qualidade', 'Valor Unitário', 'Quantidade', 'Valor Total'])

        total_quality_value = sum(
            float(str(val).replace('R$ ', '').replace('.', '').replace(',', '.'))
            for val in quality_df['Valor Total']
        )
        total_quality_row = pd.DataFrame({
            'Serviço': ['Total'],
            'Qualidade': [''],
            'Valor Unitário': [''],
            'Quantidade': [''],
            'Valor Total': [format_currency(total_quality_value)]
        })
        quality_df = pd.concat([quality_df, total_quality_row], ignore_index=True)

        st.table(quality_df)

        # IV - COMPONENTE PARA IMPLANTAÇÃO E MANUTENÇÃO DE PROGRAMAS, SERVIÇOS, PROFISSIONAIS E OUTRAS COMPOSIÇÕES DE EQUIPES QUE ATUAM NA APS
        st.subheader("IV - Componente para ações e programas da APS.")
        implantacao_manutencao_table: list[list[str | int | float]] = []

        # Todos os serviços que não estão em quality_values, têm valor em data e *não* são da Saúde Bucal
        implantacao_manutencao_services = [
            service for service in data
            if service not in quality_values
            and data[service]['valor'] != 'Sem cálculo'
            and service not in updated_categories.get('Saúde Bucal', []) # Removendo serviços da Saúde Bucal
        ]

        for service in implantacao_manutencao_services:
            quantity = selected_services.get(service, 0)
            if quantity > 0:
                # Buscar valor editado, senão buscar valor unitário de config.json
                if service in edited_values:
                    valor = edited_values[service]
                else:
                    try:
                        valor = float(data[service]['valor'].replace('R$ ', '').replace('.', '').replace(',', '.'))
                    except ValueError:
                        st.error(f"Valor inválido para {service} no config.json.")
                        valor = 0

                total = valor * quantity
                implantacao_manutencao_table.append([service, quantity, format_currency(valor), format_currency(total)])

        implantacao_manutencao_df = pd.DataFrame(implantacao_manutencao_table, columns=['Serviço', 'Quantidade', 'Valor Unitário', 'Valor Total'])

        total_implantacao_manutencao_value = sum(
            float(str(val).replace('R$ ', '').replace('.', '').replace(',', '.'))
            for val in implantacao_manutencao_df['Valor Total']
        )
        total_implantacao_manutencao_row = pd.DataFrame({
            'Serviço': ['Subtotal'],
            'Quantidade': [''],
            'Valor Unitário': [''],
            'Valor Total': [format_currency(total_implantacao_manutencao_value)]
        })
        implantacao_manutencao_df = pd.concat([implantacao_manutencao_df, total_implantacao_manutencao_row], ignore_index=True)

        st.table(implantacao_manutencao_df)

        # V - COMPONENTE PARA ATENÇÃO À SAÚDE BUCAL
        st.subheader("V - Componente para Atenção à Saúde Bucal")
        saude_bucal_table: list[list[str | int | float]] = []

        # Adiciona as linhas de serviços da Saúde Bucal
        saude_bucal_services = updated_categories.get('Saúde Bucal', [])

        for service in saude_bucal_services:
            quantity = selected_services.get(service, 0)
            if quantity > 0:
                # Buscar valor editado, senão buscar valor unitário de quality_values ou config.json
                if service in edited_values:
                    valor = edited_values[service]
                elif service in quality_values:
                    valor = float(quality_values[service][Classificacao])
                else:
                    try:
                        valor = float(data[service]['valor'].replace('R$ ', '').replace('.', '').replace(',', '.'))
                    except:
                        valor = 0

                total = valor * quantity
                saude_bucal_table.append([service, quantity, format_currency(valor), format_currency(total)])

        saude_bucal_df = pd.DataFrame(saude_bucal_table, columns=['Serviço', 'Quantidade', 'Valor Unitário', 'Valor Total'])

        total_saude_bucal_value = sum(
            float(str(val).replace('R$ ', '').replace('.', '').replace(',', '.'))
            for val in saude_bucal_df['Valor Total'].tolist()
        )

        total_saude_bucal_row = pd.DataFrame({
            'Serviço': ['Subtotal'],
            'Quantidade': [''],
            'Valor Unitário': [''],
            'Valor Total': [format_currency(total_saude_bucal_value)]
        })
        saude_bucal_df = pd.concat([saude_bucal_df, total_saude_bucal_row], ignore_index=True)

        st.table(saude_bucal_df)

        # COMPONENTE PER CAPITA (CÁLCULO SIMPLIFICADO)
        st.subheader("VI - Componente Per Capita (Cálculo Simplificado)")
        populacao = st.session_state.get('populacao', 0)
        valor_per_capita = 5.95
        total_per_capita = (valor_per_capita * populacao) / 12

        per_capita_df = pd.DataFrame({
            'Descrição': ['Valor per capita', 'População', 'Total Per Capita (Mensal)'],
            'Valor': [format_currency(valor_per_capita), populacao, format_currency(total_per_capita)]
        })
        st.table(per_capita_df)

        # CÁLCULO DO TOTAL GERAL
        total_geral = total_fixed_value + total_vinculo_value + total_quality_value + total_implantacao_manutencao_value + total_saude_bucal_value + total_per_capita

        # EXIBIÇÃO DO TOTAL GERAL
        st.subheader("Total Geral")
        total_geral_df = pd.DataFrame({
            'Descrição': ['Total Geral'],
            'Valor': [format_currency(total_geral)]
        })
        st.table(total_geral_df)

        # Destaque para o valor total geral
        st.markdown(f"<h3 style='text-align: center; color: blue;'>Total Geral: {format_currency(total_geral)}</h3>", unsafe_allow_html=True)

def main():
    pass
