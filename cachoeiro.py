import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd  # Add pandas import
import plotly.graph_objs as go

anos = list(range(2012, 2025))
media_complexidade = [
    1543317, 1564303, 1633798, 1283012, 1336533, 1282581, 1439604, 1499091, 998843, 1191071,
    1418419, 1508483, 1226758
]
alta_complexidade = [
    3188558, 3235367, 3511644, 3682222, 3778217, 4202130, 4361999, 4253314, 3628124, 3451492,
    2841493, 2778994, 1939226

]
nao_se_aplica = [
    34001, 51382, 60964, 56800, 99603, 93117, 81258, 107337, 64613, 77379,
    89133, 94432, 56252
]
grupo_procedimento = ["02 Procedimentos com finalidade diagnostica", "03 Procedimentos clinicos", "04 Procedimentos cirurgicos", "05 Transplantes de orgaos, tecidos e celulas"]
anos = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
procedimentos_diagnostica = [43, 45, 30, 33, 50, 48, 65, 39, 53, 41, 51, 63, 101]
procedimentos_clinicos = [18459, 19094, 18517, 15747, 13567, 13763, 15071, 15613, 15067, 18107, 16064, 19769, 15730]
procedimentos_cirurgicos = [10130, 10261, 9499, 10207, 10486, 10620, 10599, 10897, 9391, 9796, 10594, 15005, 12433]
transplantes_orgaos = [27, 19, 21, 27, 57, 44, 18, 26, 18, 25, 29, 24, 57]

teto_total = [354781.35, 769862.65, 1678688.29, 1177606.4, 1266711.12, 1245742.66, 2141606.39, 4097172.81, 4520008.24, 4521747.84, 4110800.75, 6423457.12, 7757060.79]

valores_sem_incentivo = [146881.35, 293762.65, 891128.29, 43246.4, 124851.12, 8182.66, 369796.39, 2059812.81, 2482648.24, 2484387.84, 2073440.75, 4353745.12, 5687348.79] # Mantém o valor de 2023

valores_incentivos = [207900, 476100, 787560, 1134360, 1141860, 1237560, 1771810, 2037360, 2037360, 2037360, 2037360, 2069712, 2069712]

# Calculando os totais (fora do dicionário, como listas)
total_ambulatorial = [sum(x) for x in zip(media_complexidade, alta_complexidade, nao_se_aplica)]
total_procedimentos = [x + y + z + w for x, y, z, w in zip(procedimentos_diagnostica, procedimentos_clinicos, procedimentos_cirurgicos, transplantes_orgaos)]

teto_total = [354781.35, 769862.65, 1678688.29, 1177606.4, 1266711.12, 1245742.66, 2141606.39, 4097172.81, 4520008.24, 4521747.84, 4110800.75, 6423457.12, 7757060.79]

valores_sem_incentivo = [146881.35, 293762.65, 891128.29, 43246.4, 124851.12, 8182.66, 369796.39, 2059812.81, 2482648.24, 2484387.84, 2073440.75, 4353745.12, 5687348.79] # Mantém o valor de 2023

valores_incentivos = [207900, 476100, 787560, 1134360, 1141860, 1237560, 1771810, 2037360, 2037360, 2037360, 2037360, 2069712, 2069712]

# Criação do menu de seleção de páginas na barra lateral
paginas = ["Introdução", "I. Evolução do Teto MAC", "II. MAC x Procedimentos Hospitalares", "III. MAC x Produção Ambulatorial", "IV. Correlação Produção vs Recursos", "V. UPA 24h", "VI. Conclusão"]

# Adicionando as logos na sidebar
st.sidebar.image('logo_maisgestor.png')
st.sidebar.image('logo.png')
st.sidebar.markdown("<h1 style='text-align: center; color: #808080;'>Análise do Teto MAC</h1>", unsafe_allow_html=True)
escolha = st.sidebar.radio("Escolha a página que deseja visualizar:", paginas)

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
    ### Análise da Evolução do Teto MAC em Cachoeiro de Itapemirim

    1. **Crescimento ao Longo dos Anos (2012-2024)**:
                
    - O Teto MAC aumentou de 354.781,35 em 2012 para 7.757.060,79 em 2024.
    - Esse crescimento não foi constante, refletindo a complexidade da gestão de recursos e as políticas públicas.

    2. **Contribuição dos Incentivos**:
    - Incentivos como "CEREST" e "CAPS" foram cruciais para o aumento do Teto MAC, especialmente nos anos iniciais.
    - A partir de 2018, os incentivos se estabilizaram em torno de R$ 2 milhões, sugerindo uma política de financiamento mais estável.

    3. **Variações nos Valores Sem Incentivo**:
    - As mudanças nos valores "Sem Incentivo" se devem a remanejamentos intra, ou seja, realocações de recursos financeiros dentro do próprio teto MAC, realizadas pela Comissão Intergestores Bipartite (CIB).
    - Essas variações mostram que os recursos base passaram por muitas realocações e ajustes internos significativos.

    4. **Impacto das Portarias**:
    - Em 2023, houve uma redução significativa de R$ 2.266.907,47 no Teto MAC.
    - Em 2024, essa redução foi compensada com um aumento para R$ 7.757.060,79, indicando ajustes frequentes nos recursos.

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
    fig1.add_trace(go.Scatter(x=anos, y=procedimentos_diagnostica, mode='lines+markers', name='Procedimentos Diagnósticos'))
    fig1.add_trace(go.Scatter(x=anos, y=transplantes_orgaos, mode='lines+markers', name='Transplantes de Órgãos'))

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
    ### Análise da Evolução do Teto MAC em Cachoeiro de Itapemirim

    A análise da evolução do Teto MAC em Cachoeiro de Itapemirim entre 2012 e 2024, comparada aos novos dados da produção hospitalar, revela uma relação complexa e não-linear entre o financiamento disponível e o volume de procedimentos realizados. O aumento substancial do Teto MAC, de :blue-background[R$ 354.781,35 em 2012] para :blue-background[R$ 7.757.060,79 em 2024], não se traduz diretamente em um crescimento proporcional em todas as categorias de procedimentos. Para entender melhor essa relação, é necessário analisar a evolução temporal de cada categoria de procedimento frente ao crescimento do Teto MAC.

    :blue[**Evolução do Teto MAC**]: O gráfico de recursos demonstra um crescimento expressivo, especialmente após 2018, impulsionado principalmente pelo aumento dos "Valores sem Incentivo." A estabilização dos "Valores com Incentivos" a partir de 2018 sugere uma mudança na política de financiamento, com maior ênfase nos recursos base.

    :blue[**Evolução da Produção Hospitalar**]: A análise da produção hospitalar por tipo de procedimento (diagnóstico, clínico, cirúrgico e transplantes) revela diferentes padrões de crescimento:
    - :violet[**Procedimentos Diagnósticos**]: O número de procedimentos permanece relativamente baixo e com flutuações, sugerindo que o aumento no Teto MAC não se traduziu em um aumento proporcional na demanda ou na capacidade de realizar esses procedimentos.
    - :violet[**Procedimentos Clínicos**]: Apresenta crescimento até 2019, seguido por uma queda, indicando uma relação não-linear com o Teto MAC. Outros fatores, como a capacidade instalada do sistema de saúde ou mudanças nas prioridades de atendimento, podem ter influenciado essa variação.
    - :violet[**Procedimentos Cirúrgicos**]: Semelhante aos procedimentos clínicos, o número de procedimentos cirúrgicos cresce até 2019 e depois diminui. Essa discrepância com o aumento do financiamento (Teto MAC) reforça a influência de fatores adicionais além do recurso financeiro.
    - :violet[**Transplantes de Órgãos**]: Esta categoria apresenta um crescimento ainda mais irregular, possivelmente por sua alta complexidade e maior dependência de fatores além da disponibilidade financeira, tais como a disponibilidade de doadores e equipes especializadas.

    :red[**Relação Teto MAC e Produção**]: A análise comparativa indica que o aumento no financiamento não garante um aumento proporcional na produção de procedimentos. Vários fatores, além da disponibilidade financeira, influenciam o volume de atendimentos:
    - :orange[**Capacidade instalada**]: Limitações de infraestrutura e recursos humanos podem impedir o atendimento de uma maior demanda.
    - :orange[**Acessibilidade**]: O acesso aos serviços pode ser limitado por fatores como tempo de espera e localização geográfica.
    - :orange[**Eficiência do Sistema**]: A gestão e a organização do sistema de saúde influenciam na capacidade de transformar recursos em atendimento.
    - :orange[**Demanda Epidemiológica**]: Mudanças nos perfis de saúde da população podem afetar a demanda por procedimentos específicos.

    :green[**Conclusões e Recomendações**]:
    Embora o aumento no Teto MAC represente um incremento nos recursos para saúde, a análise revela que a relação entre financiamento e produção hospitalar não é simples nem diretamente proporcional. Para uma compreensão completa, é crucial:
    - :green[**Analisar indicadores de saúde**]: Correlacionar os dados financeiros com indicadores como mortalidade, morbidade e taxas de internação.
    - :green[**Investigar a capacidade instalada**]: Avaliar a capacidade do sistema de saúde de atender à demanda.
    - :green[**Analisar a eficiência do sistema**]: Investigar a eficácia na utilização dos recursos financeiros disponíveis.
    - :green[**Considerar fatores epidemiológicos**]: Levar em conta as mudanças na incidência e prevalência de doenças na região.

    Em resumo, o aumento do Teto MAC é uma condição necessária, mas não suficiente para garantir um crescimento proporcional da produção de procedimentos hospitalares. Uma análise mais abrangente, incluindo indicadores de saúde e uma investigação dos fatores contextuais, é necessária para avaliar a eficácia da alocação dos recursos financeiros e o impacto no acesso e na qualidade dos serviços de saúde em Cachoeiro de Itapemirim.
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
    ### Análise da Relação entre Teto MAC e Produção Ambulatorial em Cachoeiro de Itapemirim

    A análise da relação entre a evolução do Teto MAC e a produção ambulatorial em Cachoeiro de Itapemirim, de 2012 a 2023, revela uma complexa interdependência, porém não uma relação diretamente proporcional. O gráfico de recursos demonstra um crescimento expressivo do Teto MAC, enquanto o gráfico de produção ambulatorial mostra padrões de crescimento e variação distintos para cada tipo de procedimento.

    :blue[**Recursos Financeiros (Teto MAC)**]: O gráfico de "Recursos ao Longo dos Anos" evidencia um crescimento acentuado do Teto Total, principalmente após 2018. A partir deste ano, o crescimento se dá, principalmente, nos "Valores sem Incentivo", enquanto os "Valores com Incentivos" se estabilizam. Essa mudança de padrão sugere uma possível reorientação das políticas de financiamento para saúde no município, com maior ênfase nos recursos base e menor dependência de incentivos governamentais.

    :blue[**Produção Ambulatorial**]: O gráfico "Produção Ambulatorial ao Longo dos Anos" apresenta padrões distintos para os tipos de procedimento:
    - :violet[**Média Complexidade**]: Apresenta crescimento, embora com flutuações, até 2018, mostrando uma relação relativamente consistente com o aumento do financiamento nos anos anteriores. A partir de 2018, observa-se uma queda, apesar do constante aumento nos recursos do Teto MAC. Isto sugere que outros fatores, além do financiamento, afetam a demanda ou a capacidade de atendimento para serviços de média complexidade.
    - :violet[**Alta Complexidade**]: O número de procedimentos de alta complexidade aumenta de forma mais consistente até 2019, refletindo, parcialmente, o crescimento do financiamento. No entanto, observa-se uma queda acentuada a partir de 2019, mesmo com o contínuo aumento do Teto MAC. Similarmente à média complexidade, isto aponta para fatores além do financiamento que influenciam o volume de atendimentos de alta complexidade.
    - :violet[**Não se Aplica**]: Esta categoria mostra um crescimento quase constante e modesto, não apresentando relação direta com a evolução do Teto MAC. A falta de clareza sobre o que esta categoria representa impossibilita a análise mais detalhada do impacto desta variável na evolução dos recursos.
    - :violet[**Total de Procedimentos**]: O "Total de Procedimentos" reflete a soma dos três tipos. O padrão de crescimento é influenciado pelos diferentes comportamentos de cada componente. O crescimento não acompanha o crescimento do Teto MAC, sugerindo a existência de limitações no sistema para atender à demanda.

    :red[**Interpretação e Conclusões**]:
    A análise comparativa dos gráficos sugere que o aumento no Teto MAC, embora significativo, não se traduz diretamente em um crescimento proporcional na produção ambulatorial. Fatores além do financiamento, como:
    - :orange[**Capacidade Instalada**]: Limitações na infraestrutura e recursos humanos podem estar restringindo a capacidade do sistema de saúde para atender à demanda.
    - :orange[**Acessibilidade**]: Dificuldades de acesso, como longos tempos de espera, podem afetar o volume de procedimentos realizados.
    - :orange[**Demandas Epidemiológicas**]: A demanda por serviços de saúde pode variar com a incidência de doenças, mudanças demográficas, etc.
    - :orange[**Eficiência do Sistema**]: A gestão e a eficiência do sistema de saúde também desempenham um papel fundamental na capacidade de atender à demanda.

    :green[**Recomendações**]:
    Uma análise mais robusta exigirá:
    - :green[**Identificação clara do significado da categoria "Não se Aplica"**].
    - :green[**Investigação da capacidade instalada e dos recursos humanos do sistema de saúde**].
    - :green[**Análise da eficiência do sistema de saúde**].
    - :green[**Correlação dos dados com indicadores de saúde relevantes**].
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
    ### Análise da Correlação: Teto Total vs Média Complexidade
    A análise do gráfico "Correlação: Teto Total vs Média Complexidade" revela uma correlação negativa. À medida que o Teto Total aumenta, observa-se uma tendência de redução nos valores associados à Média Complexidade. Isso pode indicar uma mudança na alocação de recursos ou uma diminuição relativa no foco deste tipo de procedimento.
    """)


    # Correlação: Teto Total vs Alta Complexidade
    st.subheader("Correlação: Teto Total vs Alta Complexidade")
    fig2 = plot_correlacao(teto_total, alta_complexidade, 'Teto Total', 'Alta Complexidade', 'Correlação: Teto Total vs Alta Complexidade')
    st.plotly_chart(fig2)
    st.markdown("""
    ### Análise da Correlação: Teto Total vs Alta Complexidade
    No gráfico "Correlação: Teto Total vs Alta Complexidade", a linha de tendência é inclinada para baixo, indicando uma correlação negativa. Isso significa que, à medida que os recursos financeiros totais alocados (Teto Total) aumentam, a quantidade de procedimentos ambulatoriais de alta complexidade realizados diminui. Portanto, existe uma relação inversa entre o aumento dos recursos financeiros e a realização desses procedimentos.
    """)


    # Correlação: Teto Total vs Não se Aplica
    st.subheader("Correlação: Teto Total vs Não se Aplica")
    fig3 = plot_correlacao(teto_total, nao_se_aplica, 'Teto Total', 'Não se Aplica', 'Correlação: Teto Total vs Não se Aplica')
    st.plotly_chart(fig3)
    st.markdown("""
    ### Análise da Correlação: Teto Total vs Não se Aplica
    A análise do gráfico "Correlação: Teto Total vs Não se Aplica" apresenta uma correlação positiva. À medida que o Teto Total aumenta, observa-se um aumento na quantidade de procedimentos classificados como "Não se Aplica". Isso sugere que, com o aumento dos recursos financeiros totais alocados, há uma tendência de aumento na quantidade desses procedimentos.
    """)


    # Correlação: Teto Total vs Total Ambulatorial
    st.subheader("Correlação: Teto Total vs Total Ambulatorial")
    fig4 = plot_correlacao(teto_total, total_ambulatorial, 'Teto Total', 'Total Ambulatorial', 'Correlação: Teto Total vs Total Ambulatorial')
    st.plotly_chart(fig4)
    st.markdown("""
    ### Análise da Correlação: Teto Total vs Total Ambulatorial
    O gráfico "Correlação: Teto Total vs Total Ambulatorial" mostra uma correlação negativa. À medida que o Teto Total aumenta, observa-se uma tendência de diminuição no Total Ambulatorial. Isso sugere que, com o aumento dos recursos financeiros totais alocados, há uma diminuição na quantidade total de procedimentos ambulatoriais realizados.
    """)


    # Correlação: Teto Total vs Procedimentos Diagnósticos
    st.subheader("Correlação: Teto Total vs Procedimentos Diagnósticos")
    fig5 = plot_correlacao(teto_total, procedimentos_diagnostica, 'Teto Total', 'Procedimentos Diagnósticos', 'Correlação: Teto Total vs Procedimentos Diagnósticos')
    st.plotly_chart(fig5)
    st.markdown("""
    ### Análise da Correlação: Teto Total vs Procedimentos Diagnósticos
    A análise do gráfico "Correlação: Teto Total vs Procedimentos Diagnósticos" revela uma correlação positiva. À medida que o Teto Total aumenta, observa-se um aumento no número de Procedimentos Diagnósticos realizados. Isso sugere que, com o aumento dos recursos financeiros totais alocados, há uma tendência de aumento na quantidade desses procedimentos.
    """)


    # Correlação: Teto Total vs Procedimentos Clínicos
    st.subheader("Correlação: Teto Total vs Procedimentos Clínicos")
    fig6 = plot_correlacao(teto_total, procedimentos_clinicos, 'Teto Total', 'Procedimentos Clínicos', 'Correlação: Teto Total vs Procedimentos Clínicos')
    st.plotly_chart(fig6)
    st.markdown("""
    ### Análise da Correlação: Teto Total vs Procedimentos Clínicos
    A análise do gráfico "Correlação: Teto Total vs Procedimentos Clínicos" revela uma correlação positiva. À medida que o Teto Total aumenta, observa-se um aumento no número de Procedimentos Clínicos realizados. Isso sugere que, com o aumento dos recursos financeiros totais alocados, há uma tendência de aumento na quantidade desses procedimentos.
    """)


    # Correlação: Teto Total vs Procedimentos Cirúrgicos
    st.subheader("Correlação: Teto Total vs Procedimentos Cirúrgicos")
    fig7 = plot_correlacao(teto_total, procedimentos_cirurgicos, 'Teto Total', 'Procedimentos Cirúrgicos', 'Correlação: Teto Total vs Procedimentos Cirúrgicos')
    st.plotly_chart(fig7)
    st.markdown("""
    ### Análise da Correlação: Teto Total vs Procedimentos Cirúrgicos
    A análise do gráfico "Correlação: Teto Total vs Procedimentos Cirúrgicos" revela uma correlação positiva. À medida que o Teto Total aumenta, observa-se um aumento no número de Procedimentos Cirúrgicos realizados. Isso sugere que, com o aumento dos recursos financeiros totais alocados, há uma tendência de aumento na quantidade desses procedimentos.
    """)


    # Correlação: Teto Total vs Transplantes de Órgãos
    st.subheader("Correlação: Teto Total vs Transplantes de Órgãos")
    fig8 = plot_correlacao(teto_total, transplantes_orgaos, 'Teto Total', 'Transplantes de Órgãos', 'Correlação: Teto Total vs Transplantes de Órgãos')
    st.plotly_chart(fig8)
    st.markdown("""
    ### Análise da Correlação: Teto Total vs Transplantes de Órgãos
    A análise do gráfico "Correlação: Teto Total vs Transplantes de Órgãos" revela uma leve correlação positiva. À medida que o Teto Total aumenta, observa-se um leve aumento no número de transplantes de órgãos realizados. Isso sugere que, com o aumento dos recursos financeiros totais alocados, há uma tendência de aumento na quantidade desses procedimentos, embora a correlação seja fraca.
    """)



# Página 5: UPA 24h
if escolha == "V. UPA 24h":
    st.title('UPA 24h')
    st.image('upa.jpg')
    st.subheader('**ANÁLISE CONFORME PORTARIA GM/MS N. 10 – 2017**')
   
    # Dados
    anos = ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]
    procedimentos = {
        "Atendimento de Urgência com Observação até 24 horas (0301060029)": [6036, 10205, 5682, 5129, 4803, 1990, 2],
        "Atendimento de Urgência em Atenção Especializada (0301060061)": [8, 10, 18, 12, 16, 2, 1],
        "Atendimento Médico em Unidade de Pronto Atendimento (0301060096)": [38064, 58784, 35268, 38602, 39990, 32840, 8055],
        "Acolhimento com Classificação de Risco (0301060118)": [74541, 69860, 41743, 32618, 32391, 27346, 4854]
    }

    # Calcular a soma dos três primeiros procedimentos
    soma_procedimentos = [sum(values) for values in zip(
        procedimentos["Atendimento de Urgência com Observação até 24 horas (0301060029)"],
        procedimentos["Atendimento de Urgência em Atenção Especializada (0301060061)"],
        procedimentos["Atendimento Médico em Unidade de Pronto Atendimento (0301060096)"]
    )]

    # Meta anual de produção
    meta_anual = 121500

    # Gráfico para Atendimento de Urgência e Unidade de Pronto Atendimento
    fig1 = go.Figure()
    for procedimento, valores in procedimentos.items():
        fig1.add_trace(go.Scatter(x=anos, y=valores, mode='lines+markers', name=procedimento))

    # Adicionar a linha para a soma dos três primeiros procedimentos
    fig1.add_trace(go.Scatter(x=anos, y=soma_procedimentos, mode='lines+markers', name="Soma dos Três Primeiros Procedimentos", line=dict(color='purple')))

    fig1.add_shape(type="line", x0=anos[0], y0=meta_anual, x1=anos[-1], y1=meta_anual, line=dict(color="red", width=2, dash="dash"), name='Meta Anual')

    fig1.update_layout(title="PRODUÇÃO DA UNIDADE DE PRONTO ATENDIMENTO DR ANTONIO JORGE ABIB NETTO",
                    xaxis_title="Ano", yaxis_title="Quantidade Aprovada",
                    legend_title="Procedimentos", legend=dict(y=-1, x=0),
                    xaxis=dict(tickmode='linear'), yaxis=dict(showgrid=True))

    st.plotly_chart(fig1)
    st.caption('Fonte: TABWIN/MS')

    # Texto explicativo
    st.markdown(
        """
        **A análise da UPA Dr. Antônio Jorge Abib Netto em Cachoeiro de Itapemirim revela uma preocupante queda na produção de procedimentos nos últimos anos, resultando em um desempenho abaixo das metas estabelecidas pela [Portaria GM/MS nº 10/2017](https://bvsms.saude.gov.br/bvs/saudelegis/gm/2017/prt0010_03_01_2017.html) para o Porte VIII.** 

        Essa baixa produção, além de comprometer a capacidade de atendimento à população, **impacta diretamente no financiamento da unidade**, uma vez que a classificação da UPA, e consequentemente o valor do custeio, está diretamente ligada à sua produção. Portanto, o aumento da produção é crucial não apenas para garantir o acesso da população aos serviços, mas também para assegurar a sustentabilidade financeira da UPA.

        ### Impacto da Portaria 10/2017

        A Portaria 10/2017 estabelece diferentes valores de custeio para cada porte de UPA, de acordo com o número de médicos e a produção esperada. A baixa produção observada na UPA de Cachoeiro de Itapemirim pode levar a um **rebaixamento de sua classificação para um porte inferior**, acarretando uma redução significativa nos recursos financeiros. Essa redução, por sua vez, criaria um ciclo vicioso, dificultando ainda mais a capacidade da UPA de atender à demanda e atingir as metas de produção.

        ### Causas da Queda na Produção

        A queda na produção pode ser **multifatorial**, incluindo:

        - Problemas na organização do trabalho
        - Integração com a rede
        - Capacidade instalada
        - Eficiência da utilização dos recursos

        No entanto, um fator crucial a ser considerado é a **qualidade do registro dos procedimentos**. A subnotificação, ou seja, a falta de registro adequado dos procedimentos realizados, pode artificialmente reduzir a produção aparente da UPA, levando a uma classificação de porte inferior e à consequente redução de recursos. A melhoria no sistema de registro é, portanto, fundamental para garantir a correta avaliação do desempenho da UPA e evitar a redução de recursos por motivos administrativos.

        ### Necessidade de Aumentar a Produção

        **O aumento da produção de procedimentos, especialmente do "Acolhimento com Classificação de Risco", é crucial para garantir:**

        - **Cumprimento das Metas da Portaria 10/2017:** Atingir as metas de produção demonstra a eficiência da UPA e garante a manutenção do seu porte e financiamento.
        - **Acesso Adequado aos Serviços:** Uma maior produção indica uma maior capacidade de atendimento à demanda da população, garantindo o acesso aos serviços de saúde.
        - **Sustentabilidade Financeira:** O aumento da produção, levando à manutenção ou aumento do porte da UPA, assegura a disponibilidade de recursos financeiros para a operação da unidade.
        - **Melhoria da Qualidade do Atendimento:** O aumento da produção, aliado a uma melhoria na qualidade do registro, permite uma avaliação mais precisa do desempenho da UPA e a implementação de medidas para melhorar a qualidade do atendimento.

        **Em resumo**, a baixa produção da UPA de Cachoeiro de Itapemirim, possivelmente agravada por problemas de registro, cria um ciclo vicioso que impacta diretamente no seu financiamento. O aumento da produção, aliado a melhorias na gestão e na organização do trabalho, é fundamental para garantir a sustentabilidade financeira da UPA e o acesso adequado da população aos serviços de saúde. Portanto, o aumento do Teto MAC deve ser acompanhado por investimentos em melhorias operacionais e na qualidade do registro para garantir a eficácia dos recursos e o cumprimento das metas estabelecidas pela Portaria 10/2017.
        """
    )

# Página 6: Conclusão
if escolha == "VI. Conclusão":
    st.title('Necessidade de Aumento do Teto MAC')

    st.markdown("""
    ## Crescimento do Teto MAC em Cachoeiro de Itapemirim

    Ao longo de mais de uma década, de **2012 a 2024**, Cachoeiro de Itapemirim, um importante polo regional de saúde no Espírito Santo, tem demonstrado um crescimento notável no financiamento da Média e Alta Complexidade (MAC), refletido no aumento expressivo do seu **Teto MAC**. Este teto, que representa o limite financeiro para procedimentos de média e alta complexidade, saltou de **354.781,35 em 2012** para **R$ 7.757.060,79 em 2024.** 

    Esse crescimento, embora substancial, foi acompanhado por uma tendência preocupante: a produção de procedimentos hospitalares e ambulatoriais da **UPA Dr. Antônio Jorge Abib Netto** não acompanhou esse ritmo, ficando consistentemente abaixo das metas estabelecidas pela **Portaria GM/MS nº 10/2017**.

    ### Desafios na Produção de Procedimentos
    A análise detalhada dos dados de produção, em especial a queda acentuada no acolhimento com classificação de risco, revela desafios significativos na gestão e na operação da UPA. A **Portaria 10/2017**, que define as diretrizes para as UPAs 24h, estabelece metas de produção que, quando não atingidas, podem resultar em rebaixamento da classificação da unidade e, consequentemente, em redução dos recursos de custeio. A UPA de Cachoeiro, estimada como **Porte VIII**, opera, na prática, com uma produção que a aproxima de um porte inferior, indicando uma utilização aquém do potencial dos recursos disponibilizados.

    ### Gargalos Operacionais e Gestão de Recursos
    Apesar da disponibilidade de uma equipe multiprofissional considerável, incluindo **48 médicos cadastrados no CNES**, e de um inventário de equipamentos aparentemente adequado, a UPA enfrenta dificuldades para converter o financiamento recebido em produção efetiva. Isso sugere a existência de gargalos operacionais, problemas na organização do trabalho, possíveis falhas na integração com a rede de atenção e, crucialmente, a necessidade de melhorias no registro e notificação dos procedimentos realizados.

    ### Importância do Teto MAC
    A correlação entre o aumento do Teto MAC e a produção ambulatorial e hospitalar mostra que o simples incremento no financiamento não garante, automaticamente, um aumento proporcional na oferta de serviços. Fatores como a **capacidade instalada**, a **eficiência na gestão dos recursos**, a **correta classificação de risco** e a **integração com a rede de atenção à saúde** são igualmente importantes para assegurar que os recursos financeiros se traduzam em atendimento efetivo à população.

    ### Conclusão
    Nesse contexto, torna-se evidente que a continuidade do crescimento do **Teto MAC** para Cachoeiro de Itapemirim é fundamental, não apenas para manter o patamar atual de financiamento, mas para impulsionar as melhorias necessárias na UPA e em todo o sistema de média e alta complexidade do município. O aumento do **Teto MAC**, quando acompanhado de investimentos em gestão, capacitação profissional, melhoria dos processos de trabalho, e aprimoramento do registro de informações, permitirá que Cachoeiro de Itapemirim não apenas atinja as metas de produção estabelecidas, mas também amplie e qualifique o atendimento à sua população, consolidando seu papel como um importante centro regional de saúde.

    Ignorar essa necessidade pode comprometer a sustentabilidade do sistema de saúde local e, consequentemente, o acesso da população a serviços essenciais de média e alta complexidade. Portanto, o aumento do **Teto MAC** é um investimento estratégico para o futuro da saúde em Cachoeiro de Itapemirim, garantindo que o município possa continuar a atender às crescentes demandas de sua população e região.
    """)




# Página 1: Evolução do Teto MAC
if escolha == "Introdução":
    st.title("Introdução")
    st.image('cidade.jpg')
    st.markdown("""
    ## História
    **Cachoeiro de Itapemirim**, localizada no sul do estado do Espírito Santo, foi fundada oficialmente em **1812**. Desde seus primórdios, a cidade destacou-se pela **cultura cafeeira**, que impulsionou sua economia durante o século XIX. O **garimpo de ouro** também contribuiu significativamente para o desenvolvimento inicial da cidade. O nome "Cachoeiro de Itapemirim" deriva das imponentes cachoeiras do rio Itapemirim, que corta a cidade e proporciona uma paisagem natural deslumbrante. A chegada da **ferrovia** e da **energia elétrica** no final do século XIX e início do século XX marcou um período de grande progresso e modernização para a cidade, facilitando o transporte e estimulando a industrialização.

    ## Demografia
    Atualmente, Cachoeiro de Itapemirim possui uma população de aproximadamente **185.784 habitantes**. A cidade é composta por **11 distritos**, cada um com suas características únicas: Burarama, Conduru, Córrego dos Monos, Coutinho, Gironda, Gruta, Itaoca, Pacotuba, São Vicente, Vargem Grande do Soturno e a sede. Esses distritos são formados por comunidades diversificadas que contribuem para a rica tapeçaria cultural e social do município. A cidade tem uma densidade demográfica que reflete tanto áreas urbanas densamente povoadas quanto zonas rurais com extensas áreas verdes.

    ## Economia
    A economia de Cachoeiro de Itapemirim é diversificada, com fortes setores de **agricultura**, **pecuária** e **indústria**. A agricultura, especialmente a produção de café e pedra ornamental, continua a ser um pilar econômico vital. A pecuária complementa a produção agrícola com a criação de gado leiteiro e de corte. A cidade também é conhecida como um dos maiores polos de extração e beneficiamento de mármore e granito do país, o que lhe confere o título de "Capital Secreta do Mármore e Granito". O município possui um Índice de Desenvolvimento Humano Municipal (IDHM) de **0,746**, classificado como alto, e um PIB per capita de aproximadamente **R$ 23.331,02**, indicadores que refletem uma economia robusta e diversificada.

    ## Educação e Saúde
    Cachoeiro de Itapemirim dispõe de um sistema educacional abrangente que inclui **escolas públicas** de ensino fundamental e médio, além de várias instituições de **ensino técnico e superior**. As escolas públicas são complementadas por uma rede de escolas particulares que oferecem alternativas de alta qualidade. Na área de saúde, a cidade é bem servida por diversos **postos de saúde** e um **hospital municipal**, que atendem às necessidades básicas da população. Além disso, existem clínicas especializadas, laboratórios e serviços de pronto atendimento, como a UPA 24h, que garantem uma cobertura de saúde ampla e eficiente para os moradores.

    ## Cultura e Turismo
    Cachoeiro de Itapemirim é famosa pela música "**Meu Pequeno Cachoeiro**", composta por Raul Sampaio e imortalizada por Roberto Carlos, que nasceu na cidade. Este vínculo cultural forte é celebrado anualmente com eventos e festivais. O turismo na cidade é focado no **ecoturismo** e no **turismo histórico**, aproveitando suas belezas naturais e seu rico patrimônio histórico. Trilhas ecológicas, cachoeiras e sítios históricos atraem visitantes que buscam contato com a natureza e a história local. Além disso, o Parque Natural Municipal do Itabira, com sua geologia singular e biodiversidade, é um ponto turístico de destaque.
    """)
