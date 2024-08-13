# -*- coding: utf-8 -*-

arquivo = open('login.txt','r')
login=arquivo.readline().strip()
login=login.split(':')
login=login[1]

senha=arquivo.readline().strip()
senha=senha.split(':')
senha=senha[1]

arquivo.close()

arquivo = open('disciplina.txt','r')
plano=arquivo.readline().strip()
plano=plano.split(':')
plano=plano[1]

disciplina=arquivo.readline().strip()
disciplina=disciplina.split(':')
disciplina=disciplina[1]

print(plano)
arquivo.close()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select

import time

import pandas as pd

# para rodar o chrome em 2º plano
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.headless = True
# navegador = webdriver.Chrome(options=chrome_options)

# abrir um navegador
navegador = webdriver.Chrome()
# caso queira deixar na mesma pasta do seu código
# navegador = webdriver.Chrome("chromedriver.exe")

navegador.get("https://unisagrado.lyceum.com.br/DOnline/DOnline/avisos/TDOL303D.tp?utm_source=Lahar&utm_medium=email&utm_campaign=_20220805_180823_Acesso_ao_Docente_Online_")
navegador.maximize_window()

wait = WebDriverWait(navegador, 10)

# Digitar usuario
navegador.find_element(By.XPATH,'//*[@id="username"]').send_keys(f"{login}")

# Digitar senha
navegador.find_element(By.XPATH,'//*[@id="password"]').send_keys(f"{senha}")

#Clica em entrar
navegador.find_element(By.XPATH,'//*[@id="sendCredentials"]').click()

#clica em Conteudo
element = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ext-gen221"]')))
navegador.find_element(By.XPATH,'//*[@id="ext-gen221"]').click()


#clica em Connect usando o texto do link
WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Connect'))).click()

# Store the ID of the original window
original_window = navegador.current_window_handle

# Check we don't have other windows open already
assert len(navegador.window_handles) == 1

#clica no link para entrar no conect
element = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ext-gen89"]/div/table/tbody/tr/td[2]/div/a')))
navegador.find_element(By.XPATH,'//*[@id="ext-gen89"]/div/table/tbody/tr/td[2]/div/a').click()

# Wait for the new window or tab
wait.until(EC.number_of_windows_to_be(2))

# Loop through until we find a new window handle
for window_handle in navegador.window_handles:
    if window_handle != original_window:
        navegador.switch_to.window(window_handle)
        break

# Wait for the new tab to finish loading content
wait.until(EC.title_is("Painel"))

#clica do painel referente a disciplina (começa no 1)
# navegador.execute_script('window.scrollBy(0, 450)')
# input()
navegador.find_element(By.XPATH,f'//*[@id="snap-pm-courses-current-cards"]/div[{disciplina}]/div/h3/a').click()

#le os dados da tabela
# tabela = pd.read_excel(f'{plano}')
tabela = pd.read_excel(f'{plano}')

for aula in range(0,len(tabela)):
    data=tabela['Unnamed: 0'][aula]
    dia=data.day
    mes=data.month

    #clica em Crie uma atividade
    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="snap-new-section"]')))
    navegador.find_element(By.XPATH,'//*[@id="snap-new-section"]').click()

    #escreve o topico (data - título da aula)
    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="newsection"]')))
    navegador.find_element(By.XPATH,'//*[@id="newsection"]').send_keys(f'{dia:02}/{mes:02} - {tabela["Unnamed: 1"][aula]}')

    #clica em Criar seção
    navegador.find_element(By.NAME,'addtopic').click()

    #clica em Criar atividade de aprendizagem
    #element = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="snap-create-activity"]/a/img')))
    navegador.find_element(By.LINK_TEXT,'Criar atividade de aprendizagem').click()

    #clica em Recursos
    element = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Recursos')))
    navegador.find_element(By.LINK_TEXT,'Recursos').click()

    #clica em Rótulo
    element = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Recursos')))
    navegador.find_element(By.LINK_TEXT,'Rótulo').click()

    #escreve o rótulo da aula
    element = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_introeditoreditable"]')))
    navegador.find_element(By.XPATH,'//*[@id="id_introeditoreditable"]').send_keys(f'{tabela["Unnamed: 2"][aula]}')

    #clica em Salvar e voltar ao curso
    navegador.find_element(By.XPATH,'//*[@id="id_submitbutton2"]').click()

    #clica em Criar atividade de aprendizagem
    navegador.find_element(By.LINK_TEXT,'Criar atividade de aprendizagem').click()

    #cria em tarefa
    element = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Tarefa'))).click()

    #escreve o nome da tarefa
    element = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_name"]')))
#     navegador.find_element(By.XPATH,'//*[@id="id_introeditoreditable"]').send_keys(f'{tabela["Unnamed: 3"][aula]}')
    element.send_keys(f'{tabela["Unnamed: 3"][aula]}')

    #escreve o texto da tarefa
    element = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="id_introeditoreditable"]')))
    navegador.find_element(By.XPATH,'//*[@id="id_introeditoreditable"]').send_keys(f'{tabela["Unnamed: 4"][aula]}')

    #seleciona o dia de entrega
    x = navegador.find_element(By.ID,'id_duedate_day')
    drop = Select(x)
    d = str(int(tabela["Unnamed: 5"][aula]))
    drop.select_by_value(d)

    #seleciona o mes de entrega
    x = navegador.find_element(By.ID,'id_duedate_month')
    drop = Select(x)
    m = str(int(tabela["Unnamed: 6"][aula]))
    drop.select_by_value(m)

    #seleciona a hora de entrega
    x = navegador.find_element(By.ID,'id_duedate_hour')
    drop = Select(x)
    h = str(int(tabela["Unnamed: 7"][aula]))
    drop.select_by_value(h)

    #seleciona os minutos de entrega
    x = navegador.find_element(By.ID,'id_duedate_minute')
    drop = Select(x)
    minute = str(int(tabela["Unnamed: 8"][aula]))
    drop.select_by_value(minute)

    #clica em Salvar e voltar ao curso
    navegador.find_element(By.XPATH,'//*[@id="id_submitbutton2"]').click()

    print(f'Aula do dia {dia:02}/{mes:02} - OK')

print('Término de preencher as aulas.')

