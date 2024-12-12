import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd  # Add pandas import
import plotly.graph_objs as go

# Anos
anos = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Valores de média complexidade
media_complexidade = [
    772092,  # 2012
    558529,  # 2013
    517025,  # 2014
    447233,  # 2015
    503369,  # 2016
    537947,  # 2017
    548146,  # 2018
    354228,  # 2019
    164705,  # 2020
    279620,  # 2021
    434067,  # 2022
    623842,  # 2023
    605166   # 2024
]

# Valores de alta complexidade
alta_complexidade = [
    12432,  # 2012
    12616,  # 2013
    13128,  # 2014
    13647,  # 2015
    13982,  # 2016
    14555,  # 2017
    15253,  # 2018
    16795,  # 2019
    16783,  # 2020
    16377,  # 2021
    16087,  # 2022
    17924,  # 2023
    13411   # 2024
]

# Valores que não se aplicam
nao_se_aplica = [
    2506,  # 2012
    2880,  # 2013
    3141,  # 2014
    4710,  # 2015
    5105,  # 2016
    2158,  # 2017
    4514,  # 2018
    3289,  # 2019
    5713,  # 2020
    2257,  # 2021
    3341,  # 2022
    4201,  # 2023
    3408   # 2024
]

# Procedimentos clínicos
procedimentos_clinicos = [
    3924,  # 2012
    885,   # 2013
    480,   # 2014
    1845,  # 2015
    1989,  # 2016
    2102,  # 2017
    2091,  # 2018
    2072,  # 2019
    2037,  # 2020
    2209,  # 2021
    2453,  # 2022
    3112,  # 2023
    2607   # 2024
]

# Procedimentos cirúrgicos
procedimentos_cirurgicos = [
    432,  # 2012
    56,   # 2013
    261,  # 2014
    1663, # 2015
    1397, # 2016
    1292, # 2017
    1372, # 2018
    1401, # 2019
    1288, # 2020
    1135, # 2021
    994,  # 2022
    1341, # 2023
    1099  # 2024
]

# Valores sem incentivo
valores_sem_incentivo = [
    1050000,  # 2012
    2100000,  # 2013
    2115768.57,  # 2014
    2123542.48,  # 2015
    2169129.98,  # 2016
    2116267.7,  # 2017
    2911596.1,  # 2018
    4075804.36,  # 2019
    4099247.93,  # 2020
    3001379.16,  # 2021
    2901379.16,  # 2022
    2901379.16,  # 2023
    9431721.46   # 2024 (atualizado)
]

# Valores de incentivos
valores_incentivos = [
    0,        # 2012
    0,        # 2013
    0,        # 2014
    0,        # 2015
    0,        # 2016
    0,        # 2017
    0,        # 2018
    0,        # 2019
    0,        # 2020
    0,        # 2021
    0,        # 2022
    26909.25, # 2023
    0         # 2024
]

# Teto total
teto_total = [
    1050000,       # 2012
    2100000,       # 2013
    2115768.57,    # 2014
    2123542.48,    # 2015
    2169129.98,    # 2016
    2116267.7,     # 2017
    2911596.1,     # 2018
    4075804.36,    # 2019
    4099247.93,    # 2020
    3001379.16,    # 2021
    2901379.16,    # 2022
    2928288.41,    # 2023
    9431721.46     # 2024 (atualizado)
]

# Calculando os totais (fora do dicionário, como listas)
total_ambulatorial = [sum(x) for x in zip(media_complexidade, alta_complexidade, nao_se_aplica)]
total_procedimentos = [x + y for x, y in zip(procedimentos_clinicos, procedimentos_cirurgicos)]

# Criação do menu de seleção de páginas na barra lateral
paginas = ["Introdução", "I. Evolução do Teto MAC", "II. MAC x Procedimentos Hospitalares", "III. MAC x Produção Ambulatorial", "IV. Correlação Produção vs Recursos", "V. UPA 24h", "VI. Conclusão"]

# Adicionando as logos na sidebar
st.sidebar.image('logo_colorida_mg.png')
st.sidebar.image('logo_guarapari.png', channels="BGR")
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
    ### Análise da Evolução do Teto MAC em Guarapari-ES

    1. **Crescimento ao Longo dos Anos (2012-2024)**:
    - O Teto MAC aumentou de **1.050.000,00** em 2012 para **R$ 9.431.721,46** em 2024.
    - Esse crescimento não foi constante, com flutuações significativas ao longo dos anos, refletindo a complexidade da gestão de recursos, as políticas públicas e as necessidades de saúde da população de Guarapari.

    2. **Contribuição dos Incentivos**:
    - Em 2023, houve um acréscimo de **R$ 107.637,00** referente ao incentivo "Saúde Mental-RAPS".
    - Esse incentivo demonstra a importância de buscar ativamente por esses recursos adicionais.

    3. **Variações nos Valores Sem Incentivo**:
    - As mudanças nos valores "Sem Incentivo" se devem a realocações de recursos financeiros dentro do próprio Teto MAC.
    - Essas variações foram significativas e frequentes, com remanejamentos em diversos anos, mostrando que os recursos base passaram por muitas realocações e ajustes internos significativos.
    - Destaca-se um remanejamento significativo em 2018 e outro recente em 2024, ambos destinados à "Média e Alta Complexidade".

    4. **Impacto da Demanda por Serviços**:
    - A análise reforça a tendência geral de aumento na demanda por serviços ambulatoriais e procedimentos.
    - Apesar das flutuações, a tendência de crescimento na demanda por serviços de saúde justifica a necessidade de um aumento no Teto MAC para garantir o atendimento adequado à população.
    - Remanejamentos frequentes indicam um esforço contínuo para adequar o financiamento à demanda real e às prioridades de saúde do município.

    ### Direcionamento para 2025
    - **Aprimorar a Captação de Incentivos**: Continuar explorando e captando incentivos específicos, como os de programas de saúde, pode ser uma estratégia eficaz. Identificar novas oportunidades de incentivo pode contribuir significativamente para o aumento do Teto MAC.
    - **Gestão Eficiente dos Recursos**: Revisar e ajustar continuamente os remanejamentos intra para garantir que os recursos estejam sendo utilizados de forma eficiente. Uma gestão dinâmica e transparente pode otimizar a alocação de recursos e justificar aumentos futuros.
    - **Monitoramento das Políticas Públicas**: Acompanhar de perto as políticas públicas e as portarias que influenciam a alocação de recursos pode ajudar a antecipar mudanças e ajustar as estratégias de financiamento conforme necessário.
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
   ### Análise da Relação entre o Teto MAC e a Produção Hospitalar em Guarapari-ES: Considerações sobre os Custos Hospitalares

    A análise da relação entre o Teto MAC e a produção hospitalar em Guarapari-ES, entre 2012 e 2024, revela um descompasso entre financiamento e demanda, agravado pelos custos hospitalares.

    #### Descompasso entre Financiamento e Produção

    - **Crescimento do Teto MAC**: O Teto MAC cresceu ao longo dos anos, mas apresentou longos períodos de estagnação. Aumentos significativos ocorreram apenas em 2019 e, especialmente, em 2024.

    - **Produção Hospitalar**: A produção hospitalar teve variações com uma tendência geral de crescimento, demonstrando a capacidade do município de manter e aumentar a produção, mesmo diante de recursos limitados.

    #### Análise por Período

    - **2012-2014**: Aumento nominal do Teto MAC foi menor devido aos custos hospitalares.
    - **2015-2018**: Estagnação do Teto MAC forçou o município a absorver aumentos dos custos.
    - **2019-2020**: Aumento do Teto MAC limitado pelos custos hospitalares crescentes.
    - **2021-2023**: Redução nominal do Teto MAC, aumento dos custos e esforço local para manter serviços.
    - **2024**: Aumento significativo do Teto MAC, mas o impacto real é reduzido devido aos custos acumulados.

    #### Implicações e Justificativa para o Aumento do Teto MAC

    - **Subfinanciamento Crônico**: O Teto MAC cresceu a um ritmo inferior à demanda e aos custos hospitalares.
    - **Erosão do Poder de Compra**: Longos períodos de estagnação representam uma perda significativa do poder de compra, dificultando a aquisição de insumos e a contratação de profissionais.
    - **Necessidade de Correção**: O aumento do Teto MAC em 2024 é necessário, mas precisa de ajustes periódicos para acompanhar os custos hospitalares.
    - **Distorção Histórica**: A defasagem entre o crescimento do Teto MAC e os custos hospitalares precisa ser corrigida para garantir financiamento adequado.

    #### Conclusão

    O município de Guarapari-ES demonstrou capacidade de manter e aumentar a produção hospitalar mesmo com recursos limitados. O aumento do Teto MAC em 2024 é crucial, mas não resolve a defasagem histórica. É necessário um Teto MAC que acompanhe a demanda e os custos hospitalares para garantir a sustentabilidade e qualidade do atendimento.
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


    st.markdown("""
    ### Análise da Relação entre o Teto MAC e a Produção Ambulatorial em Guarapari-ES

    A análise da relação entre o Teto MAC e a produção ambulatorial em Guarapari-ES, detalhada pelos valores de média e alta complexidade e por aqueles que "não se aplicam", revela nuances importantes sobre o financiamento e a prestação de serviços ambulatoriais no município.

    #### 1. Visão Geral dos Dados

    - **Teto MAC**: Como já analisado anteriormente, o Teto MAC apresentou longos períodos de estagnação, com aumentos mais significativos em 2019 e, principalmente, em 2024.

    - **Produção Ambulatorial (Total Ambulatorial)**: O somatório dos valores de média complexidade, alta complexidade e "não se aplica" (que chamaremos de "Total Ambulatorial") mostra uma tendência de crescimento ao longo do período (2012-2024), com flutuações em alguns anos.

    #### 2. Análise Detalhada por Componente

    - **Média Complexidade**: Os valores de média complexidade representam a maior parte da produção ambulatorial. Eles apresentam um comportamento irregular, com quedas acentuadas em alguns anos (como 2013, 2014, 2019 e 2020) e picos em outros (como 2012, 2018 e 2023).

    - **Alta Complexidade**: Os valores de alta complexidade são significativamente menores que os de média complexidade, mas mostram uma tendência de crescimento mais consistente ao longo do tempo, com exceção de uma leve queda em 2021 e 2022, e uma queda mais expressiva em 2024.

    - **Não se Aplica**: Os valores classificados como "não se aplica" também são relativamente baixos, mas apresentam variações consideráveis, com picos em 2015, 2016, 2020 e 2023.

    #### 3. Relação entre Teto MAC e Produção Ambulatorial

    - **Descompasso**: Assim como na análise da produção hospitalar, observa-se um descompasso entre o Teto MAC e a produção ambulatorial. Enquanto o Total Ambulatorial apresenta uma tendência de crescimento, o Teto MAC permaneceu estagnado por longos períodos.

    - **Impacto nos Serviços de Média Complexidade**: As flutuações nos valores de média complexidade podem estar relacionadas às variações no financiamento via Teto MAC. Os períodos de estagnação ou redução do Teto MAC podem ter levado a uma diminuição na oferta de serviços de média complexidade.

    - **Crescimento da Alta Complexidade**: O crescimento mais consistente dos valores de alta complexidade, mesmo em períodos de estagnação do Teto MAC, sugere uma possível priorização desses serviços, talvez devido à sua maior complexidade e custo.

    - **Valores "Não se Aplica"**: A variação nos valores "não se aplica" pode refletir mudanças nas regras de faturamento, na classificação dos procedimentos ou em necessidades pontuais do município.

    #### 4. Análise por Período

    - **2012-2014**: O Teto MAC teve um aumento, mas a produção ambulatorial (Total Ambulatorial) diminuiu, principalmente devido à queda nos valores de média complexidade.

    - **2015-2018**: O Teto MAC permaneceu estagnado, mas a produção ambulatorial se recuperou, com crescimento nos valores de média e alta complexidade. Isso sugere um esforço do município para manter os serviços, mesmo com financiamento limitado.

    - **2019-2020**: O aumento do Teto MAC em 2019 não se refletiu em um aumento proporcional da produção ambulatorial, que apresentou uma queda significativa em 2020, principalmente nos valores de média complexidade e "não se aplica".

    - **2021-2023**: O Teto MAC diminuiu, mas a produção ambulatorial voltou a crescer, atingindo seu pico em 2023. Isso reforça a ideia de um esforço local para manter os serviços, apesar das restrições financeiras.

    - **2024**: O aumento expressivo do Teto MAC em 2024 coincide com uma leve queda na produção ambulatorial. Isso pode ser explicado por diversos fatores, como a sazonalidade, a conclusão de mutirões de procedimentos ou a necessidade de um período de adaptação ao novo patamar de financiamento.

    #### 5. Implicações e Justificativa para o Aumento do Teto MAC

    - **Subfinanciamento da Atenção Ambulatorial**: A análise sugere que a atenção ambulatorial em Guarapari-ES pode ter sofrido com subfinanciamento crônico, com o Teto MAC crescendo em um ritmo inferior à demanda por serviços ambulatoriais, especialmente os de média complexidade.

    - **Necessidade de Investimentos**: O aumento do Teto MAC em 2024 é um passo importante para corrigir essa distorção e permitir investimentos na ampliação e qualificação dos serviços ambulatoriais.

    - **Priorização de Serviços**: A análise dos diferentes componentes da produção ambulatorial pode auxiliar na definição de prioridades para a alocação de recursos, buscando um equilíbrio entre a oferta de serviços de média e alta complexidade.

    #### Conclusão

    A relação entre o Teto MAC e a produção ambulatorial em Guarapari-ES, entre 2012 e 2024, foi marcada por um descompasso entre financiamento e demanda. O município demonstrou resiliência ao manter e, em alguns períodos, aumentar a produção ambulatorial, mesmo em face de recursos limitados. O aumento significativo do Teto MAC em 2024 é fundamental para corrigir essa distorção histórica e garantir a sustentabilidade do sistema de saúde local, permitindo investimentos na atenção ambulatorial, especialmente nos serviços de média complexidade. A análise reforça a necessidade de um Teto MAC condizente com a realidade da produção ambulatorial e com a crescente demanda por esses serviços em Guarapari, justificando os esforços para sua ampliação e adequação contínua, a fim de garantir o acesso universal e integral à saúde, conforme preconiza o SUS.

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
    O gráfico de correlação entre o Teto Total e a Média Complexidade em Guarapari-ES revela uma correlação fraca e negativa, indicada pela linha de tendência descendente e pela dispersão dos pontos. Esse resultado contra-intuitivo, que sugere que aumentos no Teto Total estão associados a uma tendência de diminuição na produção de Média Complexidade, corrobora as análises anteriores sobre um possível subfinanciamento crônico e a necessidade de adequação do Teto MAC. A correlação negativa levanta questões importantes sobre a gestão, a alocação de recursos e a influência de fatores externos, demandando uma investigação mais aprofundada para garantir a efetiva aplicação dos recursos e a melhoria dos serviços de média complexidade, essenciais para o acesso integral à saúde.
    """)


    # Correlação: Teto Total vs Alta Complexidade
    st.subheader("Correlação: Teto Total vs Alta Complexidade")
    fig2 = plot_correlacao(teto_total, alta_complexidade, 'Teto Total', 'Alta Complexidade', 'Correlação: Teto Total vs Alta Complexidade')
    st.plotly_chart(fig2)
    st.markdown("""
    ###### Análise da Correlação: Teto Total vs Alta Complexidade
    O gráfico de correlação entre o Teto Total e a Alta Complexidade em Guarapari-ES revela uma correlação positiva, porém fraca, indicada pela linha de tendência ascendente e pela dispersão dos pontos. Isso sugere que aumentos no Teto Total tendem a estar associados a aumentos na produção de Alta Complexidade, mas de forma limitada, possivelmente devido a fatores como a priorização desses serviços, seus custos unitários elevados e a influência de variáveis externas como a disponibilidade de profissionais e infraestrutura especializada. Embora mais alinhada com as expectativas do que a correlação com a Média Complexidade, a fraca correlação positiva reforça a complexidade do financiamento da saúde e a necessidade de se considerar múltiplas variáveis além do Teto Total.
    """)


    # Correlação: Teto Total vs Não se Aplica
    st.subheader("Correlação: Teto Total vs Não se Aplica")
    fig3 = plot_correlacao(teto_total, nao_se_aplica, 'Teto Total', 'Não se Aplica', 'Correlação: Teto Total vs Não se Aplica')
    st.plotly_chart(fig3)
    st.markdown("""
    ###### Análise da Correlação: Teto Total vs Não se Aplica
    O gráfico de correlação entre o Teto Total e os valores "Não se Aplica" em Guarapari-ES revela uma correlação positiva, porém fraca, sugerindo que aumentos no Teto Total podem estar levemente associados a aumentos nesses valores, embora a dispersão dos pontos indique a influência de outros fatores. A interpretação dessa correlação requer cautela devido à natureza genérica da categoria "Não se Aplica", que pode englobar uma variedade de registros, incluindo mudanças na classificação de procedimentos, pagamentos retroativos ou ajustes de faturamento. A análise sugere a necessidade de um olhar mais detalhado sobre os tipos de registros classificados como "Não se Aplica" para uma compreensão mais precisa dessa correlação.
    """)


    # Correlação: Teto Total vs Total Ambulatorial
    st.subheader("Correlação: Teto Total vs Total Ambulatorial")
    fig4 = plot_correlacao(teto_total, total_ambulatorial, 'Teto Total', 'Total Ambulatorial', 'Correlação: Teto Total vs Total Ambulatorial')
    st.plotly_chart(fig4)
    st.markdown("""
    ###### Análise da Correlação: Teto Total vs Total Ambulatorial
    O gráfico de correlação entre o Teto Total e o Total Ambulatorial em Guarapari-ES revela uma correlação negativa e fraca, sugerindo que aumentos no Teto Total estão associados a uma tendência de diminuição na produção ambulatorial total. Esse resultado contra-intuitivo é consistente com a correlação negativa observada entre o Teto Total e a Média Complexidade, que compõe a maior parte do Total Ambulatorial. O subfinanciamento crônico, a possível priorização da Alta Complexidade, problemas de gestão e fatores externos são possíveis explicações para essa correlação, reforçando a necessidade de uma análise aprofundada sobre o financiamento e a gestão da saúde no município para garantir a efetiva aplicação dos recursos e a expansão da produção ambulatorial.
    """)


    # Correlação: Teto Total vs Procedimentos Clínicos
    st.subheader("Correlação: Teto Total vs Procedimentos Clínicos")
    fig6 = plot_correlacao(teto_total, procedimentos_clinicos, 'Teto Total', 'Procedimentos Clínicos', 'Correlação: Teto Total vs Procedimentos Clínicos')
    st.plotly_chart(fig6)
    st.markdown("""
    ###### Análise da Correlação: Teto Total vs Procedimentos Clínicos
    O gráfico de correlação entre o Teto Total e os Procedimentos Clínicos em Guarapari-ES indica uma correlação positiva, porém fraca, sugerindo que aumentos no Teto Total tendem a estar associados a aumentos nos Procedimentos Clínicos, mas de forma limitada. A dispersão dos pontos reforça a influência de outros fatores além do financiamento, como a demanda, a capacidade instalada, a disponibilidade de recursos e a gestão. Embora mais alinhado com as expectativas do que as correlações negativas observadas anteriormente, a fraca correlação positiva ressalta a complexidade do cenário e a necessidade de se considerar múltiplas variáveis para garantir a expansão e a efetividade dos Procedimentos Clínicos.
    """)


    # Correlação: Teto Total vs Procedimentos Cirúrgicos
    st.subheader("Correlação: Teto Total vs Procedimentos Cirúrgicos")
    fig7 = plot_correlacao(teto_total, procedimentos_cirurgicos, 'Teto Total', 'Procedimentos Cirúrgicos', 'Correlação: Teto Total vs Procedimentos Cirúrgicos')
    st.plotly_chart(fig7)
    st.markdown("""
    ###### Análise da Correlação: Teto Total vs Procedimentos Cirúrgicos
    O gráfico de correlação entre o Teto Total e os Procedimentos Cirúrgicos em Guarapari-ES apresenta uma correlação positiva, porém fraca, indicando que aumentos no Teto Total tendem a estar associados a aumentos nos Procedimentos Cirúrgicos, mas de forma limitada. A dispersão dos pontos sugere a influência significativa de outros fatores, como os custos elevados e a complexidade desses procedimentos, a disponibilidade de infraestrutura e profissionais especializados, e a demanda específica por diferentes tipos de cirurgias. Similar à correlação observada com os Procedimentos Clínicos, a fraca correlação positiva com os Procedimentos Cirúrgicos reforça a complexidade do financiamento da saúde e a necessidade de uma abordagem multifatorial para garantir a expansão e a efetividade desses serviços.
    """)

# Página 5: UPA 24h
if escolha == "V. UPA 24h":
    st.title('UPA 24h')
    st.image('UPA-Guarapari-1024x576-1-1.jpg')
    st.subheader('**ANÁLISE CONFORME PORTARIA GM/MS N. 10 – 2017**')
   
    # Dados
    anos = ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]

    procedimentos = {
        "0301060029 Atendimento de Urgência com Observação até 24 horas em Atenção Especializada": [813, 45, 280, 875, 763, 39935, 51373],
        "0301060096 Atendimento Médico em Unidade de Pronto Atendimento": [52956, 2956, 153, 0, 0, 10330, 14700],
        "0301060100 Atendimento Ortopédico com Imobilização Provisória": [615, 763, 132, 252, 274, 91, 473],
        "0301060118 Acolhimento com Classificação de Risco": [46821, 5523, 30476, 36875, 48043, 67582, 63942]
    }

    # Calcular a soma dos três primeiros procedimentos
    soma_procedimentos = [sum(values) for values in zip(
        procedimentos["0301060029 Atendimento de Urgência com Observação até 24 horas em Atenção Especializada"],
        procedimentos["0301060100 Atendimento Ortopédico com Imobilização Provisória"],
        procedimentos["0301060096 Atendimento Médico em Unidade de Pronto Atendimento"]
    )]


    # Meta anual de produção
    meta_anual = 67500

    # Gráfico para Atendimento de Urgência e Unidade de Pronto Atendimento
    fig1 = go.Figure()
    for procedimento, valores in procedimentos.items():
        fig1.add_trace(go.Scatter(x=anos, y=valores, mode='lines+markers', name=procedimento))

    # Adicionar a linha para a soma dos três primeiros procedimentos
    fig1.add_trace(go.Scatter(x=anos, y=soma_procedimentos, mode='lines+markers', name="Soma dos Três Primeiros Procedimentos", line=dict(color='purple')))

    fig1.add_shape(type="line", x0=anos[0], y0=meta_anual, x1=anos[-1], y1=meta_anual, line=dict(color="red", width=2, dash="dash"), name='Meta Anual')

    fig1.update_layout(title="PRODUÇÃO DA UPA II DR JOAO BATISTA DE ALMEIDA NETO",
                    xaxis_title="Ano", yaxis_title="Quantidade Aprovada",
                    legend_title="Procedimentos", legend=dict(y=-1, x=0),
                    xaxis=dict(tickmode='linear'), yaxis=dict(showgrid=True))

    st.plotly_chart(fig1)
    st.caption('Fonte: TABWIN/MS')

    # Texto explicativo
    st.markdown(
    """
    **Análise da Produção da UPA Dr. João Batista de Almeida Neto em Guarapari e sua Relação com o Financiamento via Portaria GM/MS nº 10/2017**

    A análise da produção da UPA Dr. João Batista de Almeida Neto em Guarapari revela uma situação preocupante e inconsistente. Os dados disponíveis, referentes aos anos de 2018 a 2024, apresentam flutuações significativas e, em todos os anos analisados, a produção se encontra abaixo do mínimo exigido pela Portaria GM/MS nº 10/2017 para o Porte IV. Essa constatação levanta questionamentos sobre a adequação do atual enquadramento da UPA e, consequentemente, sobre a suficiência do financiamento recebido.

    ### Impacto da Portaria 10/2017 e a Urgência na Validação dos Dados

    A Portaria 10/2017 estabelece critérios claros de produção mínima anual para cada porte de UPA, atrelando diretamente o valor do custeio repassado pelo Ministério da Saúde a esses critérios. A produção da UPA de Guarapari, conforme os dados analisados, não atinge o mínimo necessário para o Porte IV em nenhum dos anos considerados, tanto para o somatório dos procedimentos médicos (excluindo a classificação de risco) quanto para o acolhimento com classificação de risco. Essa discrepância entre a produção real e a exigida pela Portaria sinaliza um possível subfinanciamento da unidade.

    ### Inconsistências nos Dados e Possíveis Causas

    As grandes variações na produção anual observadas nos dados fornecidos, especialmente a queda abrupta em 2019, 2020, 2021 e 2022, sugerem inconsistências que precisam ser urgentemente investigadas. Diversos fatores podem contribuir para essa situação, incluindo:

    - Flutuações na demanda: Sendo Guarapari um município turístico, a demanda por serviços de saúde pode variar sazonalmente.
    - Problemas de gestão e organização do trabalho: Dificuldades na organização interna da UPA, na integração com a rede de atenção à saúde e na alocação de recursos humanos e materiais podem impactar a produção.
    - Capacidade instalada: Limitações na infraestrutura física, equipamentos e número de profissionais podem restringir a capacidade de atendimento da UPA.
    - Subnotificação de procedimentos: A qualidade do registro dos procedimentos é um ponto crucial. A subnotificação, ou seja, a falta de registro adequado dos atendimentos realizados, pode levar a uma subestimação da produção real da UPA, resultando em uma classificação de porte inferior e, consequentemente, em um financiamento inadequado.

    ### A Necessidade de Reclassificação e Adequação do Financiamento

    A situação atual da UPA de Guarapari exige uma ação imediata. É fundamental:

    - **Validar os dados de produção:** Buscar junto à Secretaria Municipal de Saúde a confirmação dos dados de produção da UPA, com a série histórica completa, para garantir a precisão da análise.
    - **Investigar as causas das inconsistências:** Realizar um diagnóstico detalhado para identificar os fatores que contribuem para as flutuações na produção e para a possível subnotificação de procedimentos.
    - **Reavaliar o porte da UPA:** Com base em dados validados e em uma análise criteriosa da capacidade instalada e da demanda real, solicitar a reclassificação da UPA para um porte compatível com a sua realidade.
    - **Adequar o financiamento:** Garantir que o financiamento da UPA seja condizente com o seu porte e com a sua produção, assegurando os recursos necessários para o seu pleno funcionamento.
    - **Melhorar o sistema de registro:** Implementar medidas para aprimorar a qualidade do registro dos procedimentos realizados na UPA, garantindo a fidedignidade dos dados de produção.

    ### Conclusão

    A análise da produção da UPA de Guarapari, embora baseada em dados que necessitam de validação, indica que a unidade não atinge os patamares mínimos de produção exigidos para o Porte IV, o que sugere um possível subdimensionamento e subfinanciamento. A confirmação dos dados, a investigação das causas das inconsistências e a reclassificação da UPA, se necessária, são medidas urgentes para garantir a sustentabilidade financeira da unidade e o acesso adequado da população aos serviços de saúde. O aumento do Teto MAC, caso seja comprovada a necessidade, deve ser acompanhado de um plano de ação que contemple a melhoria da gestão, da organização do trabalho e da qualidade do registro dos procedimentos, assegurando a eficiência na aplicação dos recursos e o cumprimento das metas estabelecidas pela Portaria 10/2017.

    Este texto revisado enfatiza a necessidade de validação dos dados e investigação das inconsistências, evitando conclusões precipitadas sobre o porte da UPA. Ele destaca a importância de uma análise criteriosa para embasar um possível pedido de reclassificação e aumento do Teto MAC.
    """
    )


# Página 6: Conclusão
if escolha == "VI. Conclusão":
    st.title('Necessidade de Aumento do Teto MAC')

    st.markdown("""
    ## Conclusão Geral da Análise da Saúde do Município de Guarapari-ES e a Necessidade de Adequação do Teto MAC

    A análise da saúde do município de Guarapari-ES, com atenção especial à produção e ao financiamento da UPA Dr. João Batista de Almeida Neto, revela um cenário que demanda atenção e medidas para garantir a sustentabilidade do sistema de saúde local. Embora os dados analisados apresentem inconsistências que necessitam de validação, eles sugerem uma demanda por serviços de urgência e emergência que pode estar acima da capacidade de financiamento atual do município, considerando os parâmetros da Portaria GM/MS nº 10/2017.

    ### Pontos de Atenção:

    - **Inconsistências na Produção da UPA:** A UPA de Guarapari, principal porta de entrada para atendimentos de urgência e emergência, apresentou flutuações significativas na produção entre 2018 e 2024. Em alguns anos, a produção ficou muito abaixo do mínimo exigido para o maior porte previsto na Portaria (Porte VIII), enquanto em outros, superou esses valores, indicando uma possível operação acima da capacidade prevista para esse porte. Essas variações demandam uma investigação aprofundada para identificar suas causas, que podem incluir problemas de registro, variações sazonais na demanda (comum em cidades turísticas) ou até mesmo questões de gestão e organização interna.

    - **Possível Subdimensionamento do Porte da UPA:** Ainda que a validação dos dados seja crucial, a produção registrada em alguns anos sugere que a UPA opera, na prática, com uma demanda superior àquela prevista para o seu porte atual, o que pode indicar um subdimensionamento e, consequentemente, um financiamento inadequado.

    - **Impacto no Acesso e na Qualidade:** Um financiamento insuficiente pode comprometer a capacidade de atendimento da UPA, impactando negativamente o acesso da população aos serviços de urgência e emergência e a qualidade da assistência prestada.

    ### A Importância da Adequação do Financiamento:

    A análise da UPA de Guarapari, embora necessite de aprofundamento, serve como um indicativo importante da necessidade de se reavaliar o financiamento da saúde no município como um todo. Um Teto MAC defasado, que não acompanha o crescimento populacional, o perfil epidemiológico e a demanda real por serviços de saúde, pode gerar um ciclo vicioso de subfinanciamento, impactando negativamente a qualidade da assistência e a capacidade de resposta do sistema de saúde local.

    ### Recomendações:

    - **Validação e Análise Detalhada dos Dados:** É fundamental que a Secretaria Municipal de Saúde de Guarapari realize um levantamento completo e atualizado dos dados de produção de todos os seus estabelecimentos de saúde, não se restringindo apenas à UPA. Essa análise deve incluir a verificação da consistência dos registros e a identificação de possíveis falhas no processo de notificação.

    - **Avaliação da Capacidade Instalada:** Realizar um estudo da capacidade instalada da rede de saúde do município, considerando a infraestrutura, os equipamentos e os recursos humanos disponíveis, comparando-a com a demanda real por serviços.

    - **Planejamento Estratégico:** Elaborar um plano estratégico para a saúde do município, com base em dados epidemiológicos, demográficos e de produção, que contemple as necessidades de investimento em infraestrutura, equipamentos, recursos humanos e capacitação profissional.

    ### Conclusão:

    A análise da saúde de Guarapari, a partir do exemplo da UPA, sugere a necessidade de uma revisão do financiamento destinado ao município. Um Teto MAC defasado pode comprometer a capacidade de resposta do sistema de saúde e o acesso da população a serviços essenciais. Investir na melhoria da gestão, na qualificação dos profissionais, na infraestrutura e, fundamentalmente, na adequação do financiamento à real demanda por serviços de saúde é crucial para garantir a sustentabilidade do sistema e a qualidade da assistência prestada à população de Guarapari. A solicitação de aumento do Teto MAC, embasada em dados consistentes e em um planejamento estratégico sólido, é uma medida fundamental para que o município possa cumprir seu papel na garantia do direito à saúde de seus cidadãos.
    """
    )





# Página 1: Evolução do Teto MAC
if escolha == "Introdução":
    st.title("Introdução")
    st.image('BANNER-PRINCIPAL-1920x1077-21.jpg')
    st.markdown("""
    ## História
    **Guarapari**, situada no litoral do estado do Espírito Santo, é uma cidade rica em história e belezas naturais. A cidade foi fundada oficialmente em **1585** por padres jesuítas e inicialmente povoada por índios goitacás e tupiniquins. O nome "Guarapari" deriva da língua indígena tupi e significa "armadilha para pássaros" (guara: pássaro; pari: armadilha).

    ## Demografia
    Atualmente, Guarapari possui uma população de aproximadamente **134.944 habitantes**. A cidade é composta por diversos bairros, entre os quais se destacam Meaípe, Muquiçaba, Praia do Morro, Centro e Enseada Azul. A população de Guarapari cresce significativamente durante a alta temporada turística.

    ## Economia
    A economia de Guarapari é fortemente impulsionada pelo **turismo**, devido às suas famosas praias e às propriedades terapêuticas das areias monazíticas encontradas em algumas praias, como a Praia da Areia Preta. Além do turismo, a cidade também conta com atividades de **comércio** e **serviços** que atendem tanto os moradores locais quanto os visitantes.

    ## Educação e Saúde
    Guarapari possui um sistema educacional que inclui **escolas públicas** e privadas de ensino fundamental e médio, além de algumas instituições de **ensino técnico**. Na área da saúde, a cidade dispõe de **postos de saúde**, **hospitais** e **clínicas particulares**, garantindo atendimento à população local e aos turistas.

    ## Cultura e Turismo
    Conhecida por suas belas praias, Guarapari é um dos destinos turísticos mais populares do Espírito Santo. Entre as praias mais famosas estão a **Praia do Morro**, **Praia da Areia Preta**, **Praia de Meaípe** e **Praia das Castanheiras**. A cidade também é conhecida pelos eventos culturais que ocorrem ao longo do ano, atraindo visitantes de diversas partes do Brasil. Além disso, Guarapari oferece opções de **ecoturismo** e **turismo de aventura**, com trilhas, mergulho e passeios de barco.
    """)