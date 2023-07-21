import sqlite3

def mmr3(mm3):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM StringMmh3LTU WHERE mmh3_id=?', (mm3,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[1] if result else None
murmurhash = input('MurmurHash integer to find string value of: ')
print(mmr3(murmurhash))
