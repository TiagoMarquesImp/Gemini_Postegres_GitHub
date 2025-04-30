import os
from dotenv import load_dotenv
load_dotenv()
import psycopg2
from github import Github
import google.generativeai as genai
import pandas as pd
import datetime
import re

gemini_api_key = os.getenv("GEMINI_API_KEY")
github_token = os.getenv("GITHUB_TOKEN")

    
def get_postgres_public_schema_info():
    """
    Busca informações sobre todas as tabelas (colunas, tipos, etc.)
    no schema 'public' do banco de dados PostgreSQL.

    Returns:
        dict: Um dicionário onde as chaves são os nomes das tabelas
              e os valores são listas de dicionários, cada um
              representando uma coluna com seu nome, tipo,
              nulabilidade e valor padrão.
              Retorna None em caso de erro de conexão ou consulta.
    """
    conn = None
    schema_info = {}
    try:
        # Conecta ao banco de dados usando variáveis de ambiente
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"), # Adiciona valor padrão se não definido
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", "5432") # Adiciona porta padrão se não definida
        )
        cur = conn.cursor()

        # 1. Buscar todos os nomes de tabelas no schema 'public'
        query_tables = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """
        cur.execute(query_tables)
        tables = cur.fetchall() # Retorna uma lista de tuplas, ex: [('users',), ('products',)]


        # 2. Para cada tabela encontrada, buscar informações das colunas
        for table_tuple in tables:       
            
            table_name = table_tuple[0]

            # Query para buscar detalhes das colunas da tabela atual
            # Usamos parameterização (%s) para segurança contra SQL Injection
            query_columns = """
            SELECT
                column_name,      -- Nome da coluna
                data_type,        -- Tipo de dado (ex: integer, character varying)
                is_nullable,      -- Se a coluna permite nulos ('YES' ou 'NO')
                column_default    -- Valor padrão da coluna (pode ser None)
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position; -- Garante a ordem original das colunas
            """
            cur.execute(query_columns, (table_name,)) # Passa o nome da tabela como parâmetro
            columns_data = cur.fetchall()

            # Formata as informações das colunas para melhor leitura
            column_details = []
            for col in columns_data:
                column_details.append({
                    'name': col[0],
                    'type': col[1],
                    'nullable': col[2] == 'YES', # Converte para booleano
                    'default': col[3]
                })

            schema_info[table_name] = column_details
           
        cur.close()
        return schema_info

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao conectar ou buscar no PostgreSQL: {error}")
        return None
    finally:
        if conn is not None:
            conn.close()
            print("Conexão com PostgreSQL fechada.")



def list_all_files_in_repo():
    """
    Lista todos os caminhos de arquivos (paths) em um repositório do GitHub
    usando as variáveis de ambiente GITHUB_TOKEN e GITHUB_REPO.

    Retorna:
        list: Uma lista de strings, onde cada string é o caminho completo de um arquivo no repositório.
              Retorna None em caso de erro ao acessar o repositório ou a árvore git.
    """
    token = os.getenv("GITHUB_TOKEN")
    repo_name = 'impulsoteam/seat'

    if not token:
        print("Erro: Variável de ambiente GITHUB_TOKEN não definida.")
        return None
    if not repo_name:
        print("Erro: Variável de ambiente GITHUB_REPO não definida.")
        return None

    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        print(f"Acessando repositório: {repo.full_name}")

        # Obter o SHA do commit mais recente no branch padrão (ex: main, master)
        default_branch = repo.get_branch(repo.default_branch)
        commit_sha = default_branch.commit.sha
        print(f"Usando commit SHA: {commit_sha} do branch '{repo.default_branch}'")

        # Obter a árvore git recursivamente
        # recursive=True faz com que a API retorne todos os arquivos em todos os subdiretórios
        tree = repo.get_git_tree(sha=commit_sha, recursive=True)

        if not tree:
             print("Erro: Não foi possível obter a árvore git do repositório.")
             return None

        # Filtrar a árvore para incluir apenas arquivos ('blob') e extrair seus caminhos
        file_paths = [element.path for element in tree.tree if element.type == 'blob']

        # Só quero os arquivos que estão em app/models ou 
        file_paths_filtrada = []
        
        for item in file_paths:
            if 'app/models' in item:
                file_paths_filtrada.append(item)
            elif 'config/locales' in item:
                file_paths_filtrada.append(item)
            else:
                file_paths.remove(item)

        print(f"Encontrados {len(file_paths)} arquivos no repositório.")
        return file_paths_filtrada

    except GithubException as ge:
        print(f"Erro do GitHub ao acessar repositório ou árvore: {ge.status} - {ge.data}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None



def get_github_file_content(file):
    """
    Busca o conteúdo dos arquivos especificados de um repositório do GitHub.
    (Sua função original, ligeiramente ajustada para clareza)
    """
    token = os.getenv("GITHUB_TOKEN")
    repo_name = 'impulsoteam/seat'
    file_paths_filtrada = list_all_files_in_repo()

    if not token or not repo_name or not file_paths_filtrada:
         print("Erro: Token, nome do repositório ou lista de arquivos ausente.")
         return None # Retorna None se faltar informação essencial

    g = Github(token)
    file_contents = {}
    try:
        repo = g.get_repo(repo_name)
        print(f"\nBuscando conteúdo de {len(file_paths_filtrada)} arquivo(s)...")
        for file_path in file_paths_filtrada:
            if file in file_path:
                print(file_path)
                try:
                    content_item = repo.get_contents(file_path)
                    # Verifica se é um arquivo antes de tentar decodificar
                    if content_item.type == 'file':
                        # Assume que o conteúdo é texto e decodifica de base64
                        file_contents[file_path] = content_item.decoded_content.decode('utf-8')
                        print(f"  [OK] Conteúdo de '{file_path}' obtido.")
                    else:
                        print(f"  [AVISO] O caminho '{file_path}' é um diretório, não um arquivo. Ignorando.")
                        file_contents[file_path] = f"ERROR: Path is a directory, not a file." # Ou None, ou omitir

                except GithubException as file_error:
                    # Erros comuns: 404 (Not Found)
                    print(f"  [ERRO] GitHub ao buscar arquivo '{file_path}': {file_error.status} - {file_error.data}")
                    file_contents[file_path] = f"ERROR: GitHub API Error {file_error.status}" # Indica que não foi possível buscar
                except Exception as file_error:
                    print(f"  [ERRO] Genérico ao buscar arquivo '{file_path}': {file_error}")
                    file_contents[file_path] = f"ERROR: {file_error}" # Indica que não foi possível buscar
        return file_contents
    except GithubException as repo_error:
        print(f"Erro do GitHub ao acessar repositório '{repo_name}': {repo_error.status} - {repo_error.data}")
        return None # Retorna None em caso de falha ao acessar o repo
    except Exception as repo_error:
        print(f"Erro inesperado ao acessar repositório '{repo_name}': {repo_error}")
        return None




def analyze_with_gemini(prompt_text):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # Escolha o modelo apropriado (verificar documentação para os mais recentes/adequados)
        model = genai.GenerativeModel('gemini-2.0-flash-lite') # Ou 'gemini-1.0-pro', 'gemini-1.5-pro', etc.
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as error:
        print(f"Erro ao chamar a API Gemini: {error}")
        # Considerar tratamento mais específico de erros da API (rate limit, auth, etc.)
        return None


def main():
    
    lista_tabelas = get_postgres_public_schema_info()

    for nome_tabela, lista_colunas in lista_tabelas.items():
        print(nome_tabela)

        # Monta o nome do arquivo 
        filename_md = f"{nome_tabela}.md"

        if os.path.exists(filename_md):
            print(f"  Arquivo '{filename_md}' já existe. Pulando para o próximo item.")
            continue
        # ---- Defina aqui o que você quer analisar ----
        task_description = f"Gerar o dicionário de dados para a tabela '{nome_tabela}', incluindo a explicação dos enums definidos no model Rails."
        target_tables = nome_tabela
        relevant_github_files = f'app/models/{nome_tabela}' # Arquivo que contém o enum 'status'
        # ----------------------------------------------

        print(f"Iniciando tarefa: {task_description}")

        # 1. Buscar Schema do DB
        print("Buscando schema do PostgreSQL...")
        '''schema_data = get_postgres_public_schema_info('booking')
        if not schema_data:
            print("Falha ao obter dados do schema. Abortando.")
            return'''

        # 2. Buscar Arquivos do GitHub
        print("Buscando arquivos relevantes do GitHub...")
        code_data = get_github_file_content(relevant_github_files[:-2])
        if not code_data:
            print("Falha ao obter arquivos do GitHub. Abortando.")
            #return

        # 3. Construir o Prompt para Gemini
        print("Construindo prompt para Gemini...")
        prompt = f"""
        Você é um assistente especialista em análise de dados e engenharia de dados.
        Minha tarefa é: {task_description}

        Contexto do Banco de Dados (PostgreSQL - Colunas e Tipos):
        {lista_colunas}

        Contexto do Código (Ruby on Rails - Arquivos Relevantes):
        {code_data}

        Por favor, execute a tarefa solicitada com base nas informações fornecidas.
        forneça o dicionário em markdown.
        Se precisar de mais detalhes, me diga o quê.
        """
        # Opcional: Imprimir o prompt para depuração
        # print("--- PROMPT ---")
        # print(prompt)
        # print("--------------")

        # 4. Chamar a API Gemini
        print("Enviando solicitação para a API Gemini...")
        analysis_result = analyze_with_gemini(prompt)

        # 5. Exibir o Resultado
        if analysis_result:
            print("\n--- Resposta da IA ---")
            print(analysis_result)
            print("----------------------")
            # --- Bloco para gerar nome dinâmico e salvar em arquivo .md ---
        try:
            
            

            print(f"Salvando resultado em: {filename_md}")

            # Abre o arquivo no modo de escrita ('w'), usando codificação UTF-8
            with open(filename_md, 'w', encoding='utf-8') as f:
                # Escreve o conteúdo da string (resposta da IA) no arquivo
                f.write(analysis_result)

            print(f"Resultado salvo com sucesso em: {filename_md}")

        except IOError as e:
            # Informa se houve erro ao tentar salvar o arquivo
            print(f"Erro ao salvar o arquivo .md: {e}")
        # --- Fim do bloco de salvamento ---
        
    else:
        # Mensagem caso a API não retorne um resultado
        print("Não foi possível obter a análise da IA.")
        

if __name__ == "__main__":
    main()

















