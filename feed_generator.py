def generate_meta_xml(products):
    from xml.etree.ElementTree import Element, SubElement, tostring, register_namespace
    from xml.dom.minidom import parseString

    # Register the 'g' namespace
    register_namespace('g', 'http://base.google.com/ns/1.0')

    rss = Element('rss', version='2.0')
    channel = SubElement(rss, 'channel')
    SubElement(channel, 'title').text = "Corbetts Product Feed"
    SubElement(channel, 'link').text = "https://www.corbetts.com"
    SubElement(channel, 'description').text = "Live feed for Meta Commerce Manager"

    for product in products:
        item = SubElement(channel, 'item')
        SubElement(item, '{http://base.google.com/ns/1.0}id').text = str(product['id'])
        SubElement(item, 'title').text = product['name']
        SubElement(item, 'description').text = product['description']

        # Full absolute link
        full_link = f"https://www.corbetts.com{product['custom_url']['url']}"
        SubElement(item, 'link').text = full_link

        # Add condition
        SubElement(item, '{http://base.google.com/ns/1.0}condition').text = "new"

        # Add brand
        if 'brand_name' in product:
            SubElement(item, '{http://base.google.com/ns/1.0}brand').text = product['brand_name']

        SubElement(item, '{http://base.google.com/ns/1.0}price').text = f"{product['price']} CAD"

        if product['images']:
            SubElement(item, '{http://base.google.com/ns/1.0}image_link').text = product['images'][0]['url_standard']

        SubElement(item, '{http://base.google.com/ns/1.0}availability').text = (
            "in stock" if product['availability'] == "available" else "out of stock"
        )

    rough_string = tostring(rss, 'utf-8')
    reparsed = parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
