from kerykeion import AstrologicalSubjectFactory, ChartDataFactory, to_context
from kerykeion.charts.chart_drawer import ChartDrawer
from kerykeion.settings.config_constants import ALL_ACTIVE_POINTS

#Dicionário que correlaciona o nome dos planetas originais
#com os traduzidos
planetas = {
    "Sun":"Sol",
    "Moon": "Lua",
    "Mercury": "Mercúrio",
    "Venus": "Vênus",
    "Mars": "Marte",
    "Jupiter": "Júpiter",
    "Saturn": "Saturno"
}

#Conversor de casas astrológicas em números
casas_astrologicas = {
    "First_House": 1,
    "Second_House": 2,
    "Third_House": 3,
    "Fourth_House": 4,
    "Fifth_House": 5,
    "Sixth_House": 6,
    "Seventh_House": 7,
    "Eighth_House": 8,
    "Ninth_House": 9,
    "Tenth_House": 10,
    "Eleventh_House": 11,
    "Twelfth_House": 12
}

#Lista que irá agrupar os pontos que iremos usar no
#mapa, sendo os sete planetas clássicos, o Nodo Norte
#e a Parte da Fortuna
pontos = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Ascendant", "Medium_Coeli", "Pars_Fortunae", "True_North_Lunar_Node", "True_South_Lunar_Node"]

def converter_pos(pos_float: float) -> str:
    #Converte posição dada em float, separando-a em
    #graus, minutos e segundos
    graus, resto_graus = divmod(pos_float, 1)
    minutos, resto_minutos = divmod(resto_graus*60,1)
    segundos = round(resto_minutos*60)
    
    #Por precaução, vamos converter os minutos e segundos
    #caso estes sejam iguais a 60, dando 1 grau ou 1 minuto
    #respectivamente
    if segundos == 60:
        segundos = 0
        minutos += 1
    if minutos == 60:
        minutos = 0
        graus += 1

    graus = f"{graus:.0f}º{minutos:.0f}\'{segundos:.0f}\""
    return graus

def obter_dados_planetas(mapa):
    dados = {}
    
    #Laço que vai passar por cada planeta do dicionário lá em
    #cima a fim de organizar as informações a posteriori num
    #JSON a fim de enviar para a IA interpretar
    for k, v in planetas.items():
        planeta = getattr(mapa, k.lower())
        dados[v] = {
            "signo": planeta.sign,
            "posicao": converter_pos(planeta.position),
            "casa": casas_astrologicas[planeta.house],
            "retrogrado": planeta.retrograde
        }
    return dados

def obter_dados_casas(mapa):
    dados = {}

    for k,v in casas_astrologicas.items():
        casa = getattr(mapa, k.lower())
        dados[f"Casa_{v}"] = {
            "signo": casa.sign,
            "posicao": converter_pos(casa.position)
        }
    return dados

def gerar_mapa():
    #Iremos gerar o mapa conforme solicitado
    subject = AstrologicalSubjectFactory.from_current_time(
        nation="BR", lat=-25.444722, lng=-49.065278, tz_str="America/Sao_Paulo", houses_system_identifier="R", active_points=pontos
    )

    dados_planetas = obter_dados_planetas(subject)
    dados_casas = obter_dados_casas(subject)

    #Criação do JSON para envio
    payload = {
        "metadados": {
            "tipo_analise": "horaria",
            "sistema_casas": "Regiomontanus",
            "data_utc": subject.iso_formatted_utc_datetime
        },
        "pontos_cardeais":{
            "Ascendente": {
                "signo": subject.ascendant.sign,
                "posicao": converter_pos(subject.ascendant.position)
            },
            "Meio_do_Ceu": {
                "signo": subject.medium_coeli.sign,
                "posicao": converter_pos(subject.medium_coeli.position)
            }
        },
        "posicoes_planetas": dados_planetas,
        "cuspides_casas": dados_casas,
        "nodo_norte": {
            "signo": subject.true_north_lunar_node.sign,
            "posicao": converter_pos(subject.true_north_lunar_node.position),
            "casa": casas_astrologicas[subject.true_north_lunar_node.house]
        },
        "parte_da_fortuna": {
            "signo": subject.pars_fortunae.sign,
            "posicao": converter_pos(subject.pars_fortunae.position),
            "casa": casas_astrologicas[subject.pars_fortunae.house]
        }
    }
    return payload


    