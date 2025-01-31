import streamlit as st
import requests
import json
import pandas as pd
from pyUFbr.baseuf import ufbr

# Nome do arquivo JSON para armazenar os dados
DATA_FILE = "data.json"

def style_metric_cards(
    background_color: str = "#f5f5f5",
    border_size_px: int = 1,
    border_color: str = "#f39c12",
    border_radius_px: int = 5,
    border_left_color: str = "#003366",
    box_shadow: bool = True,
):
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

def metric_card(label, value):
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

def consultar_api(codigo_ibge, competencia):
    """Consulta a API de financiamento da saúde e salva os dados em um arquivo JSON com indentação."""
    
    # Mantém a competência no session_state
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
        response = requests.get(url, params=params, headers={"Accept": "application/json"}, verify=False)
        response.raise_for_status()
        dados = response.json()

        # Salva os dados em um arquivo JSON com indentação para melhor legibilidade
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

        return dados
    except requests.exceptions.RequestException as e:
        st.error(f"Erro na consulta à API: {e}")
        return None

def main():
    st.set_page_config(page_title="Financiamento da Saúde")
    
    # Centraliza a logo
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.image('logo_colorida_mg.png', width=200)
        
    st.title("🏥 Sistema de Monitoramento de Financiamento da Saúde")
    style_metric_cards()

    with st.expander("🔍 Parâmetros de Consulta", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            estados = ufbr.list_uf
            uf_selecionada = st.selectbox("Selecione um Estado", options=estados)
        with col2:
            # Usa o valor do session_state se existir, senão usa "202501" como padrão
            competencia = st.text_input("Competência (AAAAMM)", st.session_state.get('competencia', "202501"))

        if uf_selecionada:
            municipios = ufbr.list_cidades(uf_selecionada)
            municipio_selecionado = st.selectbox("Selecione um Município", options=municipios)

            if municipio_selecionado:
                try:
                    codigo_ibge = ufbr.get_cidade(municipio_selecionado).codigo
                    codigo_ibge = str(int(float(codigo_ibge)))[:-1]
                except AttributeError:
                    st.error("Erro ao obter código IBGE do município")
                    return

    if st.button("Consultar"):
        if not (uf_selecionada and municipio_selecionado and competencia):
            st.error("Por favor, preencha todos os campos de consulta.")
            return

        dados = consultar_api(codigo_ibge, competencia)
        
        # Armazena os dados no session_state
        st.session_state['dados'] = dados

    # Exibe os cards se os dados estiverem no session_state
    if 'dados' in st.session_state:
        dados = st.session_state['dados']
        # Cabeçalho
        st.subheader("Informações Gerais")
        dados_pagamentos = dados.get("pagamentos", [])
        if dados_pagamentos:
            df = pd.DataFrame(dados_pagamentos)
            populacao = df['qtPopulacao'].iloc[0] if 'qtPopulacao' in df.columns else 0
            ano_referencia = df['nuAnoRefPopulacaoIbge'].iloc[0] if 'nuAnoRefPopulacaoIbge' in df.columns else 0
            ied = df['dsFaixaIndiceEquidadeEsfEap'].iloc[0] if 'dsFaixaIndiceEquidadeEsfEap' in df.columns else "Não informado"
            
            # Armazena população e IED no session_state
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
    
import pandas as pd

# Data from the OCR text, pre-processed into a dictionary for easier use
data = {
    'eSF': {'quantidade': 1, 'valor': 'R$ 16.000,00'},
    'eAP 30h': {'quantidade': 1, 'valor': 'R$ 9.600,00'},
    'eAP 20h': {'quantidade': 1, 'valor': 'R$ 6.400,00'},
    'eMULTI Ampl.': {'quantidade': 1, 'valor': 'R$ 36.000,00'},
    'eMULTI Compl.': {'quantidade': 1, 'valor': 'R$ 24.000,00'},
    'eMULTI Estrat.': {'quantidade': 1, 'valor': 'R$ 12.000,00'},
    'eSB Comum I': {'quantidade': 1, 'valor': 'R$ 4.014,00'},
    'eSB Comum II': {'quantidade': 1, 'valor': 'R$ 7.064,00'},
    'eSB Quil. Assent. I': {'quantidade': 1, 'valor': 'R$ 6.021,00'},
    'eSB Quil. Assent. II': {'quantidade': 1, 'valor': 'R$ 10.596,00'},
    'eSB 20h': {'quantidade': 1, 'valor': 'R$ 2.007,00'},
    'eSB 30h': {'quantidade': 1, 'valor': 'R$ 3.010,00'},
    'LRPD': {'quantidade': 1, 'valor': 'R$ 11.250,00'},
    'CEO I': {'quantidade': 1, 'valor': 'R$ 8.250,00'},
    'CEO II': {'quantidade': 1, 'valor': 'R$ 11.000,00'},
    'CEO III': {'quantidade': 1, 'valor': 'R$ 19.250,00'},
    'UOM': {'quantidade': 1, 'valor': 'R$ 9.360,00'},
    'SESB': {'quantidade': 1, 'valor': 'R$ 7.200,00'},
    'eCR I': {'quantidade': 1, 'valor': 'R$ 19.900,00'},
    'eCR II': {'quantidade': 1, 'valor': 'R$ 27.300,00'},
    'eCR III': {'quantidade': 1, 'valor': 'R$ 35.200,00'},
    'UBSF': {'quantidade': 0, 'valor': 'Sem cálculo'},
    'eSFR': {'quantidade': 1, 'valor': 'R$ 10.695,00'},
    'eAPP': {'quantidade': 0, 'valor': 'Sem cálculo'},
    'IAF I': {'quantidade': 1, 'valor': 'R$ 1.000,00'},
    'IAF II': {'quantidade': 1, 'valor': 'R$ 1.500,00'},
    'IAF III': {'quantidade': 1, 'valor': 'R$ 2.000,00'},
    'ACS Efetivos': {'quantidade': 1, 'valor': 'R$ 3.036,00'},
    'ACS Contratados': {'quantidade': 1, 'valor': 'R$ 1.550,00'},
    'Mais Médicos': {'quantidade': 1, 'valor': 'R$ 0,00'},
    'CEO ADESÃO RCPD': {'quantidade': 1, 'valor': 'R$ 6.160', 'valor_implantacao': 'R$ 2.567', 'valor_implantacao_novo': 'R$ 6.160'},
    'CEO COM ESPECIALIDADES': {'quantidade': 1, 'valor': 'R$ 6.160', 'valor_implantacao': 'R$ 2.567', 'valor_implantacao_novo': 'R$ 6.160'},
    'LRPD FAIXA I': {'quantidade': 1, 'valor': 'R$ 12.600', 'valor_implantacao': 'R$ 7.500', 'valor_implantacao_novo': 'R$ 12.600'},
    'LRPD FAIXA II': {'quantidade': 1, 'valor': 'R$ 20.100', 'valor_implantacao': 'R$ 12.000', 'valor_implantacao_novo': 'R$ 20.100'},
    'LRPD FAIXA III': {'quantidade': 1, 'valor': 'R$ 30.000', 'valor_implantacao': 'R$ 18.000', 'valor_implantacao_novo': 'R$ 30.000'},
    'LRPD FAIXA IV': {'quantidade': 1, 'valor': 'R$ 37.500', 'valor_implantacao': 'R$ 22.500', 'valor_implantacao_novo': 'R$ 37.500'},
    'ESB ': {'quantidade': 1, 'valor': 'R$ 7.000', 'valor_implantacao': 'R$ 14.000'},
    'UOM ': {'quantidade': 1, 'valor': 'R$ 3.500', 'valor_implantacao': 'R$ 7.000'},
    'Implantação CEO TIPO I ': {'quantidade': 1, 'valor': 'R$ 60.000', 'valor_implantacao': 'R$ 120.000'},
    'Implantação CEO TIPO II ': {'quantidade': 1, 'valor': 'R$ 75.000', 'valor_implantacao': 'R$ 150.000'},
    'Implantação CEO TIPO III ': {'quantidade': 1, 'valor': 'R$ 120.000', 'valor_implantacao': 'R$ 240.000'},
    'SESB ': {'quantidade': 1, 'valor': 'R$ 24.000', 'valor_implantacao': 'R$ 24.000'},
}

# Categorize the services
updated_categories = {
    'Equipe de Saúde da Família': ['eSF', 'eAP 30h', 'eAP 20h'],
    'Equipe Multiprofissional': ['eMULTI Ampl.', 'eMULTI Compl.', 'eMULTI Estrat.'],
    'Saúde Bucal': [
        'eSB Comum I', 'eSB Comum II', 'eSB Quil. Assent. I', 'eSB Quil. Assent. II', 'eSB 20h', 'eSB 30h',
        'CEO I', 'CEO II', 'CEO III','CEO ADESÃO RCPD', 'CEO COM ESPECIALIDADES','Implantação CEO TIPO I ', 'Implantação CEO TIPO II ', 'Implantação CEO TIPO III ',
        'UOM', 'UOM ','SESB', 'SESB ', 
        'LRPD', 'LRPD FAIXA I', 'LRPD FAIXA II', 'LRPD FAIXA III', 'LRPD FAIXA IV'
    ],
    'Equipe de Consultório na Rua': ['eCR I', 'eCR II', 'eCR III'],
    'Unidade Básica de Saúde Fluvial': ['UBSF'],
    'Equipe de Saúde da Família Ribeirinha': ['eSFR'],
    'Equipe de Atenção Primária Prisional': ['eAPP'],
    'Incentivo Atividades Físicas': ['IAF I', 'IAF II', 'IAF III'],
    'Agentes Comunitários de Saúde': ['ACS Efetivos', 'ACS Contratados'],
    'Mais Médicos': ['Mais Médicos'],
}

subcategories = {
    'Equipe de Saúde Bucal': ['eSB Comum I', 'eSB Comum II', 'eSB Quil. Assent. I', 'eSB Quil. Assent. II', 'eSB 20h', 'eSB 30h'],
    'CEO': ['CEO I', 'CEO II', 'CEO III','CEO ADESÃO RCPD', 'CEO COM ESPECIALIDADES','Implantação CEO TIPO I ', 'Implantação CEO TIPO II ', 'Implantação CEO TIPO III '],
    'Outros': ['UOM', 'UOM ','SESB', 'SESB '],
    'LRPD': ['LRPD', 'LRPD FAIXA I', 'LRPD FAIXA II', 'LRPD FAIXA III', 'LRPD FAIXA IV']
}

# Valores para o componente de qualidade
quality_values = {
    'eSF': {'Ótimo': 8000, 'Bom': 6000, 'Suficiente': 4000, 'Regular': 2000},
    'eAP 30h': {'Ótimo': 4000, 'Bom': 3000, 'Suficiente': 2000, 'Regular': 1000},
    'eAP 20h': {'Ótimo': 3000, 'Bom': 2250, 'Suficiente': 1500, 'Regular': 750},
    'eMULTI Ampl.': {'Ótimo': 9000, 'Bom': 6750, 'Suficiente': 4500, 'Regular': 2250},
    'eMULTI Compl.': {'Ótimo': 6000, 'Bom': 4500, 'Suficiente': 3000, 'Regular': 1500},
    'eMULTI Estrat.': {'Ótimo': 3000, 'Bom': 2250, 'Suficiente': 1500, 'Regular': 750},
    'eSB Comum I': {'Ótimo': 2449, 'Bom': 1836.75, 'Suficiente': 1224.50, 'Regular': 612.25},
    'eSB Comum II': {'Ótimo': 3267, 'Bom': 2450.25, 'Suficiente': 1633.50, 'Regular': 816.75},
    'eSB Quil. Assent. I': {'Ótimo': 3673.50, 'Bom': 2755.13, 'Suficiente': 1836.75, 'Regular': 918.38},
    'eSB Quil. Assent. II': {'Ótimo': 4900.50, 'Bom': 3675.38, 'Suficiente': 2450.25, 'Regular': 1225.13},
    'eSB 20h': {'Ótimo': 2449, 'Bom': 1836.75, 'Suficiente': 1224.50, 'Regular': 612.25},
    'eSB 30h': {'Ótimo': 3267, 'Bom': 2450.25, 'Suficiente': 1633.50, 'Regular': 816.75},
}

def format_currency(value):
    """Formats a number as Brazilian currency."""
    if value == 'Sem cálculo':
        return value
    if isinstance(value, str):
        value = float(value.replace('R$ ', '').replace('.', '').replace(',', '.'))
    return "R$ {:,.2f}".format(value).replace(",", "v").replace(".", ",").replace("v", ".")

def calculate_total(selected_services, values, quality):
    """Calculates the total value for the selected services."""
    results = []
    total_geral = 0

    all_services = {service: quantity for category, services in updated_categories.items() for service, quantity in selected_services.items() if service in services}

    for (service, quantity), value in zip(all_services.items(), values.values()):
        if service in data:
            if value == 'Sem cálculo':
                valor = 0
            else:
                valor = float(value.replace('R$ ', '').replace('.', '').replace(',', '.'))
            
            quality_multiplier = quality_values.get(service, {}).get(quality, 0) if service in quality_values else 0
            total = (valor + quality_multiplier) * quantity

            if quantity > 0:
                total_geral += total
                results.append([service, quantity, format_currency(valor), format_currency(quality_multiplier), format_currency(total)])

    if total_geral > 0:
        results.append(['Total Geral', '', '', '', format_currency(total_geral)])
    return results, total_geral

st.title('Calculadora de Serviços de Saúde')

selected_services = {}
values = {}

# CSS para estilizar os campos de valor unitário
st.markdown("""
<style>
div[data-testid="stText"] {
    background-color: #a7d9ed; /* Cor de fundo azul mais escuro */
    padding: 10px;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# Use st.expander for each category and create unique keys
for category, services in updated_categories.items():
    with st.expander(category):
        # Check if the category is "Saúde Bucal" and handle subcategories
        if category == 'Saúde Bucal':
            for subcategory, sub_services in subcategories.items():
                st.markdown(f"##### {subcategory}")
                cols = st.columns(4)  # Changed to 4 columns
                col_index = 0
                
                for service in sub_services:
                    unique_key = f"{category}_{subcategory}_{service}"
                    unique_key_value = f"{category}_{subcategory}_{service}_value"

                    with cols[col_index % 4]:  # Mod to 4
                        quantity = st.number_input(f'{service} (Quantidade)', min_value=0, value=0, key=unique_key)
                        initial_value = data[service]['valor']
                        label = f"Valor {service}"
                        value = st.text_input(label, value=initial_value, key=unique_key_value)
                        selected_services[service] = quantity
                        values[unique_key_value] = value
                    
                    col_index += 1
                st.divider()
        else:
            # Regular category processing
            cols = st.columns(4)  # Changed to 4 columns
            col_index = 0
            for service in services:
                unique_key = f"{category}_{service}"
                unique_key_value = f"{category}_{service}_value"
                
                # Correção para "Mais Médicos"
                if service == 'Mais Médicos':
                    with cols[col_index % 4]:
                        quantity = st.number_input(f'{service} (Quantidade)', min_value=0, value=0, key=unique_key)
                        initial_value = data[service]['valor']
                        label = f"Valor {service}"
                        value = st.text_input(label, value=initial_value, key=unique_key_value)
                        selected_services[service] = quantity
                        values[unique_key_value] = value
                    col_index += 1
                else:
                    with cols[col_index % 4]:  # Mod to 4
                        quantity = st.number_input(f'{service} (Quantidade)', min_value=0, value=0, key=unique_key)
                        initial_value = data[service]['valor']
                        label = f"Valor {service}"
                        # Atualiza o valor de ACS Efetivos
                        if service == 'ACS Efetivos':
                            initial_value = 'R$ 3.036,00'
                        
                        value = st.text_input(label, value=initial_value, key=unique_key_value)
                        selected_services[service] = quantity
                        values[unique_key_value] = value
                    col_index += 1

# Posição do selectbox alterada para antes do botão
Classificacao = st.selectbox("Considerar Qualidade", options=['Regular', 'Suficiente', 'Bom', 'Ótimo'], index=2) # Valor inicial alterado para 'Bom'

  
    
    
    
    

# Verifica se algum serviço foi selecionado antes de calcular
if st.button('Calcular'):
    if all(q == 0 for q in selected_services.values()):
        st.error("Por favor, selecione pelo menos um serviço para calcular.")
    else:
        
        # Informações da API
        st.write("**Informações da API:**")
        st.write(f"**IED:** {st.session_state.ied}")
        st.write(f"**Competência:** {st.session_state.competencia}")
        st.write(f"**População:** {st.session_state.populacao}")
    
        # COMPONENTE 01 - COMPONENTE FIXO
       
            
        st.subheader("Componente I - Componente Fixo")
        fixed_table = []

        # Valores do componente fixo
        fixed_values = {
            'eSF': 16000,
            'eAP 30h': 9600,
            'eAP 20h': 6400,
        }

        # Construindo a tabela do componente fixo
        for service, value in fixed_values.items():
            quantity = selected_services.get(service, 0)
            if quantity > 0:
                total_value = value * quantity
                fixed_table.append([service, format_currency(value), quantity, format_currency(total_value)])

        fixed_df = pd.DataFrame(fixed_table, columns=['Serviço', 'Valor Unitário', 'Quantidade', 'Valor Total'])

        # Adicionar linha de total à tabela do componente fixo
        total_fixed_value = sum(float(val.replace('R$ ', '').replace('.', '').replace(',', '.')) for val in fixed_df['Valor Total'])
        total_fixed_row = pd.DataFrame({
            'Serviço': ['Total'],
            'Valor Unitário': [''],
            'Quantidade': [''],
            'Valor Total': [format_currency(total_fixed_value)]
        })
        fixed_df = pd.concat([fixed_df, total_fixed_row], ignore_index=True)

        st.dataframe(fixed_df)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        # COMPONENTE 02 - VÍNCULO E ACOMPANHAMENTO TERRITORIAL.

        # Tabela de Vínculo e Acompanhamento
        st.subheader("Componente II - Vínculo e Acompanhamento Territorial")
        vinculo_table = []

        # Valores do componente de vínculo e acompanhamento
        vinculo_values = {
            'eSF': {'Ótimo': 8000, 'Bom': 6000, 'Suficiente': 4000, 'Regular': 2000},
            'eAP 30h': {'Ótimo': 4000, 'Bom': 3000, 'Suficiente': 2000, 'Regular': 1000},
            'eAP 20h': {'Ótimo': 3000, 'Bom': 2250, 'Suficiente': 1500, 'Regular': 750},
        }

        # Construindo a tabela de vínculo e acompanhamento
        for service, quality_levels in vinculo_values.items():
            if Classificacao in quality_levels:
                quantity = selected_services.get(service, 0)
                if quantity > 0:
                    value = quality_levels[Classificacao]
                    total_value = value * quantity
                    vinculo_table.append([service, Classificacao, format_currency(value), quantity, format_currency(total_value)])

        vinculo_df = pd.DataFrame(vinculo_table, columns=['Serviço', 'Qualidade', 'Valor Unitário', 'Quantidade', 'Valor Total'])

        # Adicionar linha de total à tabela de vínculo e acompanhamento
        total_vinculo_value = sum(float(val.replace('R$ ', '').replace('.', '').replace(',', '.')) for val in vinculo_df['Valor Total'])
        total_vinculo_row = pd.DataFrame({
            'Serviço': ['Total'],
            'Qualidade': [''],
            'Valor Unitário': [''],
            'Quantidade': [''],
            'Valor Total': [format_currency(total_vinculo_value)]
        })
        vinculo_df = pd.concat([vinculo_df, total_vinculo_row], ignore_index=True)

        st.dataframe(vinculo_df)
        
        
        # COMPONENTE 03 - QUALIDADE

        st.subheader("Componente III - Pagamento por Desempenho")
        quality_table = []

        # Modificação para a tabela de qualidade
        for service, quality_levels in quality_values.items():
            if Classificacao in quality_levels:
                quantity = selected_services.get(service, 0)
                if quantity > 0:
                    value = quality_levels[Classificacao]
                    total_value = value * quantity
                    quality_table.append([service, Classificacao, format_currency(value), quantity, format_currency(total_value)])

        quality_df = pd.DataFrame(quality_table, columns=['Serviço', 'Qualidade', 'Valor Unitário', 'Quantidade', 'Valor Total'])

        # Adicionar linha de total à tabela de qualidade
        total_quality_value = sum(float(val.replace('R$ ', '').replace('.', '').replace(',', '.')) for val in quality_df['Valor Total'])
        total_quality_row = pd.DataFrame({
            'Serviço': ['Total'],
            'Qualidade': [''],
            'Valor Unitário': [''],
            'Quantidade': [''],
            'Valor Total': [format_currency(total_quality_value)]
        })
        quality_df = pd.concat([quality_df, total_quality_row], ignore_index=True)

        # Removendo linhas duplicadas da tabela de qualidade
        quality_df = quality_df.drop_duplicates()

        st.dataframe(quality_df)

        # IV - COMPONENTE PARA IMPLANTAÇÃO E MANUTENÇÃO DE PROGRAMAS, SERVIÇOS, PROFISSIONAIS E OUTRAS COMPOSIÇÕES DE EQUIPES QUE ATUAM NA APS
        st.subheader("IV - Componente para Implantação e Manutenção")
        implantacao_manutencao_table = []

        # Lista de serviços que pertencem a este componente (todos exceto saúde bucal e qualidade)
        implantacao_manutencao_services = [
            service for category, services in updated_categories.items() 
            for service in services 
            if category != 'Saúde Bucal' and service not in quality_values
        ]

        for service in implantacao_manutencao_services:
            quantity = selected_services.get(service, 0)
            if quantity > 0:
                value_str = values.get(f"{service}_value", '0')  # Obtém o valor do dicionário values
                if value_str == 'Sem cálculo':
                    valor = 0
                else:
                    valor = float(value_str.replace('R$ ', '').replace('.', '').replace(',', '.'))
                
                total = valor * quantity
                implantacao_manutencao_table.append([service, quantity, format_currency(valor), format_currency(total)])

        implantacao_manutencao_df = pd.DataFrame(implantacao_manutencao_table, columns=['Serviço', 'Quantidade', 'Valor Unitário', 'Valor Total'])

        # Adicionar linha de subtotal
        total_implantacao_manutencao_value = sum(float(val.replace('R$ ', '').replace('.', '').replace(',', '.')) for val in implantacao_manutencao_df['Valor Total'])
        total_implantacao_manutencao_row = pd.DataFrame({
            'Serviço': ['Subtotal'],
            'Quantidade': [''],
            'Valor Unitário': [''],
            'Valor Total': [format_currency(total_implantacao_manutencao_value)]
        })
        implantacao_manutencao_df = pd.concat([implantacao_manutencao_df, total_implantacao_manutencao_row], ignore_index=True)

        st.dataframe(implantacao_manutencao_df)

        # V - COMPONENTE PARA ATENÇÃO À SAÚDE BUCAL
        st.subheader("V - Componente para Atenção à Saúde Bucal")
        saude_bucal_table = []

        # Lista de serviços que pertencem a este componente (saúde bucal, exceto qualidade)
        saude_bucal_services = [
            service for service in updated_categories.get('Saúde Bucal', [])
            if service not in quality_values
        ]

        for service in saude_bucal_services:
            quantity = selected_services.get(service, 0)
            if quantity > 0:
                value_str = values.get(f"{service}_value", '0')  # Obtém o valor do dicionário values
                if value_str == 'Sem cálculo':
                    valor = 0
                else:
                    valor = float(value_str.replace('R$ ', '').replace('.', '').replace(',', '.'))
                
                total = valor * quantity
                saude_bucal_table.append([service, quantity, format_currency(valor), format_currency(total)])

        saude_bucal_df = pd.DataFrame(saude_bucal_table, columns=['Serviço', 'Quantidade', 'Valor Unitário', 'Valor Total'])

        # Adicionar linha de subtotal
        total_saude_bucal_value = sum(float(val.replace('R$ ', '').replace('.', '').replace(',', '.')) for val in saude_bucal_df['Valor Total'])
        total_saude_bucal_row = pd.DataFrame({
            'Serviço': ['Subtotal'],
            'Quantidade': [''],
            'Valor Unitário': [''],
            'Valor Total': [format_currency(total_saude_bucal_value)]
        })
        saude_bucal_df = pd.concat([saude_bucal_df, total_saude_bucal_row], ignore_index=True)

        st.dataframe(saude_bucal_df)
        
                # CÁLCULO DO TOTAL GERAL
        total_geral = total_fixed_value + total_vinculo_value + total_quality_value + total_implantacao_manutencao_value + total_saude_bucal_value

        # EXIBIÇÃO DO TOTAL GERAL
        st.subheader("Total Geral")
        total_geral_df = pd.DataFrame({
            'Descrição': ['Total Geral'],
            'Valor': [format_currency(total_geral)]
        })
        st.dataframe(total_geral_df)

        # Destaque para o valor total geral
        st.markdown(f"<h3 style='text-align: center; color: blue;'>Total Geral: {format_currency(total_geral)}</h3>", unsafe_allow_html=True)
