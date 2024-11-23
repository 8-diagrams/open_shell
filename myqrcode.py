import qrcode
data = 'THsLiiFRGR7Uqtziy6EJiRipxZwtBmAYft'

img = qrcode.make(data=data)
img.show()
