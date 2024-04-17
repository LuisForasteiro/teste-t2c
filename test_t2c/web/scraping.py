from botcity.web import WebBot, Browser, By
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
import json

load_dotenv()


def acessar_portal(bot: WebBot):
    try:
        bot.headless = False
        bot.browser = Browser.CHROME
        bot.driver_path = ChromeDriverManager().install()
        bot.browse("https://acme-test.uipath.com/")
        bot.maximize_window()

        portal_acessou = bot.find_element(
            'body > div > div.main-container', By.CSS_SELECTOR, waiting_time=10000)

        if portal_acessou:
            return True
        else:
            print(f'Portal nao abriu')
            return False

    except Exception as e:
        print(f'Erro ao acessar o portal: {e}')
        return False


def login_portal(bot: WebBot):
    try:
        input_email = bot.find_element(
            '//*[@id="email"]', By.XPATH, waiting_time=10000)
        input_email.send_keys(os.getenv('login_portal'))

        input_senha = bot.find_element(
            '//*[@id="password"]', By.XPATH, waiting_time=10000)
        input_senha.send_keys(os.getenv('senha_portal'))

        btn_login = bot.find_element('//button[@type="submit"]', By.XPATH)
        btn_login.click()

        return True

    except Exception as e:
        print(f'Erro ao fazer o login: {e} ')
        return False


def dashboard(bot: WebBot):
    try:
        menu_opcoes = bot.find_element('//*[@id="dashmenu"]', By.XPATH)

        if menu_opcoes:

            lista_opcoes = menu_opcoes.find_elements_by_tag_name('div')

            for opc in lista_opcoes:
                opc_text = opc.text.strip()
                print(opc_text)

                if opc_text == 'Work Items':
                    btn_work_items = opc.find_element_by_css_selector("button")
                    btn_work_items.click()
                    break

            else:
                print('Erro ao acessar')
                return False

            print(f'Acessou o Work Items')
            return True

    except Exception as e:
        print(f'Erro no metodo dashboard: {e}')
        return False


def extrair_dados_tab(bot: WebBot):

    dados_coletados = []
    contador = 1

    try:
        while True:
            tabela = bot.find_element(
                    f'body > div > div.main-container > div > table', By.CSS_SELECTOR)

            linhas_tabela = tabela.find_elements_by_tag_name("tr")

            for linha in linhas_tabela[1:]:

                dados = linha.find_elements_by_tag_name("td")

                linha_dict = {
                    "WIID": dados[1].text,
                    "Description": dados[2].text,
                    "Type": dados[3].text,
                    "Status": dados[4].text,
                    "Date": dados[5].text,
                }
                
                print(f'{dados[1].text}')

                dados_coletados.append(linha_dict)

            contador += 1
            
            try:
                btn_proxima_pagina = bot.find_element(
                    f'body > div > div.main-container > div > nav > ul > li:nth-child({contador}) > a', By.CSS_SELECTOR)
                
                btn_proxima_pagina.click()
                
            except Exception as e:
                break
            
        print(f'Total linhas/dados: {len(dados_coletados)}')
        
        with open('dados_excel.json', 'w') as arquivo:
            json.dump(dados_coletados, arquivo, indent=4)

        return True, dados_coletados

    except Exception as e:
        print(f'Erro extrair dados: {e}')
