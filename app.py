# Sistema de Equipes Multilíngue - Assessment DISC
# Funcionalidade: Interface web para equipes de agentes em diferentes idiomas
# Data: 2024-12-19

import streamlit as st
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team

# Configuração da página
st.set_page_config(
    page_title="Equipe Multilíngue - Assessment DISC",
    page_icon="🌍",
    layout="wide"
)

# Carregando variáveis de ambiente
load_dotenv('env_config.txt', override=True)

# Verificando se as chaves da API estão configuradas
if not os.getenv('OPENAI_API_KEY'):
    st.error("⚠️ AVISO: OPENAI_API_KEY não encontrada.")
    st.info("Para desenvolvimento local: Configure o arquivo env_config.txt")
    st.info("Para produção: Configure a variável de ambiente OPENAI_API_KEY")
    st.stop()

# Inicialização dos agentes
@st.cache_resource
def initialize_agents():
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

# Interface principal
def main():
    st.markdown("""
        <p style='
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #1f77b4;
        '>🌍 Equipe Multilíngue - Assessment DISC</p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <p style='
            text-align: center;
            font-size: 18px;
            color: #666;
            margin-bottom: 30px;
        '>Sistema de roteamento inteligente para perguntas em diferentes idiomas</p>
    """, unsafe_allow_html=True)
    
    # Inicializar agentes
    team = initialize_agents()
    
    # Sidebar com informações
    with st.sidebar:
        st.markdown("""
            <p style='
                font-size: 20px;
                font-weight: bold;
                color: #1f77b4;
            '>📋 Idiomas Suportados</p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color:#f0f0f0;padding:10px;border-radius:5px;margin:10px 0;'>
            <strong>🇺🇸 English</strong><br>
            <strong>🇨🇳 Chinese</strong><br>
            <strong>🇫🇷 French</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <p style='
                font-size: 16px;
                color: #666;
            '>💡 Dica: Faça sua pergunta em qualquer um dos idiomas suportados e o sistema irá rotear automaticamente para o agente apropriado.</p>
        """, unsafe_allow_html=True)
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <p style='
                font-size: 24px;
                font-weight: bold;
                color: #333;
            '>💬 Faça sua pergunta</p>
        """, unsafe_allow_html=True)
        
        # Input do usuário
        user_input = st.text_area(
            "Digite sua pergunta aqui:",
            height=100,
            placeholder="Exemplo: How are you? / Comment allez-vous? / 你好吗？"
        )
        
        if st.button("🚀 Enviar Pergunta", type="primary", use_container_width=True):
            if user_input.strip():
                with st.spinner("Processando sua pergunta..."):
                    try:
                        # Obter resposta da equipe
                        response = team.get_response(user_input)
                        
                        # Exibir resposta
                        st.markdown("""
                            <p style='
                                font-size: 20px;
                                font-weight: bold;
                                color: #1f77b4;
                                margin-top: 20px;
                            '>📝 Resposta:</p>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(response.content)
                        
                    except Exception as e:
                        st.error(f"Erro ao processar pergunta: {str(e)}")
            else:
                st.warning("Por favor, digite uma pergunta.")
    
    with col2:
        st.markdown("""
            <p style='
                font-size: 20px;
                font-weight: bold;
                color: #333;
            '>🎯 Exemplos</p>
        """, unsafe_allow_html=True)
        
        examples = [
            "🇺🇸 How are you?",
            "🇫🇷 Comment allez-vous?",
            "🇨🇳 你好吗？",
            "🇮🇹 Come stai? (não suportado)"
        ]
        
        for example in examples:
            st.markdown(f"""
                <div style='
                    background-color:#f8f9fa;
                    padding:8px;
                    border-radius:5px;
                    margin:5px 0;
                    font-size:14px;
                '>{example}</div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 