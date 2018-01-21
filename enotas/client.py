from .authorization import Authorization 
from .bind import bind_method
from .models import Venda, Produto, Cliente

SEARCH_ACCEPT_PARAMETERS = ["pageNumber", "pageSize","orderBy"]

SUPPORTED_FORMATS = ['json']


class ENotasEmissorAPI(Authorization):

    host = "app.enotas.com.br"
    base_path = "/api"
    api_key = "basic"
    protocol = "https"
    api_name = "eNotas"
    

    def __init__(self, *args, **kwargs):
        format = kwargs.get('format', 'json')
        if format in SUPPORTED_FORMATS:
            self.format = format
        else:
            raise Exception("Unsupported format")
        super(ENotasEmissorAPI, self).__init__(**kwargs)

    '''Function definition and invocation.''' 
    venda = bind_method(
                path="/vendas/{vendaId}",
                response_type="entry",
                accepts_parameters= "vendaId",
                root_class=Venda)
    '''Function definition and invocation.''' 
    vendas_by_filter = bind_method(
                path="/vendas/getFilterBy",
                accepts_parameters= SEARCH_ACCEPT_PARAMETERS + ['filter'],
                paginates=True,
                root_class=Venda)
    venda_add_or_update = bind_method(
                method="POST",
                path="/vendas",
                response_type="entry",
                accepts_parameters=["data"],
                root_class=Venda)
    produto_add_or_update = bind_method(
                method="POST",
                path="/produtos",
                response_type="entry",
                accepts_parameters=["data"],
                root_class=Produto)
    produto = bind_method(
                path="/produtos/{produtoId}",
                response_type="entry",
                accepts_parameters= "produtoId",
                root_class=Produto)
    '''Function definition and invocation.''' 
    produto_by_filter = bind_method(
                path="/produtos/getFilterBy",
                accepts_parameters= SEARCH_ACCEPT_PARAMETERS + ['filter'],
                paginates=True,
                root_class=Produto)
    cliente_add_or_update = bind_method(
                method="POST",
                path="/clientes",
                response_type="entry",
                accepts_parameters=["data"],
                root_class=Cliente)
    cliente = bind_method(
                path="/clientes/{clienteId}",
                response_type="entry",
                accepts_parameters= "clienteId",
                root_class=Cliente)
    '''Function definition and invocation.''' 
    cliente_by_filter = bind_method(
                path="/clientes/getFilterBy",
                accepts_parameters= SEARCH_ACCEPT_PARAMETERS + ['filter'],
                paginates=True,
                root_class=Cliente)
