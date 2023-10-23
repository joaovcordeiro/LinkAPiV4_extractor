from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

link_list = []

# instancia o webdriver para o Edge
driver = webdriver.Edge()

# define a url que será acessada
url = "https://developers.linkapi.solutions/"

# faz o acesso a url
driver.get(url)

# espera até que o elemento seja visível
wait = WebDriverWait(driver, 10)

# defines o Xpath para os elemento que serão acessados
intro_path = "//*[@id='content']/div[1]/div[1]/ul/li[1]/a"
section_path = '//*[@id="hub-sidebar"]/section'

# espera até que o elemento seja visível
link = wait.until(EC.visibility_of_element_located((By.XPATH, intro_path)))

# faz o click no elemento
link.click()

# espera até que o elemento seja visível
section = wait.until(EC.visibility_of_element_located((By.XPATH, section_path)))

# pega todos os elementos que estão dentro da section que possuem a tag <a>
links = section.find_elements(By.TAG_NAME, "a")

dict = {}


for link_element in links:
    # pega o atributo href do elemento
    url = link_element.get_attribute("href")
    # pega o texto que está dentro do elemento
    spanText = link_element.get_attribute("innerText")

    # adiciona o texto e o link em um dicionário
    dict[spanText] = url

    # adiciona o dicionário em uma lista
    link_list.append(dict)

# fecha o webdriver
driver.quit()

# remove o ultimo elemento da lista
dict.pop("")

# cria um arquivo csv e escreve o lista no arquivo
with open("links.csv", "w") as file:
    file.write("Page Name;URL\n")
    for key in dict.keys():
        file.write(key + ";" + dict[key] + "\n")
