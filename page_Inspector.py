import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import re


def obter_ultimo_arquivo(diretorio):
    lista_de_arquivos = os.listdir(diretorio)
    lista_de_arquivos = [
        f for f in lista_de_arquivos if os.path.isfile(os.path.join(diretorio, f))
    ]
    lista_de_arquivos = sorted(
        lista_de_arquivos,
        key=lambda x: os.path.getctime(os.path.join(diretorio, x)),
        reverse=True,
    )
    return lista_de_arquivos[0] if lista_de_arquivos else None


def extrair_conteudo_e_salvar(url, nome_do_arquivo):
    driver = webdriver.Edge()
    driver.get(url)
    time.sleep(2)
    element = driver.find_element(By.CLASS_NAME, "ng-non-bindable")
    content = element.get_attribute("innerHTML")
    driver.quit()

    with open(nome_do_arquivo, "wb") as file:
        file.write(content.encode("utf-8"))


# Diretório de saída
diretorio_de_saida = "pages/"

# Verifica o último arquivo criado
ultimo_arquivo = obter_ultimo_arquivo(diretorio_de_saida)

with open("links.csv", "r") as file:
    reader = csv.reader(file, delimiter=";")
    next(reader)

    for row in reader:
        nome_da_pagina = re.sub(r"\W", "", row[0])
        nome_do_arquivo = f"pages/{nome_da_pagina}.html"

        # Verifica se o arquivo já existe
        if nome_do_arquivo == ultimo_arquivo:
            print(f"O arquivo {nome_do_arquivo} já existe. Pulando a extração.")
            continue

        extrair_conteudo_e_salvar(row[1], nome_do_arquivo)
