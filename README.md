- - -

**_esta lib não é oficial. Prossiga por sua conta e risco!_**

- - - 

python-enotas-emissor
======
API do eNotas emissor REST APIs para python 2/3 client

instalação
-----
```
pip install python-enotas-emissor
```
Requires
-----
  * httplib2
  * simplejson
  * six


eNotas emissor REST APIs
------------------------------
 [developer site](http://enotas.com.br) eNotas REST APIs.


auth
-----

eNotas API usa Basic auth

``` python
from enotas.client import ENotasEmissorAPI

api = ENotasEmissorAPI(api_key = 'MDMwYWRkMTctNWYyYS00YzYyLTkzZDItOTQ5YTlkZjhlMjg3')
```
       


``` python
api_key = 'sua api key'
api = ENotasEmissorAPI(api_key = api_key)
vendas, proxima_pagina, total_vendas = api.vendas_by_filter(pageNumber = 0, pageSize = 50,
                                  filter = "(situacao eq 2 or situacao eq 3) and ((data ge getFirstDayOfLastMonth() and data le getLastDayOfLastMonth()))",orderBy = 'data desc')

for venda in vendas:
    print venda.valorTotal
```

filtro:
-----

voce pode usar a API para vendas, clientes ou produto:

``` python
# busca venda por filtro
vendas, proxima_pagina, total_vendas = api.vendas_by_filter(pageNumber = 0, pageSize = 50,
                                  filter = "(situacao eq 2 or situacao eq 3) and ((data ge getFirstDayOfLastMonth() and data le getLastDayOfLastMonth()))",orderBy = 'data desc')

# busca produto por filtro
#Possíveis campos: createdAt, nome, idExterno, tags
produto, proxima_pagina, total_produto = api.produto_by_filter(pageNumber = 0, pageSize = 50,
                                  filter = "(contains(nome, 'enotas') or contains(idExterno, 'enotas'))")
								  
# busca cliente por filtro
Possíveis campos: createdAt, nome, email, cpfCnpj, uf, cidade
cliente, proxima_pagina, total_cliente = api.cliente_by_filter(pageNumber = 0, pageSize = 50,
                                  filter = "(contains(nome, 'enotas'))")
```

busca por id:

``` python
# busca venda por id
venda = api.venda(vendaId = 'id')

# busca produto por id
produto = api.produto(produtoId = 'id')

# busca cliente por id
cliente = api.produto(clienteId = 'id')
```
    

criar ou atualizar:
-----

venda:

``` python
criar = {'data': '17/12/2017', 'produto': {'nome': 'enotas'}, 'valorTotal' : 10}
atualizar = {'id': idvenda, 'data': '17/12/2017', 'produto': {'nome': 'enotas'}, 'valorTotal' : 10}
venda = api.venda_add_or_update(data = criar/atualizar)
```            

produto:

``` python
criar = { 'nome': 'Como adestrar cachorros', 'idExterno': '324', 'valorTotal': 29.00, 'diasGarantia': 30, 'tags': 'adestramento'}
atualizar = { 'id': idproduto, 'nome': 'Como adestrar cachorros', 'idExterno': '324', 'valorTotal': 29.00, 'diasGarantia': 30, 'tags': 'adestramento'}
produto = api.produto_add_or_update(data = criar/atualizar)
```

cliente:
    
``` python
criar = {
"nomeFantasia": None,
"inscricaoMunicipal": None,
"inscricaoEstadual": None,
"email": "jose@romualdo.com.br",
"telefone": "31231231231",
"nome": "José Romualdo",
"cpfCnpj": "15112512121",
"endereco": {
	cidade": "Belo Horizonte",
	"codigoIbgeCidade": 3106200,
	"logradouro": "R. Engenheiro Alberto Pontes",
	"numero": "427",
	"complemento": None,
	"bairro": "Buritis",
	"cep": "12412512"
	}
}
atualizar = {
"id": idcliente
"nomeFantasia": None,
"inscricaoMunicipal": None,
"inscricaoEstadual": None,
"email": "jose@romualdo.com.br",
"telefone": "31231231231",
"nome": "José Romualdo",
"cpfCnpj": "15112512121",
"endereco": {
	cidade": "Belo Horizonte",
	"codigoIbgeCidade": 3106200,
	"logradouro": "R. Engenheiro Alberto Pontes",
	"numero": "427",
	"complemento": None,
	"bairro": "Buritis",
	"cep": "12412512"
	}
}
cliente = api.cliente_add_or_update(data = json.dumps(criar/atualizar))
```    
 
lib baseada na lib do Instagram
