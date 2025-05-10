import Rate1 

if __name__ == '__main__' :
    
    c = Rate1.conv('USD', 'EUR', 100 )
    print( c )
    import SendMetric
    key = 'stats.gauges.ccrate.USD.EUR.A486695'
    stat = f'{key}:{c}|g'
    SendMetric.send_udp_message(stat, 'udpstatus.newgai.com', 8125  )
    