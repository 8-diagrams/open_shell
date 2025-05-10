import requests 

def conv(from_ccy, to_ccy, amount ) :
    
    url = f'https://v6.exchangerate-api.com/v6/f3ee39a5557c367216ecbe48/latest/{from_ccy}'        
    response = requests.get(url) 
    r =  response.json() 
    #print(" json =>", r )   
    if r.get('result') == 'success':
        conversion_rates = r['conversion_rates']
        conversion_rates[f'{to_ccy}']
        ret = conversion_rates.get(f'{to_ccy}') * float( amount )
        return round(ret, 5)
    return None                                                           
    
if __name__ == '__main__':
    d = conv('USD', 'EUR', 100) 
    print( "d=>", d)