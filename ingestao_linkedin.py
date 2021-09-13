import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, ResultSet
import requests
import os
import warnings

warnings.filterwarnings("ignore")

class Scrappy():
    def entrar_linkedin(self):
        options = Options()
        options.add_argument(('window-size=400,800'))
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://www.linkedin.com/feed/')
        self.pagina = 0
        self.lista_vagas = []

    def iniciar(self):
        self.entrar_linkedin()
        self.login()
        self.busca_vaga()
        self.armazena_vagas()
        self.scroll_down2()
        self.armazena_vagas()
        self.proxima_pagina()
        self.armazena_vagas()
        self.scroll_down2()
        self.armazena_vagas()
        self.proxima_pagina()
        self.armazena_vagas()
        self.scroll_down2()
        self.armazena_vagas()
        self.proxima_pagina()
        self.armazena_vagas()
        self.scroll_down2()
        self.armazena_vagas()
        self.proxima_pagina()
        self.armazena_vagas()
        self.cria_dataframe()

    def login(self):
        self.driver.find_element_by_link_text('Entre').click()
        sleep(0.5)
        self.login = self.driver.find_element_by_id('username')
        self.email = input('Insira seu e-mail: ')
        self.login.send_keys(self.email)
        self.senha = self.driver.find_element_by_id('password')
        self.sua_senha = input('Insira sua senha: ')
        self.senha.send_keys(self.sua_senha)
        self.driver.find_element_by_tag_name('button').click()

    def busca_vaga(self):
        self.url_jobs = 'https://www.linkedin.com/jobs/search/?keywords='

        self.vaga_desejada = input('Qual a área que deseja buscar? ')

        self.driver.get(self.url_jobs + self.vaga_desejada)

    def scroll_down2(self):
        self.last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
            # Wait to load the page.
            self.driver.implicitly_wait(30)  # seconds
            self.new_height = self.driver.execute_script("return document.body.scrollHeight")

            if self.new_height == self.last_height:
                break
            self.last_height = self.new_height
            # sleep for 30s
            self.driver.implicitly_wait(30)  # seconds

    def proxima_pagina(self):
        self.pagina += 25
        self.driver.get(f'https://www.linkedin.com/jobs/search/?keywords={self.vaga_desejada}&start={self.pagina}')

    # noinspection PyAttributeOutsideInit
    def armazena_vagas(self):
        self.site = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.vagas: ResultSet = self.site.findAll('div', attrs={
            'class': 'flex-grow-1 artdeco-entity-lockup__content ember-view'})

        for vaga in self.vagas:

            titulo = vaga.find('a',
                               attrs={'class': 'disabled ember-view job-card-container__link job-card-list__title'})

            empresa = vaga.find('a',
                                attrs={'class': 'job-card-container__link job-card-container__company-name ember-view'})
            #colocar outra opção de classe

            local = vaga.find('li', attrs={'job-card-container__metadata-item'})

            if titulo is not None:

                if empresa is not None:

                    if local is not None:
                        self.lista_vagas.append([titulo.text, empresa.text, local.text])

                    self.lista_vagas.append([titulo.text, empresa.text])

                self.lista_vagas.append([titulo.text])

    def cria_dataframe(self):
        self.result = pd.DataFrame(self.lista_vagas, columns=['Título', 'Empresa', 'Local'])
        self.result.dropna(subset=['Empresa'], inplace=True)
        self.result.dropna(subset=['Local'], inplace=True)
        self.nome_vaga = input("Como você gostaria de salvar o arquivo?")
        self.formato = '.xlsx'
        self.result.to_excel(f'{self.nome_vaga}{self.formato}', index=False)
        #os.system(fr'start C:\Users\{self.nome_vaga}{self.formato}')


start = Scrappy()
start.iniciar()