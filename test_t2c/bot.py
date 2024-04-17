# Import for the Web Bot
from botcity.web import WebBot, Browser, By
from web.scraping import *
from utils.gerar_excel import *
from utils.qnt_tipos import *
from mail.send_email import *
import json

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


bot = WebBot()


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    # Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    if acessar_portal(bot=bot):
        if login_portal(bot=bot):
            if dashboard(bot=bot):
                extrair_dados_ok, dados_total = extrair_dados_tab(bot=bot)
                if extrair_dados_ok:
                    if criar_excel_dados(lista_dados=dados_total):
                        contagem_tipos_ok, tipo_qnt = contagem_tipos()
                        if contagem_tipos_ok:
                            envia_email(destinatario=['luisfelipes.cg@gmail.com'],
                                        assunto=f'T2CGroup Prova Desenvolvedor RPA', msg=f"Resultado<br>Linhas totais {len(dados_total)}", arquivo=['dados_excel.xlsx'], dados=tipo_qnt)
    
    # Wait 3 seconds before closing
    bot.wait(3000)

    bot.stop_browser()


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
