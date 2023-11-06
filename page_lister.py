from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


def acessar_url(driver, url):
    driver.get(url)


def esperar_elemento(driver, tempo, xpath):
    wait = WebDriverWait(driver, tempo)
    return wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))


def extrair_dados_link(link_element):
    classes = link_element.get_attribute("class")

    if classes and len(classes.split()) == 2:
        h3_element = link_element.find_element(By.XPATH, "preceding::h3[1]")
        h3_element_text = h3_element.text.strip()
        first_children = link_element.find_elements(By.XPATH, "./*")

        dados_link = {h3_element_text: {}}
        for child in first_children:
            first_child_url = child.find_element(By.XPATH, ".//a").get_attribute("href")
            first_child_name = child.get_attribute("innerText")
            dados_link[h3_element_text].update(
                {first_child_name: {"URL": first_child_url}}
            )

            second_children = child.find_elements(By.XPATH, ".//li")

            if second_children:
                dados_link[h3_element_text][first_child_name]["Subpages"] = {}
                for second_child in second_children:
                    second_child_url = second_child.find_element(
                        By.XPATH, ".//a"
                    ).get_attribute("href")
                    second_child_name = second_child.get_attribute("innerText")

                    dados_link[h3_element_text][first_child_name]["Subpages"].update(
                        {second_child_name: {"URL": second_child_url}}
                    )
        return dados_link
    else:
        return {}


def main():
    teste_json = {}

    with webdriver.Edge() as driver:
        url = "https://developers.linkapi.solutions/docs/documentation-intro"
        acessar_url(driver, url)

        section_xpath = '//*[@id="hub-sidebar"]/section'
        section = esperar_elemento(driver, 10, section_xpath)

        links = section.find_elements(By.CLASS_NAME, "Sidebar-list3cZWQLaBf9k8")

        for link_element in links:
            dados_link = extrair_dados_link(link_element)
            teste_json.update(dados_link)

    with open("links.json", "w", encoding="utf-8") as json_file:
        json.dump(teste_json, json_file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
