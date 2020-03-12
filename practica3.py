from urllib.request import urlopen
import mysql.connector as mysql
from bs4 import BeautifulSoup


conexion= mysql.connect(host='localhost',user='root',passwd='',db='prueba')
operacion = conexion.cursor()

def check(pagina):
    elementos=0
    print("pagina: "+pagina)
    url=urlopen(pagina)
    try:
        bs=BeautifulSoup(url.read(),'html.parser')
    except Exception:
        return
    for enlaces in bs.find_all('a'):
        enlace_encontrado='href: {}'.format(enlaces.get('href'))
        try:
            enlace_encontrado=enlace_encontrado[6:]
        except KeyError:
            continue
        if not enlace_encontrado.startswith('http'):
            continue
        try:
            mysql_insert="""INSERT INTO paginas (pagina,status) values (%s,%s)""" 
            val=(enlace_encontrado,False)
            operacion.execute(mysql_insert,val)
            elementos+=1
            conexion.commit()
        except mysql.errors.IntegrityError:
            continue
    print("elementos: ", elementos)

pagina_inicial=input('Ingrese pagina: ')
#'http://sagitario.itmorelia.edu.mx/~rogelio/'
print('\nExtraer los enlaces de la página web: '+pagina_inicial+'\n')
check(pagina_inicial)



while True:
    operacion.execute("SELECT * FROM paginas WHERE status=False")
    for pagina, status in operacion.fetchall():
        try:
            check(pagina)
        except Exception as e:
            operacion.execute(f'UPDATE paginas SET status=True WHERE pagina="{pagina}"')
            continue
        operacion.execute(f'UPDATE paginas SET status=True WHERE pagina="{pagina}"')
 

'''while True:
    operacion.execute("SELECT * FROM paginas WHERE status=FALSE")
    pagina = operacion.fetchone()
    if not pagina:
        break
    try:
        check(pagina)
    except Exception as e:
        operacion.execute(f'UPDATE paginas SET status=TRUE WHERE pagina="{pagina}"')
        continue
    operacion.execute(f'UPDATE paginas SET status=TRUE WHERE pagina="{pagina}"')
    operacion.execute("SELECT * FROM paginas")
    rows = operacion.fetchall()
    print(f"Entradas: {len(rows)}")
    conexion.commit()'''


conexion.close()
