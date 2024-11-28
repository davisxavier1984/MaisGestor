import os
import pandas as pd
import streamlit as st
import requests
import tempfile
import google.generativeai as genai
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import time
from streamlit_option_menu import option_menu
import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Acessa a variável de ambiente GROQ_API_KEY
api_key = os.getenv("Api_key")

# Display the logo at the top of the page, centered
st.image('logo_maisgestor.png')

data_atual = datetime.date.today()
data_formatada = data_atual.strftime("%d de %B de %Y")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

from datetime import datetime, timedelta

# Função para calcular os prazos exatos dos documentos

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



# Função para analisar a tabela usando a API Google Generative AI
def analisar_dataframe_gemini(df: pd.DataFrame, api_key: str, prompt: str, municipio: str, model: str = 'gemini-1.5-flash', temperature: float = 0, stop_sequence: str = '17') -> str:
    """
    Usa a API Google Generative AI para analisar um DataFrame de acordo com o prompt fornecido.

    Parâmetros:
    df (pd.DataFrame): DataFrame com os dados a serem analisados.
    api_key (str): Chave da API para autenticação.
    prompt (str): O prompt de análise que orienta o modelo.
    municipio (str): Nome do município a ser incluído na análise.
    model (str): Modelo do Google Generative AI a ser usado (default: 'gemini-1.5-flash').
    temperature (float): Controla a criatividade e variabilidade das respostas (default: 0.7).
    stop_sequence (str): Sequência de parada para a geração de conteúdo (default: '\n').

    Retorna:
    str: Análise gerada pelo modelo Google Generative AI.
    """
    # Configura a chave da API
    genai.configure(api_key=api_key)

    # Converte o DataFrame para uma string formatada
    df_text = df.to_string(index=False) if isinstance(df, pd.DataFrame) else df

    # Cria o prompt completo com a tabela e o nome do município
    full_prompt = f"{prompt}\n\nAqui está a tabela de dados para o município de {municipio}:\n\n{df_text}"
    
    # Configura o modelo e a geração de conteúdo
    config = genai.GenerationConfig(temperature=temperature, stop_sequences=[stop_sequence])
    model = genai.GenerativeModel(model, system_instruction=None)
    
    # Executa a geração de conteúdo com o modelo especificado
    response = model.generate_content(contents=[full_prompt], generation_config=config)

    # Retorna o texto da resposta ou uma mensagem de erro em branco
    return response.text.strip() if response and response.text.strip() else "Nenhum resultado gerado. Por favor, verifique o prompt e tente novamente."




# Função para formatar as cores da Tabela
def highlight_cells(val):
   
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

# Função para gerar a tabela formatada
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

# Função para carregar credenciais OAuth2 e armazenar em session_state
def carregar_credenciais():
    if 'creds' in st.session_state:
        return st.session_state['creds']
        
    creds = None

    # Verifica se o arquivo de token existe e o carrega
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Se as credenciais não estão válidas, executa o fluxo OAuth2
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)  # Usando run_local_server
            
        # Salva o token para uso futuro
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Armazena as credenciais em session_state para reutilização
    st.session_state['creds'] = creds
    return creds



# Função para criar a mensagem do email
def criar_mensagem(remetente, destinatario, assunto, conteudo):
    mensagem = MIMEText(conteudo)
    mensagem['to'] = destinatario
    mensagem['from'] = remetente
    mensagem['subject'] = assunto
    return {'raw': base64.urlsafe_b64encode(mensagem.as_bytes()).decode()}

# Função para enviar o email
def enviar_email(remetente, destinatario, assunto, conteudo):
    creds = carregar_credenciais()
    try:
        # Constrói o serviço da API do Gmail
        service = build('gmail', 'v1', credentials=creds)
        mensagem = criar_mensagem(remetente, destinatario, assunto, conteudo)
        # Envia o email usando a API do Gmail
        enviado = service.users().messages().send(userId="me", body=mensagem).execute()
        return f"Mensagem enviada com sucesso! Em breve entraremos em contato."

    except Exception as e:
        return f"Erro ao enviar email: {e}"
    
# Função para mapear estados para os seus respectivos códigos UF
def get_uf_code(state):
    uf_codes = {
        'AC': '12', 'AL': '27', 'AM': '13', 'AP': '16', 'BA': '29', 'CE': '23',
        'DF': '53', 'ES': '32', 'GO': '52', 'MA': '21', 'MG': '31', 'MS': '50',
        'MT': '51', 'PA': '15', 'PB': '25', 'PE': '26', 'PI': '22', 'PR': '41',
        'RJ': '33', 'RN': '24', 'RO': '11', 'RR': '14', 'RS': '43', 'SC': '42',
        'SE': '28', 'SP': '35', 'TO': '17'
    }
    return uf_codes.get(state.upper())

@st.cache_data
def Carregando_arquivos(state):
    uf_code = get_uf_code(state)
    if uf_code is None:
        st.error(f"Código da UF para o estado '{state}' não encontrado.")
        return None
    url = f'https://digisusgmp.saude.gov.br/v1.5/transparencia/extracao/csv?uf={uf_code}'
    temp_dir = tempfile.gettempdir()
    local_file = os.path.join(temp_dir, f'{state}.csv')
    try:
        response = requests.get(url)
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

@st.cache_data
def load_data_from_state(state):
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

# Autenticação automática ao iniciar o aplicativo
if 'creds' not in st.session_state:
    carregar_credenciais()

def contato():
    
    st.title('Formulário de Contato')

    if 'creds' in st.session_state:
        with st.form(key='form_email'):
            estado = st.session_state['estado_selecionado']
            municipio = st.session_state['municipio']
            remetente = st.text_input('Seu Email :red[*]')
            assunto = st.text_input("Contato (Fone/Whatsapp)")
            conteudo = st.text_area("Deixe uma mensagem", placeholder=f'Olá, sou de {municipio}-{estado}, e gostaria de mais informações!')
            submit_button = st.form_submit_button(label='Enviar')

        destinatario_fixo = 'Alyssonmentoria@gmail.com'

        if submit_button:
            if remetente and assunto and conteudo:
                #municipio = st.session_state['municipio']
                #estado = st.session_state['estado_selecionado']
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

def main():
    st.title('Situação do DigiSUS - Módulo Planejamento')
    st.markdown('*Consulte a situação do DigiSUS no seu município*')

    estados = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
    estado_selecionado = st.selectbox('Selecione o Estado', estados)

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
                    styled_df = tabela_formatada.style.map(highlight_cells)
                    styled_df2 = tabela_ideal.style.map(highlight_cells)
                    st.subheader('Como está seu município:')
                    st.dataframe(styled_df)
                    st.subheader('Como deveria estar:')
                    st.dataframe(styled_df2)
                    
            # Transcrever a tabela
            with st.spinner('Analisando a tabela, por favor aguarde...'):
                def transcrever_tabela(df):
                    linhas = []
                    for index, row in df.iterrows():
                        linha = f"FASE: {row['FASE']}, EXERCICIO: {row['EXERCICIO']}, PMS: {row['PMS']}, PAS: {row['PAS']}, 1º RDQA: {row['1º RDQA']}, 2º RDQA: {row['2º RDQA']}, 3º RDQA: {row['3º RDQA']}, RAG: {row['RAG']}"
                        linhas.append(linha)
                    return "\n".join(linhas)

                tabela_transcrita = transcrever_tabela(tabela_formatada)

                prazos_por_fase = calcular_prazos_por_fase(df)

                api_key = "AIzaSyCAsdH3sVjucefEudnHnGABAlayMXPE5Wo"
                
                prompt = f"""
                Analise a tabela de dados fornecida, que mostra a entrega dos seguintes documentos: Plano Municipal de Saúde (PMS), Programação Anual de Saúde (PAS), Relatórios Detalhados do Quadrimestre Anterior (RDQA) e Relatório Anual de Gestão (RAG).
                Título: Situação do DigiSUS de {municipio}-{estado_selecionado}.
                A análise deve cobrir os seguintes aspectos:
                1. Verifique se todos os documentos foram apresentados conforme exigido (estamos em {data_formatada}).
                2. Avalie a conformidade dos documentos com a Lei nº 8.142/90, a Lei Complementar nº 141/12 e a Portaria de Consolidação nº 1/2017.
                3. Destaque quaisquer lacunas ou atrasos na apresentação dos documentos. (:red[Destaque de vermelho os pontos mais graves])
                4. Sugira melhorias para garantir a conformidade e a qualidade dos documentos.
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

                prompt += f"(estamos em {data_formatada}). Calcule quantos dias do prazo para cada documento. \n"
                prompt += f"- Quando EXERCÍCIO for 0, comente sobre o PMS, quando o valor for > 0, analise os demais documentos. \n"
                prompt += f"- Não comente o conteúdo dos documentos, apenas a tempestividade de sua apresentação. \n"
                prompt += f"- Todo Aprovado está no prazo. \n"
                prompt += f"- Tudo que for da data atual pra frente está em dia. \n"
                prompt += f"- Nunca cite o Exercício 0. \n"
                prompt += f"- Não fale em prazos de entrega. \n"
                prompt += f"- Não cite datas. \n"
                prompt += f"- Qualquer situação só é grave com mais de 1 ano de atraso. \n"
                prompt += f"- Destaque o texto com verde, laranja e vermelho onde aplicável. \n"
                #prompt += f"- Ao final, confira os prazos novamente. \n"
                prompt += f"Colored text and background colors for text, using the syntax :color[text to be colored] and :color-background[text to be colored], respectively. color must be replaced with any of the following supported colors: blue, green, orange, red, violet, gray/grey, rainbow. For example, you can use :orange[your text here] or :blue-background[your text here]. \n"
                
                
                # st.write(tabela_transcrita)
                # st.write(prompt)
                # st.write(municipio)
                analise_ia = analisar_dataframe_gemini(tabela_transcrita, api_key, prompt, municipio)
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
                    Conte com o Mais Gestor para transformar a realidade da sua secretaria de forma rápida e eficiente.
                    Juntos, vamos construir um futuro mais saudável para todos.
                    <br><br>
                    <strong>Entre em contato agora mesmo clicando no menu acima.</strong>
                </p>
                """
                st.markdown(texto, unsafe_allow_html=True)

# Define the horizontal menu with streamlit_option_menu
selected_page = option_menu(
    menu_title=None,   # No title for horizontal layout
    options=["Consulta", "Contato"],
    icons=["search", "envelope"],  # Icons for each option
    menu_icon="cast",  # Icon for the menu (not relevant here)
    default_index=0,   # Default selection
    orientation="horizontal"  # Horizontal layout
)

# Display the selected page
if selected_page == "Contato":
    if 'municipio' in st.session_state and 'estado_selecionado' in st.session_state:
        contato()
    else:
        st.warning("Por favor, realize a consulta primeiro para definir o município e o estado.")
else:
    main()
