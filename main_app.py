# Assessment DISC - Aplicação Principal
# Função: Interface Streamlit para o sistema de equipes multi-idioma
# Data: 06/06/2025

import os
import streamlit as st
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Assessment DISC - Equipe Multi-idioma",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar se as chaves API estão configuradas
def check_api_keys():
    """Verifica se as chaves API estão configuradas"""
    openai_key = os.getenv('OPENAI_API_KEY')
    tavily_key = os.getenv('TAVILY_API_KEY')
    
    if not openai_key or openai_key == 'your_openai_api_key_here':
        st.error("❌ Chave API do OpenAI não configurada!")
        st.info("Configure a variável OPENAI_API_KEY no Render.com ou no arquivo .env")
        return False
    
    if not tavily_key or tavily_key == 'your_tavily_api_key_here':
        st.warning("⚠️ Chave API do Tavily não configurada!")
        st.info("Configure a variável TAVILY_API_KEY no Render.com ou no arquivo .env")
    
    return True

# Inicializar agentes
@st.cache_resource
def initialize_agents():
    """Inicializa os agentes da equipe multi-idioma"""
    try:
        english_agent = Agent(
            name="English Agent",
            role="You only answer in English",
            model=OpenAIChat(id='gpt-4o-mini'),
        )
        
        chinese_agent = Agent(
            name="Chinese Agent",
            role="You only answer in Chinese",
            model=OpenAIChat(id='gpt-4o-mini'),
        )
        
        french_agent = Agent(
            name="French Agent",
            role="You can only answer in French",
            model=OpenAIChat(id='gpt-4o-mini'),
        )
        
        multi_language_team = Team(
            name="Multi Language Team",
            mode="route",
            model=OpenAIChat(id='gpt-4o-mini'),
            members=[english_agent, chinese_agent, french_agent],
            show_tool_calls=True,
            markdown=True,
            description="You are a language router that directs questions to the appropriate language agent.",
            instructions=[
                "Identify the language of the user's question and direct it to the appropriate language agent.",
                "If the user asks in a language whose agent is not a team member, respond in English with:",
                "'I can only answer in the following languages: English, Chinese, French. Please ask your question in one of these languages.'",
                "Always check the language of the user's input before routing to an agent.",
                "For unsupported languages like Italian, respond in English with the above message.",
            ],
            show_members_responses=True,
        )
        
        return multi_language_team
        
    except Exception as e:
        st.error(f"❌ Erro ao inicializar agentes: {str(e)}")
        return None

# Interface principal
def main():
    st.markdown("""
        <p style='
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #1f77b4;
        '>🌍 Assessment DISC - Equipe Multi-idioma</p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <p style='
            text-align: center;
            font-size: 18px;
            color: #666;
        '>Sistema de roteamento inteligente para respostas em múltiplos idiomas</p>
    """, unsafe_allow_html=True)
    
    # Verificar chaves API
    if not check_api_keys():
        st.stop()
    
    # Inicializar agentes
    with st.spinner("🔄 Inicializando agentes..."):
        team = initialize_agents()
    
    if team is None:
        st.error("❌ Não foi possível inicializar os agentes. Verifique as configurações.")
        st.stop()
    
    st.success("✅ Agentes inicializados com sucesso!")
    
    # Interface de chat
    st.markdown("---")
    st.markdown("### 💬 Chat Multi-idioma")
    
    # Área de entrada
    user_input = st.text_area(
        "Digite sua mensagem (suporta Inglês, Chinês e Francês):",
        height=100,
        placeholder="Ex: How are you? / Comment allez-vous? / 你好吗？"
    )
    
    # Botão de envio
    if st.button("🚀 Enviar Mensagem", type="primary"):
        if user_input.strip():
            with st.spinner("🔄 Processando..."):
                try:
                    # Obter resposta da equipe
                    response = team.print_response(user_input, stream=True)
                    
                    # Exibir resposta
                    st.markdown("### 📝 Resposta:")
                    st.markdown(response)
                    
                except Exception as e:
                    st.error(f"❌ Erro ao processar mensagem: {str(e)}")
        else:
            st.warning("⚠️ Por favor, digite uma mensagem.")
    
    # Informações sobre idiomas suportados
    st.markdown("---")
    st.markdown("### 🌐 Idiomas Suportados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background-color:#f0f0f0;padding:10px;border-radius:5px;text-align:center;'>
            <h4>🇺🇸 Inglês</h4>
            <p>Respostas em inglês</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color:#f0f0f0;padding:10px;border-radius:5px;text-align:center;'>
            <h4>🇨🇳 Chinês</h4>
            <p>Respostas em chinês</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color:#f0f0f0;padding:10px;border-radius:5px;text-align:center;'>
            <h4>🇫🇷 Francês</h4>
            <p>Respostas em francês</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Informações do ambiente
    st.markdown("---")
    st.markdown("### ℹ️ Informações do Sistema")
    
    env = os.getenv('ENVIRONMENT', 'development')
    debug = os.getenv('DEBUG', 'False')
    
    st.info(f"""
    - **Ambiente**: {env}
    - **Debug**: {debug}
    - **Modelo**: GPT-4o-mini (OpenAI)
    - **Versão**: Assessment DISC v1.0
    """)

if __name__ == "__main__":
    main() 