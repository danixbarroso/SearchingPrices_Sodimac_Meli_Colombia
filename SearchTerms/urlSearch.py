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
            else:
                print(f"Erro ao acessar a página: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erro de requisição: {e}")
            return None
    return None

def buscaSodimac(url):
    
    response = fetch_with_retry(url)
    print(response)
    soup = BeautifulSoup(response.text, "html.parser")

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

#lendo arquivo
df = pd.read_excel("S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/SearchTerms/PortfolioSodimac2025_Teste.xlsx")
resultsSodimac = []

for index, row in df.iterrows():
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