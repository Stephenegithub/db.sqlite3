from django import template

register = template.Library()


@register.filter
def generate_table(products, categories):
    html = '<table>'
    html += '<thead><tr><th>Name</th><th>Category</th><th>In Stock</th></tr></thead>'
    html += '<tbody>'

    for product in products:
        html += f'<tr><td>{product.name}</td><td>{product.category}</td><td>{product.inventory}</td></tr>'

    html += '</tbody></table>'
    return html
