import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

# Função para criar gráficos de correlação
def plot_correlacao(x, y, xlabel, ylabel, title):
    fig = px.scatter(x=x, y=y, trendline='ols', labels={ 'x': xlabel, 'y': ylabel }, title=title)
    return fig

# Dados
anos = list(range(2010, 2024))
media_complexidade = [
    151694, 127422, 220052, 227475, 222191, 200032, 146300, 224518, 280250, 353468,
    221360, 273353, 447797, 584719
]
alta_complexidade = [
    0, 0, 4605, 0, 0, 0, 0, 0, 0, 2125,
    14227, 21867, 27490, 32891
]
nao_se_aplica = [
    20160, 23375, 24132, 22151, 18853, 15258, 23989, 29480, 68997, 64769,
    20961, 20588, 17827, 28739
]
total_ambulatorial = [
    243335, 261463, 598461, 479218, 437725, 567417, 612453, 673326, 349654, 433406,
    261073, 316824, 494952, 647923
]
teto_total = [
    1995962.74, 3422104.76, 3717137.9, 3609136.8, 3500116.8,
    3520116.68, 3666022.02, 3620148.55, 5725025.51, 6090350.64,
    6163326.42, 6473076.42, 7037782.17, 6844944.34
]
valores_sem_incentivo = [
    1995962.74, 3422104.76, 3377477.9, 3269476.8, 3160456.8,
    3160456.68, 3206362.02, 3160488.55, 3165365.51, 3530690.64,
    3603666.42, 3603666.42, 3654957.17, 3757538.67
]
valores_incentivos = [
    0, 0, 339660, 339660, 339660,
    359660, 459660, 459660, 2559660, 2559660,
    2559660, 2869410, 3382825, 3087405.67
]
proced_clinicos = [
    2906, 1861, 1721, 1621, 1569, 1478, 2004, 2485, 2434, 2460,
    2169, 2127, 2095, 2361
]
proced_cirurgicos = [
    746, 680, 750, 656, 745, 333, 1165, 1724, 1831, 1836,
    1451, 1433, 2213, 2825
]
total_procedimentos = [
    3652, 2541, 2471, 2277, 2314, 1811, 3169, 4209, 4265, 4296,
    3620, 3560, 4308, 5186
]

# Criação do menu de seleção de páginas na barra lateral
paginas = ["I. Evolução do Teto MAC", "II. MAC x Procedimentos Hospitalares", "III. MAC x Produção Ambulatorial", "IV. Correlação Produção vs Recursos", "V. Conclusão"]

# Adicionando as logos na sidebar
st.sidebar.image('logo_maisgestor.png')
st.sidebar.image('logo.png')
escolha = st.sidebar.radio("Escolha a página que deseja visualizar:", paginas)

# Página 1: Evolução do Teto MAC
if escolha == "I. Evolução do Teto MAC":
    st.title("Evolução do Teto MAC (2010-2023)")
    
    # Criando o gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(anos, teto_total, label="Teto Total (R$)", marker='o')
    ax.plot(anos, valores_sem_incentivo, label="Sem Incentivos (R$)", marker='o')
    ax.plot(anos, valores_incentivos, label="Incentivos (R$)", marker='o')

    # Personalização
    ax.set_title("Evolução do Teto MAC em Euclides da Cunha - BA (2010-2023)", fontsize=14)
    ax.set_xlabel("Ano", fontsize=12)
    ax.set_ylabel("Valor (R$)", fontsize=12)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    fig.tight_layout()

    st.pyplot(fig)
    
    st.markdown("""
    **Essa tabela apresenta o histórico do teto MAC (Média e Alta Complexidade) do município de Euclides da Cunha - BA, com variações anuais tanto nos valores sem incentivos quanto nos valores com incentivos. Seguem algumas observações sobre a evolução:**

    ### **Análise Geral**
    1. **Crescimento até 2011**: O maior aumento percentual ocorreu em 2011, com um crescimento de **71,45%** no valor total sem incentivos, resultando no maior aumento proporcional no teto geral para aquele ano.

    2. **Flutuações em 2012-2017**:
       - Após o pico de 2011, os valores sem incentivos apresentaram variações negativas consecutivas entre 2012 e 2014.
       - Apesar de quedas nos valores sem incentivos, o teto total apresentou certa estabilidade entre 2015 e 2017, com pequenas oscilações.

    3. **Aumento significativo em 2018**:
       - O ano de 2018 trouxe um aumento expressivo de **456,86%** nos incentivos, levando a um crescimento de **58,14%** no teto geral, com os incentivos contribuindo fortemente para essa alta.

    4. **Estabilização e pequenas variações em 2019-2022**:
       - A partir de 2019, os valores sem incentivos retomaram um ritmo de crescimento moderado.
       - O maior aumento percentual no valor com incentivos ocorreu em 2022 (**17,89%**), impulsionando o teto total em **8,72%**.

    5. **Declínio em 2023**:
       - Em 2023, houve uma redução no valor com incentivos (**-8,73%**) e, consequentemente, uma queda no teto total em **-2,74%**. Este foi o primeiro ano com variação negativa no teto total desde 2017.

    ### **Tendências e Observações**
    - **Dependência de incentivos**: A participação de incentivos tem se tornado mais relevante ao longo do tempo, especialmente após 2018.
    - **Variações políticas e econômicas**: As oscilações podem refletir mudanças em políticas públicas de saúde e alocação de recursos, além de fatores externos, como crises econômicas.
    - **Crescimento moderado recente**: O crescimento nos últimos anos tem sido mais tímido, com exceção de 2022, quando os incentivos foram aumentados.

    ### **Destaques numéricos**
    - **Maior teto total**: Em 2022, com **R$ 7.037.782,17**.
    - **Maior variação positiva**: 2018, com aumento de **R$ 2.104.876,96** no teto total.
    - **Maior variação negativa**: 2023, com redução de **R$ 192.837,83**.

    Essas informações podem ajudar a entender o impacto das políticas de saúde no município e como os recursos têm sido alocados ao longo dos anos.
    """)

# Página 2: Procedimentos Hospitalares e Recursos
if escolha == "II. MAC x Procedimentos Hospitalares":
    st.title("Procedimentos Hospitalares e Recursos ao Longo dos Anos")
    
    # Criando o gráfico
    fig, axs = plt.subplots(2, 1, figsize=(14, 7))
    
    # Procedimentos ao longo dos anos
    axs[0].plot(anos, proced_clinicos, label='Procedimentos Clínicos')
    axs[0].plot(anos, proced_cirurgicos, label='Procedimentos Cirúrgicos')
    axs[0].plot(anos, total_procedimentos, label='Total de Procedimentos')
    axs[0].set_xlabel('Anos')
    axs[0].set_ylabel('Número de Procedimentos')
    axs[0].set_title('Procedimentos Hospitalares ao Longo dos Anos')
    axs[0].legend()
    axs[0].grid(True)
    
    # Recursos ao longo dos anos
    axs[1].plot(anos, teto_total, label='Teto Total')
    axs[1].plot(anos, valores_sem_incentivo, label='Valores Sem Incentivo')
    axs[1].plot(anos, valores_incentivos, label='Valores com Incentivos')
    axs[1].set_xlabel('Anos')
    axs[1].set_ylabel('Valores (R$)')
    axs[1].set_title('Recursos ao Longo dos Anos')
    axs[1].legend()
    axs[1].grid(True)
    
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    ### **Análise Geral dos Procedimentos Hospitalares**

    #### Procedimentos Clínicos
    - **Tendência Decrescente Inicial (2010-2015)**: Houve uma queda consistente no número de procedimentos clínicos de 2010 a 2015.
    - **Aumento e Estabilidade (2016-2022)**: A partir de 2016, observa-se um aumento no número de procedimentos clínicos, atingindo um pico em 2022. Esse aumento pode indicar uma melhora na capacidade de atendimento clínico ao longo dos anos.

    #### Procedimentos Cirúrgicos
    - **Flutuações (2010-2015)**: Os procedimentos cirúrgicos flutuaram entre 2010 e 2015, com um mínimo em 2015.
    - **Crescimento Acentuado (2016-2023)**: A partir de 2016, há um aumento significativo nos procedimentos cirúrgicos, que continua até 2023. Isso pode ser atribuído a melhorias nas infraestruturas cirúrgicas e em políticas de saúde que incentivam cirurgias.

    #### Total de Procedimentos
    - **Tendência Geral de Crescimento**: O total de procedimentos seguiu um padrão semelhante aos procedimentos cirúrgicos, com um aumento significativo a partir de 2016.

    ### **Relação entre Produções e Recursos MAC**
    1. **Crescimento Sustentado de Recursos**: O aumento contínuo do teto total até 2022 sugere uma expansão dos recursos financeiros alocados para a saúde, o que pode ter contribuído para o aumento do número de procedimentos hospitalares, especialmente cirúrgicos.
    2. **Impacto dos Incentivos**: O aumento significativo nos valores com incentivos a partir de 2016 mostra a eficácia das políticas de incentivo na ampliação da capacidade de atendimento hospitalar.
    3. **Estabilidade Relativa dos Valores Sem Incentivo**: A estabilidade dos valores sem incentivo ao longo dos anos reflete uma manutenção do financiamento básico, mesmo com flutuações no cenário econômico.
    4. **Ajuste em 2023**: A redução nos recursos totais em 2023 pode ser um indicativo de ajustes orçamentários ou mudanças nas políticas de financiamento da saúde.

    ### **Destaques Numéricos**
    - **Procedimentos Cirúrgicos**: O aumento substancial de 2016 a 2023 destaca uma melhora significativa na capacidade cirúrgica.
    - **Teto Total Máximo**: Em 2022, com R$ 7.037.782,17, indicando o ponto alto de financiamento antes do ajuste em 2023.
    - **Incentivos e Procedimentos**: A correlação entre o aumento dos valores com incentivos e o número total de procedimentos sugere uma relação direta entre os incentivos financeiros e a capacidade de atendimento.
    """)

# Página 3: MAC x Produção Ambulatorial
if escolha == "III. MAC x Produção Ambulatorial":
    st.title("Produção Ambulatorial ao Longo dos Anos")
    
    # Criando o gráfico
    fig, axs = plt.subplots(2, 1, figsize=(14, 7))
    
    # Produção ambulatorial ao longo dos anos
    axs[0].plot(anos, media_complexidade, label="Média Complexidade", marker='o')
    axs[0].plot(anos, alta_complexidade, label="Alta Complexidade", marker='o')
    axs[0].plot(anos, nao_se_aplica, label="Não se Aplica", marker='o')
    axs[0].plot(anos, total_ambulatorial, label="Total de Procedimentos")
    axs[0].set_xlabel('Anos')
    axs[0].set_ylabel('Quantidade de Procedimentos')
    axs[0].set_title('Produção Ambulatorial ao Longo dos Anos')
    axs[0].legend()
    axs[0].grid(True)

    # Recursos ao longo dos anos
    axs[1].plot(anos, teto_total, label='Teto Total')
    axs[1].plot(anos, valores_sem_incentivo, label='Valores Sem Incentivo')
    axs[1].plot(anos, valores_incentivos, label='Valores com Incentivos')
    axs[1].set_xlabel('Anos')
    axs[1].set_ylabel('Valores (R$)')
    axs[1].set_title('Recursos ao Longo dos Anos')
    axs[1].legend()
    axs[1].grid(True)
    
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    ### **Análise Geral da Produção Ambulatorial**

    #### Média Complexidade
    - **Crescimento Inicial e Flutuações (2010-2015)**: A produção de média complexidade cresceu inicialmente até 2012, com uma leve queda em 2013 e 2014, seguida de um declínio em 2015.
    - **Recuperação e Picos (2016-2023)**: Após 2015, houve uma recuperação com um pico significativo em 2022 e 2023, indicando um aumento na capacidade de atendimento ou maior demanda por esses serviços.

    #### Alta Complexidade
    - **Início Tardio e Aumento Gradual (2012-2024)**: Procedimentos de alta complexidade começaram a ser realizados a partir de 2012, com um crescimento gradual e picos em 2022 e 2023.
    - **Consistência Recente (2020-2024)**: A partir de 2020, a produção de alta complexidade tornou-se mais consistente, refletindo avanços na capacidade técnica e infraestrutural.

    #### Não se Aplica
    - **Estabilidade e Queda (2010-2024)**: A quantidade de procedimentos classificados como "Não se Aplica" manteve-se estável até 2018, com uma tendência de declínio subsequente, possivelmente devido a melhorias na categorização dos procedimentos.

    ### Total de Procedimentos
    - **Tendência Geral de Crescimento e Declínio (2010-2024)**: O total de procedimentos aumentou até 2013, seguido por uma diminuição até 2017. A partir de 2021, houve um aumento acentuado, com o pico em 2022.

    ### **Explicações das Categorias**
    - **Média Complexidade**:
      - **02 Procedimentos com Finalidade Diagnóstica**: Inclui procedimentos como exames e diagnósticos.
      - **03 Procedimentos Clínicos**: Engloba tratamentos e consultas clínicas.
      - **04 Procedimentos Cirúrgicos**: Abrange cirurgias de menor complexidade.

    - **Alta Complexidade**:
      - **0305 Tratamento em Nefrologia**: Envolve tratamentos avançados para doenças renais.
      - **0405 Cirurgia do Aparelho da Visão**: Inclui cirurgias oftalmológicas.
      - **0418 Cirurgia em Nefrologia**: Cirurgias especializadas em condições renais.

    - **Não se Aplica**:
      - **0701 Órteses, Próteses e Materiais Especiais Não Relacionados ao Ato Cirúrgico**: Equipamentos médicos não utilizados em cirurgias.
      - **0702 Órteses, Próteses e Materiais Especiais Relacionados ao Ato Cirúrgico**: Equipamentos médicos utilizados durante cirurgias.
      - **TFD (Tratamento Fora de Domicílio)**: Refere-se a tratamentos realizados fora do município do paciente.

    ### **Relação entre Produções e Recursos MAC**
    1. **Crescimento Sustentado de Recursos**: O aumento contínuo do teto total até 2022 sugere uma expansão dos recursos financeiros alocados para a saúde, o que pode ter contribuído para o aumento do número de procedimentos ambulatoriais.
    2. **Impacto dos Incentivos**: O aumento significativo nos valores com incentivos a partir de 2016 mostra a eficácia das políticas de incentivo na ampliação da capacidade de atendimento ambulatorial.
    3. **Estabilidade Relativa dos Valores Sem Incentivo**: A estabilidade dos valores sem incentivo ao longo dos anos reflete uma manutenção do financiamento básico, mesmo com flutuações no cenário econômico.
    4. **Ajuste em 2023**: A redução nos recursos totais em 2023 pode ser um indicativo de ajustes orçamentários ou mudanças nas políticas de financiamento da saúde.

    ### **Destaques Numéricos**
    - **Maior Produção Total**: O ano de 2022 destaca-se com o maior número de procedimentos ambulatoriais, totalizando 647.923.
    - **Alta Complexidade Máxima**: 2022 também foi o ano com o maior número de procedimentos de alta complexidade, evidenciando melhorias significativas na capacidade de atendimento especializado.
    - **Tendência Recente**: Os dados de 2024 mostram uma tendência de estabilização ou possível redução na produção total, o que pode refletir mudanças nas políticas de saúde ou nas demandas da população.

    Estas análises ajudam a entender melhor a dinâmica da produção ambulatorial no município e a identificar áreas para futuras melhorias e investimentos.
    """)

# Página 4: Correlação Produção vs Recursos
if escolha == "IV. Correlação Produção vs Recursos":
    # Introdução às correlações
    st.title('Correlação entre os Recursos e a Produção')
    st.subheader("Como foram calculadas as correlações")
    st.markdown("""
    As correlações entre os valores recebidos (Teto Total, Valores Sem Incentivo, Valores com Incentivos) e a produção ambulatorial foram calculadas usando o coeficiente de correlação de _Pearson_. Este coeficiente mede a força e a direção da associação linear entre duas variáveis. Valores próximos de 1 ou -1 indicam uma correlação forte, enquanto valores próximos de 0 indicam pouca ou nenhuma correlação.
    """)

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
    
    with st.expander('Exemplo de Cálculo'):
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

            # Apresentação das correlações calculadas
    st.markdown("""
    A seguir, apresentamos as correlações calculadas.
    """)

    st.subheader("Correlação: Teto Total vs Média Complexidade")
    fig1 = plot_correlacao(teto_total, media_complexidade, 'Teto Total', 'Média Complexidade', 'Correlação: Teto Total vs Média Complexidade')
    st.plotly_chart(fig1)
    st.markdown("""
    **Observações:**
    - **Eixo X (Teto Total)**: Representa os recursos financeiros totais alocados.
    - **Eixo Y (Média Complexidade)**: Representa a quantidade de procedimentos ambulatoriais de média complexidade realizados.
    - **Linha de Tendência**: A linha de tendência inclinada para cima indica uma correlação positiva. Ou seja, à medida que os recursos financeiros aumentam, o número de procedimentos de média complexidade também tende a aumentar.
    """)

    st.subheader("Correlação: Teto Total vs Alta Complexidade")
    fig2 = plot_correlacao(teto_total, alta_complexidade, 'Teto Total', 'Alta Complexidade', 'Correlação: Teto Total vs Alta Complexidade')
    st.plotly_chart(fig2)
    st.markdown("""
    **Observações:**
    - **Eixo X (Teto Total)**: Representa os recursos financeiros totais alocados.
    - **Eixo Y (Alta Complexidade)**: Representa a quantidade de procedimentos ambulatoriais de alta complexidade realizados.
    - **Linha de Tendência**: A linha de tendência inclinada para cima indica uma correlação positiva. Isso significa que, com o aumento dos recursos financeiros, a quantidade de procedimentos de alta complexidade também aumenta.
    """)

    st.subheader("Correlação: Teto Total vs Não se Aplica")
    fig3 = plot_correlacao(teto_total, nao_se_aplica, 'Teto Total', 'Não se Aplica', 'Correlação: Teto Total vs Não se Aplica')
    st.plotly_chart(fig3)
    st.markdown("""
    **Observações:**
    - **Eixo X (Teto Total)**: Representa os recursos financeiros totais alocados.
    - **Eixo Y (Não se Aplica)**: Representa a quantidade de procedimentos classificados como "Não se Aplica".
    - **Linha de Tendência**: A linha de tendência tem uma inclinação menos pronunciada, indicando uma correlação mais fraca. Isso significa que os aumentos no Teto Total têm uma relação menos direta com a quantidade desses procedimentos.
    """)

    st.subheader("Correlação: Teto Total vs Total Ambulatorial")
    fig4 = plot_correlacao(teto_total, total_ambulatorial, 'Teto Total', 'Total Ambulatorial', 'Correlação: Teto Total vs Total Ambulatorial')
    st.plotly_chart(fig4)
    st.markdown("""
    **Observações:**
    - **Eixo X (Teto Total)**: Representa os recursos financeiros totais alocados.
    - **Eixo Y (Total Ambulatorial)**: Representa o número total de procedimentos ambulatoriais realizados.
    - **Linha de Tendência**: A linha de tendência plana ou ligeiramente descendente sugere uma correlação muito fraca ou inexistente. Isso indica que, ao observar todos os tipos de procedimentos juntos, o aumento dos recursos financeiros totais não está fortemente associado a um aumento no número total de procedimentos ambulatoriais.
    """)

    # Quebra de página
    st.markdown("---")

    # Conclusão Geral
    #st.subheader("Conclusão Geral")
    st.markdown("""
    A análise revela uma forte correlação positiva entre o Teto Total (recursos financeiros) e os procedimentos de média e alta complexidade, indicando que mais recursos financeiros estão associados a um maior número de procedimentos nessas categorias. No entanto, a relação entre o Teto Total e os procedimentos classificados como "Não se Aplica" ou o total de procedimentos ambulatoriais é mais fraca, sugerindo que outros fatores podem estar influenciando esses aspectos da produção ambulatorial.

    Estes insights podem ser usados para argumentar que aumentar os recursos financeiros disponíveis pode ajudar a melhorar a capacidade de realizar procedimentos mais complexos, mas que a relação com o total geral de procedimentos pode ser mais complexa e depender de outros fatores além dos recursos financeiros disponíveis.
    """)


# Página 5: Conclusão
if escolha == "V. Conclusão":
    st.title('Conclusão e Necessidade de Aumento do Teto MAC')

    st.markdown("""
    ## Conclusão

    A análise detalhada dos procedimentos hospitalares e ambulatoriais em Euclides da Cunha, BA, no período de 2010 a 2023, revela uma tendência clara de crescimento na demanda por serviços de saúde. Essa demanda crescente é evidenciada pelo aumento significativo no número de procedimentos de média e alta complexidade, bem como pelos investimentos contínuos em recursos financeiros.

    ### Importância de Manter o Nível Atual de Produção

    A capacidade de atender à população com serviços de saúde de qualidade depende diretamente do financiamento adequado. Nos últimos anos, observamos um aumento substancial nos procedimentos cirúrgicos e na produção ambulatorial, que só foi possível graças ao incremento nos valores do teto MAC e dos incentivos financeiros. Sem o aumento contínuo desses recursos, a sustentabilidade e a qualidade dos serviços de saúde podem ser comprometidas, levando a:

    - **Aumento nos tempos de espera**: Com a alta demanda e recursos financeiros limitados, os tempos de espera para procedimentos médicos podem aumentar significativamente.
    - **Redução na qualidade do atendimento**: A insuficiência de recursos pode levar à sobrecarga dos profissionais de saúde, resultando em uma queda na qualidade do atendimento e no cuidado aos pacientes.
    - **Desigualdade no acesso aos serviços de saúde**: A falta de recursos pode exacerbar as desigualdades no acesso aos serviços, afetando desproporcionalmente as populações mais vulneráveis.

    ### Necessidade de Aumento dos Recursos

    Para garantir que a produção atual possa ser sustentada e aprimorada, é essencial aumentar os valores do teto MAC. 
    Com base nos dados analisados, estimamos que um aumento de **pelo menos 15%** seja necessário para atender às demandas futuras. Isso significaria um incremento aproximado de **R$ 1.026.741,65**, garantindo:

    - **Continuidade dos serviços de saúde**: Manter a capacidade de atender à população com serviços de saúde de qualidade e em tempo hábil.
    - **Aprimoramento das infraestruturas de saúde**: Investimentos contínuos em equipamentos, instalações e capacitação dos profissionais de saúde.
    - **Resiliência do sistema de saúde**: Preparação para enfrentar possíveis crises sanitárias e atender à demanda crescente por serviços especializados.

    ### Conclusão

    A análise dos dados indica uma forte correlação positiva entre o aumento dos recursos financeiros e a melhoria nos serviços de saúde, especialmente nos procedimentos de média e alta complexidade. Para garantir um sistema de saúde sustentável e equitativo, é imperativo que os recursos financeiros continuem a crescer em conformidade com a demanda. Um aumento no teto MAC é não apenas uma necessidade, mas uma responsabilidade para assegurar a saúde e o bem-estar da população de Euclides da Cunha, BA. Investir na saúde é investir no futuro.
    """)