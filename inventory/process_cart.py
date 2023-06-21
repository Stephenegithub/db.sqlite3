import cgi

# Get the form data
form = cgi.FieldStorage()
product_name = form.getvalue('product_name')
quantity = form.getvalue('quantity')
price = form.getvalue('price')
shipping_address = form.getvalue('shipping_address')

# Validate the form data
if not product_name or not quantity or not price or not shipping_address:
    print("Content-Type: text/html")
    print()
    print("<h1>Error: Please fill in all fields.</h1>")
    exit()

# Perform additional validation or processing if needed

# Example: Print the cart details
print("Content-Type: text/html")
print()
print("<h1>Cart Details</h1>")
print("<p>Product Name: {}</p>".format(product_name))
print("<p>Quantity: {}</p>".format(quantity))
print("<p>Price: {}</p>".format(price))
print("<p>Shipping Address: {}</p>".format(shipping_address))
