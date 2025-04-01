import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import zipfile

#Url do site da ANS
url_base = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

#Criação do diretório para armazenar os PDFs
os.makedirs("anexos", exist_ok=True)

def download_pdf(url, nome_arquivo):
    """Baixa o PDF e salva no diretório 'anexos"""
    resposta = requests.get(url, stream=True)
    if resposta.status_code == 200:
        caminho_arquivo = os.path.join("anexos", nome_arquivo)
        with open(caminho_arquivo, "wb") as f:
            f.write(resposta.content)
            print(f"📂 Baixado: {nome_arquivo}")   
    else:
        print(f"❌ Erro ao baixar {nome_arquivo}")

# Fazendo a requisição e parseia a página
resposta = requests.get(url_base)
soup = BeautifulSoup(resposta.text, "html.parser")

# Encontra todos os links da página
links = soup.find_all("a", href=True)

# Filtra os links dos anexos I e II
pdfs_downloads = []
for link in links:
    href = link["href"]
    if "anexo" in href.lower() and href.lower().endswith(".pdf"):
        pdf_url = urljoin(url_base, href)
        nome_arquivo = pdf_url.split("/")[-1]
        download_pdf(pdf_url, nome_arquivo)
        pdfs_downloads.append(nome_arquivo)


# Criação do ZIP com os PDFS baixados

zip_filename = "anexos.zip"
with zipfile.ZipFile(zip_filename, "w") as zipf:
    for pdf in pdfs_downloads:
        zipf.write(os.path.join("anexos", pdf), pdf)

print(f"📦 Arquivos compactados em: {zip_filename}")