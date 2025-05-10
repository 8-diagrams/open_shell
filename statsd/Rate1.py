
import requests

def conv(from_ccy, to_ccy, amount ) :
    url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"

    querystring = {"from":f"{from_ccy}","to":f"{to_ccy}","amount":f"{amount}"}

    headers = {
        "x-rapidapi-key": "9071219a43mshfeef19bbc40593cp1decb2jsnc49660e669a6",
        "x-rapidapi-host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    r =  response.json() 
    #print(" json =>", r )
    if r.get('success') :
        return r.get('result') 
    else:
        return None 

if __name__ == '__main__':
    c = conv( 'USD', 'EUR' , 100 )
    print ("rate => ", c )