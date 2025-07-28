# Aplicação principal para deploy no Render.com
# Funcionalidade: Equipe multilíngue com OpenAI
# Data: 2024-12-19

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team

# Carregando variáveis de ambiente
load_dotenv('env_config.txt', override=True)

# Verificando se as chaves da API estão configuradas
if not os.getenv('OPENAI_API_KEY'):
    print("⚠️  AVISO: OPENAI_API_KEY não encontrada.")
    print("   Para desenvolvimento local: Configure o arquivo env_config.txt")
    print("   Para produção: Configure a variável de ambiente OPENAI_API_KEY")
    raise ValueError("OPENAI_API_KEY não configurada")

# Criando agentes
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

# Criando equipe multilíngue
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

def main():
    """Função principal para execução"""
    print("🌐 Equipe Multilíngue Iniciada!")
    print("Idiomas suportados: Inglês, Chinês, Francês")
    print()
    
    # Testes automáticos
    print("=== TESTES AUTOMÁTICOS ===")
    
    # Teste em francês
    print("🇫🇷 Teste em francês:")
    response = multi_language_team.run("Comment allez-vous?")
    print(f"Resposta: {response}")
    print()
    
    # Teste em inglês
    print("🇺🇸 Teste em inglês:")
    response = multi_language_team.run("How are you?")
    print(f"Resposta: {response}")
    print()
    
    # Teste em chinês
    print("🇨🇳 Teste em chinês:")
    response = multi_language_team.run("你好吗？")
    print(f"Resposta: {response}")
    print()
    
    # Teste em italiano (idioma não suportado)
    print("🇮🇹 Teste em italiano (não suportado):")
    response = multi_language_team.run("Come stai?")
    print(f"Resposta: {response}")
    print()
    
    print("✅ Todos os testes concluídos!")

if __name__ == "__main__":
    main() 