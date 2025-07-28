# Projeto Agno - Equipe Multilíngue

## 📋 Descrição
Sistema de agentes multilíngue usando OpenAI GPT-4o-mini para responder em diferentes idiomas.

## 🚀 Configuração Local

### 1. Instalar dependências
```bash
uv sync
```

### 2. Configurar variáveis de ambiente
Copie o arquivo de exemplo e configure suas chaves:
```bash
cp env_example.txt env_config.txt
```

Edite o arquivo `env_config.txt` e adicione suas chaves reais:
```
OPENAI_API_KEY=sua_chave_openai_aqui
TAVILY_API_KEY=sua_chave_tavily_aqui
```

### 3. Executar o projeto
```bash
uv run 41_teams.py
```

## 🌐 Deploy no Render.com

### 1. Configurar variáveis de ambiente no Render
No painel do Render, vá em **Environment** e adicione:
- `OPENAI_API_KEY`: sua_chave_openai_aqui
- `TAVILY_API_KEY`: sua_chave_tavily_aqui

### 2. Configurar build
- **Build Command**: `uv sync`
- **Start Command**: `uv run 41_teams.py`

## 🔒 Segurança

### Arquivos protegidos (não enviados para GitHub):
- `env_config.txt` - arquivo com chaves reais
- `*.db` - bancos de dados
- `*.log` - logs

### Arquivos seguros para GitHub:
- `env_example.txt` - exemplo de configuração
- `41_teams.py` - código principal
- `pyproject.toml` - dependências

## 📝 Funcionalidades

### Idiomas suportados:
- 🇺🇸 **Inglês**: English Agent
- 🇨🇳 **Chinês**: Chinese Agent  
- 🇫🇷 **Francês**: French Agent

### Testes automáticos:
- Francês: "Comment allez-vous?"
- Inglês: "How are you?"
- Chinês: "你好吗？"
- Italiano: "Come stai?" (resposta de idioma não suportado)

## 🛠️ Estrutura do Projeto

```
curso agno/
├── 41_teams.py          # Código principal
├── env_example.txt      # Exemplo de configuração
├── env_config.txt       # Configuração local (não commitado)
├── .gitignore          # Arquivos ignorados pelo Git
├── pyproject.toml      # Dependências
└── README.md           # Este arquivo
```

## ⚠️ Importante

1. **NUNCA** commite o arquivo `env_config.txt` com chaves reais
2. Use variáveis de ambiente no Render.com para produção
3. Mantenha as chaves seguras e não as compartilhe
