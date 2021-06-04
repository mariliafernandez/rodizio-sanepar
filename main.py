from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def check_dates(rua, cep=None, bairro=None):

  if bairro:
    bairro = bairro.lower()
  else:
    bairro = ''
  if not cep:
    cep = ''
  
  rua = rua.lower()
  
  driver = webdriver.Chrome()
  driver.implicitly_wait(5) # seconds
  driver.get("https://sanepar.maps.arcgis.com/apps/webappviewer/index.html?id=cb3ba1eb80424c09b4af0109192b1399")
  wait = WebDriverWait(driver, 10)
  
  try:
    el = wait.until(EC.presence_of_element_located((By.ID, "esri_dijit_Search_0_input")))
  
  except:
    driver.quit()
    raise Exception()

  el.send_keys(f'{rua}, {bairro}, Curitiba, {cep[:5]}')
  
  try:
    menu = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "suggestionsMenu")))
 
  except:
    driver.quit()
    raise Exception()

  div_child = menu.find_element_by_tag_name("div")
  ul_child = div_child.find_element_by_tag_name("ul")
  li_options = ul_child.find_elements_by_tag_name("li")

  for li in li_options:
      if rua in li.text.lower():
        if cep:
          if cep[:5] in li.text:
            li.click()
        if bairro:
          if bairro in li.text.lower():
            li.click()
  
  body_text = driver.find_element_by_tag_name("body").text

  while 'rodízio' not in body_text:
    body_text = driver.find_element_by_tag_name("body").text

  pattern_inicio = 'Início do rodízio:.*\n'
  pattern_volta = 'Previsão de volta da água:.*\n'

  re.compile(pattern_inicio)
  re.compile(pattern_volta)

  result_inicio = re.findall(pattern_inicio, body_text)[0].replace('\n', '')
  result_volta = re.findall(pattern_volta, body_text)[0].replace('\n', '')

  driver.close()
  
  return result_inicio, result_volta
  


if __name__ == '__main__':

  cep = '82560---'
  rua = 'Vicente Ciccarino'
  
  inicio, volta = check_dates(rua, cep)

  print(inicio)
  print(volta)