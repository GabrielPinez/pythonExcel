import pandas as pd
import os

# 1. Configurações de caminhos e nomes
pasta_arquivos = r"C:\dev\pythonExcel"
arquivo_excel_origem = "SPDadosCriminais_2025.xlsx"

# Lista das abas de dados que existem dentro do arquivo Excel de 2025
abas_de_dados = ["JAN-JUN_2025", "JUL-DEZ_2025"]

coluna_municipio = 'NOME_MUNICIPIO'

def converter_excel_para_csv_campinas():
    caminho_excel = os.path.join(pasta_arquivos, arquivo_excel_origem)
    
    # Verificação de segurança para o arquivo de origem
    if not os.path.exists(caminho_excel):
        print(f"❌ Erro crítico: O arquivo Excel '{arquivo_excel_origem}' não foi encontrado na pasta {pasta_arquivos}.")
        return

    print(f"🔄 Iniciando a conversão do arquivo Excel: {arquivo_excel_origem}")
    print("🎯 Filtrando registros exclusivamente para a cidade de CAMPINAS...")

    for aba in abas_de_dados:
        try:
            print(f"\n📖 Lendo a aba '{aba}' (isso pode levar alguns segundos devido ao tamanho)...")
            
            # Carrega a aba atual do Excel
            df = pd.read_excel(caminho_excel, sheet_name=aba)
            
            # Limpa espaços invisíveis do cabeçalho
            df.columns = df.columns.str.strip()
            
            # Tratamento caso a SSP tenha usado uma variação no nome da coluna
            if coluna_municipio not in df.columns:
                print(f"   ⚠️ Coluna '{coluna_municipio}' não encontrada. Procurando alternativas...")
                alternativas = [col for col in df.columns if "MUNICI" in col.upper()]
                if alternativas:
                    coluna_atual = alternativas[0]
                    print(f"   🔍 Usando a coluna encontrada: '{coluna_atual}'")
                else:
                    print(f"   ❌ Erro: Não foi possível mapear a coluna de município na aba {aba}.")
                    continue
            else:
                coluna_atual = coluna_municipio

            # 2. FILTRO: Mantém apenas as linhas onde o município é Campinas
            df_campinas = df[df[coluna_atual].astype(str).str.strip().str.upper() == 'CAMPINAS']
            
            total_estado = len(df)
            total_campinas = len(df_campinas)
            
            print(f"   🔹 Ocorrências totais no Estado nesta aba: {total_estado}")
            print(f"   🎯 Ocorrências filtradas em Campinas: {total_campinas}")
            
            # 3. Salva em um arquivo CSV limpo, leve e exclusivo de Campinas
            nome_csv_saida = f"SPDadosCriminais_{aba}_CAMPINAS.csv"
            caminho_csv_saida = os.path.join(pasta_arquivos, nome_csv_saida)
            
            # Configurações ideais para o padrão do Excel brasileiro (sep=';' e utf-8-sig)
            df_campinas.to_csv(caminho_csv_saida, index=False, sep=';', encoding='utf-8-sig')
            print(f"   💾 Arquivo CSV salvo com sucesso: '{nome_csv_saida}'")
            
        except Exception as e:
            print(f"   ❌ Erro inesperado ao processar a aba {aba}: {e}")

    print("\n✅ Processo de conversão e filtragem concluído!")

if __name__ == "__main__":
    converter_excel_para_csv_campinas()