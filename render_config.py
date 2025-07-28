# Script para converter env_config.txt para formato do Render.com
# Data: 2024-12-19

import os
import re

def parse_env_file(filename):
    """Converte arquivo env_config.txt para formato do Render.com"""
    
    if not os.path.exists(filename):
        print(f"❌ Arquivo {filename} não encontrado!")
        return
    
    print("=== CONFIGURAÇÃO PARA RENDER.COM ===")
    print("Copie estas variáveis para o painel do Render:")
    print()
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            # Pular linhas vazias e comentários
            if not line or line.startswith('#'):
                continue
            
            # Extrair chave e valor
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                print(f"🔑 {key}")
                print(f"   Valor: {value}")
                print()
    
    print("=== INSTRUÇÕES ===")
    print("1. Acesse https://render.com")
    print("2. Vá para seu projeto")
    print("3. Clique em 'Environment'")
    print("4. Adicione cada variável acima")
    print("5. Clique em 'Save Changes'")
    print("6. Faça deploy novamente")

if __name__ == "__main__":
    parse_env_file('env_config.txt') 