def product_to_string(product):
    contents = [
        "title:",
        product['title'],
        "url:",
        product['url']
    ]
    if 'category' in product:
        contents = contents + [
            "category:",
            product['category'],
            "color:",
            product['color']['color'],
            ','.join(product['color']['descriptions']),
        ] + ([] if product['pattern']['pattern'] is None else [
            "pattern:",
            product['pattern']['pattern'],
            ','.join(product['pattern']['descriptions']),
        ]) + [
            "style:",
            ','.join(product['style']['styles']),
            product['style']['description'],
        ] + [
            'occasions:',
        ] + [
            occasion['name'] + '\n' + occasion['description']
            for occasion in product['occasions']['occasions']
        ] + [
            'seasons:',
        ] + [
            season['name'] + '\n' + season['description']
            for season in product['season']
        ] + [
            'weather:',
        ] + [
            weather['name'] + '\n' + weather['description']
            for weather in product['weather']
        ] + [
                product['description']
        ]
    return '\n'.join(contents)