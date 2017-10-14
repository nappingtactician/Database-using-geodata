import urllib
import sqlite3
import json
import ssl

serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

conn = sqlite3.connect('geodata.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE geodata(address, geometrylat, geometrylng, viewportnortheastlat, viewportnortheastlng, viewportsouthwestlat, viewportsouthwestlng, place_id, formatted_address)''')

while True:
    
    address = raw_input("Enter address: ")
    url = serviceurl + urllib.urlencode({'sensor':'false', 'address': address})
    print url

    uh = urllib.urlopen(url)
    data = uh.read()
    

    try:js = json.loads(str(data))
    except: js = None
    if 'status' not in js or js['status'] != 'OK':
        print "---------FAILURE TO RETRIEVE---------"
    continue
    print json.dumps(js, indent = 2)


    lata = js["results"][0]["geometry"]["location"]["lat"]
    lnga = js["results"][0]["geometry"]["location"]["lng"]
    latb = js["results"][0]["geometry"]["viewport"]["northeast"]["lat"]
    lngb = js["results"][0]["geometry"]["viewport"]["northeast"]["lng"]
    latc = js["results"][0]["geometry"]["viewport"]["southwest"]["lat"]
    lngc = js["results"][0]["geometry"]["viewport"]["southwest"]["lng"]
    place_id = js["results"][0]["place_id"]
    formatted_address = js["results"][0]["formatted_address"]

    print lata, lnga, latb, lngb, latc, lngc, place_id, formatted_address

    c.execute('''INSERT INTO geodata(address, geometrylat, geometrylng, viewportnortheastlat, viewportnortheastlng, viewportsouthwestlat, viewportsouthwestlng, place_id, formatted_address) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')'''.format(address,lata, lnga, latb, lngb, latc, lngc, place_id, formatted_address))


conn.commit()
conn.close()
