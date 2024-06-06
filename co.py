import pandas as pd

# Definição da função de busca
def buscar_dados(arquivo_csv, nome=None, cpf=None, nome_parcial=None, data_nascimento=None, chunksize=100000):
    # Criar um iterador para ler em pedaços com o separador correto
    chunk_iter = pd.read_csv(arquivo_csv, chunksize=chunksize, sep='|', dtype=str)
    
    resultados = pd.DataFrame()  # DataFrame vazio para acumular resultados

    for df_chunk in chunk_iter:
        # Filtrar o chunk pelo CPF, nome ou nome parcial e data de nascimento
        if cpf:
            resultados_chunk = df_chunk[df_chunk['CPF'] == cpf]
        elif nome:
            resultados_chunk = df_chunk[df_chunk['Nome Completo'].str.contains(nome, case=False, na=False)]
        elif nome_parcial and data_nascimento:
            resultados_chunk = df_chunk[df_chunk['Nome Completo'].str.contains(nome_parcial, case=False, na=False) & (df_chunk['Data de Nascimento'] == data_nascimento)]

        # Se encontrar resultados, adicioná-los ao DataFrame de resultados
        if not resultados_chunk.empty:
            resultados = pd.concat([resultados, resultados_chunk])
    
    return resultados

# Exemplo de uso
arquivo_csv = 'brasil.csv'  # Substitua pelo caminho do seu arquivo CSV

# Solicitar ao usuário para escolher o tipo de busca
tipo_busca = input('''Digite '1' para buscar por Nome Completo.
Digite '2' para buscar por CPF.
Digite '3' para buscar por Nome Parcial e Data de Nascimento.
Escolha: ''')

# Realizar a busca conforme o tipo escolhido
if tipo_busca == '1':
    nome_para_buscar = input("Digite o Nome Completo do indivíduo: ")
    resultados = buscar_dados(arquivo_csv, nome=nome_para_buscar)
elif tipo_busca == '2':
    cpf_para_buscar = input("Digite o CPF do indivíduo: ")
    resultados = buscar_dados(arquivo_csv, cpf=cpf_para_buscar)
elif tipo_busca == '3':
    nome_parcial_para_buscar = input("Digite o Nome Parcial do indivíduo (sem sobrenome do meio, ou ultimo): ")
    data_nascimento_para_buscar = input("Digite a Data de Nascimento do indivíduo (formato DD/MM/AAAA): ")
    resultados = buscar_dados(arquivo_csv, nome_parcial=nome_parcial_para_buscar, data_nascimento=data_nascimento_para_buscar)
else:
    raise ValueError("Opção inválida. Você deve digitar '1', '2' ou '3'.")
    
# Exibir os resultados
print(resultados)
