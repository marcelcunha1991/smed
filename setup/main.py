data = {
    'purchase_orders': [
        {
            'purchase_order': 'purchase_order1',
            'client': 'client1',
            'products': ['product1', 'product2']
        },
        {
            'purchase_order': 'purchase_order3',
            'client': 'client1',
            'products': ['product1', 'product3']
        },
        {
            'purchase_order': 'purchase_order2',
            'client': 'client2',
            'products': ['product2', 'product3']
        },
        {
            'purchase_order': 'purchase_order5',
            'client': 'client2',
            'products': ['product2', 'product2', 'product2']
        },
        {
            'purchase_order': 'purchase_order4',
            'client': 'client3',
            'products': ['product4']
        }
    ]
}


def contaProduto():
    dicionario = dict()


    for i in data['purchase_orders']:

        for k in i['products']:

            if (i['client']+"_"+k in dicionario):

                dicionario[i['client']+"_"+k] = dicionario.get(i['client']+"_"+k) + 1

            else:
                dicionario[i['client']+"_"+k] = 1
    print (dicionario)


def main():
    contaProduto()


if __name__ == "__main__":
    main()

