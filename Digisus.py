import os
import pandas as pd
import streamlit as st
import requests
import tempfile
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import time
from streamlit_option_menu import option_menu
import datetime

data_atual = datetime.date.today()
data_formatada = data_atual.strftime("%d de %B de %Y")


# Configurações globais
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
api_key = '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'

# Exibir o logotipo no topo da página, centralizado
if os.path.exists('logo_maisgestor.png'):
    st.image('logo_maisgestor.png')
else:
    st.warning("O arquivo 'Logo.jpg' não foi encontrado. Certifique-se de que ele está no diretório correto.")

# Data atual e formatação
data_atual = datetime.date.today()
data_formatada = data_atual.strftime("%d de %B de %Y")

# Esconder o menu principal, footer e header do Streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Dados da tabela ideal
tabela_ideal_dados = {
    'FASE': ['2018-2021', '2018-2021', '2018-2021', '2018-2021', '2018-2021', '2022-2025', '2022-2025', '2022-2025', '2022-2025', '2022-2025'],
    'EXERCICIO': [0, 2018, 2019, 2020, 2021, 0, 2022, 2023, 2024, 2025],
    'PMS': ['Aprovado', '', '', '', '', 'Aprovado', '', '', '', ''],
    'PAS': ['', 'Aprovado', 'Aprovado', 'Aprovado', 'Aprovado', '', 'Aprovado', 'Aprovado', 'Aprovado', 'Aprovado'],
    '1º RDQA': ['', 'Avaliado', 'Avaliado', 'Avaliado', 'Avaliado', '', 'Avaliado', 'Avaliado', 'Avaliado', 'Não Iniciado'],
    '2º RDQA': ['', 'Avaliado', 'Avaliado', 'Avaliado', 'Avaliado', '', 'Avaliado', 'Avaliado', 'Avaliado', 'Não Iniciado'],
    '3º RDQA': ['', 'Avaliado', 'Avaliado', 'Avaliado', 'Avaliado', '', 'Avaliado', 'Avaliado', 'Não Iniciado', 'Não Iniciado'],
    'RAG': ['', 'Aprovado', 'Aprovado', 'Aprovado', 'Aprovado', '', 'Aprovado', 'Aprovado', 'Não Iniciado', 'Não Iniciado']
}
tabela_ideal = pd.DataFrame(tabela_ideal_dados)

def analisar_dataframe_groq(
    df: pd.DataFrame, 
    prompt: str, 
    municipio: str, 
    model: str = 'llama-3.2-90b-vision-preview', 
    temperature: float = 0, 
    max_tokens: int = 1024,
    top_p: float = 1
) -> str:
    """
    Usa a API Groq para analisar um DataFrame de acordo com o prompt fornecido.
    """
    try:
        # Converte o DataFrame para uma string formatada
        df_text = df.to_string(index=False)

        # Inicializa o cliente Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        # Cria o prompt completo com a tabela e o nome do município
        full_prompt = (
            f"Analise a tabela a seguir: {df_text}\n\n"
            f"Responda em tópicos, oculte detalhes dos prazos e vá para o resumo: {prompt}"
        )

        # Executa a geração de conteúdo com o modelo especificado
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": full_prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=True,
        )

        # Compila a resposta do stream
        response_text = "".join(chunk.choices[0].delta.content for chunk in completion)

        return response_text.strip()
    except Exception as e:
        return f"Erro ao analisar a tabela com Groq: {e}"

# Função para formatar as cores da tabela
def highlight_cells(val):
    """
    Aplica estilos a células com base nos valores.
    """
    if val in ['Aprovado', 'Avaliado', 'Aprovado com Ressalvas']:
        color = 'green'
        font_color = 'white'
    elif val in ['Não Iniciado', 'Não Aprovado']:
        color = 'red'
        font_color = 'white'
    elif val in ['Em Análise no Conselho de Saúde', 'Em Elaboração', 'Retornado para Ajustes']:
        color = 'yellow'
        font_color = 'black'
    else:
        color = ''
        font_color = 'black'  # Cor padrão para o texto
    return f'background-color: {color}; color: {font_color}'

# Função para gerar uma tabela formatada com base no município
def gerar_tabela_formatada(df, municipio):
    tabela_municipio = df[df['MUNICIPIO'] == municipio]
    if tabela_municipio.empty:
        return pd.DataFrame()
    # Identificar linhas com PMS e zerar outras colunas
    pms_index = tabela_municipio[tabela_municipio['TIPO_INSTRUMENTO'] == 'PMS'].index
    # Transferir conteúdo de "Plano de Saúde" já foi tratado na carga dos dados
    tabela_municipio.loc[tabela_municipio['TIPO_INSTRUMENTO'] == 'Plano de Saúde', 'TIPO_INSTRUMENTO'] = 'PMS'
    # Separar as linhas de PMS e exercícios
    pms_lines = tabela_municipio[tabela_municipio['TIPO_INSTRUMENTO'] == 'PMS']
    exercicios_lines = tabela_municipio[tabela_municipio['TIPO_INSTRUMENTO'] != 'PMS']
    # Ordenar os exercícios e concatenar PMS antes deles
    exercicios_lines = exercicios_lines.sort_values(by=['FASE', 'EXERCICIO'])
    tabela_municipio = pd.concat([pms_lines, exercicios_lines])
    tabela_formatada = tabela_municipio.pivot_table(index=['FASE', 'EXERCICIO'],
                                                    columns='TIPO_INSTRUMENTO',
                                                    values='SITUACAO',
                                                    aggfunc=lambda x: x).reset_index()
    tabela_formatada.insert(0, 'MUNICÍPIO', municipio)
    tabela_formatada.fillna('', inplace=True)
    # Remover a coluna "Pactuação" se presente
    if 'Pactuação' in tabela_formatada.columns:
        tabela_formatada.drop(columns=['Pactuação'], inplace=True)
    # Garantir que as colunas PMS e PAS estejam presentes
    if 'PMS' not in tabela_formatada.columns:
        tabela_formatada['PMS'] = ''
    if 'PAS' not in tabela_formatada.columns:
        tabela_formatada['PAS'] = ''
    # Reordenar colunas
    colunas_ordem = ['FASE', 'EXERCICIO', 'PMS', 'PAS'] + [col for col in tabela_formatada.columns if col not in ['MUNICÍPIO', 'FASE', 'EXERCICIO', 'PMS', 'PAS']]
    tabela_formatada = tabela_formatada[colunas_ordem]
    return tabela_formatada

# Função para mapear estados para os seus respectivos códigos UF
def get_uf_code(state):
    """
    Retorna o código UF correspondente ao estado informado.
    """
    uf_codes = {
        'AC': '12', 'AL': '27', 'AM': '13', 'AP': '16', 'BA': '29', 'CE': '23',
        'DF': '53', 'ES': '32', 'GO': '52', 'MA': '21', 'MG': '31', 'MS': '50',
        'MT': '51', 'PA': '15', 'PB': '25', 'PE': '26', 'PI': '22', 'PR': '41',
        'RJ': '33', 'RN': '24', 'RO': '11', 'RR': '14', 'RS': '43', 'SC': '42',
        'SE': '28', 'SP': '35', 'TO': '17'
    }
    return uf_codes.get(state.upper())

# Função para baixar e salvar arquivos de estado
@st.cache_data
def Carregando_arquivos(state):
    """
    Baixa o arquivo CSV correspondente ao estado informado e salva temporariamente.
    """
    uf_code = get_uf_code(state)
    if uf_code is None:
        st.error(f"Código da UF para o estado '{state}' não encontrado.")
        return None

    # URL para baixar o CSV
    url = f'https://digisusgmp.saude.gov.br/v1.5/transparencia/extracao/csv?uf={uf_code}'
    temp_dir = tempfile.gettempdir()
    local_file = os.path.join(temp_dir, f'{state}.csv')

    try:
        # Requisição HTTP
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(local_file, 'wb') as f:
                f.write(response.content)
        else:
            st.error(f"Erro ao baixar o arquivo. Código de status: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao baixar o arquivo: {e}")
        return None

    return local_file

# Função para carregar dados de estado
@st.cache_data
def load_data_from_state(state):
    """
    Carrega os dados de um estado específico em um DataFrame do Pandas.
    """
    local_file = Carregando_arquivos(state)
    if local_file is None:
        return pd.DataFrame()

    try:
        df = pd.read_csv(local_file, delimiter=';', on_bad_lines='skip')
    except pd.errors.ParserError as e:
        st.error(f"Erro ao ler o arquivo CSV: {e}")
        return pd.DataFrame()
    except FileNotFoundError:
        st.error(f"Arquivo {local_file} não encontrado.")
        return pd.DataFrame()

    # Validar se a coluna REGIAO existe
    if 'REGIAO' not in df.columns:
        st.error(f"A coluna 'REGIAO' não foi encontrada no arquivo {local_file}.")
        return pd.DataFrame()

    # Preencher valores nulos e ajustar colunas
    df['EXERCICIO'] = df['EXERCICIO'].fillna(0).astype(int).astype(str)
    df.loc[df['SITUACAO'].isnull(), 'SITUACAO'] = 'Não Iniciado'
    df['TIPO_INSTRUMENTO'] = df['TIPO_INSTRUMENTO'].replace({
        'Plano Municipal de Saúde': 'PMS',
        'Programação Anual de Saúde': 'PAS',
        'Plano de Saúde': 'PMS'
    })

    return df

# Função para carregar credenciais OAuth2 e armazená-las em `session_state`
def carregar_credenciais():
    """
    Carrega as credenciais OAuth2 para acesso à API do Gmail. Armazena-as em `st.session_state` para reutilização.
    """
    if 'creds' in st.session_state:
        return st.session_state['creds']

    creds = None

    # Verifica se o arquivo de token existe e o carrega
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Se as credenciais não estão válidas, executa o fluxo OAuth2
    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Salva o token para uso futuro
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            st.error(f"Erro durante a autenticação: {e}")
            return None

    # Armazena as credenciais em session_state para reutilização
    st.session_state['creds'] = creds
    return creds

# Função para criar uma mensagem de e-mail
def criar_mensagem(remetente, destinatario, assunto, conteudo):
    """
    Cria uma mensagem de e-mail no formato MIME.
    """
    mensagem = MIMEText(conteudo)
    mensagem['to'] = destinatario
    mensagem['from'] = remetente
    mensagem['subject'] = assunto
    return {'raw': base64.urlsafe_b64encode(mensagem.as_bytes()).decode()}

# Função para enviar e-mails usando a API Gmail
def enviar_email(remetente, destinatario, assunto, conteudo):
    """
    Envia um e-mail utilizando a API Gmail.
    """
    creds = carregar_credenciais()
    if not creds:
        return "Erro: Não foi possível autenticar as credenciais."

    try:
        # Constrói o serviço da API Gmail
        service = build('gmail', 'v1', credentials=creds)
        mensagem = criar_mensagem(remetente, destinatario, assunto, conteudo)

        # Envia o e-mail
        enviado = service.users().messages().send(userId="me", body=mensagem).execute()
        return f"Mensagem enviada com sucesso! ID: {enviado['id']}."
    except Exception as e:
        return f"Erro ao enviar e-mail: {e}"

def contato():
    """
    Exibe o formulário de contato no Streamlit.
    """
    st.title('Formulário de Contato')

    # Verificar se o estado e município foram selecionados previamente
    if 'creds' in st.session_state:
        with st.form(key='form_email'):
            estado = st.session_state.get('estado_selecionado', 'Não informado')
            municipio = st.session_state.get('municipio', 'Não informado')

            # Campos do formulário
            remetente = st.text_input('Seu Email :red[*]', placeholder="Digite seu e-mail")
            assunto = st.text_input("Contato (Fone/Whatsapp)", placeholder="Digite seu telefone ou WhatsApp")
            conteudo = st.text_area(
                "Deixe uma mensagem",
                placeholder=f'Olá, sou de {municipio}-{estado}, e gostaria de mais informações!'
            )
            submit_button = st.form_submit_button(label='Enviar')

        destinatario_fixo = 'sconsultoria2024@gmail.com'

        # Processar envio do formulário
        if submit_button:
            if remetente and assunto and conteudo:
                conteudo = f"{conteudo}\n\nMunicípio: {municipio}\nEstado: {estado}"
                status = enviar_email(remetente, destinatario_fixo, assunto, conteudo)
                if "sucesso" in status:
                    st.success(status)
                else:
                    st.error(status)
            else:
                st.error("Por favor, preencha todos os campos antes de enviar.")
    else:
        st.warning("Aguarde, autenticando com o Google...")

from datetime import datetime

# Função para calcular prazos por fase
def calcular_prazos_por_fase(fases):
    dados = []

    # Considera apenas as fases '2018-2021' e '2022-2025'
    fases_consideradas = ['2018-2021', '2022-2025']
    
    for item in fases:
        fase = item[0]
        exercicio = item[1]
        
        if fase not in fases_consideradas:
            continue
        
        # Define os anos de início e fim da fase
        fase_inicio_ano, fase_fim_ano = map(int, fase.split('-'))
        fase_inicio = datetime(fase_inicio_ano, 1, 1)
        fase_fim = datetime(fase_fim_ano, 1, 1)
        
        # Datas para o PMS e execução da fase
        pms_prazo = fase_inicio if exercicio == 0 else None
        pms_execucao_inicio = fase_inicio if exercicio == 0 else None
        pms_execucao_fim = fase_fim if exercicio == 0 else None
        
        if exercicio != 0:
            # Calcula o prazo do RAG para o ano seguinte ao exercício atual
            rag_prazo = datetime(exercicio + 1, 3, 30)
            
            # Define o prazo do PAS para 1º de outubro do ano corrente
            pas_prazo = datetime(exercicio, 10, 1)
            
            # Calcula os prazos dos RDQA nos quadrimestres correspondentes
            rdqa_prazos = [
                datetime(exercicio, 6, 2),
                datetime(exercicio, 9, 1),
                datetime(exercicio, 12, 1),
                datetime(exercicio + 1, 3, 3)
            ]
            rdqa_prazos = [rdqa.strftime("%d de %B de %Y") for rdqa in rdqa_prazos]
        else:
            rag_prazo = None
            pas_prazo = None
            rdqa_prazos = [None, None, None, None]
        
        dados.append({
            'Fase': fase,
            'Exercício': exercicio,
            'PMS': pms_prazo.strftime("%d de %B de %Y") if pms_prazo else None,
            'PMS Execução Início': pms_execucao_inicio.strftime("%d de %B de %Y") if pms_execucao_inicio else None,
            'PMS Execução Fim': pms_execucao_fim.strftime("%d de %B de %Y") if pms_execucao_fim else None,
            'RAG': rag_prazo.strftime("%d de %B de %Y") if rag_prazo else None,
            'PAS': pas_prazo.strftime("%d de %B de %Y") if pas_prazo else None,
            '1º RDQA': rdqa_prazos[0],
            '2º RDQA': rdqa_prazos[1],
            '3º RDQA': rdqa_prazos[2],
            '4º RDQA': rdqa_prazos[3]
        })
    
    df_prazos = pd.DataFrame(dados)
    return df_prazos

# Exemplo de uso
fases_dados = [
    ('2018-2021', 0), ('2018-2021', 2018), ('2018-2021', 2019), ('2018-2021', 2020), ('2018-2021', 2021),
    ('2022-2025', 0), ('2022-2025', 2022), ('2022-2025', 2023), ('2022-2025', 2024), ('2022-2025', 2025)
]

df_prazos = calcular_prazos_por_fase(fases_dados)

def main():
    """
    Interface principal do aplicativo para consulta e visualização de dados.
    """
    st.title('Situação do DigiSUS - Módulo Planejamento')
    st.markdown('*Consulte a situação do DigiSUS no seu município*')

    # Seleção de estado
    estados = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT',
               'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
    estado_selecionado = st.selectbox('Selecione o Estado', estados)

    # Seleção de município
    municipios_validos = []
    df = pd.DataFrame()
    if estado_selecionado:
        df = load_data_from_state(estado_selecionado)
        if not df.empty:
            municipios_validos = df['MUNICIPIO'].dropna().unique()

    municipio = st.selectbox('Selecione o Município', municipios_validos)

    if st.button('Consultar'):
        st.divider()
        if municipio:
            st.session_state['municipio'] = municipio
            st.session_state['estado_selecionado'] = estado_selecionado

            with st.spinner('Processando consulta...'):
                tabela_formatada = gerar_tabela_formatada(df, municipio)
                time.sleep(2)  # Simula um tempo de processamento

                if not tabela_formatada.empty:
                    # Exibir tabelas formatadas
                    styled_df = tabela_formatada.style.map(highlight_cells)
                    styled_df2 = tabela_ideal.style.map(highlight_cells)

                    st.subheader('Como está seu município:')
                    st.dataframe(styled_df)
                    st.subheader('Como deveria estar:')
                    st.dataframe(styled_df2)

                    # Criar prompt para análise do Groq
                    prompt = f"""
                    Analise a tabela de dados fornecida, que mostra a entrega dos seguintes documentos: Plano Municipal de Saúde (PMS), Programação Anual de Saúde (PAS), Relatórios Detalhados do Quadrimestre Anterior (RDQA) e Relatório Anual de Gestão (RAG).
                    Título: Situação do DigiSUS de {municipio}-{estado_selecionado}.
                    A análise deve cobrir os seguintes aspectos:
                    1. Verifique se todos os documentos foram apresentados conforme exigido (estamos em {data_formatada}).
                    2. Avalie a conformidade dos documentos com a Lei nº 8.142/90, a Lei Complementar nº 141/12 e a Portaria de Consolidação nº 1/2017.
                    3. Destaque quaisquer lacunas ou atrasos na apresentação dos documentos. :red-background[Destaque de vermelho os atrasos com mais de 1 ano])
                    4. Sugira melhorias para garantir a conformidade e a qualidade dos documentos.
                    
                    Verifique com cuidado estes prazos:
                    Prazos:
                    """

                    for _, row in df_prazos.iterrows():
                        fase = row['Fase']
                        exercicio = row['Exercício']
                        if exercicio == 0:
                            prompt += f"\nFase {fase} - PMS:\n"
                            prompt += f"- Plano Municipal de Saúde (PMS): prazo até {row['PMS']}. Execução inicia-se em {row['PMS Execução Início']} e finaliza-se em {row['PMS Execução Fim']}.\n"
                        else:
                            prompt += f"\nFase {fase} - {exercicio}:\n"
                            prompt += f"- Relatório Anual de Gestão (RAG): prazo até {row['RAG']}.\n"
                            prompt += f"- Programação Anual de Saúde (PAS): prazo até {row['PAS']}.\n"
                            prompt += f"- Relatório Quadrimestral: 1º RDQA: {row['1º RDQA']}, 2º RDQA: {row['2º RDQA']}, 3º RDQA: {row['3º RDQA']}, 4º RDQA: {row['4º RDQA']}.\n"

                    prompt += f"""
                    ATENÇÃO:
                    (estamos em {data_formatada}). Calcule quantos dias do prazo para cada documento.
                    - Quando EXERCÍCIO for 0, comente sobre o PMS, quando o valor for > 0, analise os demais documentos.
                    - Não comente o conteúdo dos documentos, apenas a tempestividade de sua apresentação.
                    - Todo Aprovado está no prazo.
                    - Tudo que for da data atual pra frente está em dia.
                    - Nunca cite o Exercício 0.
                    - Não fale em prazos de entrega.
                    - Não cite datas.
                    - Destaque o texto com verde, laranja e vermelho onde aplicável.
                    
                    Colored text and background colors for text, usando a sintaxe :color[text to be colored] e :color-background[text to be colored], respectivamente. color deve ser substituído por qualquer uma das seguintes cores suportadas: blue, green, orange, red, violet, gray/grey, rainbow. Por exemplo, você pode usar :orange[your text here] ou :blue-background[your text here].
                    """
                    
                    analise_ia = analisar_dataframe_groq(tabela_formatada, prompt, municipio)
                    st.subheader('Análise IA:')
                    st.markdown(analise_ia)

                    st.subheader('Quem somos?')
                    st.image('robo.png', caption='Estamos comprometidos em impulsionar a gestão da saúde pública municipal ao próximo nível.')
                    texto = """
                    <p style="text-align: justify;">
                        Somos especializados em gestão pública de saúde e ajudamos secretarias municipais a alcançar a excelência em sua gestão, garantindo um sistema de saúde mais eficiente, transparente e humanizado.
                        <strong>Nossas vantagens incluem:</strong>
                        <ul>
                            <li><strong>Eficiência com IA e Automação</strong>: Utilizamos inteligência artificial e automação para analisar dados municipais e elaborar documentos com máxima assertividade e rapidez.</li>
                            <li><strong>Expertise Técnica</strong>: Nossos técnicos possuem vasta experiência na gestão da saúde, oferecendo soluções de ponta.</li>
                            <li><strong>Transparência</strong>: Implementamos práticas que asseguram a clareza e a responsabilidade em todas as operações.</li>
                            <li><strong>Humanização</strong>: Colocamos o cidadão no centro das nossas estratégias, proporcionando um atendimento mais humano e acolhedor.</li>
                        </ul>
                        <strong>Seja referência em gestão pública de saúde.</strong>
                         Conte com Mais Gestor para transformar a realidade da sua secretaria de forma rápida e eficiente.
                         Juntos, vamos construir um futuro mais saudável para todos.
                        <br><br>
                        <strong>Entre em contato agora mesmo clicando no menu acima.</strong>
                    </p>
                    """
                    st.markdown(texto, unsafe_allow_html=True)

# Define o menu horizontal com a biblioteca streamlit_option_menu
selected_page = option_menu(
    menu_title=None,   # Sem título para o layout horizontal
    options=["Consulta", "Contato"],
    icons=["search", "envelope"],  # Ícones para cada opção
    menu_icon="cast",  # Ícone do menu (não usado aqui)
    default_index=0,   # Seleção padrão
    orientation="horizontal"  # Layout horizontal
)

# Mostra a página selecionada
if selected_page == "Contato":
    if 'municipio' in st.session_state and 'estado_selecionado' in st.session_state:
        contato()
    else:
        st.warning("Por favor, realize a consulta primeiro para definir o município e o estado.")
else:
    main()
