import csv
import sqlite3

def pobrisi_tabele(cur):
    '''Pobrise tabele iz baze'''
    cur.execute("DROP TABLE IF EXISTS gost;")
    cur.execute("DROP TABLE IF EXISTS soba;")
    cur.execute("DROP TABLE IF EXISTS zaposeni;")
    cur.execute("DROP TABLE IF EXISTS vpis;")
    cur.execute("DROP TABLE IF EXISTS skrbi;")

def ustvari_tabelo_gost(cur):
    '''Ustvari tabelo gost'''
    cur.execute("""
    CREATE TABLE gost (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ime STRING NOT NULL,
        naslov STRING NOT NULL,
        bancna INTEGER NOT NULL
    );      
    """)

def ustvari_tabelo_soba(cur):
    '''Ustvari tabelo soba'''
    cur.execute("""
    CREATE TABLE soba (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        namen STRING NOT NULL,
        prostost INTEGER NOT NULL
    );      
    """)

def ustvari_tabelo_zaposleni(cur):
    '''Ustvari tabelo zaposleni'''
    cur.execute("""
    CREATE TABLE zaposleni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ime STRING NOT NULL,
        naslov STRING NOT NULL,
        delovno_mesto STRING NOT NULL,
        vrsta_zaposlitve STRING NOT NULL
    );      
    """)

def ustvari_tabelo_vpis(cur):
    '''Ustvari tabelo vpis'''
    cur.execute("""
    CREATE TABLE vpis (
        stranka INTEGER REFERENCES gost (id),
        id_sobe INTEGER REFERENCES soba (id),
        zacetek DATE NOT NULL,
        konec   DATE NOT NULL,
        placano INTEGER NOT NULL,
        PRIMARY KEY(
            stranka,
            id_sobe,
            zacetek
        )
    );      
    """)

def ustvari_tabelo_skrbi(cur):
    '''Ustvari tabelo skrbi'''
    cur.execute("""
    CREATE TABLE skrbi (
        id_zaposleni INTEGER REFERENCES zaposelni (id),
        id_sobe INTEGER REFERENCES soba (id),
        zacetek DATE NOT NULL,
        konec   DATE NOT NULL,
        PRIMARY KEY(
            id_zaposleni,
            id_sobe,
            zacetek
        )
    );      
    """)

def ustvari_tabele(cur):
    '''Ustvari vse tabele v bazi'''
    ustvari_tabelo_gost(cur)
    ustvari_tabelo_soba(cur)
    ustvari_tabelo_vpis(cur)
    ustvari_tabelo_zaposleni(cur)
    ustvari_tabelo_skrbi(cur)


def uvozi_podatke_o_gostih(cur):
    '''Uvozi podatke o gostih v PB'''
    cur.execute("DELETE FROM gost")
    with open('CsvPodatki/PodatkiGosti.csv') as dat:
        podatki=csv.reader(dat)
        stolpci=next(podatki)
        poizvedba= """
            INSERT INTO gost VALUES ({})
        """.format(', '.join(["?"]*len(stolpci)))
        for vrstica in podatki:
            cur.execute(poizvedba,vrstica)


def uvozi_podatke_o_zaposlenih(cur):
    '''Uvozi podatke o zaposlenih v PB'''
    cur.execute("DELETE FROM zaposleni")
    with open('CsvPodatki/PodatkiZaposleni.csv') as dat:
        podatki=csv.reader(dat)
        stolpci=next(podatki)
        poizvedba= """
            INSERT INTO zaposleni VALUES ({})
        """.format(', '.join(["?"]*len(stolpci)))
        for vrstica in podatki:
            cur.execute(poizvedba,vrstica)

def uvozi_podatke_sob(cur):
    '''Uvozi podatke sob v PB'''
    cur.execute("DELETE FROM soba")
    with open('CsvPodatki/PodatkiSobe.csv') as dat:
        podatki=csv.reader(dat)
        stolpci=next(podatki)
        poizvedba= """
            INSERT INTO soba VALUES ({})
        """.format(', '.join(["?"]*len(stolpci)))
        for vrstica in podatki:
            cur.execute(poizvedba,vrstica)

def uvozi_podatke_vpisa(cur):
    '''Uvozi podatke o vpisu.'''
    cur.execute("DELETE FROM vpis")
    with open('CsvPodatki/PodatkiVpisa.csv') as dat:
        podatki=csv.reader(dat)
        stolpci=next(podatki)
        poizvedba="""
        INSERT INTO vpis VALUES ({})
        """.format(', '.join(["?"]*len(stolpci)))
        for vrstica in podatki:
            cur.execute(poizvedba,vrstica)

def uvozi_podatke_skrbnistvaSob(cur):
    '''Uvozi podatke o skrbnistvu sob.'''
    cur.execute("DELETE FROM vpis")
    with open('CsvPodatki/PodatkiSkrbnistva.csv') as dat:
        podatki=csv.reader(dat)
        stolpci=next(podatki)
        poizvedba="""
        INSERT INTO skrbi VALUES ({})
        """.format(', '.join(["?"]*len(stolpci)))
        for vrstica in podatki:
            cur.execute(poizvedba,vrstica)

def uvozi_vse(cur):
    '''Uvozi vse podatke v bazo'''
    uvozi_podatke_o_gostih(cur)
    uvozi_podatke_o_zaposlenih(cur)
    uvozi_podatke_sob(cur)
    uvozi_podatke_skrbnistvaSob(cur)
    uvozi_podatke_vpisa(cur)

def zgradi_bazo(cur):
    '''Naredi bazo in jo napolne s podatki'''
    pobrisi_tabele(cur)
    ustvari_tabele(cur)
    uvozi_vse(cur)

def zgradi_bazo_ne_obstaja(cur):
    '''Če baza ne obstaja, jo naredi'''
    with cur:
        conn=cur.execute("SELECT COUNT(*) FROM sqlite_master")
        if conn.fetchone()==(0, ):
            zgradi_bazo(cur)