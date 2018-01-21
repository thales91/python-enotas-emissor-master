from .helper import timestamp_to_datetime
import six


class ApiModel(object):

    @classmethod
    def object_from_dictionary(cls, entry):
        # make dict keys all strings
        if entry is None:
            return ""
        entry_str_dict = dict([(str(key), value) for key, value in entry.items()])
        return cls(**entry_str_dict)

    def __repr__(self):
        return str(self)
        # if six.PY2:
        #     return six.text_type(self).encode('utf8')
        # else:
        #     return self.encode('utf8')

    def __str__(self):
        if six.PY3:
            return self.__unicode__()
        else:
            return unicode(self).encode('utf-8')

class Endereco(ApiModel):

    def __init__(self, codigoIbgeUf = None, codigoIbgeCidade = None, pais = None, uf = None, cidade = None, logradouro = None, numero = None,
                 complemento = None, bairro = None, cep = None):
        self.codigoIbgeUf = codigoIbgeUf
        self.codigoIbgeCidade = codigoIbgeCidade
        self.pais = pais
        self.uf = uf
        self.cidade = cidade
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cep = cep


class Cliente(ApiModel):
    def __init__(self, id = None, createdAt = None, tipoPessoa = None, nome = None, email = None, email2 = None, email3 = None,
                 cpfCnpj = None,inscricaoMunicipal = None, inscricaoEstadual = None,nomeFantasia = None, telefone = None,
                 endereco = None, valorMovimentado = None, clienteId = None):
        self.id = id
        self.createdAt = createdAt
        self.tipoPessoa = tipoPessoa
        self.nome = nome
        self.email = email
        self.email2 = email2
        self.email3 = email3 
        self.cpfCnpj = cpfCnpj
        self.inscricaoMunicipal = inscricaoMunicipal
        self.inscricaoEstadual = inscricaoEstadual
        self.nomeFantasia = nomeFantasia
        self.telefone = telefone
        self.endereco = Endereco.object_from_dictionary(endereco)
        self.valorMovimentado = valorMovimentado
        self.clienteId = clienteId


class ServicoMunicipalUnificado(ApiModel):
    def __init__(self,codigoServicoMunicipalUnificado = None, descricaoServicoMunicipalUnificado = None):
        self.codigoServicoMunicipalUnificado = codigoServicoMunicipalUnificado
        self.descricaoServicoMunicipalUnificado = descricaoServicoMunicipalUnificado


class Produto(ApiModel):
    def __init__(self, cadastradoAutomaticamente = None , aliquotaIss = None,
                 codigoServicoMunicipal = None, codigoServicoMunicipio = None,
                 itemListaServicoLC116 = None, cnae = None , createdAt = None,
                 descricaoServico = None, diasGarantia = None,
                 discriminacaoServico = None , id = None ,idExterno = None,
                 informacaoComplementarTemplate = None ,nome = None,
                 porcentagemTributoEstadual = None,porcentagemTributoFederal = None,
                 porcentagemTributoMunicipal = None, porcentagemTributoSimplificado = None,
                 servicoModificadoManualmente = None ,servicoMunicipalUnificado = None,
                 tags = None ,valorTotal = None ,vencimento = None, produtoId = None):
        
        self.aliquotaIss = aliquotaIss
        self.cadastradoAutomaticamente = cadastradoAutomaticamente
        self.codigoServicoMunicipio = codigoServicoMunicipio
        self.itemListaServicoLC116 = itemListaServicoLC116
        self.cnae = cnae
        self.createdAt = createdAt
        self.descricaoServico = descricaoServico
        self.diasGarantia = diasGarantia
        self.discriminacaoServico = discriminacaoServico
        self.id = id
        self.idExterno = idExterno
        self.informacaoComplementarTemplate = informacaoComplementarTemplate
        self.nome = nome
        self.porcentagemTributoEstadual = porcentagemTributoEstadual
        self.porcentagemTributoFederal = porcentagemTributoFederal
        self.porcentagemTributoMunicipal = porcentagemTributoMunicipal
        self.porcentagemTributoSimplificado = porcentagemTributoSimplificado
        self.servicoModificadoManualmente = servicoModificadoManualmente
        self.servicoMunicipalUnificado = ServicoMunicipalUnificado.object_from_dictionary(servicoMunicipalUnificado)
        self.tags = tags
        self.valorTotal = valorTotal
        self.vencimento = vencimento
        self.produtoId = produtoId


class Canal(ApiModel):
    def __init__(self ,id = None ,nome = None):
        self.id = id
        self.nome = nome


class RPS(ApiModel):
    def __init__(self, dataCompetencia = None):
        self.dataCompetencia = dataCompetencia


class Empresa(ApiModel):
    def __init__(self,id = None,nomeFantasia = None):
        self.id = id
        self.nomeFantasia = nomeFantasia


class ImpostosFederais(ApiModel):
    def __init__(self,porcentagemCofins = None ,porcentagemCsll = None ,porcentagemInss = None ,porcentagemIr = None ,porcentagemPis = None ,valorCofins = None ,valorCsll = None ,valorInss = None ,valorIr = None ,valorPis = None):
        self.porcentagemCofins = porcentagemCofins
        self.porcentagemCsll = porcentagemCsll
        self.porcentagemInss = porcentagemInss
        self.porcentagemIr = porcentagemIr
        self.porcentagemPis = porcentagemPis
        self.valorCofins = valorCofins
        self.valorCsll = valorCsll
        self.valorInss = valorInss
        self.valorIr = valorIr
        self.valorPis = valorPis

    
class MunicipioPrestacao(ApiModel):
    def __init__(self,codigoIbge = None,nome = None):
        self.codigoIbge = codigoIbge
        self.nome = nome

    
class Prefeitura(ApiModel):
    def __init__(self,codigoVerificacao = None ,dataEmissao = None ,linkImpressao = None ,linkXml = None ,numero = None):
        self.codigoVerificacao = codigoVerificacao
        self.dataEmissao = dataEmissao
        self.linkImpressao = linkImpressao
        self.linkXml = linkXml
        self.numero = numero


class NFE(ApiModel):
    def __init__(self,aliquotaIss = None ,baseCalculo = None ,cancelamentoRejeitado = None ,dataTentativaCancelamento = None ,deducoes = None ,descontos = None ,discriminacao = None ,empresa = None ,id = None ,impostosFederais = None ,issRetidoFonte = None ,motivoRejeicaoCancelamento = None ,motivoSituacao = None ,municipioPrestacao = None ,observacoes = None ,prefeitura = None ,rps = None ,situacao = None ,valorIss = None ,valorLiquido = None ,valorTotal = None):
        self.aliquotaIss = aliquotaIss
        self.baseCalculo = baseCalculo
        self.cancelamentoRejeitado = cancelamentoRejeitado
        self.dataTentativaCancelamento = dataTentativaCancelamento
        self.deducoes = deducoes
        self.descontos = descontos
        self.discriminacao = discriminacao
        self.empresa = Empresa.object_from_dictionary(empresa)
        self.id = id
        self.impostosFederais = ImpostosFederais.object_from_dictionary(impostosFederais)
        self.issRetidoFonte = issRetidoFonte
        self.motivoRejeicaoCancelamento = motivoRejeicaoCancelamento
        self.motivoSituacao = motivoSituacao
        self.municipioPrestacao = MunicipioPrestacao.object_from_dictionary(municipioPrestacao)
        self.observacoes = observacoes
        self.prefeitura = Prefeitura.object_from_dictionary(prefeitura)
        self.rps = RPS.object_from_dictionary(rps)
        self.situacao = situacao
        self.valorIss = valorIss
        self.valorLiquido = valorLiquido
        self.valorTotal = valorTotal
    
    
class Venda(ApiModel):
    def __init__(self, id = None ,data = None ,cliente = None ,
                 transacaoCanal = None ,produto = None ,canal = None ,
                 nfe = None ,dataNFeEnviadoPorEmail = None ,idExterno = None ,
                 situacao = None ,valorTotal = None ,tags = None ,
                 vencimento = None ,quandoEmitirNFe = None ,
                 enviarNFeCliente = None ,meioPagamento = None, vendaId = None):
        self.id = id
        self.data = data
        self.cliente = Cliente.object_from_dictionary(cliente)
        self.transacaoCanal = transacaoCanal
        self.produto = Produto.object_from_dictionary(produto)
        self.canal = Canal.object_from_dictionary(canal)
        self.nfe = NFE.object_from_dictionary(nfe)
        self.dataNFeEnviadoPorEmail = dataNFeEnviadoPorEmail
        self.idExterno = idExterno
        self.situacao = situacao
        self.valorTotal = valorTotal
        self.tags = tags
        self.vencimento = vencimento
        self.quandoEmitirNFe = quandoEmitirNFe
        self.enviarNFeCliente = enviarNFeCliente
        self.meioPagamento = meioPagamento
        self.vendaId = vendaId

    
