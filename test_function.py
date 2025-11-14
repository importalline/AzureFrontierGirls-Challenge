"""
Testes unitários para a Azure Function de busca educacional
"""
import pytest
import json
from function_app import (
    simular_busca, 
    criar_questoes, 
    criar_resumo, 
    calcular_pontos, 
    gerar_mensagem_motivacao,
    gerar_dashboard_demo
)


class TestSimularBusca:
    """Testes para a função de simulação de busca"""
    
    def test_busca_matematica(self):
        """Testa busca por matemática retorna resultados corretos"""
        resultado = simular_busca("matematica", 3)
        
        assert len(resultado) <= 3
        assert len(resultado) > 0
        assert any("matemática" in r["titulo"].lower() or "math" in r["titulo"].lower() 
                   for r in resultado)
    
    def test_busca_fisica(self):
        """Testa busca por física"""
        resultado = simular_busca("fisica", 2)
        
        assert len(resultado) <= 2
        assert len(resultado) > 0
        assert any("física" in r["snippet"].lower() or "fís" in r["titulo"].lower() 
                   for r in resultado)
    
    def test_busca_enem(self):
        """Testa busca sobre ENEM"""
        resultado = simular_busca("dicas para o ENEM", 5)
        
        assert len(resultado) > 0
        assert all(isinstance(r, dict) for r in resultado)
        assert all("titulo" in r and "url" in r and "snippet" in r for r in resultado)
    
    def test_busca_memorizar(self):
        """Testa busca por técnicas de memorização"""
        resultado = simular_busca("como memorizar melhor", 3)
        
        assert len(resultado) > 0
        assert any("memor" in r["titulo"].lower() or "memor" in r["snippet"].lower() 
                   for r in resultado)
    
    def test_busca_concentracao(self):
        """Testa busca sobre concentração"""
        resultado = simular_busca("melhorar foco e concentracao", 2)
        
        assert len(resultado) > 0
        assert any("pomodoro" in r["titulo"].lower() or "concentra" in r["snippet"].lower() 
                   or "foco" in r["snippet"].lower() for r in resultado)
    
    def test_busca_termo_desconhecido(self):
        """Testa busca com termo não mapeado retorna resultado genérico"""
        resultado = simular_busca("xyzabc123desconhecido", 1)
        
        assert len(resultado) > 0
        assert "titulo" in resultado[0]
        assert "url" in resultado[0]
        assert "snippet" in resultado[0]
    
    def test_max_results_respeitado(self):
        """Testa que o limite de resultados é respeitado"""
        resultado = simular_busca("matematica", 2)
        assert len(resultado) <= 2
        
        resultado = simular_busca("estudo", 1)
        assert len(resultado) <= 1
    
    def test_estrutura_resultado(self):
        """Testa que cada resultado tem a estrutura correta"""
        resultado = simular_busca("portugues", 3)
        
        for r in resultado:
            assert isinstance(r, dict)
            assert "titulo" in r
            assert "url" in r
            assert "snippet" in r
            assert isinstance(r["titulo"], str)
            assert isinstance(r["url"], str)
            assert isinstance(r["snippet"], str)
            assert len(r["titulo"]) > 0
            assert len(r["url"]) > 0
            assert len(r["snippet"]) > 0
    
    def test_busca_multiplos_temas(self):
        """Testa busca que pode retornar múltiplos temas"""
        resultado = simular_busca("tecnicas de estudo para vestibular", 5)
        
        assert len(resultado) > 0
        # Pode retornar tanto técnicas gerais quanto dicas de vestibular


class TestIntegracaoCompleta:
    """Testes de integração simulando uso real"""
    
    def test_fluxo_estudante_matematica(self):
        """Simula estudante buscando recursos de matemática"""
        queries = [
            "preciso estudar matematica",
            "calculo",
            "algebra"
        ]
        
        for query in queries:
            resultado = simular_busca(query, 3)
            assert len(resultado) > 0
    
    def test_fluxo_preparacao_enem(self):
        """Simula estudante se preparando para ENEM"""
        queries = [
            "enem",
            "redacao enem",
            "cronograma de estudos"
        ]
        
        for query in queries:
            resultado = simular_busca(query, 5)
            assert len(resultado) > 0
    
    def test_diferentes_max_results(self):
        """Testa diferentes valores de max_results"""
        for max_r in [1, 2, 3, 5, 10]:
            resultado = simular_busca("historia", max_r)
            assert len(resultado) <= max_r


class TestCasosEspeciais:
    """Testes para casos especiais e edge cases"""
    
    def test_query_vazia_segura(self):
        """Testa que query vazia é tratada sem erro"""
        resultado = simular_busca("", 5)
        assert isinstance(resultado, list)
    
    def test_query_com_acentos(self):
        """Testa queries com acentuação portuguesa"""
        queries = [
            "técnicas de memorização",
            "física quântica",
            "redação dissertativa"
        ]
        
        for query in queries:
            resultado = simular_busca(query, 3)
            assert len(resultado) > 0
    
    def test_query_maiusculas(self):
        """Testa que busca é case-insensitive"""
        resultado_lower = simular_busca("matematica", 3)
        resultado_upper = simular_busca("MATEMATICA", 3)
        resultado_mixed = simular_busca("MaTeMaTiCa", 3)
        
        assert len(resultado_lower) > 0
        assert len(resultado_upper) > 0
        assert len(resultado_mixed) > 0


class TestGeradorSimulados:
    """Testes para o gerador de simulados"""
    
    def test_criar_questoes_matematica(self):
        """Testa criação de questões de matemática"""
        questoes = criar_questoes("matematica", 5, "medio")
        
        assert len(questoes) == 5
        assert all(isinstance(q, dict) for q in questoes)
        assert all("enunciado" in q for q in questoes)
        assert all("alternativas" in q for q in questoes)
        assert all("resposta_correta" in q for q in questoes)
    
    def test_criar_questoes_fisica(self):
        """Testa criação de questões de física"""
        questoes = criar_questoes("fisica", 3, "facil")
        
        assert len(questoes) == 3
        assert all(len(q["alternativas"]) == 5 for q in questoes)
        assert all(q["resposta_correta"] in ["A", "B", "C", "D", "E"] for q in questoes)
    
    def test_criar_questoes_dificuldade(self):
        """Testa diferentes níveis de dificuldade"""
        for dificuldade in ["facil", "medio", "dificil"]:
            questoes = criar_questoes("quimica", 2, dificuldade)
            assert len(questoes) == 2
    
    def test_criar_questoes_materia_generica(self):
        """Testa criação de questões para matéria não específica"""
        questoes = criar_questoes("Filosofia", 3, "medio")
        
        assert len(questoes) == 3
        assert all("enunciado" in q for q in questoes)
    
    def test_numero_questoes_variavel(self):
        """Testa diferentes quantidades de questões"""
        for num in [1, 3, 5, 10]:
            questoes = criar_questoes("biologia", num, "medio")
            assert len(questoes) == num
    
    def test_questoes_numeradas(self):
        """Testa que questões são numeradas corretamente"""
        questoes = criar_questoes("historia", 5, "facil")
        
        for i, questao in enumerate(questoes, 1):
            assert questao["numero"] == i


class TestGeradorResumos:
    """Testes para o gerador de resumos"""
    
    def test_criar_resumo_basico(self):
        """Testa criação de resumo básico"""
        resumo = criar_resumo("fotossintese", "biologia", "completo")
        
        assert "conceito" in resumo
        assert "pontos_principais" in resumo
        assert "palavras_chave" in resumo
        assert isinstance(resumo["pontos_principais"], list)
    
    def test_criar_resumo_rapido(self):
        """Testa resumo rápido (menos detalhado)"""
        resumo = criar_resumo("segunda guerra", "historia", "rapido")
        
        assert "conceito" in resumo
        assert len(resumo["pontos_principais"]) <= 2
        assert len(resumo["palavras_chave"]) <= 3
    
    def test_criar_resumo_detalhado(self):
        """Testa resumo detalhado (mais completo)"""
        resumo = criar_resumo("fotossintese", "biologia", "detalhado")
        
        assert "mapa_mental" in resumo
        assert "tecnicas_estudo" in resumo
        assert len(resumo["tecnicas_estudo"]) > 0
    
    def test_criar_resumo_generico(self):
        """Testa criação de resumo para tópico não específico"""
        resumo = criar_resumo("Teoria da Relatividade", "fisica", "completo")
        
        assert "conceito" in resumo
        assert "pontos_principais" in resumo
    
    def test_tipos_resumo(self):
        """Testa todos os tipos de resumo"""
        for tipo in ["rapido", "completo", "detalhado"]:
            resumo = criar_resumo("teste", "", tipo)
            assert isinstance(resumo, dict)


class TestDashboardProgresso:
    """Testes para o sistema de progresso e dashboard"""
    
    def test_calcular_pontos_basico(self):
        """Testa cálculo de pontos"""
        pontos = calcular_pontos(30, 2)  # 30 min, 2 tópicos
        
        assert pontos > 0
        assert pontos == (30 * 2) + (2 * 10)  # 60 + 20 = 80
    
    def test_calcular_pontos_variavel(self):
        """Testa pontos com diferentes tempos"""
        pontos_curto = calcular_pontos(15, 1)
        pontos_longo = calcular_pontos(60, 5)
        
        assert pontos_longo > pontos_curto
    
    def test_mensagem_motivacao_variavel(self):
        """Testa mensagens motivacionais baseadas no tempo"""
        msg_curta = gerar_mensagem_motivacao(20)
        msg_media = gerar_mensagem_motivacao(45)
        msg_longa = gerar_mensagem_motivacao(90)
        msg_muito_longa = gerar_mensagem_motivacao(150)
        
        assert isinstance(msg_curta, str)
        assert isinstance(msg_media, str)
        assert isinstance(msg_longa, str)
        assert isinstance(msg_muito_longa, str)
        assert len(msg_curta) > 0
    
    def test_gerar_dashboard_diario(self):
        """Testa geração de dashboard diário"""
        dashboard = gerar_dashboard_demo("usuario1", "diario")
        
        assert "estatisticas_gerais" in dashboard
        assert "distribuicao_materias" in dashboard
        assert "conquistas" in dashboard
        assert "recomendacoes" in dashboard
    
    def test_gerar_dashboard_semanal(self):
        """Testa geração de dashboard semanal"""
        dashboard = gerar_dashboard_demo("usuario1", "semanal")
        
        assert dashboard["estatisticas_gerais"]["total_horas_estudadas"] > 0
        assert len(dashboard["progresso_semanal"]) == 7
    
    def test_gerar_dashboard_mensal(self):
        """Testa geração de dashboard mensal"""
        dashboard = gerar_dashboard_demo("usuario1", "mensal")
        
        assert "meta_semanal" in dashboard
        assert dashboard["estatisticas_gerais"]["materias_diferentes"] > 0
    
    def test_dashboard_conquistas(self):
        """Testa sistema de conquistas"""
        dashboard = gerar_dashboard_demo("usuario1", "semanal")
        conquistas = dashboard["conquistas"]
        
        assert len(conquistas) > 0
        assert all("nome" in c for c in conquistas)
        assert all("descricao" in c for c in conquistas)
        assert all("desbloqueado" in c for c in conquistas)
    
    def test_dashboard_distribuicao_materias(self):
        """Testa distribuição de horas por matéria"""
        dashboard = gerar_dashboard_demo("usuario1", "semanal")
        distribuicao = dashboard["distribuicao_materias"]
        
        assert len(distribuicao) > 0
        assert all(isinstance(v, float) for v in distribuicao.values())


class TestIntegracaoNovasFuncoes:
    """Testes de integração para as novas funcionalidades"""
    
    def test_fluxo_completo_estudo(self):
        """Testa fluxo completo: busca → resumo → simulado → progresso"""
        # 1. Buscar material
        resultados_busca = simular_busca("matematica", 3)
        assert len(resultados_busca) > 0
        
        # 2. Criar resumo
        resumo = criar_resumo("equacoes", "matematica", "completo")
        assert "conceito" in resumo
        
        # 3. Gerar simulado
        questoes = criar_questoes("matematica", 5, "medio")
        assert len(questoes) == 5
        
        # 4. Calcular progresso
        pontos = calcular_pontos(60, 3)  # 1 hora, 3 tópicos
        assert pontos > 0
    
    def test_preparacao_prova(self):
        """Simula estudante se preparando para prova"""
        # Buscar conteúdo
        conteudo = simular_busca("fisica mecanica", 5)
        assert len(conteudo) > 0
        
        # Fazer resumo
        resumo = criar_resumo("leis de newton", "fisica", "detalhado")
        assert "mapa_mental" in resumo
        
        # Treinar com simulado
        simulado = criar_questoes("fisica", 10, "medio")
        assert len(simulado) == 10
        
        # Ver progresso
        dashboard = gerar_dashboard_demo("estudante", "semanal")
        assert "estatisticas_gerais" in dashboard
    
    def test_diferentes_materias_integradas(self):
        """Testa integração com várias matérias"""
        materias = ["matematica", "fisica", "quimica", "biologia"]
        
        for materia in materias:
            # Busca, resumo e simulado para cada matéria
            busca = simular_busca(materia, 2)
            resumo = criar_resumo(materia, materia, "rapido")
            questoes = criar_questoes(materia, 3, "facil")
            
            assert len(busca) > 0
            assert "conceito" in resumo
            assert len(questoes) == 3
