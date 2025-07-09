def generate_meta_xml(products):
    from xml.etree.ElementTree import Element, SubElement, tostring, register_namespace
    from xml.dom.minidom import parseString

    # Register the 'g' namespace
    register_namespace('g', 'http://base.google.com/ns/1.0')

    rss = Element('rss', version='2.0')
    channel = SubElement(rss, 'channel')
    SubElement(channel, 'title').text = "BigCommerce Product Feed"
    SubElement(channel, 'link').text = "https://yourstore.com"
    SubElement(channel, 'description').text = "Live feed for Meta Commerce Manager"

    for product in products:
        item = SubElement(channel, 'item')
        SubElement(item, '{http://base.google.com/ns/1.0}id').text = str(product['id'])
        SubElement(item, 'title').text = product['name']
        SubElement(item, 'description').text = product['description']
        SubElement(item, 'link').text = product['custom_url']['url']
        SubElement(item, '{http://base.google.com/ns/1.0}price').text = f"{product['price']} CAD"
        if product['images']:
            SubElement(item, '{http://base.google.com/ns/1.0}image_link').text = product['images'][0]['url_standard']
        SubElement(item, '{http://base.google.com/ns/1.0}availability').text = (
            "in stock" if product['availability'] == "available" else "out of stock"
        )

    rough_string = tostring(rss, 'utf-8')
    reparsed = parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
