import sqlite3
import zgradiBazo

conn=sqlite3.connect('hotel.db')
zgradiBazo.zgradi_bazo_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys= ON')

def poisci_gosta(ime):
    '''funkcija poisce vse goste z danim imenom v tabeli gosti'''
    poizvedba="""
        SELECT ime,naslov,bancna 
        FROM gost
        WHERE ime=?
    """
    return conn.execute(poizvedba,ime)

def dobi_podatke_o_zaposlenem(ime):
    '''funkcija poisce vse podatke o zaposlenih osebah z danim imenom'''
    poizvedba="""
        SELECT ime,naslov,delovno_mesto,vrsta_zaposlitve
        FROM zaposleni
        WHERE ime=?
    """
    return conn.execute(poizvedba,ime)

def vpisi_podatke_gosta(ime,naslov,bancna):
    '''funkcija vpise danega gosta v pb'''
    poizvedba="""
        UPDATE gost (ime,naslov,bancna)
        VALUES (?,?,?)
        """
    return conn.execute(poizvedba,[ime,naslov,bancna])

def vpisi_podatke_zaposlenega(ime,naslov,delovno_mesto,vrsta_zaposlitve):
    '''funkcija vpise podatke o zaposlenem v pb'''
    poizvedba="""
        UPDATE zaposleni (ime,naslov,delovno_mesto,vrsta_zaposlitve)
        VALUES (?,?,?,?)
        """
    return conn.execute(poizvedba,[ime,naslov,delovno_mesto,vrsta_zaposlitve])

