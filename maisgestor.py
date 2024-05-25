import streamlit as st
import pandas as pd
import datetime
from pyUFbr.baseuf import ufbr

ibge_creche = mat_creche = ibge_pre = mat_pre = ibge_1a5 = mat_1a5 = ibge_6a9 = mat_6a9 = ibge_contra = mat_contra = ibge_eja = mat_eja = ibge_especial = mat_especial = 0

def formatar_numero(num):
    # Formatação do número para duas casas decimais com ponto como separador de milhar
    num_formatado = "{:,.2f}".format(num)

    # Substituindo ponto por vírgula e vírgula por ponto
    num_formatado = num_formatado.replace(",", "x").replace(".", ",").replace("x", ".")

    # Adicionando o símbolo de Real (R$) na frente
    num_formatado = "R$ " + num_formatado

    return num_formatado

def formatar_numero2(numero):
    return '{:,.0f}'.format(numero).replace(',', '.')

# Interface:

st.set_page_config(page_title='Mais Gestor - Situacional da Educação')
st.markdown(
    """
    <style>
    .reportview-container {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.image('logo_maisgestor.png', width=200)
    st.header('Situacional da Educação')
    st.divider()

with st.container():
    st.subheader('Informações:')

    with st.expander("Matrícula"):
        mat_creche = st.number_input("CRECHE", value=0, help="Número de matrículas na creche")
        mat_pre = st.number_input("PRÉ-ESCOLA", value=0, help="Número de matrículas na pré-escola")
        mat_1a5 = st.number_input("ANOS INICIAIS 1º AO 5º ANO", value=0, help="Número de matrículas nos anos iniciais (1º ao 5º ano)")
        mat_6a9 = st.number_input("ANOS INICIAIS 6º AO 9º ANO", value=0, help="Número de matrículas nos anos iniciais (6º ao 9º ano)")
        mat_contra = st.number_input("CONTRA TURNO", value=0, help="Número de matrículas em contra turno")
        mat_eja = st.number_input("EJA", value=0, help="Número de matrículas na Educação de Jovens e Adultos (EJA)")
        mat_especial = st.number_input("EDUCAÇÃO ESPECIAL", value=0, help="Número de matrículas na Educação Especial")

    with st.expander("IBGE"):
        ibge_creche = st.number_input("CRECHE", value=0, help="Número de matrículas na creche segundo o IBGE")
        ibge_pre = st.number_input("PRÉ-ESCOLA", value=0, help="Número de matrículas na pré-escola segundo o IBGE")
        ibge_1a5 = st.number_input("ANOS INICIAIS 1º AO 5º ANO", value=0, help="Número de matrículas nos anos iniciais (1º ao 5º ano) segundo o IBGE")
        ibge_6a9 = st.number_input("ANOS INICIAIS 6º AO 9º ANO", value=0, help="Número de matrículas nos anos iniciais (6º ao 9º ano) segundo o IBGE")
        ibge_contra = st.number_input("CONTRA TURNO", value=0, help="Número de matrículas em contra turno segundo o IBGE")
        ibge_eja = st.number_input("EJA", value=0, help="Número de matrículas na Educação de Jovens e Adultos (EJA) segundo o IBGE")
        ibge_especial = st.number_input("EDUCAÇÃO ESPECIAL", value=0, help="Número de matrículas na Educação Especial segundo o IBGE")

    est_creche = ibge_creche - mat_creche
    est_pre = ibge_pre - mat_pre
    est_1a5 = ibge_1a5 - mat_1a5
    est_6a9 = ibge_6a9 - mat_6a9
    est_contra = ibge_contra - mat_contra
    est_eja = ibge_eja - mat_eja
    est_especial = ibge_especial - mat_especial
    total_est = est_creche + est_pre + est_1a5 + est_6a9 + est_contra + est_eja + est_especial

    valor_creche = 5260.00
    valor_pre_escola = 5260.00
    valor_anos_iniciais = 5260.00
    valor_contra_turno = 8000.00
    valor_eja = 10520.00
    valor_educacao_especial = 10520.00
    #total_valor_ano = valor_creche + valor_pre_escola + valor_anos_iniciais * 2 + valor_contra_turno + valor_eja + valor_educacao_especial


    data = [
        {"MATRICULA POR ETAPA": "CRECHE", "ESTIMATIVA DE FALTANTES": formatar_numero2(est_creche), "VALOR ANO ALUNO": formatar_numero(valor_creche), "VALOR ESTIMADO": formatar_numero(valor_creche * est_creche)},
        {"MATRICULA POR ETAPA": "PRÉ-ESCOLA", "ESTIMATIVA DE FALTANTES": formatar_numero2(est_pre), "VALOR ANO ALUNO": formatar_numero(valor_pre_escola), "VALOR ESTIMADO": formatar_numero(valor_pre_escola * est_pre)},
        {"MATRICULA POR ETAPA": "ANOS INICIAIS 1º ANO AO 5º ANO", "ESTIMATIVA DE FALTANTES": formatar_numero2(est_1a5), "VALOR ANO ALUNO": formatar_numero(valor_anos_iniciais), "VALOR ESTIMADO": formatar_numero(valor_anos_iniciais * est_1a5)},
        {"MATRICULA POR ETAPA": "ANOS INICIAIS 6º ANO AO 9º ANO", "ESTIMATIVA DE FALTANTES": formatar_numero2(est_6a9), "VALOR ANO ALUNO": formatar_numero(valor_anos_iniciais), "VALOR ESTIMADO": formatar_numero(valor_anos_iniciais * est_6a9)},
        {"MATRICULA POR ETAPA": "CONTRA TURNO", "ESTIMATIVA DE FALTANTES": formatar_numero2(est_contra), "VALOR ANO ALUNO": formatar_numero(valor_contra_turno), "VALOR ESTIMADO": formatar_numero(valor_contra_turno * est_contra)},
        {"MATRICULA POR ETAPA": "EJA", "ESTIMATIVA DE FALTANTES": formatar_numero2(est_eja), "VALOR ANO ALUNO": formatar_numero(valor_eja), "VALOR ESTIMADO": formatar_numero(valor_eja * est_eja)},
        {"MATRICULA POR ETAPA": "EDUCAÇÃO ESPECIAL", "ESTIMATIVA DE FALTANTES": formatar_numero2(est_especial), "VALOR ANO ALUNO": formatar_numero(valor_educacao_especial), "VALOR ESTIMADO": formatar_numero(valor_educacao_especial * est_especial)},
    ]

    df = pd.DataFrame(data)

    st.dataframe(df, hide_index=True)
        
    total_est = formatar_numero2(total_est)
    st.markdown(f"<span style='font-size:20px;'>**Total de faltantes:** <span style='color:red;'>**{total_est}**</span></span>", unsafe_allow_html=True)
        
    valor_total_estimado = 0

    for etapa in data:
        valor_estimado = etapa["VALOR ESTIMADO"].replace("R$", "").replace(".", "").replace(",", ".") # Remove "R$", pontos e substitui vírgulas por ponto
        valor_total_estimado += float(valor_estimado)

    valor_total_estimado = formatar_numero(valor_total_estimado)
    st.markdown(f"<span style='font-size:24px;'>**Valor Total Estimado:** <span style='color:red;'>**{valor_total_estimado}**</span></span>", unsafe_allow_html=True)

    st.divider()
    st.subheader('Distribuição por etapa')
    df['ESTIMATIVA DE FALTANTES'] = df['ESTIMATIVA DE FALTANTES'].astype(int)
    df = df.set_index("MATRICULA POR ETAPA")["ESTIMATIVA DE FALTANTES"]
    st.bar_chart(df)