from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
import time
import json


link_list = []
teste_json = {}

# Instancia o webdriver para o Edge
with webdriver.Edge() as driver:
    # Define a url que será acessada
    url = "https://developers.linkapi.solutions/docs/documentation-intro"

    # Faz o acesso a url
    driver.get(url)

    # Espera até que o elemento seja visível
    wait = WebDriverWait(driver, 10)

    # Define o XPath para os elementos que serão acessados
    section_path = '//*[@id="hub-sidebar"]/section'

    # Espera até que o elemento seja visível
    section = wait.until(EC.visibility_of_element_located((By.XPATH, section_path)))

    # Pega todos os elementos que estão dentro da section que possuem a tag <a>
    # Encontra todos os elementos dentro da section que possuem as classes específicas
    links = section.find_elements(By.CLASS_NAME, "Sidebar-list3cZWQLaBf9k8")

    for link_element in links:
        classes = link_element.get_attribute("class")

        if classes and len(classes.split()) == 2:
            h3_element = link_element.find_element(By.XPATH, "preceding::h3[1]")
            h3_element_text = h3_element.text.strip()
            first_children = link_element.find_elements(By.XPATH, "./*")

            teste_json[h3_element_text] = {}
            for child in first_children:
                first_child_url = child.find_element(By.XPATH, ".//a").get_attribute(
                    "href"
                )
                first_child_name = child.get_attribute("innerText")
                teste_json[h3_element_text].update(
                    {first_child_name: {"URL": first_child_url}}
                )

                second_children = child.find_elements(By.XPATH, ".//li")

                if second_children:
                    teste_json[h3_element_text][first_child_name]["Subpages"] = {}
                    for second_child in second_children:
                        second_child_url = second_child.find_element(
                            By.XPATH, ".//a"
                        ).get_attribute("href")
                        second_child_name = second_child.get_attribute("innerText")

                        teste_json[h3_element_text][first_child_name][
                            "Subpages"
                        ].update({second_child_name: {"URL": second_child_url}})


with open("links.json", "w", encoding="utf-8") as json_file:
    json.dump(teste_json, json_file, ensure_ascii=False, indent=2)
