import csv
import os
import Ocorrencia

vetor_de_ocorrencias = []
caminho_csv = r"C:\dev\pythonExcel\SPDadosCriminais_JAN-JUN_2025_CAMPINAS.csv"

def principal():
    pegar_dados()
    if vetor_de_ocorrencias:
        print(f"{len(vetor_de_ocorrencias)} ocorrências carregadas no vetor.")
        conectar_ao_banco()
        guardar_no_banco()
    else:
        print("Nenhuma ocorrência foi carregada.")

def pegar_dados():
    global vetor_de_ocorrencias
    if not os.path.exists(caminho_csv):
        print("caminho para o arquivo .csv nao existe")
        return 
    
    try:
        with open(caminho_csv, mode='r', encoding='utf-8-sig') as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=';')
            for linha in leitor:
                numero_bo = linha.get('NUM_BO')
                if numero_bo and numero_bo != "":
                    try:
                        lat_raw = linha.get('LATITUDE')
                        long_raw = inline_long = linha.get('LONGITUDE')
                        
                        latitude = float(str(lat_raw).replace(',', '.')) if lat_raw and str(lat_raw).upper() != 'NULL' else 0.0
                        longitude = float(str(long_raw).replace(',', '.')) if long_raw and str(long_raw).upper() != 'NULL' else 0.0
                        
                        nova_ocorrencia = Ocorrencia.Ocorrencia(
                            numero_bo=numero_bo,
                            latitude=latitude,
                            longitude=longitude,
                            natureza=linha.get('NATUREZA_APURADA')
                        )
                        vetor_de_ocorrencias.append(nova_ocorrencia)
                    except (ValueError, Exception):
                        continue
    except Exception as e:
        print(f"erro ao ler o arquivo .csv, erro: {e}")
    
    print(len(vetor_de_ocorrencias))

def conectar_ao_banco():
    try:
        print("Conectando ao banco de dados...")
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")

def guardar_no_banco():
    try:
        print("Guardando dados no banco...")
    except Exception as e:
        print(f"Erro ao guardar no banco: {e}")    

if __name__ == "__main__":
    principal()