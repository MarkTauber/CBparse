import urllib.request                 
import xml.etree.ElementTree as ET     
from datetime import timedelta, date  
import statistics                    

daymath = 0    
Valuemath = 0   
dod = 0
Fulldata = []

li = [[] for _ in range(90)]
namem = [[] for _ in range(90)]

while dod < 90:     #цикл 90 дней
    Datesearch = date.today() - timedelta(days=dod) 
    date_string = Datesearch.strftime('%d/%m/%Y') 
    url = "http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req="+ date_string #Генерация ссылки
    #print("Parsing url: " + url)                           
    webFile = urllib.request.urlopen(url)       
    data = webFile.read()            
    
    with open("data.xml", "wb") as localFile:   #Дебаг, можно читать из переменной data
        localFile.write(data)                   
    
    lst = []          
    lsts = []         
    root = ET.parse('data.xml').getroot()
    
    for country in root.findall('Valute'):      #Корень дерева <ValCurs Date="дата" name="Foreign Currency Market">
        Charcode = country.find('Name').text    #Имя валюты 
        Value = country.find('Value').text      #Стоимость
        lst.append(Value)                   
        lsts.append(Charcode)               
    
    d = 0            
    Fulldata.append(date_string)    
    
    while d < 34:  
        li[daymath].append(lst[d])         
        namem[daymath].append(lsts[d])     
        d+=1
    
    daymath+=1 
    dod=dod+1      
    
dni = 0  
dengi = 0
maxxx = []

reportes = open("reports.txt", "w")
reportes.write("")
reportes.close() 
reportes = open("reports.txt", "a")

while dengi < 34: 

    while dni<90:
        sheesh=li[dni][dengi].replace(",",".") #Форматируем данные
        maxxx.append(float(sheesh))
        dni+=1
        
    statist = statistics.mean(maxxx)                                  #среднее арифметическое 
    index1, max_value = max(enumerate(maxxx), key=lambda i_v: i_v[1]) #Получаем максимальное значение и его адрес
    index2, min_value = min(enumerate(maxxx), key=lambda i_v: i_v[1]) #Получаем миниальное значение и его адрес
    ass = float('{:.4f}'.format(statist))                             #Чистим выходные данные от мусора
    
    print("Aritmetic mean of " + str(namem[0][dengi]) + " is [" + str(ass) + "]") 
    print("Maxinum of " + str(namem[0][dengi]) + " is [" + str(max_value) + "] at date [" + Fulldata[index1] + "]")   
    print("Minimum of " + str(namem[0][dengi]) + " is [" + str(min_value) + "] at date [" + Fulldata[index2] + "] \n")  
    
    reportes.write("Aritmetic mean of " + str(namem[0][dengi]) + " is [" + str(ass) + "]\n" + "Maxinum of " + 
    str(namem[0][dengi]) + " is [" + str(max_value) + "] at date [" + Fulldata[index1] + "]\n" + "Minimum of " + 
    str(namem[0][dengi]) + " is [" + str(min_value) + "] at data [" + Fulldata[index2] + "]\n\n")
    
    dengi+=1 
    dni = 0 
    maxxx = [] 
    
reportes.close() 
print('Report was created as "report.txt"')