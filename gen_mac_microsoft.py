import requests
import lxml
from lxml import etree

if __name__ == '__main__':
    url='https://macadmins.software/latest.xml'
    resp = requests.get(url)
    #print ( resp.content )    
    tree = etree.XML( resp.content )
    
    nodes = tree.xpath('//package')
    for node in nodes:
        
        imgurl= node.xpath("./icon/text()")[0] 
        print ( '<img src="%s" width="60px" height="60px" />'%(imgurl) )
        print ("<pre>")
        print ( "名称：" +node.xpath("./title/text()")[0] )
        print ( node.xpath("./subtext/text()")[0] )
        #version
        #download
        print ( node.xpath("./version/text()")[0] )
        print ( node.xpath("./download/text()")[0] )
        
        print ( "下载链接: " + node.xpath("./sha1/text()")[0] )

        print ("</pre>")


