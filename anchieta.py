import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd  # Add pandas import
import plotly.graph_objs as go

anos = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

media_complexidade = [
    267924, 208427, 228350, 240491, 212345, 259454, 242082, 273517, 220826, 317777, 359352, 413023, 358764
]

alta_complexidade = [
    0, 0, 2, 0, 0, 0, 49, 72, 186, 61, 6, 1, 0
]

nao_se_aplica = [
    389, 1689, 1257, 859, 659, 14337, 22678, 14613, 4314, 6815, 16341, 18673, 16450
]

procedimentos_clinicos = [
    2009, 2049, 1880, 1748, 1174, 1353, 841, 697, 768, 695, 543, 407, 337
]

procedimentos_cirurgicos = [
    415, 490, 586, 500, 427, 418, 227, 120, 91, 193, 260, 249, 224
]

valores_sem_incentivo = [
    1771855.26, 1940986.9, 2185573.08, 1448833.26, 1405480.91, 1397996.03, 1495656.04, 1637323.23, 1694061.02, 1695934.41, 1648115.83, 1571333.25, 3203367.45
]

valores_incentivos = [
    339660, 226587.08, 356526.48, 1082162.76, 1082162.76, 1077219.72, 1077219.76, 1072276.74, 1072276.74, 1072276.74, 1072276.74, 1095295.74, 1095295.74
]

teto_total = [
    2111515.26, 2167573.98, 2542099.56, 2530996.02, 2487643.67, 2475215.75, 2572875.8, 2709599.97, 2766337.76, 2768211.15, 2720392.57, 2666628.99, 4298663.19
]

total_ambulatorial = [
    sum(x) for x in zip(media_complexidade, alta_complexidade, nao_se_aplica)
]

total_procedimentos = [
    sum(x) for x in zip(procedimentos_clinicos, procedimentos_cirurgicos)
]

# Calculando os totais (fora do dicionário, como listas)
total_ambulatorial = [sum(x) for x in zip(media_complexidade, alta_complexidade, nao_se_aplica)]
total_procedimentos = [x + y for x, y in zip(procedimentos_clinicos, procedimentos_cirurgicos)]

# Criação do menu de seleção de páginas na barra lateral
paginas = ["Introdução", "I. Evolução do Teto MAC", "II. MAC x Procedimentos Hospitalares", "III. MAC x Produção Ambulatorial", "IV. Correlação Produção vs Recursos", "V. Conclusão"]

# Adicionando as logos na sidebar
st.sidebar.image('logo_colorida_mg.png')
st.sidebar.image('anchieta.png', channels="BGR")
st.sidebar.markdown("<h1 style='text-align: center; color: #808080;'>Análise do Teto MAC</h1>", unsafe_allow_html=True)
escolha = st.sidebar.radio("Escolha a página que deseja visualizar:", paginas)
st.sidebar.markdown(
    """
    <style>
    .css-1d391kg {
        background-color: #2f4f4f; /* Substitua #f0f0f5 pelo código da cor que desejar */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Página 2: Evolução do Teto MAC
if escolha == "I. Evolução do Teto MAC":
    st.title("Evolução do Teto MAC (2012-2024)")

    df = pd.DataFrame({
        "Ano": anos * 3,
        "Valor (R$)": teto_total + valores_sem_incentivo + valores_incentivos,
        "Categoria": ["Teto Total"] * len(teto_total) +
                     ["Valores Sem Incentivo"] * len(valores_sem_incentivo) +
                     ["Valores Incentivos"] * len(valores_incentivos)
    })

    # Criando o gráfico
    fig = px.line(df, x='Ano', y='Valor (R$)', color='Categoria', labels={'value': 'Valores', 'variable': 'Categorias'}, markers=True)
    fig.update_layout(
        title='Dados ao longo dos anos',
        xaxis_title='Ano',
        yaxis_title='Valores',
        legend_title_text='Categorias',
        legend=dict(
            itemsizing='constant',
            orientation='h'
        )
    )

    fig.update_traces(marker=dict(size=12))
    fig.update_xaxes(showgrid=True, gridwidth=0.1, gridcolor='LightGrey')
    fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='LightGrey')

    st.plotly_chart(fig)
    st.caption('Fonte: Sismac/MS')

    st.markdown("""
    ### Análise da Evolução do Teto MAC em Anchieta-ES (2012-2024)

    Este relatório analisa a evolução do Teto MAC do município de Anchieta-ES entre 2012 e 2024, com o objetivo de justificar a necessidade de aumento para 2025. A análise considera valores de média e alta complexidade, procedimentos clínicos e cirúrgicos, valores com e sem incentivos, e o teto total, além de remanejamentos recentes.

    **1. Crescimento e Flutuações do Teto MAC (2012-2024):**

    - O Teto MAC de Anchieta-ES apresentou flutuações ao longo dos anos, com um valor inicial de 2.111.515,26 em 2012, atingindo 2.666.628,99 em 2023 e R$ 4.298.663,19 em 2024.
    - Essas flutuações refletem a complexidade da gestão de recursos, as políticas públicas e as necessidades de saúde da população de Anchieta-ES.

    **2. Impacto da Demanda por Serviços e Justificativa para Aumento do Teto MAC:**

    - A análise dos dados, especialmente o crescimento do Total Ambulatorial e a redução no número de procedimentos, reforça a tendência de aumento na demanda por serviços de saúde em Anchieta-ES, sem um financiamento proporcional.
    - Remanejamentos frequentes indicam um esforço contínuo para adequar o financiamento à demanda real e às prioridades de saúde do município.
    - A estagnação do Teto MAC entre 2015 e 2023, mesmo com o aumento da demanda, evidencia a necessidade de um reajuste.
    - A redução no número de procedimentos clínicos e cirúrgicos sugere uma possível limitação na oferta de serviços, provavelmente decorrente da insuficiência de recursos.
    - Portanto, o aumento do Teto MAC para Anchieta-ES é fundamental para garantir o atendimento adequado à população, suprir a demanda reprimida e ampliar a oferta de serviços de saúde, especialmente na média complexidade.

    ### Direcionamento para 2025

    - **Aprimorar a Captação de Incentivos**: Continuar explorando e captando incentivos específicos de programas de saúde pode ser uma estratégia eficaz. Identificar novas oportunidades de incentivo pode contribuir significativamente para o aumento do Teto MAC.
    - **Gestão Eficiente dos Recursos**: Revisar e ajustar continuamente os remanejamentos intra-teto para garantir que os recursos sejam utilizados de forma eficiente, priorizando a média complexidade, que concentra a maior parte da demanda. Uma gestão dinâmica e transparente pode otimizar a alocação de recursos e justificar aumentos futuros.
    - **Monitoramento das Políticas Públicas**: Acompanhar de perto as políticas públicas que influenciam a alocação de recursos pode ajudar a antecipar mudanças e ajustar as estratégias de financiamento conforme necessário.
    - **Justificativa Robusta para o Aumento do Teto MAC**: Utilizar os dados apresentados neste relatório para demonstrar a defasagem entre o financiamento atual e a demanda crescente por serviços de saúde, embasando a solicitação de aumento do Teto MAC para 2025.

    **Conclusão:**

    A análise da evolução do Teto MAC de Anchieta-ES entre 2012 e 2024 demonstra claramente a necessidade de um aumento substancial no financiamento para 2025. O crescimento da demanda por serviços de saúde, evidenciado pelo aumento do Total Ambulatorial e pela redução no número de procedimentos, aliado à estagnação do Teto MAC nos últimos anos, justifica a solicitação de um reajuste que permita ao município atender adequadamente às necessidades de sua população. A captação de incentivos e a gestão eficiente dos recursos são estratégias complementares importantes, mas não substituem a necessidade de um Teto MAC compatível com a realidade de Anchieta-ES.
    
    """)




# Página 2: Procedimentos Hospitalares e Recursos
if escolha == "II. MAC x Procedimentos Hospitalares":
    st.title("Procedimentos Hospitalares e Recursos ao Longo dos Anos")
    
    # Criando o gráfico
    fig1 = go.Figure()

    # Procedimentos ao longo dos anos
    fig1.add_trace(go.Scatter(x=anos, y=procedimentos_clinicos, mode='lines+markers', name='Procedimentos Clínicos'))
    fig1.add_trace(go.Scatter(x=anos, y=procedimentos_cirurgicos, mode='lines+markers', name='Procedimentos Cirúrgicos'))
    
    fig1.update_layout(
        title='Procedimentos Hospitalares ao Longo dos Anos',
        xaxis_title='Anos',
        yaxis_title='Número de Procedimentos',
        legend_title='Tipo de Procedimento',
        legend=dict(orientation='h', y=-0.2, x=0)
    )


    fig2 = go.Figure()

    # Recursos ao longo dos anos
    fig2.add_trace(go.Scatter(x=anos, y=teto_total, mode='lines+markers', name='Teto Total'))
    fig2.add_trace(go.Scatter(x=anos, y=valores_sem_incentivo, mode='lines+markers', name='Valores Sem Incentivo'))
    fig2.add_trace(go.Scatter(x=anos, y=valores_incentivos, mode='lines+markers', name='Valores com Incentivos'))

    fig2.update_layout(
        title='Recursos ao Longo dos Anos',
        xaxis_title='Anos',
        yaxis_title='Valores (R$)',
        legend_title='Tipo de Recurso',
        legend=dict(orientation='h', y=-0.2, x=0)
    )

    # Exibir os gráficos no Streamlit
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.caption('Fonte: Tabnet/Datasus/MS')

    st.markdown("""
    ### Análise da Relação entre o Teto MAC e a Produção Ambulatorial em Anchieta-ES: Considerações sobre os Custos dos Procedimentos Ambulatoriais

    A análise da relação entre o Teto MAC e a produção ambulatorial em Anchieta-ES, entre 2012 e 2024, revela um descompasso entre financiamento e demanda, agravado pelos custos dos procedimentos ambulatoriais.

    #### Descompasso entre Financiamento e Produção

    - **Crescimento do Teto MAC**: O Teto MAC cresceu ao longo dos anos, mas apresentou longos períodos de estagnação. Aumentos significativos ocorreram em 2019 e, especialmente, em 2024.
    - **Produção Ambulatorial**: A produção ambulatorial, medida pelo somatório dos valores de média complexidade, alta complexidade e "não se aplica", teve variações com uma tendência geral de crescimento, demonstrando a capacidade do município de manter e aumentar a produção, mesmo diante de recursos limitados.

    #### Análise por Período

    - **2012-2014**: O aumento nominal do Teto MAC de 2.111.515,26 para R$ 2.542.099,56 foi menor devido ao aumento dos custos dos procedimentos ambulatoriais.
    - **2015-2018**: A estagnação do Teto MAC em torno de R$ 2.500.000,00 forçou o município a absorver os aumentos dos custos dos procedimentos.
    - **2019-2020**: O aumento do Teto MAC para 2.709.599,97 em 2019 e R$ 2.766.337,76 em 2020 foi limitado pelo crescimento dos custos ambulatoriais.
    - **2021-2023**: A redução nominal do Teto MAC para 2.768.211,15 em 2021, 2.720.392,57 em 2022 e R$ 2.666.628,99 em 2023, com o aumento dos custos, implicou em um esforço local para manter os serviços ambulatoriais.
    - **2024**: O aumento significativo do Teto MAC para R$ 4.298.663,19 é, em grande parte, uma realocação interna, com impacto real reduzido devido aos custos acumulados e à inflação do período.

    #### Implicações e Justificativa para o Aumento do Teto MAC

    - **Subfinanciamento Crônico**: O Teto MAC cresceu a um ritmo inferior à demanda e aos custos dos procedimentos ambulatoriais, como evidenciado pela redução no número de procedimentos clínicos e cirúrgicos realizados.
    - **Erosão do Poder de Compra**: Longos períodos de estagnação, como entre 2015 e 2018, representam uma perda significativa do poder de compra, dificultando a aquisição de insumos e a contratação de profissionais para os procedimentos ambulatoriais.
    - **Necessidade de Correção**: O aumento do Teto MAC em 2024 é necessário, mas precisa de ajustes periódicos para acompanhar os custos dos procedimentos ambulatoriais e a demanda crescente.
    - **Distorção Histórica**: A defasagem entre o crescimento do Teto MAC e os custos dos procedimentos ambulatoriais precisa ser corrigida para garantir financiamento adequado e a sustentabilidade dos serviços.

    #### Conclusão

    O município de Anchieta-ES demonstrou capacidade de manter e até aumentar a produção ambulatorial, mesmo com recursos limitados. O aumento do Teto MAC em 2024 é crucial, mas não resolve a defasagem histórica. É necessário um Teto MAC que acompanhe a demanda, a complexidade dos procedimentos e os custos ambulatoriais para garantir a sustentabilidade e qualidade do atendimento, especialmente na média complexidade, que concentra a maior parte da demanda.
    """)


# Página 3: MAC x Produção Ambulatorial
if escolha == "III. MAC x Produção Ambulatorial":
    st.title("Produção Ambulatorial ao Longo dos Anos")
    
    # Criar figuras
    fig1 = go.Figure()

    # Produção ambulatorial ao longo dos anos
    fig1.add_trace(go.Scatter(x=anos, y=media_complexidade, mode='lines+markers', name='Média Complexidade'))
    fig1.add_trace(go.Scatter(x=anos, y=alta_complexidade, mode='lines+markers', name='Alta Complexidade'))
    fig1.add_trace(go.Scatter(x=anos, y=nao_se_aplica, mode='lines+markers', name='Não se Aplica'))
    fig1.add_trace(go.Scatter(x=anos, y=total_ambulatorial, mode='lines', name='Total de Procedimentos'))

    fig1.update_layout(
        title='Produção Ambulatorial ao Longo dos Anos',
        xaxis_title='Anos',
        yaxis_title='Quantidade de Procedimentos',
        legend_title='Tipo de Procedimento',
        legend=dict(orientation='h', y=-0.2, x=0)

    )

    fig2 = go.Figure()

    # Recursos ao longo dos anos
    fig2.add_trace(go.Scatter(x=anos, y=teto_total, mode='lines+markers', name='Teto Total'))
    fig2.add_trace(go.Scatter(x=anos, y=valores_sem_incentivo, mode='lines+markers', name='Valores Sem Incentivo'))
    fig2.add_trace(go.Scatter(x=anos, y=valores_incentivos, mode='lines+markers', name='Valores com Incentivos'))

    fig2.update_layout(
        title='Recursos ao Longo dos Anos',
        xaxis_title='Anos',
        yaxis_title='Valores (R$)',
        legend_title='Tipo de Recurso',
        legend=dict(orientation='h', y=-0.2, x=0)

    )

    # Exibir os gráficos no Streamlit
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.caption('Fonte: Tabnet/Datasus/MS')


    import streamlit as st

    st.markdown("""
    ### Análise da Relação entre o Teto MAC e a Produção Ambulatorial em Anchieta-ES

    A análise da relação entre o Teto MAC e a produção ambulatorial em Anchieta-ES revela nuances importantes sobre o financiamento e a prestação de serviços ambulatoriais no município.

    #### 1. Visão Geral dos Dados

    - **Teto MAC**: Apresentou períodos de estagnação, com aumentos significativos em 2019 e 2024.
    - **Produção Ambulatorial**: O Total Ambulatorial, somatório dos valores de média complexidade, alta complexidade e "não se aplica", mostrou tendência de crescimento com algumas flutuações.

    #### 2. Análise Detalhada por Componente

    - **Média Complexidade**: Representa a maior parte da produção ambulatorial, com comportamento irregular, apresentando quedas e picos.
    - **Alta Complexidade**: Valores menores e mais consistentes de 2014 a 2022.
    - **Não se Aplica**: Valores baixos mas variáveis, com picos em certos anos.

    #### 3. Relação entre Teto MAC e Produção Ambulatorial

    - **Descompasso**: O Teto MAC estagnou enquanto a produção ambulatorial cresceu.
    - **Impacto nos Serviços**: Reduções no Teto MAC podem ter limitado a oferta de serviços de média complexidade.
    - **Crescimento da Alta Complexidade**: Sugere possível priorização desses serviços.
    - **Valores "Não se Aplica"**: Variabilidade pode refletir mudanças nas regras ou necessidades locais.

    #### 4. Análise por Período

    - **2012-2014**: Aumento do Teto MAC, mas diminuição da produção ambulatorial.
    - **2015-2018**: Estagnação do Teto MAC, recuperação da produção ambulatorial.
    - **2019-2020**: Aumento do Teto MAC não refletido na produção, que caiu em 2020.
    - **2021-2023**: Redução do Teto MAC, crescimento da produção ambulatorial.
    - **2024**: Aumento expressivo do Teto MAC, leve queda na produção.

    #### 5. Implicações e Justificativa para o Aumento do Teto MAC

    - **Subfinanciamento**: A atenção ambulatorial pode ter sofrido com subfinanciamento crônico.
    - **Necessidade de Investimentos**: Aumento do Teto MAC em 2024 é crucial para investimentos.
    - **Priorização de Serviços**: Análise dos componentes auxilia na definição de prioridades.

    #### Conclusão

    A relação entre o Teto MAC e a produção ambulatorial em Anchieta-ES entre 2012 e 2024 mostrou um descompasso entre financiamento e demanda. O aumento do Teto MAC em 2024 é fundamental para corrigir essa distorção e garantir a sustentabilidade do sistema de saúde local. A análise reforça a necessidade de um Teto MAC compatível com a realidade de produção ambulatorial e a crescente demanda por serviços de saúde em Anchieta, justificando esforços para sua ampliação e adequação contínua.

    """)


# Página 4: Correlação Produção vs Recursos
if escolha == "IV. Correlação Produção vs Recursos":
    # Introdução às correlações
    st.title('Correlação entre os Recursos e a Produção')
    st.markdown("""
        As correlações entre os valores recebidos (Teto Total, Valores Sem Incentivo, Valores com Incentivos) e a produção ambulatorial foram calculadas usando o coeficiente de correlação de _Pearson_. Este coeficiente mede a força e a direção da associação linear entre duas variáveis. Valores próximos de 1 ou -1 indicam uma correlação forte, enquanto valores próximos de 0 indicam pouca ou nenhuma correlação.
        """)

    
    with st.expander('Como foram calculadas as correlações'):
        st.subheader("Exemplo de cálculo")
        
        st.latex(r'''
        r = \frac{n(\sum xy) - (\sum x)(\sum y)}{\sqrt{[n\sum x^2 - (\sum x)^2][n\sum y^2 - (\sum y)^2]}}
        ''')

        # Explicação dos componentes da fórmula
        st.markdown("Onde:")
        st.latex(r'''
        \begin{align*}
        r & \text{ é o coeficiente de correlação de Pearson} \\
        n & \text{ é o número de pares de valores} \\
        \sum xy & \text{ é a soma do produto de cada par de valores} \\
        \sum x & \text{ é a soma dos valores da variável } x \\
        \sum y & \text{ é a soma dos valores da variável } y \\
        \sum x^2 & \text{ é a soma dos quadrados dos valores da variável } x \\
        \sum y^2 & \text{ é a soma dos quadrados dos valores da variável } y \\
        \end{align*}
        ''')
        
    
        # Valores hipotéticos para as variáveis x e y
        x = [10, 20, 30, 40, 50]
        y = [5, 10, 15, 20, 25]

        # Soma dos Produtos
        sum_xy = sum([a * b for a, b in zip(x, y)])

        # Mostrando o cálculo na aplicação Streamlit
        st.markdown("1. **Soma dos Produtos**")
        st.latex(r'''
        \sum xy = (10 \times 5) + (20 \times 10) + (30 \times 15) + (40 \times 20) + (50 \times 25) = 50 + 200 + 450 + 800 + 1250 = 2750
        ''')
        # Somatório das Variáveis
        sum_x = sum(x)
        sum_y = sum(y)

        # Mostrando o cálculo na aplicação Streamlit
        st.markdown("2. **Somatório das Variáveis**")
        st.latex(r'\sum x = 10 + 20 + 30 + 40 + 50 = 150')
        st.latex(r'\sum y = 5 + 10 + 15 + 20 + 25 = 75')

        # Soma dos Quadrados
        sum_x2 = sum([a**2 for a in x])
        sum_y2 = sum([b**2 for b in y])

        # Mostrando o cálculo na aplicação Streamlit
        st.markdown("3. **Soma dos Quadrados**")
        st.latex(r'\sum x^2 = 10^2 + 20^2 + 30^2 + 40^2 + 50^2 = 100 + 400 + 900 + 1600 + 2500 = 5500')
        st.latex(r'\sum y^2 = 5^2 + 10^2 + 15^2 + 20^2 + 25^2 = 25 + 100 + 225 + 400 + 625 = 1375')

        # Número de pares
        n = len(x)

        # Mostrando o cálculo na aplicação Streamlit
        st.markdown("4. **Número de Pares**")
        st.latex(r'n = \text{Número de pares de valores} = 5')

        # Aplicação da Fórmula
        r = (n * sum_xy - sum_x * sum_y) / ((n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2))**0.5

        # Mostrando o cálculo na aplicação Streamlit
        st.markdown("5. **Aplicação da Fórmula**")
        st.latex(r'''
        r = \frac{n(\sum xy) - (\sum x)(\sum y)}{\sqrt{[n\sum x^2 - (\sum x)^2][n\sum y^2 - (\sum y)^2]}}
        ''')
        st.latex(r'''
        r = \frac{5 \times 2750 - 150 \times 75}{\sqrt{[5 \times 5500 - 150^2][5 \times 1375 - 75^2]}}
        ''')
        st.latex(r'''
        r = \frac{13750 - 11250}{\sqrt{[27500 - 22500][6875 - 5625]}}
        ''')
        st.latex(r'''
        r = \frac{2500}{\sqrt{5000 \times 1250}}
        ''')
        st.latex(r'''
        r = \frac{2500}{2500}
        ''')
        st.latex(r'''
        r = 1
        ''')
        st.write(f"Coeficiente de Correlação de Pearson ( r = {r} )")

    # Função para criar gráficos de correlação
    def plot_correlacao(x, y, xlabel, ylabel, title):
        fig = px.scatter(x=x, y=y, trendline='ols', labels={'x': xlabel, 'y': ylabel}, title=title)
        return fig

    # Apresentação das correlações calculadas
    
    # Correlação: Teto Total vs Média Complexidade
    st.subheader("Correlação: Teto Total vs Média Complexidade")
    fig1 = plot_correlacao(teto_total, media_complexidade, 'Teto Total', 'Média Complexidade', 'Correlação: Teto Total vs Média Complexidade')
    st.plotly_chart(fig1)
    st.markdown("""
    ###### Análise da Correlação: Teto Total vs Média Complexidade
    O gráfico revela uma correlação positiva, porém fraca, indicada pela linha de tendência ascendente e pela dispersão considerável dos pontos. Observa-se que, de modo geral, a um aumento no Teto Total corresponde um aumento nos valores de Média Complexidade, o que seria esperado. Contudo, a dispersão dos pontos sugere que outros fatores, além do Teto Total, influenciam significativamente os valores de Média Complexidade. Essa correlação, embora positiva, indica a necessidade de uma análise mais aprofundada para entender as nuances dessa relação e os fatores que contribuem para a variação nos valores de Média Complexidade, a fim de otimizar a alocação de recursos e garantir a efetividade dos serviços prestados.    """)


    # Correlação: Teto Total vs Alta Complexidade
    st.subheader("Correlação: Teto Total vs Alta Complexidade")
    fig2 = plot_correlacao(teto_total, alta_complexidade, 'Teto Total', 'Alta Complexidade', 'Correlação: Teto Total vs Alta Complexidade')
    st.plotly_chart(fig2)
    st.markdown("""
    ###### Análise da Correlação: Teto Total vs Alta Complexidade
    Correlação praticamente inexistente, indicada pela linha de tendência quase horizontal e pela dispersão dos pontos, com muitos valores de Alta Complexidade iguais a zero. Isso sugere que o Teto Total não tem influência significativa sobre os valores de Alta Complexidade no município. Essa ausência de correlação pode ser explicada pela baixa demanda ou pela capacidade limitada de oferta de serviços de Alta Complexidade em Anchieta-ES, como indicado na análise anterior. A análise reforça a necessidade de investigar as razões para os baixos valores de Alta Complexidade, que podem estar relacionados a fatores como infraestrutura, disponibilidade de profissionais especializados ou encaminhamento de pacientes para outros municípios.    """)


    # Correlação: Teto Total vs Não se Aplica
    st.subheader("Correlação: Teto Total vs Não se Aplica")
    fig3 = plot_correlacao(teto_total, nao_se_aplica, 'Teto Total', 'Não se Aplica', 'Correlação: Teto Total vs Não se Aplica')
    st.plotly_chart(fig3)
    st.markdown("""
    ###### Análise da Correlação: Teto Total vs Não se Aplica
    O gráfico revela uma correlação positiva, mas relativamente fraca, indicada pela linha de tendência ascendente e pela dispersão moderada dos pontos. Observa-se que, de modo geral, a um aumento no Teto Total corresponde um aumento nos valores "Não se Aplica". No entanto, a dispersão dos pontos, especialmente a presença de valores altos de "Não se Aplica" com Tetos Totais relativamente baixos, sugere que a relação não é linear e que outros fatores influenciam esses valores. Essa correlação pode indicar uma complexidade na classificação dos procedimentos ou uma variação nas regras de faturamento ao longo do tempo. Uma análise mais aprofundada, que considere esses fatores, é necessária para uma compreensão mais completa dessa relação e para a otimização da alocação de recursos.    """)


    # Correlação: Teto Total vs Total Ambulatorial
    st.subheader("Correlação: Teto Total vs Total Ambulatorial")
    fig4 = plot_correlacao(teto_total, total_ambulatorial, 'Teto Total', 'Total Ambulatorial', 'Correlação: Teto Total vs Total Ambulatorial')
    st.plotly_chart(fig4)
    st.markdown("""
    ###### Análise da Correlação: Teto Total vs Total Ambulatorial
    Correlação positiva, mas fraca, indicada pela linha de tendência ascendente e pela dispersão considerável dos pontos. Embora, de modo geral, a um aumento no Teto Total corresponda um aumento no Total Ambulatorial, a dispersão dos pontos sugere que essa relação não é fortemente linear e que outros fatores influenciam significativamente os valores do Total Ambulatorial. Essa correlação reforça a necessidade de uma análise mais aprofundada para entender as nuances dessa relação e os fatores que contribuem para a variação no Total Ambulatorial, incluindo a possível influência de subfinanciamento crônico, variações na demanda e a efetividade das políticas públicas de saúde ao longo do tempo. A correlação positiva, ainda que fraca, indica que o aumento do Teto Total é um passo importante, mas não suficiente, para garantir a melhoria dos serviços ambulatoriais em Anchieta-ES.    """)

    # Correlação: Teto Total vs Procedimentos Clínicos
    st.subheader("Correlação: Teto Total vs Procedimentos Clínicos")
    fig6 = plot_correlacao(teto_total, procedimentos_clinicos, 'Teto Total', 'Procedimentos Clínicos', 'Correlação: Teto Total vs Procedimentos Clínicos')
    st.plotly_chart(fig6)
    st.markdown("""
    ###### Análise da Correlação: Teto Total vs Procedimentos Clínicos
    Correlação negativa e moderada, indicada pela linha de tendência descendente e pela dispersão dos pontos. Observa-se que, de modo geral, a um aumento no Teto Total corresponde uma diminuição nos Procedimentos Clínicos, uma relação contra-intuitiva que sugere a influência de outros fatores não capturados pelo gráfico. Essa correlação negativa pode indicar uma possível ineficiência na alocação de recursos, onde o aumento do financiamento não se traduz em um aumento na realização de procedimentos clínicos. Além disso, a dispersão dos pontos reforça a necessidade de uma análise mais aprofundada para entender as causas dessa correlação e os fatores que impactam a realização de procedimentos clínicos em Anchieta-ES, como a demanda reprimida, a capacidade de oferta de serviços e a gestão dos recursos disponíveis.    """)

    # Correlação: Teto Total vs Procedimentos Cirúrgicos
    st.subheader("Correlação: Teto Total vs Procedimentos Cirúrgicos")
    fig7 = plot_correlacao(teto_total, procedimentos_cirurgicos, 'Teto Total', 'Procedimentos Cirúrgicos', 'Correlação: Teto Total vs Procedimentos Cirúrgicos')
    st.plotly_chart(fig7)
    st.markdown("""
    ###### Análise da Correlação: Teto Total vs Procedimentos Cirúrgicos
    Correlação negativa e fraca, indicada pela linha de tendência descendente e pela dispersão significativa dos pontos. Essa correlação sugere que, de modo geral, a um aumento no Teto Total corresponde uma diminuição nos Procedimentos Cirúrgicos, uma relação contra-intuitiva que demanda uma investigação mais aprofundada. A dispersão dos pontos, com uma concentração de valores mais altos de Procedimentos Cirúrgicos em Tetos Totais mais baixos, reforça a influência de outros fatores além do financiamento. Essa correlação negativa pode estar relacionada a questões como a capacidade de oferta de serviços cirúrgicos, a demanda reprimida por esses procedimentos, ou até mesmo a eficiência na gestão dos recursos. Uma análise mais detalhada, que considere esses fatores, é essencial para entender as causas dessa correlação e para orientar políticas públicas que visem a melhoria do acesso a procedimentos cirúrgicos em Anchieta-ES.    """)

# Página 5: Conclusão
if escolha == "V. Conclusão":
    st.title('Necessidade de Aumento do Teto MAC')

    st.markdown("""
    ## Conclusão Geral da Análise da Saúde do Município de Anchieta-ES e a Necessidade de Adequação do Teto MAC

    A análise da saúde do município de Anchieta-ES, com foco na relação entre o Teto MAC e a produção ambulatorial, revela um cenário que demanda atenção e medidas para garantir a sustentabilidade do sistema de saúde local. Os dados analisados, embora indiquem a necessidade de ajustes, mostram um descompasso entre o financiamento e a demanda por serviços ambulatoriais, sugerindo um possível subfinanciamento crônico que impacta a capacidade de atendimento e a qualidade da assistência prestada à população.

    ### Pontos de Atenção:

    - **Descompasso entre Teto MAC e Produção Ambulatorial:** A análise demonstrou que, embora o Teto MAC tenha apresentado crescimento ao longo dos anos, este se deu em ritmo inferior ao da demanda por serviços ambulatoriais, especialmente os de média complexidade. Longos períodos de estagnação do Teto MAC, como observado entre 2015 e 2018, coincidiram com momentos de esforço do município para manter a produção, mesmo diante de recursos limitados.
    - **Correlação Fraca ou Negativa com Indicadores de Produção:** As análises de correlação entre o Teto Total e diversos indicadores de produção (Média Complexidade, Alta Complexidade, "Não se Aplica", Total Ambulatorial, Procedimentos Clínicos e Procedimentos Cirúrgicos) revelaram correlações fracas, muitas vezes negativas e contra-intuitivas. Isso sugere que o aumento do Teto MAC, isoladamente, não se traduz automaticamente em melhoria na produção ambulatorial, indicando a influência de outros fatores, como a gestão dos recursos, a capacidade de oferta e a demanda reprimida.
    - **Queda nos Procedimentos Clínicos e Cirúrgicos:** A redução no número de procedimentos clínicos e cirúrgicos ao longo do período analisado, mesmo com o aumento do Total Ambulatorial, é um forte indicativo de que o financiamento atual pode ser insuficiente para atender às necessidades da população, levando a uma possível limitação na oferta de serviços e ao represamento da demanda.
    - **Impacto na Média Complexidade:** A análise detalhada por componente da produção ambulatorial evidenciou que os serviços de média complexidade, que representam a maior parte da demanda, foram os mais afetados pelos períodos de estagnação ou redução do Teto MAC.

    ### A Importância da Adequação do Financiamento:

    A análise da saúde de Anchieta-ES demonstra a necessidade premente de se reavaliar o financiamento destinado ao município. Um Teto MAC defasado, que não acompanha o crescimento populacional, o perfil epidemiológico e a demanda real por serviços de saúde, gera um ciclo vicioso de subfinanciamento, impactando negativamente a qualidade da assistência e a capacidade de resposta do sistema de saúde local.

    ### Recomendações:

    - **Revisão do Teto MAC:** Solicitar ao Ministério da Saúde a revisão do Teto MAC de Anchieta-ES, com base em dados atualizados de produção, demanda e custos dos procedimentos ambulatoriais, considerando as particularidades do município e a necessidade de garantir a sustentabilidade do sistema de saúde.
    - **Fortalecimento da Gestão:** Investir na melhoria da gestão dos recursos, com foco na eficiência, transparência e otimização dos processos, para garantir que o financiamento disponível seja utilizado da melhor forma possível.
    - **Monitoramento e Avaliação:** Implementar um sistema robusto de monitoramento e avaliação dos indicadores de saúde, incluindo a produção ambulatorial, a fim de identificar precocemente problemas e ajustar as estratégias de financiamento e gestão.
    - **Planejamento Estratégico:** Elaborar um plano estratégico para a saúde do município, com base em dados epidemiológicos, demográficos e de produção, que contemple as necessidades de investimento em infraestrutura, equipamentos, recursos humanos e capacitação profissional, com foco na ampliação do acesso e na melhoria da qualidade dos serviços ambulatoriais, especialmente os de média complexidade.

    ### Conclusão:

    A análise da saúde de Anchieta-ES evidencia a necessidade de uma adequação do financiamento destinado ao município. O aumento do Teto MAC em 2024, embora importante, mostrou-se insuficiente para corrigir a defasagem histórica e garantir a sustentabilidade do sistema de saúde local. Um Teto MAC compatível com a realidade da produção ambulatorial e com a crescente demanda por esses serviços é crucial para que Anchieta-ES possa cumprir seu papel na garantia do direito à saúde de seus cidadãos. Investir na melhoria da gestão, na qualificação dos profissionais, na infraestrutura e, fundamentalmente, na adequação do financiamento à real demanda por serviços de saúde é crucial para assegurar a sustentabilidade do sistema e a qualidade da assistência prestada à população de Anchieta-ES. A solicitação de aumento do Teto MAC, embasada em dados consistentes e em um planejamento estratégico sólido, é uma medida fundamental para que o município possa garantir o acesso universal e integral à saúde, conforme preconiza o SUS.
    """)





# Página 1: Evolução do Teto MAC
if escolha == "Introdução":
    st.title("Introdução")
    st.image('anchieta.jpg')
    st.markdown("""
    ## História
    **Anchieta**, situada no litoral do estado do Espírito Santo, possui uma história rica e fascinante. A cidade foi fundada oficialmente em **1569** por padres jesuítas, com o estabelecimento do aldeamento de Reritiba, liderado por São José de Anchieta. O nome atual da cidade é uma homenagem a este importante missionário jesuíta.

    ## Demografia
    Atualmente, Anchieta possui uma população de aproximadamente **29.779 habitantes**. A cidade é composta por diversos bairros e comunidades, como Iriri, Ubu, Mãe-Bá, Castelhanos, Inhaúma e Jabaquara. Durante a alta temporada turística, a população da cidade pode aumentar significativamente.

    ## Economia
    A economia de Anchieta é impulsionada principalmente pelo **turismo**, devido às suas belas praias e à rica herança histórica. Além do turismo, a cidade conta com atividades de **comércio**, **indústria** (especialmente siderurgia) e **pesca**. A exploração de recursos naturais e o cultivo de mariscos também desempenham um papel importante na economia local.

    ## Educação e Saúde
    Anchieta dispõe de um sistema educacional que inclui **escolas públicas** e privadas de ensino fundamental e médio, além de algumas instituições de **ensino técnico**. Na área da saúde, a cidade conta com **postos de saúde**, **hospitais** e **clínicas particulares**, garantindo atendimento à população local e aos visitantes.

    ## Cultura e Turismo
    Conhecida por suas praias encantadoras, Anchieta é um dos destinos turísticos mais procurados do Espírito Santo. Entre as praias mais conhecidas estão a **Praia de Castelhanos**, **Praia de Ubu**, **Praia de Iriri** e **Praia dos Padres**. A cidade também é famosa pelos eventos culturais que ocorrem ao longo do ano, atraindo turistas de diversas partes do Brasil. Além disso, Anchieta oferece opções de **ecoturismo** e **turismo religioso**, com trilhas, visitas ao Santuário Nacional de São José de Anchieta e outros pontos históricos.

    """)