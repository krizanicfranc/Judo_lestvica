
# coding: utf-8

# In[1]:
import orodja
import csv
import os
import requests
import sys
import re


def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def shrani(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {}...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')


def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke) as datoteka:
        vsebina = datoteka.read()
    return vsebina


def datoteke(imenik):
    '''Vrne imena vseh datotek v danem imeniku skupaj z imenom imenika.'''
    return [os.path.join(imenik, datoteka) for datoteka in os.listdir(imenik)]


def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)



# In[2]:

kateg={1:'-60kg', 2:'-66kg', 3:'-73kg', 4:'-81kg', 5:'-90kg', 6:'-100kg', 7:'+100kg',
      8:'-48kg', 9:'-52kg', 10: '-57kg', 11:'-63kg', 12:'-70kg', 13:'-78kg', 14:'+78jg'}


# In[3]:

def prenesi_m():
    for teza in range(1,8):
               
        for stran in range(1, 15):
            naslov='https://www.ijf.org/wrl?age=seniors&gender=m&id_weight={}&p={}'.format(teza, stran)
            datoteka='JUDO\m{}{:02}.html'.format(kateg[teza], stran)
            shrani(naslov, datoteka)
#prenesi_m()


# In[86]:

def prenesi_w():
    for teza in range(8,15):
               
        for stran in range(1, 15):
            naslov='https://www.ijf.org/wrl?age=seniors&gender=m&id_weight={}&p={}'.format(teza, stran)
            datoteka='JUDO\w{}{:02}.html'.format(kateg[teza], stran)
            shrani(naslov, datoteka)
#prenesi_w()


# In[ ]:
def pocisti_ime(judoka):
    podatki = judoka.groupdict()
    podatki['ime'] = re.sub('[\n]','',podatki['ime'])
    return podatki

def pripravi_db():
    regex_db = re.compile(
        r'<a href="(?P<povezava>/athlete/\d+)">\s*(?P<ime>.*?\s?.*?)\s*</a>'  
        r'.*?<img src="https:.*?<small>(?P<drzava>.*?)</small>'
        r'.*?<td class="text-center">\s*(?P<tocke>\d+) points\s*</td>'
        ,flags=re.DOTALL
    )
    
    judoke = []
    for dat in datoteke('JUDO/'):
        
        for judoka in re.finditer(regex_db, vsebina_datoteke(dat)):

            #print (pocisti_ime(judoka))
            judoke.append(pocisti_ime(judoka))

    orodja.zapisi_tabelo(judoke, ['povezava','ime', 'drzava', 'tocke'], 'judoke.csv')

            
            
                  
pripravi_db()





