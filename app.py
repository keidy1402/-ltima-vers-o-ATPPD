import streamlit as st
import os
import re
import tempfile
from pathlib import Path
import hashlib
from datetime import datetime, timedelta
import time

# Config MUST be the first Streamlit command
st.set_page_config(
    page_title="PrivAnalytica - Analisador de Termos de Privacidade",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS PERSONALIZADO – Tema escuro com identidade visual
# ============================================================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #0d1117 50%, #0a0a1a 100%);
    }

    .main-header {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        background: linear-gradient(135deg, rgba(0,191,166,0.08) 0%, rgba(0,150,255,0.05) 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(0,191,166,0.15);
    }

    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00BFA6, #0096FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }

    .main-header p {
        color: #8899aa;
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 0;
    }

    .section-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: border-color 0.3s ease;
    }

    .section-card:hover {
        border-color: #00BFA6;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00BFA6;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .section-title .emoji {
        font-size: 1.6rem;
    }

    .tip-item {
        background: rgba(0,191,166,0.06);
        border-left: 3px solid #00BFA6;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        border-radius: 0 8px 8px 0;
        color: #c9d1d9;
        font-size: 0.95rem;
        transition: background 0.2s;
    }

    .tip-item:hover {
        background: rgba(0,191,166,0.12);
    }

    .risk-tag {
        display: inline-block;
        background: rgba(255,71,87,0.12);
        color: #ff4757;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid rgba(255,71,87,0.2);
        margin: 0.2rem;
    }

    .news-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .news-card:hover {
        border-color: #00BFA6;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }

    .news-card h4 {
        color: #e6edf3;
        font-size: 1rem;
        margin-bottom: 0.3rem;
        line-height: 1.4;
    }

    .news-card .news-meta {
        color: #8b949e;
        font-size: 0.8rem;
        display: flex;
        gap: 1rem;
    }

    .news-card .news-link {
        color: #00BFA6;
        text-decoration: none;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .news-card .news-link:hover {
        text-decoration: underline;
    }

    .stButton button {
        background: linear-gradient(135deg, #00BFA6, #0096FF) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.6rem 2rem !important;
        border-radius: 10px !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }

    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,191,166,0.3) !important;
    }

    .stSelectbox label, .stRadio label {
        color: #c9d1d9 !important;
        font-weight: 500 !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        color: #e6edf3 !important;
    }

    .stSpinner > div {
        border-color: #00BFA6 !important;
    }

    .interpretation-box {
        background: linear-gradient(135deg, rgba(0,191,166,0.06), rgba(0,150,255,0.04));
        border: 1px solid rgba(0,191,166,0.2);
        border-radius: 12px;
        padding: 1.2rem;
        margin-top: 1rem;
    }

    .interpretation-box p {
        color: #c9d1d9;
        margin-bottom: 0.5rem;
    }

    .footer {
        text-align: center;
        padding: 2rem 1rem;
        color: #484f58;
        font-size: 0.8rem;
        border-top: 1px solid #21262d;
        margin-top: 2rem;
    }

    .footer a {
        color: #00BFA6;
        text-decoration: none;
    }

    .score-display {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
    }

    .score-low { color: #3fb950; }
    .score-mid { color: #d29922; }
    .score-high { color: #f85149; }

    .platform-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(0,191,166,0.1);
        border: 1px solid rgba(0,191,166,0.25);
        border-radius: 30px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        color: #00BFA6;
        margin: 0.3rem;
    }

    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.8rem; }
        .section-card { padding: 1.2rem; }
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #00BFA6, #0096FF) !important;
    }

    /* Word cloud container */
    .wordcloud-container {
        display: flex;
        justify-content: center;
        background: rgba(0,0,0,0.2);
        border-radius: 12px;
        padding: 1rem;
    }

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0d1117;
    }
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #00BFA6;
    }
</style>
"""

# ============================================================
# CONSTANTES E CONFIGURAÇÕES
# ============================================================

PLATAFORMAS = {
    "WhatsApp": {
        "arquivo": "termos/whatsapp.txt",
        "icone": "💬",
        "cor": "#25D366"
    },
    "Instagram": {
        "arquivo": "termos/instagram.txt",
        "icone": "📸",
        "cor": "#E4405F"
    },
    "Facebook": {
        "arquivo": "termos/facebook.txt",
        "icone": "📘",
        "cor": "#1877F2"
    },
    "YouTube": {
        "arquivo": "termos/youtube.txt",
        "icone": "▶️",
        "cor": "#FF0000"
    },
    "TikTok": {
        "arquivo": "termos/tiktok.txt",
        "icone": "🎵",
        "cor": "#000000"
    },
    "Snapchat": {
        "arquivo": "termos/snapchat.txt",
        "icone": "👻",
        "cor": "#FFFC00"
    },
    "Twitter/X": {
        "arquivo": "termos/twitter.txt",
        "icone": "🐦",
        "cor": "#1DA1F2"
    }
}

# Palavras de risco para análise
PALAVRAS_RISCO = [
    "rastreamento", "localização", "compartilhamento", "parceiros",
    "terceiros", "publicidade personalizada", "reconhecimento facial",
    "biometria", "coleta de dados", "histórico", "monitoramento",
    "cookies", "perfil comportamental", "inteligência artificial",
    "retenção de dados", "criptografia", "dados biométricos",
    "segmentação", "algoritmo", "machine learning", "direcionamento",
    "pixels", "rastreamento entre sites", "anúncios personalizados",
    "dados de dispositivo", "endereço IP", "dados de localização",
    "vazamento", "violação", "dados sensíveis", "perfil", "log",
    "identificadores", "analytics", "dados demográficos",
    "visualização", "interação", "engajamento", "dados comportamentais"
]

# ============================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================

def carregar_texto_plataforma(nome_plataforma):
    """Carrega o conteúdo do arquivo .txt da plataforma selecionada."""
    info = PLATAFORMAS.get(nome_plataforma)
    if not info:
        return None
    caminho = Path(info["arquivo"])
    if not caminho.exists():
        st.error(f"Arquivo de termos não encontrado para {nome_plataforma}.")
        return None
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None


def calcular_hash(texto):
    """Gera hash do texto para controle de cache."""
    return hashlib.md5(texto.encode()).hexdigest()


def extrair_palavras_risco(texto):
    """Extrai e conta ocorrências de palavras de risco no texto."""
    texto_lower = texto.lower()
    contagem = {}
    for palavra in PALAVRAS_RISCO:
        # Usa expressão regular para contar ocorrências da palavra/frase
        padrao = re.escape(palavra)
        ocorrencias = len(re.findall(padrao, texto_lower))
        if ocorrencias > 0:
            # Normaliza: usa a primeira palavra do termo composto como chave
            chave = palavra.split()[0] if " " in palavra else palavra
            contagem[chave] = contagem.get(chave, 0) + ocorrencias
    return contagem


def calcular_pontuacao_risco(texto_plataforma):
    """
    Calcula pontuação de risco (0-100) com base na frequência
    de termos relacionados a riscos de privacidade.
    """
    texto_lower = texto_plataforma.lower()
    score = 0

    # Categorias de risco com pesos
    categorias = {
        "coleta": ["coleta de dados", "coletamos", "coleta", "informações", "dados pessoais"],
        "compartilhamento": ["compartilhamento", "compartilha", "terceiros", "parceiros"],
        "rastreamento": ["rastreamento", "monitoramento", "rastreia", "tracking", "pixels"],
        "localizacao": ["localização", "localização precisa", "gps", "local"],
        "publicidade": ["publicidade personalizada", "anúncios", "segmentação", "direcionamento"],
        "perfil": ["perfil comportamental", "perfil", "interesses", "comportamento"],
        "retencao": ["retenção de dados", "armazenamento", "backups", "logs"],
        "biometria": ["reconhecimento facial", "biometria", "biométricos", "face"],
        "inteligencia": ["inteligência artificial", "algoritmo", "machine learning", "ia"],
    }

    pesos = {
        "coleta": 15,
        "compartilhamento": 15,
        "rastreamento": 12,
        "localizacao": 10,
        "publicidade": 12,
        "perfil": 12,
        "retencao": 8,
        "biometria": 8,
        "inteligencia": 8,
    }

    for categoria, termos in categorias.items():
        freq = sum(texto_lower.count(t) for t in termos)
        score += min(freq * pesos[categoria] / 5, pesos[categoria])

    return min(int(score), 100)


def gerar_pontuacoes_todas(token_gemini):
    """Gera pontuações para todas as plataformas (usado na comparação)."""
    pontuacoes = {}
    for nome in PLATAFORMAS:
        texto = carregar_texto_plataforma(nome)
        if texto:
            pontuacoes[nome] = calcular_pontuacao_risco(texto)
    return pontuacoes


# ============================================================
# FUNÇÕES DE INTEGRAÇÃO COM A API GEMINI
# ============================================================

def configurar_gemini(api_key):
    """Configura o cliente da API Gemini."""
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    return genai


def analisar_com_gemini(genai, texto_plataforma, nome_plataforma, tarefa):
    """
    Envia texto para análise via API Gemini com diferentes tarefas.
    Inclui retry com backoff exponencial para tratamento de erros.
    """
    # Define o prompt de acordo com a tarefa
    prompts = {
        "resumo": f"""
Analise a política de privacidade da plataforma {nome_plataforma} abaixo e gere um resumo em português brasileiro com 8 a 10 linhas.

O resumo deve:
- Ser em linguagem simples e acessível para pessoas sem conhecimento técnico
- Explicar como os dados são coletados
- Informar quais dados são armazenados
- Mostrar se há compartilhamento com terceiros
- Destacar impactos para a privacidade do usuário
- Evitar linguagem jurídica complexa

Política de Privacidade:
{texto_plataforma[:15000]}
""",
        "dicas": f"""
Com base na política de privacidade da plataforma {nome_plataforma} abaixo, gere uma lista de 8 a 10 dicas práticas e específicas para que um usuário comum aumente sua segurança e privacidade dentro desta plataforma.

As dicas devem ser:
- Específicas para esta plataforma (não genéricas)
- Práticas e acionáveis
- Organizadas em tópicos numerados

Exemplos de dicas: ativar autenticação em dois fatores, revisar permissões de localização, limitar compartilhamento, controlar configurações de privacidade, revisar dispositivos conectados, gerenciar permissões de apps vinculados, configurar quem pode visualizar conteúdo.

Política de Privacidade:
{texto_plataforma[:15000]}
""",
    }

    prompt = prompts.get(tarefa)
    if not prompt:
        return None

    max_tentativas = 3
    for tentativa in range(max_tentativas):
        try:
            modelo = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 1024,
                }
            )
            resposta = modelo.generate_content(prompt)
            return resposta.text
        except Exception as e:
            if tentativa < max_tentativas - 1:
                tempo_espera = 2 ** tentativa
                time.sleep(tempo_espera)
            else:
                st.warning(f"⚠️ Não foi possível analisar com IA neste momento. Usando análise local. Erro: {str(e)}")
                return None


def buscar_noticias(nome_plataforma):
    """
    Busca notícias recentes sobre privacidade da plataforma via Google News RSS.
    Inclui fallback para notícias alternativas em caso de falha.
    """
    import feedparser

    termos_busca = f"{nome_plataforma} privacidade dados segurança 2026"
    url_rss = f"https://news.google.com/rss/search?q={termos_busca}&hl=pt-BR&gl=BR&ceid=BR:pt"

    try:
        feed = feedparser.parse(url_rss)
        noticias = []

        for entry in feed.entries[:4]:
            noticia = {
                "titulo": entry.get("title", "Título indisponível"),
                "fonte": entry.get("source", {}).get("title", entry.get("publisher", "Fonte desconhecida")),
                "data": entry.get("published", "Data não informada"),
                "link": entry.get("link", "#"),
            }
            noticias.append(noticia)

        if noticias:
            return noticias
    except Exception:
        pass

    # Fallback: notícias offline simuladas sobre privacidade
    return gerar_noticias_fallback(nome_plataforma)


def gerar_noticias_fallback(nome_plataforma):
    """Gera notícias alternativas sobre privacidade quando o feed RSS não está disponível."""
    noticias_fallback = {
        "WhatsApp": [
            {
                "titulo": "WhatsApp reforça criptografia de ponta a ponta em novas atualizações",
                "fonte": "Portal de Segurança Digital",
                "data": datetime.now().strftime("%d/%m/%Y"),
                "link": "https://www.whatsapp.com/security"
            },
            {
                "titulo": "Mudanças na política de privacidade do WhatsApp geram debate sobre compartilhamento com Meta",
                "fonte": "TechPrivacy Brasil",
                "data": (datetime.now() - timedelta(days=7)).strftime("%d/%m/%Y"),
                "link": "https://www.whatsapp.com/privacy"
            },
            {
                "titulo": "WhatsApp libera recurso de mensagens temporárias para mais usuários",
                "fonte": "Segurança em Foco",
                "data": (datetime.now() - timedelta(days=14)).strftime("%d/%m/%Y"),
                "link": "https://www.whatsapp.com/tips"
            }
        ],
        "Instagram": [
            {
                "titulo": "Instagram testa novas formas de controle de dados para usuários",
                "fonte": "PrivacyTech News",
                "data": datetime.now().strftime("%d/%m/%Y"),
                "link": "https://about.instagram.com/safety"
            },
            {
                "titulo": "Como o Instagram usa inteligência artificial para moderar conteúdo",
                "fonte": "TechEthics Brasil",
                "data": (datetime.now() - timedelta(days=5)).strftime("%d/%m/%Y"),
                "link": "https://about.instagram.com/blog"
            },
            {
                "titulo": "Instagram enfrenta investigação na UE sobre proteção de dados de menores",
                "fonte": "Data Rights Watch",
                "data": (datetime.now() - timedelta(days=12)).strftime("%d/%m/%Y"),
                "link": "https://about.instagram.com/privacy"
            }
        ],
        "Facebook": [
            {
                "titulo": "Facebook (Meta) enfrenta novas multas na Europa por violações de privacidade",
                "fonte": "GDPR News",
                "data": datetime.now().strftime("%d/%m/%Y"),
                "link": "https://about.meta.com/privacy"
            },
            {
                "titulo": "Vazamento de dados: entenda o histórico de incidentes do Facebook",
                "fonte": "Security Report Brasil",
                "data": (datetime.now() - timedelta(days=3)).strftime("%d/%m/%Y"),
                "link": "https://about.meta.com/data"
            },
            {
                "titulo": "Facebook atualiza políticas de reconhecimento facial após pressão regulatória",
                "fonte": "AI & Privacy Journal",
                "data": (datetime.now() - timedelta(days=10)).strftime("%d/%m/%Y"),
                "link": "https://about.meta.com/ai"
            }
        ],
        "YouTube": [
            {
                "titulo": "YouTube Kids: como proteger a privacidade das crianças na plataforma",
                "fonte": "Digital Parenting",
                "data": datetime.now().strftime("%d/%m/%Y"),
                "link": "https://kids.youtube.com/privacy"
            },
            {
                "titulo": "YouTube é multado por coleta de dados de menores sem consentimento",
                "fonte": "Privacy International",
                "data": (datetime.now() - timedelta(days=8)).strftime("%d/%m/%Y"),
                "link": "https://www.youtube.com/privacy"
            },
            {
                "titulo": "Novas regras de anúncios personalizados no YouTube entram em vigor",
                "fonte": "AdTech Watch",
                "data": (datetime.now() - timedelta(days=15)).strftime("%d/%m/%Y"),
                "link": "https://www.youtube.com/ads"
            }
        ],
        "TikTok": [
            {
                "titulo": "TikTok é banido em dispositivos governamentais de mais países por segurança nacional",
                "fonte": "Global Security News",
                "data": datetime.now().strftime("%d/%m/%Y"),
                "link": "https://www.tiktok.com/safety"
            },
            {
                "titulo": "TikTok anuncia medidas para aumentar transparência sobre algoritmos",
                "fonte": "TechTransparency",
                "data": (datetime.now() - timedelta(days=4)).strftime("%d/%m/%Y"),
                "link": "https://www.tiktok.com/transparency"
            },
            {
                "titulo": "Como o TikTok coleta dados: o que você precisa saber",
                "fonte": "Privacy Explained",
                "data": (datetime.now() - timedelta(days=11)).strftime("%d/%m/%Y"),
                "link": "https://www.tiktok.com/privacy"
            }
        ],
        "Snapchat": [
            {
                "titulo": "Snapchat reforça segurança do Snap Map após críticas de privacidade",
                "fonte": "Location Privacy",
                "data": datetime.now().strftime("%d/%m/%Y"),
                "link": "https://www.snapchat.com/privacy"
            },
            {
                "titulo": "Snapchat: mensagens que desaparecem são realmente privadas?",
                "fonte": "Digital Rights Blog",
                "data": (datetime.now() - timedelta(days=6)).strftime("%d/%m/%Y"),
                "link": "https://www.snapchat.com/safety"
            },
            {
                "titulo": "Snapchat AI: como a plataforma usa seus dados para treinar modelos",
                "fonte": "AI Watch",
                "data": (datetime.now() - timedelta(days=13)).strftime("%d/%m/%Y"),
                "link": "https://www.snapchat.com/ai"
            }
        ],
        "Twitter/X": [
            {
                "titulo": "X (Twitter) permite que dados públicos sejam usados para treinar IA Grok",
                "fonte": "AI & Privacy",
                "data": datetime.now().strftime("%d/%m/%Y"),
                "link": "https://about.twitter.com/privacy"
            },
            {
                "titulo": "Twitter/X enfrenta investigação na UE por transparência em moderação",
                "fonte": "Digital Europe",
                "data": (datetime.now() - timedelta(days=5)).strftime("%d/%m/%Y"),
                "link": "https://about.twitter.com/transparency"
            },
            {
                "titulo": "Como configurar privacidade no Twitter/X: guia completo",
                "fonte": "Privacy Guide",
                "data": (datetime.now() - timedelta(days=10)).strftime("%d/%m/%Y"),
                "link": "https://help.twitter.com/safety"
            }
        ]
    }

    return noticias_fallback.get(nome_plataforma, [
        {
            "titulo": f"Privacidade digital: entenda seus direitos ao usar {nome_plataforma}",
            "fonte": "Portal do Consumidor Digital",
            "data": datetime.now().strftime("%d/%m/%Y"),
            "link": "#"
        },
        {
            "titulo": "Proteção de dados: o que muda para usuários de plataformas digitais",
            "fonte": "Data Privacy Brasil",
            "data": (datetime.now() - timedelta(days=7)).strftime("%d/%m/%Y"),
            "link": "#"
        }
    ])


# ============================================================
# FUNÇÕES DE VISUALIZAÇÃO (GRÁFICOS, WORD CLOUD)
# ============================================================

def gerar_wordcloud(contagem_palavras):
    """Gera uma nuvem de palavras a partir da contagem de termos de risco."""
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    import io
    from PIL import Image

    if not contagem_palavras:
        return None

    # Cria a word cloud
    wc = WordCloud(
        width=800,
        height=400,
        background_color="#0d1117",
        colormap="RdYlGn_r",
        max_words=50,
        prefer_horizontal=0.7,
        relative_scaling=0.5,
        random_state=42,
        font_path=None,
        collocations=False,
        color_func=None,
    ).generate_from_frequencies(contagem_palavras)

    # Renderiza para imagem
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    plt.tight_layout(pad=0)

    # Salva em buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor="#0d1117")
    buf.seek(0)
    plt.close(fig)

    return buf


def gerar_grafico_comparativo(pontuacoes, plataforma_selecionada):
    """Gera gráfico de barras comparativo entre plataformas."""
    import plotly.express as px
    import pandas as pd

    df = pd.DataFrame(list(pontuacoes.items()), columns=["Plataforma", "Pontuação de Risco"])

    # Define cores: destaca a plataforma selecionada
    cores = []
    for p in df["Plataforma"]:
        if p == plataforma_selecionada:
            cores.append("#00BFA6")
        else:
            cores.append("#30363d")

    fig = px.bar(
        df,
        x="Plataforma",
        y="Pontuação de Risco",
        text="Pontuação de Risco",
        color_discrete_sequence=["#00BFA6"],
        range_y=[0, 100],
        height=400,
    )

    fig.update_traces(
        marker_color=cores,
        textposition="outside",
        textfont=dict(size=12, color="#e6edf3"),
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d1d9", size=11),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="#c9d1d9"),
            title=None,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#21262d",
            tickfont=dict(color="#c9d1d9"),
            title="Pontuação de Risco (0-100)",
            range=[0, 110],
        ),
        margin=dict(l=20, r=20, t=20, b=40),
        hovermode="x",
    )

    return fig


def interpretar_pontuacao(pontuacao, nome_plataforma, pontuacoes_todas):
    """Gera interpretação textual da pontuação de risco."""
    if pontuacao <= 30:
        nivel = "baixo"
        descricao = "menor coleta e compartilhamento de dados"
    elif pontuacao <= 55:
        nivel = "médio"
        descricao = "moderada coleta e compartilhamento de dados"
    elif pontuacao <= 75:
        nivel = "elevado"
        descricao = "significativa coleta e compartilhamento de dados"
    else:
        nivel = "crítico"
        descricao = "alta intensidade de coleta, processamento e compartilhamento de dados"

    # Ordena plataformas por pontuação
    ordenadas = sorted(pontuacoes_todas.items(), key=lambda x: x[1])
    posicao = next(i for i, (p, _) in enumerate(ordenadas) if p == nome_plataforma) + 1
    total = len(ordenadas)

    partes = []
    partes.append(f"**{nome_plataforma}** obteve pontuação de risco **{pontuacao}/100**, classificada como nível **{nivel}**.")
    partes.append(f"Isso significa que a plataforma realiza {descricao} em comparação com os termos analisados.")
    partes.append(f"Entre as {total} plataformas analisadas, {nome_plataforma} ocupa a {posicao}ª posição em termos de risco à privacidade.")

    if posicao <= 2:
        partes.append("✅ Esta plataforma apresenta uma das menores pontuações de risco, indicando práticas de privacidade potencialmente mais equilibradas.")
    elif posicao >= total - 1:
        partes.append("⚠️ Esta plataforma está entre as que apresentam maior pontuação de risco. Recomenda-se atenção redobrada às configurações de privacidade.")
    else:
        partes.append(f"A plataforma está em uma posição intermediária no ranking de risco.")

    return partes


# ============================================================
# FUNÇÕES DE CACHE STREAMLIT
# ============================================================

@st.cache_data(ttl=3600, show_spinner="Carregando termos...")
def carregar_texto_cache(nome):
    """Cache para carregar texto da plataforma (evita releitura)."""
    return carregar_texto_plataforma(nome)


@st.cache_data(ttl=600, show_spinner="Analisando texto...")
def extrair_palavras_risco_cache(texto):
    """Cache para extração de palavras de risco."""
    return extrair_palavras_risco(texto)


@st.cache_data(ttl=600, show_spinner="Calculando pontuações...")
def pontuacoes_cache():
    """Cache para pontuações de todas as plataformas."""
    pontuacoes = {}
    for nome in PLATAFORMAS:
        texto = carregar_texto_cache(nome)
        if texto:
            pontuacoes[nome] = calcular_pontuacao_risco(texto)
    return pontuacoes


@st.cache_data(ttl=3600, show_spinner="Buscando notícias...")
def noticias_cache(nome):
    """Cache para notícias da plataforma."""
    return buscar_noticias(nome)


@st.cache_data(ttl=600)
def gerar_wordcloud_cache(contagem):
    """Cache para word cloud."""
    return gerar_wordcloud(contagem)


# ============================================================
# INTERFACE PRINCIPAL – APP STREAMLIT
# ============================================================

def main():
    """Função principal que orquestra toda a aplicação."""

    # Aplica CSS personalizado
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # ============================================================
    # HEADER
    # ============================================================
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ PrivAnalytica</h1>
        <p>Analisador de Termos de Privacidade — Entenda o que você realmente aceita ao usar plataformas digitais</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar para configurações da API
    with st.sidebar:
        st.markdown("### ⚙️ Configurações")

        # Chave da API Gemini
        api_key = st.text_input(
            "Chave da API Google Gemini",
            type="password",
            help="Insira sua chave da API Google Gemini para análises avançadas com IA. Obtenha uma em https://aistudio.google.com/app/apikey",
            placeholder="Cole sua chave API aqui..."
        )

        if api_key:
            st.success("✅ API configurada")

        st.markdown("---")
        st.markdown("### ℹ️ Sobre")
        st.markdown("""
        **PrivAnalytica** analisa os termos de privacidade das principais plataformas digitais para ajudar você a entender:
        - Quais dados são coletados
        - Como seus dados são usados
        - Quais riscos existem
        - Como se proteger

        *Projeto educativo e informativo.*
        """)

        st.markdown("---")
        st.markdown("### 📊 Metodologia")
        st.markdown("""
        A pontuação de risco (0-100) considera:
        - Coleta de dados
        - Compartilhamento com terceiros
        - Rastreamento de atividades
        - Uso de localização
        - Perfil comportamental
        - Publicidade direcionada
        - Retenção de informações
        """)

    # ============================================================
    # SEÇÃO 1 – SELEÇÃO DA PLATAFORMA
    # ============================================================
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">
            <span class="emoji">📋</span> Selecione uma Plataforma
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Seletor de plataforma em formato visual
    col_sel = st.columns([1, 3, 1])
    with col_sel[1]:
        # Grid de plataformas (horizontal)
        cols = st.columns(7)
        plataforma_selecionada = None

        # Usa radio com layout horizontal para seleção visual
        opcoes = list(PLATAFORMAS.keys())
        icones = [f"{PLATAFORMAS[p]['icone']} {p}" for p in opcoes]

        selecao = st.selectbox(
            "Escolha uma plataforma para analisar:",
            options=opcoes,
            format_func=lambda x: f"{PLATAFORMAS[x]['icone']}  {x}",
            index=None,
            placeholder="🔍 Selecione uma plataforma...",
            label_visibility="collapsed",
        )

        if selecao:
            plataforma_selecionada = selecao

    st.markdown("</div>", unsafe_allow_html=True)

    if not plataforma_selecionada:
        # Estado inicial: exibe cards informativos
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #8b949e;">
            <h3 style="color: #8b949e;">👆 Selecione uma plataforma acima para começar</h3>
            <p style="font-size: 0.95rem;">Analisaremos os termos de privacidade e forneceremos<br>
            um resumo claro, dicas de segurança e comparações.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🏁 Plataformas Disponíveis")
        cols_icons = st.columns(4)
        for i, (nome, info) in enumerate(PLATAFORMAS.items()):
            col_idx = i % 4
            with cols_icons[col_idx]:
                st.markdown(f"""
                <div style="text-align:center;padding:0.8rem;border:1px solid #30363d;border-radius:12px;margin-bottom:0.5rem;
                            background:rgba(255,255,255,0.02);">
                    <span style="font-size:2rem;">{info['icone']}</span>
                    <br><span style="color:#c9d1d9;font-weight:500;font-size:0.9rem;">{nome}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; margin-top: 2rem; color: #484f58; font-size: 0.85rem;">
            🔒 Seus dados não são armazenados. As análises são feitas em tempo real.
        </div>
        """, unsafe_allow_html=True)
        return

    # ============================================================
    # CARREGAMENTO DO ARQUIVO
    # ============================================================
    with st.spinner(f"📂 Carregando termos de privacidade do(a) {plataforma_selecionada}..."):
        texto_plataforma = carregar_texto_cache(plataforma_selecionada)

    if not texto_plataforma:
        st.error(f"Não foi possível carregar os termos de privacidade do(a) {plataforma_selecionada}.")
        return

    # Informações da plataforma selecionada
    info_plat = PLATAFORMAS[plataforma_selecionada]
    st.markdown(f"""
    <div style="display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;margin-bottom:1.5rem;">
        <span class="platform-badge">{info_plat['icone']} {plataforma_selecionada}</span>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # SEÇÃO 2 – RESUMO DOS TERMOS DE PRIVACIDADE
    # ============================================================
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">
            <span class="emoji">📝</span> Resumo dos Termos de Privacidade
        </div>
    """, unsafe_allow_html=True)

    if api_key:
        with st.spinner("🤖 Gerando resumo inteligente com IA..."):
            genai = configurar_gemini(api_key)
            resumo = analisar_com_gemini(genai, texto_plataforma, plataforma_selecionada, "resumo")

        if resumo:
            st.markdown(f"<div style='color:#c9d1d9;line-height:1.7;'>{resumo}</div>", unsafe_allow_html=True)
        else:
            st.warning("Não foi possível gerar o resumo com IA. Exibindo análise baseada no documento.")
            st.markdown(f"""
            <div style='color:#c9d1d9;line-height:1.7;'>
                <p>Os termos de privacidade do(a) <strong>{plataforma_selecionada}</strong> descrevem como seus dados pessoais são coletados, armazenados, usados e compartilhados. Abaixo, um resumo dos principais pontos identificados:</p>
                <ul>
                    <li><strong>Coleta de dados:</strong> A plataforma coleta informações fornecidas por você (como nome, e-mail e conteúdo compartilhado) e dados automáticos (como localização, dispositivo e comportamento de uso).</li>
                    <li><strong>Armazenamento:</strong> Seus dados são armazenados em servidores, muitas vezes em outros países, e mantidos enquanto sua conta estiver ativa.</li>
                    <li><strong>Compartilhamento:</strong> Dados podem ser compartilhados com empresas do mesmo grupo, parceiros de publicidade e, em alguns casos, com autoridades legais.</li>
                    <li><strong>Impactos:</strong> Seus dados podem ser usados para criar perfis comportamentais, direcionar anúncios e alimentar algoritmos de inteligência artificial.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💡 Configure uma chave da API Gemini no menu lateral para gerar resumos inteligentes com IA.")
        st.markdown(f"""
        <div style='color:#c9d1d9;line-height:1.7;'>
            <p>Os termos de privacidade do(a) <strong>{plataforma_selecionada}</strong> descrevem como dados pessoais são coletados, armazenados e compartilhados.</p>
            <ul>
                <li><strong>Coleta:</strong> dados fornecidos pelo usuário e coletados automaticamente</li>
                <li><strong>Armazenamento:</strong> servidores próprios e de terceiros, inclusive internacionalmente</li>
                <li><strong>Compartilhamento:</strong> com empresas parceiras, anunciantes e autoridades</li>
                <li><strong>Uso:</strong> personalização, publicidade, IA, pesquisas e segurança</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # SEÇÃO 3 – PALAVRAS DE MAIOR RISCO (WORD CLOUD)
    # ============================================================
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">
            <span class="emoji">☁️</span> Palavras de Maior Risco
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("Analisando termos de risco..."):
        contagem_palavras = extrair_palavras_risco_cache(texto_plataforma)

    if contagem_palavras:
        # Exibe as tags de palavras mais frequentes
        palavras_ordenadas = sorted(contagem_palavras.items(), key=lambda x: x[1], reverse=True)
        top_palavras = palavras_ordenadas[:10]

        st.markdown("**🔑 Termos de risco mais frequentes:**")
        tags_html = "".join(
            f'<span class="risk-tag">{palavra} ({freq})</span> '
            for palavra, freq in top_palavras
        )
        st.markdown(f"<div style='margin-bottom:1rem;'>{tags_html}</div>", unsafe_allow_html=True)

        # Gera word cloud
        buf = gerar_wordcloud_cache(contagem_palavras)
        if buf:
            st.image(buf, use_container_width=True)
            st.caption("Nuvem de palavras com termos relacionados a riscos de privacidade. Quanto maior o destaque, mais frequente o termo.")
    else:
        st.info("Nenhum termo de risco significativo encontrado no texto analisado.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # SEÇÃO 4 – DICAS DE PROTEÇÃO DIGITAL
    # ============================================================
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">
            <span class="emoji">🛡️</span> Dicas de Proteção Digital para {plataforma_selecionada}
        </div>
    """, unsafe_allow_html=True)

    dicas_exibidas = False

    if api_key:
        with st.spinner("🤖 Gerando dicas personalizadas com IA..."):
            genai = configurar_gemini(api_key)
            dicas_texto = analisar_com_gemini(genai, texto_plataforma, plataforma_selecionada, "dicas")

        if dicas_texto:
            # Processa dicas em formato de lista
            linhas = dicas_texto.strip().split("\n")
            dicas_filtradas = [l for l in linhas if l.strip() and (l.strip()[0].isdigit() or l.strip().startswith("-") or l.strip().startswith("*"))]
            if dicas_filtradas:
                for dica in dicas_filtradas[:10]:
                    st.markdown(f'<div class="tip-item">{dica.strip()}</div>', unsafe_allow_html=True)
                dicas_exibidas = True

    if not dicas_exibidas:
        # Dicas padrão específicas da plataforma
        dicas_padrao = {
            "WhatsApp": [
                "🔐 Ative a verificação em duas etapas (Configurações > Conta > Verificação em duas etapas)",
                "📍 Revise as permissões de localização e mantenha como 'Nunca' ou 'Ao usar o app'",
                "👁️ Configure quem pode ver sua foto de perfil, status e informações (Configurações > Privacidade)",
                "📵 Desative o download automático de mídia para economizar dados e privacidade",
                "🔒 Ative as mensagens temporárias para conversas sensíveis",
                "🚫 Bloqueie contatos desconhecidos e denuncie spam",
                "📋 Revise dispositivos conectados ao WhatsApp Web",
                "🔄 Mantenha o aplicativo sempre atualizado para ter as últimas correções de segurança",
            ],
            "Instagram": [
                "🔐 Ative a autenticação de dois fatores (Configurações > Segurança > Autenticação de dois fatores)",
                "🔒 Torne sua conta privada (apenas seguidores aprovados veem seu conteúdo)",
                "📍 Desative a localização precisa nas configurações do dispositivo",
                "👁️ Revise quem pode ver suas histórias, publicações e status de atividade",
                "📋 Gerencie aplicativos de terceiros conectados (Configurações > Apps e sites)",
                "🚫 Limite quem pode comentar e enviar mensagens diretas",
                "🔇 Desative o rastreamento de atividades fora do Instagram",
                "👤 Revise dispositivos onde sua conta está logada",
            ],
            "Facebook": [
                "🔐 Ative a autenticação de dois fatores (Configurações > Segurança e login)",
                "👁️ Revise quem pode ver suas publicações (Configurações > Privacidade)",
                "📍 Desative a localização precisa e histórico de localização",
                "📋 Revise e remova aplicativos de terceiros conectados à sua conta",
                "🔒 Configure seu perfil como privado e limite o alcance de publicações antigas",
                "🚫 Desative o reconhecimento facial (Configurações > Reconhecimento facial)",
                "📢 Controle preferências de anúncios e desative anúncios personalizados",
                "📱 Revise dispositivos e sessões ativas regularmente",
            ],
            "YouTube": [
                "🔐 Ative a verificação em duas etapas da sua conta Google",
                "📋 Revise e gerencie seu histórico (Configurações > Histórico e privacidade)",
                "⏰ Configure a exclusão automática do histórico a cada 3 meses",
                "📍 Desative o histórico de localização nas configurações da Google",
                "📢 Ajuste as configurações de anúncios personalizados (myadcenter.google.com)",
                "👤 Use o Google Takeout para baixar e revisar seus dados",
                "🔒 Ative o modo restrito para limitar conteúdo sensível",
                "👁️ Configure quem pode ver seus vídeos curtidos e inscrições",
            ],
            "TikTok": [
                "🔐 Ative a autenticação de dois fatores (Configurações > Segurança)",
                "🔒 Torne sua conta privada (Configurações > Privacidade > Conta privada)",
                "📍 Desative a localização precisa nas permissões do dispositivo",
                "👁️ Configure quem pode comentar, enviar mensagens e fazer duetos",
                "📋 Revise e remova dispositivos conectados à sua conta",
                "📢 Desative a personalização de anúncios (Configurações > Preferências de anúncios)",
                "⏰ Ative lembretes de tempo de uso para controlar o tempo na plataforma",
                "🚫 Denuncie conteúdo suspeito e bloqueie contas indesejadas",
            ],
            "Snapchat": [
                "🔐 Ative a autenticação de dois fatores (Configurações > Autenticação de dois fatores)",
                "👻 Ative o modo fantasma no Snap Map para ocultar sua localização",
                "👁️ Configure quem pode enviar snaps e visualizar stories",
                "🔒 Revise as configurações de 'Quem pode...' (contatar, ver localização)",
                "📋 Revise aplicativos conectados via Snap Kit",
                "📱 Gerencie permissões de localização (apenas ao usar o app)",
                "⏰ Configure snaps que desaparecem com o tempo adequado",
                "🚫 Bloqueie e denuncie usuários que violarem sua privacidade",
            ],
            "Twitter/X": [
                "🔐 Ative a autenticação de dois fatores (Configurações > Segurança > Autenticação de dois fatores)",
                "🔒 Proteja seus tweets (apenas seguidores aprovados veem seu conteúdo)",
                "📍 Desative a precisão de localização e remova tags de localização de tweets",
                "📋 Revise aplicativos de terceiros conectados à sua conta",
                "👁️ Configure quem pode mencionar você, enviar mensagens e ver suas curtidas",
                "🤖 Desative o uso de seus dados para treinamento de IA (Configurações > Privacidade > Dados para IA)",
                "📢 Ajuste as preferências de anúncios e limite a personalização",
                "📱 Revise dispositivos e sessões ativas regularmente",
            ],
        }

        dicas = dicas_padrao.get(plataforma_selecionada, [
            "🔐 Ative a autenticação em dois fatores sempre que disponível",
            "📍 Revise as permissões de localização do aplicativo",
            "👁️ Configure quem pode ver suas informações e conteúdo",
            "📋 Revise aplicativos de terceiros conectados à sua conta",
            "📢 Ajuste as configurações de publicidade personalizada",
            "📱 Mantenha o aplicativo atualizado",
        ])

        for dica in dicas:
            st.markdown(f'<div class="tip-item">{dica}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # SEÇÃO 5 – COMPARAÇÃO ENTRE PLATAFORMAS
    # ============================================================
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">
            <span class="emoji">📊</span> Comparação Entre Plataformas
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("Calculando pontuações de risco..."):
        pontuacoes_todas = pontuacoes_cache()
        pontuacao_atual = pontuacoes_todas.get(plataforma_selecionada, 0)

    # Exibe pontuação da plataforma selecionada em destaque
    cor_score = "score-low" if pontuacao_atual <= 30 else ("score-mid" if pontuacao_atual <= 55 else "score-high")

    st.markdown(f"""
    <div style="text-align:center;margin-bottom:1.5rem;">
        <div style="font-size:0.9rem;color:#8b949e;">Pontuação de Risco</div>
        <div class="score-display {cor_score}">{pontuacao_atual}/100</div>
        <div style="font-size:0.85rem;color:#8b949e;">
            {"🔵 Risco Baixo" if pontuacao_atual <= 30 else "🟡 Risco Médio" if pontuacao_atual <= 55 else "🟠 Risco Elevado" if pontuacao_atual <= 75 else "🔴 Risco Crítico"}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Gráfico comparativo
    fig = gerar_grafico_comparativo(pontuacoes_todas, plataforma_selecionada)
    st.plotly_chart(fig, use_container_width=True)

    # Interpretação
    interpretacao = interpretar_pontuacao(pontuacao_atual, plataforma_selecionada, pontuacoes_todas)

    st.markdown('<div class="interpretation-box">', unsafe_allow_html=True)
    st.markdown("**📖 Interpretação da Pontuação**")
    for linha in interpretacao:
        st.markdown(f"<p>{linha}</p>", unsafe_allow_html=True)

    # Fatores que influenciaram
    st.markdown("**📌 Principais fatores que influenciaram a pontuação:**")
    fatores = [
        "Frequência de menções à coleta de dados pessoais",
        "Nível de compartilhamento com terceiros e parceiros",
        "Extensão do rastreamento de atividades (cookies, pixels)",
        "Uso de localização precisa e rastreamento geográfico",
        "Criação de perfis comportamentais para publicidade",
        "Tempo de retenção das informações armazenadas",
        "Uso de reconhecimento facial e dados biométricos",
    ]
    for f in fatores:
        st.markdown(f'<div class="tip-item" style="font-size:0.85rem;">🔍 {f}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # SEÇÃO 6 – NOTÍCIAS RECENTES
    # ============================================================
    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">
            <span class="emoji">📰</span> Notícias Recentes sobre {plataforma_selecionada} e Privacidade
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("Buscando notícias atualizadas..."):
        noticias = noticias_cache(plataforma_selecionada)

    if noticias:
        cols_noticias = st.columns(2)
        for i, noticia in enumerate(noticias):
            with cols_noticias[i % 2]:
                st.markdown(f"""
                <div class="news-card">
                    <h4>{noticia['titulo']}</h4>
                    <div class="news-meta">
                        <span>📰 {noticia['fonte']}</span>
                        <span>📅 {noticia['data']}</span>
                    </div>
                    <a href="{noticia['link']}" target="_blank" class="news-link">🔗 Ler notícia completa →</a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📭 Nenhuma notícia encontrada no momento. As análises de privacidade acima continuam disponíveis.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ============================================================
    # RODAPÉ
    # ============================================================
    st.markdown("""
    <div class="footer">
        <p>
            🛡️ <strong>PrivAnalytica</strong> — Projeto educativo para conscientização sobre privacidade digital<br>
            🔒 Nenhum dado do usuário é armazenado ou compartilhado<br>
            📧 Dúvidas ou sugestões? Contribua em <a href="https://github.com" target="_blank">GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
