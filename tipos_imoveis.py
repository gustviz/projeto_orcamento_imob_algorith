VALOR_APARTAMENTO = 700.00
VALOR_CASA = 900.00
VALOR_ESTUDIO = 1200.00

VALOR_CONTRATO = 2000.00

ACRESCIMO_APARTAMENTO_2_QUARTOS = 200.00
ACRESCIMO_CASA_2_QUARTOS = 250.00
ACRESCIMO_GARAGEM_CASA_APARTAMENTO = 300.00
ACRESCIMO_ESTUDIO_2_VAGAS = 250.00
ACRESCIMO_ESTUDIO_VAGA_EXTRA = 60.00

DESCONTO_SEM_FILHOS = 0.05  # 5%


def calcular_aluguel(tipo_imovel, quartos, garagem, tem_criancas):
    """
    Calcula o valor do aluguel mensal baseado nas opções escolhidas.Retorna o valor do aluguel mensal calculado.
    """
    # Valor base
    if tipo_imovel == 'Apartamento':
        valor = VALOR_APARTAMENTO
    elif tipo_imovel == 'Casa':
        valor = VALOR_CASA
    elif tipo_imovel == 'Estudio':
        valor = VALOR_ESTUDIO
    else:
        return 0
    
    # Acréscimo Apartamento e Casa
    if tipo_imovel == 'Apartamento' and quartos == 2:
        valor += ACRESCIMO_APARTAMENTO_2_QUARTOS
    elif tipo_imovel == 'Casa' and quartos == 2:
        valor += ACRESCIMO_CASA_2_QUARTOS
    
    # Acréscimo garagem/vagas
    if tipo_imovel in ['Apartamento', 'Casa']:
        if garagem > 0:
            valor += ACRESCIMO_GARAGEM_CASA_APARTAMENTO
    elif tipo_imovel == 'Estudio':
        # Estudio: 2 vagas = R$ 250,00, cada vaga adicional = R$ 60,00
        if garagem >= 2:
            valor += ACRESCIMO_ESTUDIO_2_VAGAS
            if garagem > 2:
                vagas_extras = garagem - 2
                valor += vagas_extras * ACRESCIMO_ESTUDIO_VAGA_EXTRA
        elif garagem == 1:
            valor += ACRESCIMO_ESTUDIO_2_VAGAS / 2
    
    # Desconto para apartamentos sem crianças
    if tipo_imovel == 'Apartamento' and not tem_criancas:
        valor *= (1 - DESCONTO_SEM_FILHOS)
    
    return round(valor, 2)


def calcular_parcela_contrato(num_parcelas):
    """
    Calcula o valor de cada parcela do contrato: número de parcelas (1 a 5). Retorna o valor da parcela.
    """
    if num_parcelas < 1:
        num_parcelas = 1
    elif num_parcelas > 5:
        num_parcelas = 5
    
    return round(VALOR_CONTRATO / num_parcelas, 2)


def gerar_parcelas_mensais(valor_aluguel, num_meses=12, num_parcelas_contrato=1, valor_parcela_contrato=0):
    """
    Gera lista de parcelas mensais do aluguel. Retorna lista de dicionários com mês e valor.
    Nos primeiros meses, inclui a parcela do contrato.
    """
    parcelas = []
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    for i in range(num_meses):
        # Nos primeiros meses, adiciona a parcela do contrato
        if i < num_parcelas_contrato:
            valor_mes = valor_aluguel + valor_parcela_contrato
        else:
            valor_mes = valor_aluguel
        
        parcelas.append({
            'mes': meses[i % 12],
            'valor': round(valor_mes, 2)
        })
    
    return parcelas

