import azure.functions as func
import logging
import json
import requests
import os
from datetime import datetime
from functools import lru_cache

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Cache in-memory simples para otimização
CACHE_SIZE = 128

@app.route(route="buscar")
def buscar_web(req: func.HttpRequest) -> func.HttpResponse:
    """
    Função que busca informações na web usando simulação inteligente
    """
    start_time = datetime.now()
    logging.info(f'[{start_time}] Função de busca web acionada')

    try:
        # Obter parâmetros da requisição com validação
        req_body = req.get_json()
        
        # Validação: query é obrigatória
        query = req_body.get('query', '').strip()
        if not query:
            logging.warning('Query vazia recebida')
            return func.HttpResponse(
                json.dumps({
                    "erro": "Query não fornecida ou vazia",
                    "mensagem": "Por favor, forneça um termo de busca válido"
                }, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )
        
        # Validação: query não pode ser muito longa
        if len(query) > 200:
            logging.warning(f'Query muito longa: {len(query)} caracteres')
            return func.HttpResponse(
                json.dumps({
                    "erro": "Query muito longa",
                    "mensagem": "Limite de 200 caracteres"
                }, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )
        
        # Validação: max_results
        max_results = req_body.get('max_results', 5)
        if not isinstance(max_results, int) or max_results < 1 or max_results > 10:
            logging.warning(f'max_results inválido: {max_results}')
            max_results = 5  # Default
        
        logging.info(f'Buscando: "{query}" (max_results: {max_results})')
        
        # Buscar resultados reais (DuckDuckGo + Wikipedia + fallback simulação)
        resultados = buscar_web_real(query, max_results)
        
        # Calcular tempo de resposta
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        
        response_data = {
            "query": query,
            "total_resultados": len(resultados),
            "resultados": resultados,
            "tempo_resposta_ms": round(elapsed, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        logging.info(f'Busca concluída: {len(resultados)} resultados em {elapsed:.2f}ms')
        
        return func.HttpResponse(
            json.dumps(response_data, ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )
        
    except ValueError as e:
        logging.error(f"Erro de validação JSON: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "erro": "JSON inválido",
                "mensagem": "O corpo da requisição deve ser um JSON válido"
            }, ensure_ascii=False),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}", exc_info=True)
        return func.HttpResponse(
            json.dumps({
                "erro": "Erro interno do servidor",
                "mensagem": "Ocorreu um erro ao processar sua requisição"
            }, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )

@app.route(route="gerar-cronograma")
def gerar_cronograma(req: func.HttpRequest) -> func.HttpResponse:
    """
    Gera um cronograma personalizado de estudos
    """
    start_time = datetime.now()
    logging.info(f'[{start_time}] Função de geração de cronograma acionada')
    
    try:
        req_body = req.get_json()
        
        # Validar parâmetros
        materias = req_body.get('materias', [])
        dias_semana = req_body.get('dias_semana', 5)
        horas_dia = req_body.get('horas_dia', 3)
        prioridades = req_body.get('prioridades', {})
        
        # Validações
        if not materias or not isinstance(materias, list):
            return func.HttpResponse(
                json.dumps({
                    "erro": "Lista de matérias inválida",
                    "mensagem": "Forneça uma lista de matérias para estudar"
                }, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )
        
        if dias_semana < 1 or dias_semana > 7:
            dias_semana = 5
        
        if horas_dia < 1 or horas_dia > 12:
            horas_dia = 3
        
        logging.info(f'Gerando cronograma: {len(materias)} matérias, {dias_semana} dias, {horas_dia}h/dia')
        
        # Gerar cronograma
        cronograma = criar_cronograma(materias, dias_semana, horas_dia, prioridades)
        
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        
        response_data = {
            "cronograma": cronograma,
            "resumo": {
                "total_materias": len(materias),
                "dias_semana": dias_semana,
                "horas_por_dia": horas_dia,
                "total_horas_semana": sum(dia["total_horas"] for dia in cronograma)
            },
            "tempo_resposta_ms": round(elapsed, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        logging.info(f'Cronograma gerado em {elapsed:.2f}ms')
        
        return func.HttpResponse(
            json.dumps(response_data, ensure_ascii=False, indent=2),
            status_code=200,
            mimetype="application/json"
        )
        
    except ValueError as e:
        logging.error(f"Erro de validação JSON: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "erro": "JSON inválido",
                "mensagem": "O corpo da requisição deve ser um JSON válido"
            }, ensure_ascii=False),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}", exc_info=True)
        return func.HttpResponse(
            json.dumps({
                "erro": "Erro interno",
                "mensagem": "Erro ao gerar cronograma"
            }, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )

def criar_cronograma(materias, dias_semana, horas_dia, prioridades):
    """
    Cria um cronograma distribuído de forma inteligente
    """
    dias_nomes = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    cronograma = []
    
    # Calcular peso de cada matéria
    pesos = {}
    for materia in materias:
        pesos[materia] = prioridades.get(materia, 1)
    
    total_peso = sum(pesos.values())
    
    # Distribuir horas
    for dia_idx in range(dias_semana):
        dia_nome = dias_nomes[dia_idx]
        sessoes = []
        horas_restantes = horas_dia
        
        # Distribuir matérias proporcionalmente
        for materia in materias:
            if horas_restantes <= 0:
                break
            
            # Calcular horas para esta matéria neste dia
            proporcao = pesos[materia] / total_peso
            horas_materia = max(0.5, min(horas_restantes, horas_dia * proporcao))
            
            # Arredondar para blocos de 30 min
            horas_materia = round(horas_materia * 2) / 2
            
            if horas_materia > 0:
                sessoes.append({
                    "materia": materia,
                    "duracao_horas": horas_materia,
                    "prioridade": pesos[materia],
                    "dica": gerar_dica_estudo(materia, horas_materia)
                })
                horas_restantes -= horas_materia
        
        cronograma.append({
            "dia": dia_nome,
            "sessoes": sessoes,
            "total_horas": sum(s["duracao_horas"] for s in sessoes)
        })
    
    return cronograma

def gerar_dica_estudo(materia, horas):
    """
    Gera dica personalizada baseada na matéria e duração
    """
    dicas_gerais = {
        "curta": "Sessão rápida: foco em revisão e exercícios",
        "media": "Tempo ideal para: teoria + prática + revisão",
        "longa": "Sessão extensa: aprofunde conceitos e faça muitos exercícios"
    }
    
    if horas <= 1:
        tipo = "curta"
    elif horas <= 2:
        tipo = "media"
    else:
        tipo = "longa"
    
    dica_base = dicas_gerais[tipo]
    
    # Dicas específicas por matéria
    dicas_especificas = {
        "matematica": "Use muitos exercícios práticos",
        "fisica": "Desenhe diagramas e esquemas",
        "quimica": "Revise reações e faça resumos",
        "historia": "Crie linhas do tempo",
        "portugues": "Leia e pratique redação",
        "biologia": "Use mapas mentais"
    }
    
    materia_lower = materia.lower()
    for key in dicas_especificas:
        if key in materia_lower:
            return f"{dica_base}. {dicas_especificas[key]}"
    
    return dica_base


def buscar_web_real(query: str, max_results: int = 5):
    """
    Busca real usando DuckDuckGo API + Wikipedia (100% grátis)
    Estratégia em camadas: DuckDuckGo → Wikipedia → Simulação
    """
    try:
        # Endpoint DuckDuckGo Instant Answer API
        url = "https://api.duckduckgo.com/"
        params = {
            'q': query,
            'format': 'json',
            'no_html': 1,
            'skip_disambig': 1
        }
        
        logging.info(f"Buscando em DuckDuckGo: {query}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        resultados = []
        
        # Processar Abstract (resposta principal)
        if data.get('Abstract'):
            resultados.append({
                "titulo": data.get('Heading', query),
                "descricao": data.get('Abstract', ''),
                "url": data.get('AbstractURL', ''),
                "fonte": data.get('AbstractSource', 'DuckDuckGo')
            })
        
        # Processar RelatedTopics (tópicos relacionados)
        for item in data.get('RelatedTopics', [])[:max_results]:
            if isinstance(item, dict) and 'Text' in item:
                resultados.append({
                    "titulo": item.get('Text', '').split(' - ')[0][:100],
                    "descricao": item.get('Text', ''),
                    "url": item.get('FirstURL', ''),
                    "fonte": "DuckDuckGo"
                })
        
        # Se não encontrou resultados, fazer busca alternativa
        if not resultados:
            logging.warning(f"DuckDuckGo sem resultados para: {query}")
            return buscar_wikipedia(query, max_results)
        
        logging.info(f"DuckDuckGo retornou {len(resultados)} resultados")
        return resultados[:max_results]
        
    except Exception as e:
        logging.error(f"Erro DuckDuckGo: {str(e)}")
        # Tentar Wikipedia como fallback
        return buscar_wikipedia(query, max_results)


def buscar_wikipedia(query: str, max_results: int = 5):
    """
    Busca na Wikipedia em português (fallback gratuito)
    """
    try:
        url = "https://pt.wikipedia.org/w/api.php"
        params = {
            'action': 'opensearch',
            'search': query,
            'limit': max_results,
            'format': 'json',
            'namespace': 0
        }
        
        # Headers necessários para evitar bloqueio 403
        headers = {
            'User-Agent': 'EstudaiBot/1.0 (Azure Function; Educational Purpose)'
        }
        
        logging.info(f"Buscando na Wikipedia: {query}")
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        resultados = []
        if len(data) >= 4:
            titulos = data[1]
            descricoes = data[2]
            urls = data[3]
            
            for i in range(min(len(titulos), max_results)):
                resultados.append({
                    "titulo": titulos[i],
                    "descricao": descricoes[i] if i < len(descricoes) else "",
                    "url": urls[i] if i < len(urls) else "",
                    "fonte": "Wikipedia"
                })
        
        # Se ainda não tem resultados, usar dados simulados
        if not resultados:
            logging.warning("Nenhum resultado encontrado, usando simulação")
            return simular_busca(query, max_results)
        
        logging.info(f"Wikipedia retornou {len(resultados)} resultados")
        return resultados
        
    except Exception as e:
        logging.error(f"Erro Wikipedia: {str(e)}")
        return simular_busca(query, max_results)


@lru_cache(maxsize=CACHE_SIZE)
def simular_busca(query: str, max_results: int):
    """
    Simula resultados de busca baseados em palavras-chave
    Em produção real, faria chamada à Bing Search API
    
    Cache: Resultados são cached para melhorar performance
    """
    logging.info(f'simular_busca chamada para: "{query}"')
    
    # Base de conhecimento simulada para diferentes tópicos de estudo
    base_conhecimento = {
        "matematica": [
            {
                "titulo": "Khan Academy - Matemática",
                "url": "https://pt.khanacademy.org/math",
                "snippet": "Aprenda matemática gratuitamente com vídeos e exercícios interativos"
            },
            {
                "titulo": "Técnicas de Estudo para Matemática",
                "url": "https://exemplo.com/tecnicas-matematica",
                "snippet": "Pratique regularmente, entenda conceitos ao invés de decorar fórmulas, refaça exercícios errados"
            },
            {
                "titulo": "Calculadora Científica Online",
                "url": "https://www.wolframalpha.com",
                "snippet": "Resolva equações e visualize gráficos com WolframAlpha"
            }
        ],
        "historia": [
            {
                "titulo": "Brasil Escola - História",
                "url": "https://brasilescola.uol.com.br/historia",
                "snippet": "Conteúdo completo de história do Brasil e história geral"
            },
            {
                "titulo": "Dicas para Estudar História",
                "url": "https://exemplo.com/dicas-historia",
                "snippet": "Crie linhas do tempo, conecte eventos causais, use mapas mentais"
            }
        ],
        "portugues": [
            {
                "titulo": "Português - Gramática e Literatura",
                "url": "https://exemplo.com/portugues",
                "snippet": "Guia completo de gramática, literatura e redação"
            },
            {
                "titulo": "Acordo Ortográfico - Guia Prático",
                "url": "https://exemplo.com/acordo-ortografico",
                "snippet": "Entenda as mudanças da reforma ortográfica com exemplos práticos"
            }
        ],
        "fisica": [
            {
                "titulo": "Física Interativa",
                "url": "https://phet.colorado.edu/pt_BR",
                "snippet": "Simulações interativas de física para facilitar o entendimento de conceitos"
            },
            {
                "titulo": "Fórmulas de Física - Guia Completo",
                "url": "https://exemplo.com/formulas-fisica",
                "snippet": "Principais fórmulas de mecânica, termodinâmica, eletromagnetismo e óptica"
            }
        ],
        "quimica": [
            {
                "titulo": "Tabela Periódica Interativa",
                "url": "https://ptable.com/pt",
                "snippet": "Explore elementos químicos com informações detalhadas e propriedades"
            },
            {
                "titulo": "Química Orgânica - Reações e Mecanismos",
                "url": "https://exemplo.com/quimica-organica",
                "snippet": "Guia completo de reações orgânicas, nomenclatura e mecanismos"
            }
        ],
        "biologia": [
            {
                "titulo": "Só Biologia - Conteúdo Completo",
                "url": "https://www.sobiologia.com.br",
                "snippet": "Citologia, genética, ecologia, evolução e fisiologia explicados"
            },
            {
                "titulo": "Atlas de Anatomia Humana",
                "url": "https://exemplo.com/anatomia",
                "snippet": "Ilustrações detalhadas dos sistemas do corpo humano"
            }
        ],
        "ingles": [
            {
                "titulo": "Duolingo - Aprenda Inglês Grátis",
                "url": "https://www.duolingo.com",
                "snippet": "Pratique inglês de forma gamificada e interativa"
            },
            {
                "titulo": "BBC Learning English",
                "url": "https://www.bbc.co.uk/learningenglish",
                "snippet": "Recursos gratuitos para melhorar gramática, vocabulário e pronúncia"
            }
        ],
        "redacao": [
            {
                "titulo": "Guia de Redação ENEM",
                "url": "https://exemplo.com/redacao-enem",
                "snippet": "Estrutura, competências, repertório sociocultural e temas frequentes"
            },
            {
                "titulo": "Banco de Redações Nota 1000",
                "url": "https://exemplo.com/redacoes-nota-1000",
                "snippet": "Exemplos comentados de redações que tiraram nota máxima"
            }
        ],
        "memorizar": [
            {
                "titulo": "Técnicas de Memorização - Palácio da Memória",
                "url": "https://exemplo.com/palacio-memoria",
                "snippet": "Use visualização espacial para memorizar grandes quantidades de informação"
            },
            {
                "titulo": "Flashcards Anki - Sistema de Repetição Espaçada",
                "url": "https://apps.ankiweb.net",
                "snippet": "Software gratuito que otimiza a retenção de longo prazo"
            },
            {
                "titulo": "Mnemônicos e Acrônimos para Estudos",
                "url": "https://exemplo.com/mnemonicos",
                "snippet": "Crie associações criativas para lembrar listas, fórmulas e conceitos"
            }
        ],
        "organizacao": [
            {
                "titulo": "Como Criar um Cronograma de Estudos Eficiente",
                "url": "https://exemplo.com/cronograma",
                "snippet": "Planeje horários fixos, intercale matérias e inclua pausas estratégicas"
            },
            {
                "titulo": "Notion para Estudantes",
                "url": "https://www.notion.so",
                "snippet": "Organize anotações, tarefas e projetos em um workspace digital"
            }
        ],
        "concentracao": [
            {
                "titulo": "Técnica Pomodoro - Estudo Focado",
                "url": "https://francescocirillo.com/pages/pomodoro-technique",
                "snippet": "Estude 25 minutos, descanse 5. Melhora foco e produtividade drasticamente"
            },
            {
                "titulo": "Como Evitar Distrações Durante o Estudo",
                "url": "https://exemplo.com/evitar-distracoes",
                "snippet": "Desligue notificações, use bloqueadores de sites e crie ambiente adequado"
            }
        ],
        "enem": [
            {
                "titulo": "Guia Completo do ENEM 2025",
                "url": "https://exemplo.com/enem-2025",
                "snippet": "Datas, conteúdo programático, dicas de estudo e simulados"
            },
            {
                "titulo": "Questões Comentadas ENEM",
                "url": "https://exemplo.com/questoes-enem",
                "snippet": "Resolução detalhada de provas anteriores por disciplina"
            }
        ],
        "vestibular": [
            {
                "titulo": "Estratégias para Vestibulares Concorridos",
                "url": "https://exemplo.com/vestibular-estrategias",
                "snippet": "Foco em editais específicos, provas anteriores e simulados cronometrados"
            }
        ]
    }
    
    # Detectar tema da query
    query_lower = query.lower()
    resultados = []
    
    # Mapeamento de palavras-chave para temas
    keywords_map = {
        "matematica": ["matematica", "calculo", "algebra", "geometria", "equacao"],
        "fisica": ["fisica", "mecanica", "termodinamica", "eletricidade", "optica"],
        "quimica": ["quimica", "reacao", "tabela periodica", "organica", "inorganica"],
        "biologia": ["biologia", "celula", "genetica", "ecologia", "anatomia"],
        "historia": ["historia", "historico", "guerra", "revolucao", "imperio"],
        "portugues": ["portugues", "gramatica", "literatura", "ortografia", "sintaxe"],
        "ingles": ["ingles", "english", "vocabulary", "grammar"],
        "redacao": ["redacao", "dissertacao", "texto", "enem redacao"],
        "memorizar": ["memorizar", "memoria", "decorar", "lembrar", "memorização"],
        "organizacao": ["organizar", "cronograma", "planejar", "rotina"],
        "concentracao": ["concentrar", "foco", "atencao", "pomodoro", "distracao"],
        "enem": ["enem", "exame nacional"],
        "vestibular": ["vestibular", "fuvest", "unicamp", "unesp"]
    }
    
    # Buscar temas relevantes
    temas_encontrados = []
    for tema, keywords in keywords_map.items():
        if any(kw in query_lower for kw in keywords):
            temas_encontrados.append(tema)
    
    # Se não encontrou tema específico, buscar por palavras gerais de estudo
    if not temas_encontrados:
        palavras_gerais = ["estudo", "estudar", "aprender", "tecnica", "dica", "ajuda"]
        if any(palavra in query_lower for palavra in palavras_gerais):
            # Retorna uma mistura de técnicas gerais
            temas_encontrados = ["memorizar", "concentracao", "organizacao"]
    
    # Coletar resultados dos temas encontrados
    for tema in temas_encontrados:
        if tema in base_conhecimento:
            resultados.extend(base_conhecimento[tema])
    
    # Se ainda não encontrou nada, retorna resultado genérico
    if not resultados:
        resultados = [
            {
                "titulo": f"Busca por: {query}",
                "url": "https://www.google.com/search?q=" + query.replace(" ", "+"),
                "snippet": f"Não encontrei recursos específicos sobre '{query}' na base de conhecimento educacional. Tente termos relacionados a matérias escolares ou técnicas de estudo."
            }
        ]
    
    # Limitar ao número máximo solicitado
    return resultados[:max_results]


@app.route(route="gerar-simulado", methods=["POST"])
def gerar_simulado(req: func.HttpRequest) -> func.HttpResponse:
    """
    Gera um simulado personalizado com questões de múltipla escolha
    """
    start_time = datetime.now()
    logging.info(f'[{start_time}] Função gerar-simulado acionada')
    
    try:
        req_body = req.get_json()
        
        # Validações
        materia = req_body.get('materia', '').strip()
        if not materia:
            return func.HttpResponse(
                json.dumps({
                    "erro": "Matéria não fornecida",
                    "mensagem": "Informe a matéria do simulado"
                }, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )
        
        num_questoes = req_body.get('num_questoes', 5)
        dificuldade = req_body.get('dificuldade', 'medio').lower()
        
        # Validar parâmetros
        if num_questoes < 1 or num_questoes > 20:
            return func.HttpResponse(
                json.dumps({
                    "erro": "Número de questões inválido",
                    "mensagem": "Escolha entre 1 e 20 questões"
                }, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )
        
        if dificuldade not in ['facil', 'medio', 'dificil']:
            dificuldade = 'medio'
        
        # Gerar questões
        questoes = criar_questoes(materia, num_questoes, dificuldade)
        
        # Calcular tempo estimado (2-3 min por questão)
        tempo_estimado = num_questoes * 2.5
        
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        logging.info(f'Simulado gerado: {materia}, {num_questoes} questões, {dificuldade} - {response_time:.2f}ms')
        
        return func.HttpResponse(
            json.dumps({
                "materia": materia,
                "dificuldade": dificuldade,
                "num_questoes": len(questoes),
                "tempo_estimado_minutos": tempo_estimado,
                "questoes": questoes,
                "instrucoes": "Leia cada questão com atenção. Marque apenas uma alternativa por questão.",
                "response_time_ms": round(response_time, 2)
            }, ensure_ascii=False),
            mimetype="application/json"
        )
        
    except ValueError as e:
        logging.error(f'Erro de validação: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "erro": "Dados inválidos",
                "mensagem": str(e)
            }, ensure_ascii=False),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f'Erro ao gerar simulado: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "erro": "Erro interno",
                "mensagem": "Não foi possível gerar o simulado"
            }, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="gerar-resumo", methods=["POST"])
def gerar_resumo(req: func.HttpRequest) -> func.HttpResponse:
    """
    Gera resumo estruturado de um tópico educacional
    """
    start_time = datetime.now()
    logging.info(f'[{start_time}] Função gerar-resumo acionada')
    
    try:
        req_body = req.get_json()
        
        # Validações
        topico = req_body.get('topico', '').strip()
        if not topico:
            return func.HttpResponse(
                json.dumps({
                    "erro": "Tópico não fornecido",
                    "mensagem": "Informe o tópico para resumir"
                }, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )
        
        materia = req_body.get('materia', '').strip()
        tipo = req_body.get('tipo', 'completo').lower()
        
        if tipo not in ['rapido', 'completo', 'detalhado']:
            tipo = 'completo'
        
        # Gerar resumo
        resumo = criar_resumo(topico, materia, tipo)
        
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        logging.info(f'Resumo gerado: {topico} ({tipo}) - {response_time:.2f}ms')
        
        return func.HttpResponse(
            json.dumps({
                "topico": topico,
                "materia": materia or "Geral",
                "tipo": tipo,
                "resumo": resumo,
                "response_time_ms": round(response_time, 2)
            }, ensure_ascii=False),
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f'Erro ao gerar resumo: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "erro": "Erro interno",
                "mensagem": "Não foi possível gerar o resumo"
            }, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="registrar-progresso", methods=["POST"])
def registrar_progresso(req: func.HttpRequest) -> func.HttpResponse:
    """
    Registra progresso de estudo do usuário
    """
    start_time = datetime.now()
    logging.info(f'[{start_time}] Função registrar-progresso acionada')
    
    try:
        req_body = req.get_json()
        
        # Validações
        usuario_id = req_body.get('usuario_id', 'default')
        materia = req_body.get('materia', '').strip()
        tempo_minutos = req_body.get('tempo_minutos', 0)
        topicos_estudados = req_body.get('topicos_estudados', [])
        
        if not materia:
            return func.HttpResponse(
                json.dumps({
                    "erro": "Matéria não fornecida"
                }, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )
        
        if tempo_minutos < 1:
            return func.HttpResponse(
                json.dumps({
                    "erro": "Tempo de estudo inválido"
                }, ensure_ascii=False),
                status_code=400,
                mimetype="application/json"
            )
        
        # Registrar progresso (simulado - em produção usaria banco de dados)
        progresso_registrado = {
            "usuario_id": usuario_id,
            "materia": materia,
            "tempo_minutos": tempo_minutos,
            "topicos_estudados": topicos_estudados,
            "data_registro": datetime.now().isoformat(),
            "status": "registrado"
        }
        
        # Calcular estatísticas
        horas_total = tempo_minutos / 60
        pontos_conquistados = calcular_pontos(tempo_minutos, len(topicos_estudados))
        
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        logging.info(f'Progresso registrado: {materia}, {tempo_minutos}min - {response_time:.2f}ms')
        
        return func.HttpResponse(
            json.dumps({
                "mensagem": "Progresso registrado com sucesso!",
                "progresso": progresso_registrado,
                "estatisticas": {
                    "horas_estudadas": round(horas_total, 2),
                    "topicos_concluidos": len(topicos_estudados),
                    "pontos_ganhos": pontos_conquistados
                },
                "motivacao": gerar_mensagem_motivacao(tempo_minutos),
                "response_time_ms": round(response_time, 2)
            }, ensure_ascii=False),
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f'Erro ao registrar progresso: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "erro": "Erro interno",
                "mensagem": "Não foi possível registrar o progresso"
            }, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )


@app.route(route="obter-dashboard", methods=["POST"])
def obter_dashboard(req: func.HttpRequest) -> func.HttpResponse:
    """
    Retorna dashboard com estatísticas de progresso
    """
    start_time = datetime.now()
    logging.info(f'[{start_time}] Função obter-dashboard acionada')
    
    try:
        req_body = req.get_json()
        usuario_id = req_body.get('usuario_id', 'default')
        periodo = req_body.get('periodo', 'semanal').lower()
        
        if periodo not in ['diario', 'semanal', 'mensal']:
            periodo = 'semanal'
        
        # Gerar dashboard (simulado - em produção viria do banco)
        dashboard = gerar_dashboard_demo(usuario_id, periodo)
        
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        logging.info(f'Dashboard gerado: {periodo} - {response_time:.2f}ms')
        
        return func.HttpResponse(
            json.dumps({
                "usuario_id": usuario_id,
                "periodo": periodo,
                "dashboard": dashboard,
                "response_time_ms": round(response_time, 2)
            }, ensure_ascii=False),
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f'Erro ao gerar dashboard: {str(e)}')
        return func.HttpResponse(
            json.dumps({
                "erro": "Erro interno",
                "mensagem": "Não foi possível gerar o dashboard"
            }, ensure_ascii=False),
            status_code=500,
            mimetype="application/json"
        )


# ============ FUNÇÕES AUXILIARES ============

def criar_questoes(materia: str, num_questoes: int, dificuldade: str) -> list:
    """Gera questões de múltipla escolha personalizadas"""
    
    # Base de questões por matéria
    questoes_base = {
        "matematica": [
            {
                "enunciado": "Qual é o valor de x na equação 2x + 5 = 15?",
                "alternativas": ["A) 3", "B) 5", "C) 7", "D) 10", "E) 15"],
                "resposta_correta": "B",
                "explicacao": "2x = 15 - 5 → 2x = 10 → x = 5",
                "dificuldade": "facil"
            },
            {
                "enunciado": "A área de um triângulo com base 8cm e altura 6cm é:",
                "alternativas": ["A) 14 cm²", "B) 24 cm²", "C) 28 cm²", "D) 48 cm²", "E) 56 cm²"],
                "resposta_correta": "B",
                "explicacao": "Área = (base × altura) / 2 = (8 × 6) / 2 = 24 cm²",
                "dificuldade": "medio"
            },
            {
                "enunciado": "Qual é a derivada de f(x) = 3x² + 2x - 1?",
                "alternativas": ["A) 6x + 2", "B) 3x + 2", "C) 6x - 1", "D) 3x² + 2", "E) 6x"],
                "resposta_correta": "A",
                "explicacao": "f'(x) = 6x + 2 (regra da potência)",
                "dificuldade": "dificil"
            }
        ],
        "fisica": [
            {
                "enunciado": "A fórmula da velocidade média é:",
                "alternativas": ["A) v = d/t", "B) v = t/d", "C) v = d×t", "D) v = a×t", "E) v = m×a"],
                "resposta_correta": "A",
                "explicacao": "Velocidade média = distância / tempo",
                "dificuldade": "facil"
            },
            {
                "enunciado": "Um corpo em queda livre acelera a aproximadamente:",
                "alternativas": ["A) 5 m/s²", "B) 9,8 m/s²", "C) 15 m/s²", "D) 20 m/s²", "E) 30 m/s²"],
                "resposta_correta": "B",
                "explicacao": "A aceleração da gravidade na Terra é aproximadamente 9,8 m/s²",
                "dificuldade": "medio"
            },
            {
                "enunciado": "A energia cinética é dada pela fórmula:",
                "alternativas": ["A) Ec = mv", "B) Ec = mv²", "C) Ec = mv²/2", "D) Ec = mgh", "E) Ec = ma"],
                "resposta_correta": "C",
                "explicacao": "Energia cinética = (massa × velocidade²) / 2",
                "dificuldade": "dificil"
            }
        ],
        "quimica": [
            {
                "enunciado": "Quantos prótons tem o átomo de Carbono (C)?",
                "alternativas": ["A) 4", "B) 6", "C) 8", "D) 12", "E) 14"],
                "resposta_correta": "B",
                "explicacao": "O número atômico do Carbono é 6, portanto tem 6 prótons",
                "dificuldade": "facil"
            },
            {
                "enunciado": "A fórmula da água é:",
                "alternativas": ["A) H₂O", "B) HO", "C) H₃O", "D) H₂O₂", "E) HO₂"],
                "resposta_correta": "A",
                "explicacao": "Água é formada por 2 átomos de Hidrogênio e 1 de Oxigênio",
                "dificuldade": "facil"
            },
            {
                "enunciado": "O pH neutro na escala de pH é:",
                "alternativas": ["A) 0", "B) 3", "C) 7", "D) 10", "E) 14"],
                "resposta_correta": "C",
                "explicacao": "pH 7 é neutro (nem ácido nem básico)",
                "dificuldade": "medio"
            }
        ],
        "biologia": [
            {
                "enunciado": "A menor unidade viva dos seres vivos é:",
                "alternativas": ["A) Molécula", "B) Célula", "C) Tecido", "D) Órgão", "E) Átomo"],
                "resposta_correta": "B",
                "explicacao": "A célula é a unidade básica da vida",
                "dificuldade": "facil"
            },
            {
                "enunciado": "A fotossíntese ocorre principalmente nas:",
                "alternativas": ["A) Raízes", "B) Flores", "C) Folhas", "D) Frutos", "E) Sementes"],
                "resposta_correta": "C",
                "explicacao": "As folhas contêm clorofila para realizar fotossíntese",
                "dificuldade": "medio"
            },
            {
                "enunciado": "O DNA é uma molécula de:",
                "alternativas": ["A) Proteína", "B) Lipídio", "C) Carboidrato", "D) Ácido nucleico", "E) Vitamina"],
                "resposta_correta": "D",
                "explicacao": "DNA (ácido desoxirribonucleico) é um ácido nucleico",
                "dificuldade": "medio"
            }
        ],
        "historia": [
            {
                "enunciado": "A Independência do Brasil ocorreu em:",
                "alternativas": ["A) 1500", "B) 1789", "C) 1822", "D) 1889", "E) 1922"],
                "resposta_correta": "C",
                "explicacao": "O Brasil declarou independência em 7 de setembro de 1822",
                "dificuldade": "facil"
            },
            {
                "enunciado": "A Revolução Francesa aconteceu no século:",
                "alternativas": ["A) XVI", "B) XVII", "C) XVIII", "D) XIX", "E) XX"],
                "resposta_correta": "C",
                "explicacao": "A Revolução Francesa começou em 1789 (século XVIII)",
                "dificuldade": "medio"
            }
        ],
        "portugues": [
            {
                "enunciado": "Qual é o plural de 'cidadão'?",
                "alternativas": ["A) cidadões", "B) cidadães", "C) cidadãos", "D) cidadans", "E) cidadaos"],
                "resposta_correta": "C",
                "explicacao": "Palavras terminadas em -ão podem fazer plural em -ãos",
                "dificuldade": "facil"
            },
            {
                "enunciado": "Qual frase está correta?",
                "alternativas": [
                    "A) Haviam muitas pessoas", 
                    "B) Havia muitas pessoas", 
                    "C) Houveram muitas pessoas",
                    "D) Houve muitas pessoas",
                    "E) Ambas B e D"
                ],
                "resposta_correta": "E",
                "explicacao": "O verbo 'haver' no sentido de existir é impessoal (singular)",
                "dificuldade": "medio"
            }
        ]
    }
    
    # Buscar questões da matéria
    materia_lower = materia.lower()
    questoes_disponiveis = []
    
    for mat_key in questoes_base.keys():
        if mat_key in materia_lower or materia_lower in mat_key:
            questoes_disponiveis = questoes_base[mat_key]
            break
    
    # Se não encontrou questões específicas, criar questões genéricas
    if not questoes_disponiveis:
        questoes_disponiveis = [
            {
                "enunciado": f"Questão sobre {materia} - Em desenvolvimento",
                "alternativas": ["A) Opção 1", "B) Opção 2", "C) Opção 3", "D) Opção 4", "E) Opção 5"],
                "resposta_correta": "A",
                "explicacao": "Esta é uma questão de exemplo para a matéria solicitada",
                "dificuldade": dificuldade
            }
        ] * 5
    
    # Filtrar por dificuldade se possível
    questoes_filtradas = [q for q in questoes_disponiveis if q.get('dificuldade') == dificuldade]
    if not questoes_filtradas:
        questoes_filtradas = questoes_disponiveis
    
    # Selecionar questões (repetindo se necessário para atingir num_questoes)
    questoes_selecionadas = []
    import random
    
    # Garantir que sempre temos questões suficientes
    while len(questoes_selecionadas) < num_questoes:
        questao = random.choice(questoes_filtradas).copy()
        questao['numero'] = len(questoes_selecionadas) + 1
        questoes_selecionadas.append(questao)
    
    return questoes_selecionadas


def criar_resumo(topico: str, materia: str, tipo: str) -> dict:
    """Gera resumo estruturado de um tópico"""
    
    resumos_base = {
        "fotossintese": {
            "conceito": "Processo pelo qual plantas convertem luz solar em energia química",
            "pontos_principais": [
                "Ocorre nos cloroplastos das células vegetais",
                "Equação: 6CO₂ + 6H₂O + luz → C₆H₁₂O₆ + 6O₂",
                "Libera oxigênio para a atmosfera",
                "Fase clara e fase escura (Ciclo de Calvin)"
            ],
            "palavras_chave": ["clorofila", "luz", "glicose", "oxigênio", "CO₂"],
            "dica_memorizacao": "Lembre-se: Luz + CO₂ + Água = Glicose + O₂"
        },
        "segunda guerra": {
            "conceito": "Conflito global entre 1939-1945 envolvendo Aliados vs Eixo",
            "pontos_principais": [
                "Causas: Tratado de Versalhes, crise econômica, totalitarismo",
                "Principais países: Alemanha, Itália, Japão (Eixo) vs EUA, Reino Unido, URSS (Aliados)",
                "Eventos importantes: Pearl Harbor, Dia D, Bombas atômicas",
                "Consequências: ONU, Guerra Fria, descolonização"
            ],
            "palavras_chave": ["Hitler", "nazismo", "holocausto", "aliados", "eixo"],
            "dica_memorizacao": "1939-1945: Eixo (A-I-J) vs Aliados (EUA-UK-URSS)"
        }
    }
    
    # Buscar resumo específico ou criar genérico
    topico_lower = topico.lower()
    resumo_encontrado = None
    
    for key in resumos_base.keys():
        if key in topico_lower or topico_lower in key:
            resumo_encontrado = resumos_base[key]
            break
    
    if not resumo_encontrado:
        # Criar resumo genérico
        resumo_encontrado = {
            "conceito": f"Resumo sobre: {topico}",
            "pontos_principais": [
                "Definição e contexto do tópico",
                "Principais características",
                "Aplicações e importância",
                "Relações com outros conceitos"
            ],
            "palavras_chave": [topico],
            "dica_memorizacao": f"Revise {topico} regularmente para fixar o conteúdo"
        }
    
    # Ajustar conteúdo baseado no tipo
    if tipo == 'rapido':
        return {
            "conceito": resumo_encontrado["conceito"],
            "pontos_principais": resumo_encontrado["pontos_principais"][:2],
            "palavras_chave": resumo_encontrado["palavras_chave"][:3]
        }
    elif tipo == 'completo':
        return resumo_encontrado
    else:  # detalhado
        resumo_encontrado["mapa_mental"] = {
            "centro": topico,
            "ramificacoes": resumo_encontrado["palavras_chave"]
        }
        resumo_encontrado["tecnicas_estudo"] = [
            "Faça mapas mentais visuais",
            "Crie flashcards com os pontos principais",
            "Explique o conceito para outra pessoa",
            "Resolva exercícios práticos"
        ]
        return resumo_encontrado


def calcular_pontos(tempo_minutos: int, num_topicos: int) -> int:
    """Calcula pontos de gamificação baseado no estudo"""
    pontos_base = tempo_minutos * 2  # 2 pontos por minuto
    bonus_topicos = num_topicos * 10  # 10 pontos por tópico concluído
    return pontos_base + bonus_topicos


def gerar_mensagem_motivacao(tempo_minutos: int) -> str:
    """Gera mensagem motivacional baseada no tempo estudado"""
    if tempo_minutos < 30:
        return "Bom começo! Continue assim! 📚"
    elif tempo_minutos < 60:
        return "Ótimo ritmo de estudos! Você está no caminho certo! 🌟"
    elif tempo_minutos < 120:
        return "Incrível! Mais de 1 hora de foco! Seu esforço vai valer a pena! 🚀"
    else:
        return "WOW! Dedicação impressionante! Você é um exemplo de persistência! 🏆"


def gerar_dashboard_demo(usuario_id: str, periodo: str) -> dict:
    """Gera dashboard de demonstração com estatísticas"""
    
    # Dados simulados (em produção viriam do banco de dados)
    import random
    
    if periodo == 'diario':
        total_horas = round(random.uniform(1, 4), 1)
        materias_estudadas = random.randint(2, 4)
        dias_consecutivos = random.randint(1, 7)
    elif periodo == 'semanal':
        total_horas = round(random.uniform(8, 20), 1)
        materias_estudadas = random.randint(4, 8)
        dias_consecutivos = random.randint(3, 7)
    else:  # mensal
        total_horas = round(random.uniform(30, 80), 1)
        materias_estudadas = random.randint(6, 12)
        dias_consecutivos = random.randint(10, 30)
    
    return {
        "estatisticas_gerais": {
            "total_horas_estudadas": total_horas,
            "materias_diferentes": materias_estudadas,
            "dias_consecutivos": dias_consecutivos,
            "media_horas_dia": round(total_horas / max(dias_consecutivos, 1), 1)
        },
        "distribuicao_materias": {
            "Matematica": round(total_horas * 0.25, 1),
            "Fisica": round(total_horas * 0.20, 1),
            "Quimica": round(total_horas * 0.15, 1),
            "Biologia": round(total_horas * 0.15, 1),
            "Historia": round(total_horas * 0.10, 1),
            "Portugues": round(total_horas * 0.15, 1)
        },
        "progresso_semanal": [
            {"dia": "Seg", "horas": round(random.uniform(1, 3), 1)},
            {"dia": "Ter", "horas": round(random.uniform(1, 3), 1)},
            {"dia": "Qua", "horas": round(random.uniform(1, 3), 1)},
            {"dia": "Qui", "horas": round(random.uniform(1, 3), 1)},
            {"dia": "Sex", "horas": round(random.uniform(1, 3), 1)},
            {"dia": "Sab", "horas": round(random.uniform(2, 4), 1)},
            {"dia": "Dom", "horas": round(random.uniform(1, 2), 1)}
        ],
        "conquistas": [
            {
                "nome": "Estudante Dedicado",
                "descricao": f"Estudou por {dias_consecutivos} dias consecutivos",
                "icone": "🔥",
                "desbloqueado": dias_consecutivos >= 5
            },
            {
                "nome": "Maratonista",
                "descricao": "Estudou mais de 3 horas em um dia",
                "icone": "🏃",
                "desbloqueado": periodo != 'diario' or total_horas > 3
            },
            {
                "nome": "Multitask",
                "descricao": "Estudou 5 ou mais matérias diferentes",
                "icone": "🎯",
                "desbloqueado": materias_estudadas >= 5
            }
        ],
        "recomendacoes": [
            "Continue mantendo a consistência nos estudos",
            "Tente aumentar o tempo em matérias com menor dedicação",
            "Faça pausas regulares para melhor absorção",
            "Revise conteúdos antigos para fixação"
        ],
        "meta_semanal": {
            "horas_objetivo": 20,
            "horas_atual": total_horas if periodo == 'semanal' else random.randint(8, 15),
            "percentual_atingido": round((total_horas / 20) * 100, 1) if periodo == 'semanal' else random.randint(40, 75)
        }
    }
