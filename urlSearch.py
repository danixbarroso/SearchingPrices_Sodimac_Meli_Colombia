import pandas as pd
import random
import os
from dotenv import load_dotenv
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import requests
from requests_kerberos import HTTPKerberosAuth
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
from datetime import date


##################################################################################################################################################

#Regras de Conexão

# Carrega as variáveis do arquivo .env
load_dotenv()

# Acessa a variável de ambiente
api_key = os.getenv("API_KEY")

# Definições do proxy
proxy_port = '8080'
proxy_ip = 'rb-proxy-de.bosch.com'

class HTTPAdapterWithProxyKerberosAuth(requests.adapters.HTTPAdapter):
    def proxy_headers(self, proxy):
        headers = {}
        auth = HTTPKerberosAuth()
        parsed_url = urlparse(proxy)
        negotiate_details = auth.generate_request_header(None, parsed_url.hostname, is_preemptive=True)
        headers['Proxy-Authorization'] = negotiate_details
        return headers
    
# Defina os filtros conforme necessário
software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

# Crie uma instância do UserAgent com os filtros definidos
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

# Obtenha uma lista de User-Agents
user_agents = user_agent_rotator.get_user_agents()

# Selecione um User-Agent aleatório
random_user_agent = user_agent_rotator.get_random_user_agent()

# Função para fazer a requisição com retry e Kerberos Auth
def fetch_with_retry(url, retries=3, backoff_factor=2.0):
    session = requests.Session()
    session.proxies = {"http": f'{proxy_ip}:{proxy_port}', "https": f'{proxy_ip}:{proxy_port}'}
    session.mount('http://', HTTPAdapterWithProxyKerberosAuth())
    session.mount('https://', HTTPAdapterWithProxyKerberosAuth())

    for i in range(retries):
        try:
            headers = {
                'User-Agent': random_user_agent,
                'Authorization': f'Bearer f{api_key}'
                }
            response = session.get(url, headers=headers)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                wait_time = backoff_factor * (2 ** i)
                print(f"Erro 429. Tentando novamente em {wait_time} segundos...")
                time.sleep(wait_time)
            elif response.status_code == 403:
                wait_time = backoff_factor * (10 ** i)
                print(f"Erro 403. Tentando novamente em {wait_time} segundos...")
                time.sleep(wait_time)
            elif response.status_code == 443:
                wait_time = backoff_factor * (10 ** i)
                print(f"Erro 443. Tentando novamente em {wait_time} segundos...")
                time.sleep(wait_time)
            else:
                print(f"Erro ao acessar a página: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erro de requisição: {e}")
            return None
    return None
#####################################################################################################################################################

def buscaSodimac(url, retries=5, backoff_factor=2.0):
    
    for attempt in range(retries):
        response = fetch_with_retry(url)
        if response and response.status_code == 200:
            print(f"Resposta recebida com sucesso no attempt {attempt + 1}.")
            soup = BeautifulSoup(response.text, "html.parser")
            break
        else:
            print(f"Falha ao acessar {url} após {retries} tentativas.")
            return None, None, None, None    
    
    #Extraindo link
    try:
        
        link = soup.find("a", id="title-pdp-link")
        link = link.get('href')
        link = f"https://www.homecenter.com.co{link}"
        print(f"link extraído com sucesso: {link}")
        
    except:
        print("Erro ao extrair link")
        link = None
        
    #Extraindo título
    try:
        
        title = soup.find("h2", class_="jsx-3015145513 product-title")
        title = title.text
        print (f"Título do anúncio: {title}")
        
    except:
        print("Erro ao extrair título")
        title = None
    
    # Extraindo imagem com base no título
    try:
        # Buscando a tag <img> que tem o atributo alt igual ao título
        image_tag = soup.find("img", {"alt": title})
        image = image_tag['src'] if image_tag else None
        if image:
            print(f"Imagem encontrada: {image}")
        else:
            print("Imagem não encontrada")
    except Exception as e:
        print(f"Erro ao extrair imagem: {e}")
        image = None

        
    #Extraindo preço
    try:
        price = soup.find("span", class_="jsx-3773524781 parsedPrice")
        price = price.text.replace('$', '').replace('.', '')
        price = float(price)
        print(f"Preço extraído no valor de: {price}")
    except Exception as e:
        print(f"Preço não extraído devido ao erro: {e}")
        price = None       
        
    return link, image, title, price

##################################################################################################################################################

def coletandoMeli(ean):
    urlmodel = 'https://api.mercadolibre.com/sites/MCO/search?q='
    eanSTR = str(ean).replace('.0','')
    url = urlmodel + eanSTR
    
    response = fetch_with_retry(url)
    if response.status_code == 200:
        json_data = response.json()
        if 'results' in json_data and len(json_data['results']) > 0:
            df_temp = pd.DataFrame(json_data['results'])
            df_temp['query'] = eanSTR
            now = date.today()
            df_temp['dateSearch'] = now
            df_temp['source'] = 'Meli'
            for col in ['thumbnail', 'permalink', 'price', 'seller.id', 'title']:
                if col not in df_temp.columns:
                    df_temp[col] = None
            df_temp = df_temp.rename(columns={'seller.id': 'seller'})
            df_temp = df_temp[['query', 'dateSearch', 'thumbnail', 'permalink', 'price', 'seller', 'source', 'title']]
            for _, row in df_temp.iterrows():
                print(f"Preço encontrado no Mercado Libre para EAN {row['query']}: {row['price']}")
            return df_temp


#############################################################################################################################################

#lENDO E SALVANDO DADOS MELI
tabela = pd.read_excel("S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/SearchTerms/PortfolioMeli2025.xlsx")
dfMeli = pd.DataFrame()

for index, row in tabela.iterrows():
    ean = row['EAN']
    sku = row['SKU Bosch']
    print(f'Processando SKU: {sku}')
    df_temp = coletandoMeli(ean)
    dfMeli = pd.concat([dfMeli, df_temp], ignore_index=True, sort=False)
    time.sleep(1)

pathMeli = 'S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/Backup/Meli'
dfMeli.to_csv(f"{pathMeli}/ResultadosMeli_{date.today()}.csv", index=False)
print(f'Arquivo Meli salvo com sucesso em: {pathMeli}')


#####################################################################################################################################################################################


#lendo arquivo SODIMAC
df = pd.read_excel("S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/SearchTerms/PortfolioSodimac2025.xlsx")
resultsSodimac = []

for index, row in tqdm(df.iterrows()):
    codSodimac = row['SKU Sodimac']
    url = f"https://www.homecenter.com.co/homecenter-co/search?Ntt={codSodimac}"
    sku = row['SKU Bosch']
    eanBosch = row['EAN']
    print(f'Processando SKU: {sku}')
    
    # Adicionando tempo variável antes de cada requisição
    wait_time = random.uniform(1, 5)  # Tempo aleatório entre 1 e 5 segundos
    time.sleep(wait_time)
    
    link, image, title, price = buscaSodimac(url)
    today = date.today()
    resultsSodimac.append({
            'query': sku,
            'dateSearch': today,
            'thumbnail': image,
            'permalink': link,
            'price': price,
            'source': 'Sodimac',
            'title': title
        })

#resultados Sodimac
df_resultsSodimac = pd.DataFrame(resultsSodimac)
pathSodimac = f"S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/Backup/Sodimac"
df_resultsSodimac.to_csv(f"{pathSodimac}/ResultadosSodimac_{date.today()}.csv", index=False)

print(f"Arquivo Sodimac Salvo com sucesso em: {pathSodimac}")


#############################################################################################################################################

#Concatenar os DFs
df_sodimac = df_resultsSodimac.reset_index(drop=True)
df_mercado_libre = dfMeli.reset_index(drop=True)

# Garantir que ambos os DataFrames tenham as mesmas colunas e remover duplicatas de colunas
common_columns = ['query', 'dateSearch', 'price', 'thumbnail', 'permalink', 'seller', 'source', 'title']
df_mercado_libre = df_mercado_libre.loc[:, ~df_mercado_libre.columns.duplicated()].reindex(columns=common_columns)
df_sodimac = df_sodimac.loc[:, ~df_sodimac.columns.duplicated()].reindex(columns=common_columns)

# Consolidando resultados em um único DataFrame
df_master = pd.concat([df_mercado_libre, df_sodimac], ignore_index=True, sort=False)

# Carregar o arquivo master existente se houver, para consolidar
master_file_path = 'S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/Masterprice_Colombia.csv'
try:
    df_master_existing = pd.read_csv(master_file_path).reset_index(drop=True)
    df_master = pd.concat([df_master_existing, df_master], ignore_index=True, sort=False)
except FileNotFoundError:
    print("Arquivo MasterPrice.csv não encontrado, criando um novo.")
    df_master.to_csv(master_file_path, index=False)
# Salvar backup do master antes de sobrescrever
backup_dir = 'S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Peru/SearchingPrices_Sodimac_Meli_Peru/Backup/MasterResults'
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)
backup_path = f'{backup_dir}/MasterPrice_Backup_{date.today()}.csv'
df_master.to_csv(backup_path, index=False)
print(f"Backup do arquivo master salvo em {backup_path}")

# Salvar o arquivo master atualizado
df_master.to_csv(master_file_path, index=False)
print(f"Consolidação completa e salva em MasterPrice.csv")