import os
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import json


with open("links.json", "r") as file:
    links_dict = json.loads(file.read())
    categories = links_dict.keys()


def extrair_conteudo_e_salvar(url, nome_do_arquivo):
    driver = webdriver.Edge()
    driver.get(url)
    time.sleep(2)
    element = driver.find_element(By.CLASS_NAME, "ng-non-bindable")
    content = element.get_attribute("innerHTML")
    driver.quit()

    with open(nome_do_arquivo, "wb") as file:
        file.write(content.encode("utf-8"))


def processar_pagina(category, page, links_dict, path):
    page_slug = links_dict[category][page]["URL"].split("/")[-1]
    os.makedirs(os.path.join(path, category, page_slug), exist_ok=True)
    extrair_conteudo_e_salvar(
        links_dict[category][page]["URL"],
        os.path.join(path, category, page_slug, f"{page_slug}.html"),
    )

    if len(links_dict[category][page]) != 1:
        os.makedirs(os.path.join(path, category, page_slug, "subpages"), exist_ok=True)
        for subpage in links_dict[category][page]["Subpages"]:
            subpage_slug = links_dict[category][page]["Subpages"][subpage]["URL"].split(
                "/"
            )[-1]
            extrair_conteudo_e_salvar(
                links_dict[category][page]["Subpages"][subpage]["URL"],
                os.path.join(
                    path, category, page_slug, "subpages", f"{subpage_slug}.html"
                ),
            )


def main():
    path = "./pages/"
    os.makedirs(path, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for category in categories:
            os.makedirs(os.path.join(path, category), exist_ok=True)
            for page in links_dict[category]:
                futures.append(
                    executor.submit(processar_pagina, category, page, links_dict, path)
                )

        # Aguardar a conclusão de todas as tarefas
        concurrent.futures.wait(futures)


if __name__ == "__main__":
    main()
