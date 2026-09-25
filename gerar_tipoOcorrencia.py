import pandas as pd
import json
import os

# 1. Configurações de caminhos e colunas
pasta_arquivos = r"C:\dev\pythonExcel"
arquivos_csv = [
    "SPDadosCriminais_JAN-JUN_2025.csv",
    "SPDadosCriminais_JUL-DEZ_2025.csv"
]
coluna_natureza = 'NATUREZA_APURADA'

def ler_csv_com_seguranca(caminho):
    try:
        return pd.read_csv(caminho, sep=';', encoding='utf-8', low_memory=False)
    except Exception:
        return pd.read_csv(caminho, sep=';', encoding='iso-8859-1', low_memory=False)

def extrair_naturezas_2025():
    naturezas_encontradas = set()
    print("🔄 Iniciando a extração de naturezas dos arquivos de 2025...")

    for arquivo in arquivos_csv:
        caminho_completo = os.path.join(pasta_arquivos, arquivo)
        
        if not os.path.exists(caminho_completo):
            print(f"⚠️ Arquivo não encontrado, pulando: {arquivo}")
            continue
            
        print(f"📖 Lendo arquivo: {arquivo}...")
        df = ler_csv_com_seguranca(caminho_completo)
        
        # Limpa o cabeçalho contra caracteres invisíveis
        df.columns = df.columns.str.strip().str.replace('ï»¿', '', regex=False)
        
        if coluna_natureza in df.columns:
            # Pega os valores únicos da coluna nesta planilha
            valores_unicos = df[coluna_natureza].dropna().unique()
            
            for valor in valores_unicos:
                texto_limpo = str(valor).strip().upper()
                # Ignora valores nulos ou vazios textuais
                if texto_limpo and texto_limpo not in ['NULL', 'NAN']:
                    naturezas_encontradas.add(texto_limpo)
        else:
            print(f"❌ Erro: Coluna '{coluna_natureza}' não encontrada no arquivo {arquivo}.")

    # Converte para lista e ordena alfabeticamente
    lista_final = sorted(list(naturezas_encontradas))

    # 2. Salva o resultado final no arquivo JSON
    caminho_saida_json = os.path.join(pasta_arquivos, 'naturezas_permitidas.json')
    with open(caminho_saida_json, 'w', encoding='utf-8') as f:
        json.dump(lista_final, f, ensure_ascii=False, indent=4)

    print(f"\n✅ Sucesso!")
    print(f"📊 Foram mapeadas {len(lista_final)} naturezas únicas dentro das bases de 2025.")
    print(f"💾 Arquivo atualizado salvo em: '{caminho_saida_json}'")

if __name__ == "__main__":
    extrair_naturezas_2025()