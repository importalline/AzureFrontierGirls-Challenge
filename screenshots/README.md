# 📸 Screenshots - Estudaí

Este diretório contém capturas de tela demonstrando o funcionamento do projeto **Estudaí** para o Azure Frontier Girls Challenge 2024.

---

## 📋 Checklist de Screenshots Necessários

### 1. ✅ Configuração do Agente no AI Foundry
**Arquivo:** `ai-foundry-agent-config.png`

**O que capturar:**
- Tela do Azure AI Foundry mostrando o agente "Estudaí"
- 3 ferramentas habilitadas visíveis:
  - ✅ Code Interpreter
  - ✅ File Search
  - ✅ OpenAPI Actions
- Instruções customizadas no campo "Instructions"

**Como capturar:**
1. Acesse https://ai.azure.com
2. Abra seu projeto
3. Vá em "Agents" → "Estudaí"
4. Capture a tela mostrando as ferramentas ativas
5. Salve como `ai-foundry-agent-config.png`

---

### 2. ✅ Busca Web Funcionando
**Arquivo:** `busca-web-fotossintese.png`

**O que capturar:**
- Playground do AI Foundry
- Pergunta: "Me busque recursos sobre fotossíntese"
- Resposta do agente mostrando:
  - Lista de 5 artigos Wikipedia
  - Links clicáveis
  - Snippets dos artigos
  - Indicação de que usou a função `buscarWeb`

**Como capturar:**
1. No Playground do agente
2. Digite: "Me busque recursos sobre fotossíntese"
3. Aguarde a resposta completa
4. Capture mostrando a lista de resultados
5. Salve como `busca-web-fotossintese.png`

---

### 3. ✅ Cronograma Gerado
**Arquivo:** `cronograma-gerado.png`

**O que capturar:**
- Conversa no Playground
- Pergunta: "Crie um cronograma de estudos para Matemática, Física e Química. Tenho 3 horas por dia, de segunda a sexta."
- Resposta mostrando:
  - Cronograma semanal formatado
  - Distribuição de matérias por dia
  - Horários e durações
  - Total de horas calculado

**Como capturar:**
1. No Playground
2. Digite o prompt de cronograma
3. Capture a resposta completa
4. Salve como `cronograma-gerado.png`

---

### 4. ✅ Simulado ENEM-Style
**Arquivo:** `simulado-matematica.png`

**O que capturar:**
- Conversa no Playground
- Pergunta: "Gere um simulado de Matemática com 3 questões fáceis"
- Resposta mostrando:
  - Questões numeradas
  - Alternativas A, B, C, D, E
  - Gabarito indicado
  - Explicações das respostas

**Como capturar:**
1. No Playground
2. Digite o prompt de simulado
3. Capture as questões geradas
4. Salve como `simulado-matematica.png`

---

### 5. ✅ Dashboard Gamificado
**Arquivo:** `dashboard-progresso.png`

**O que capturar:**
- Conversa no Playground
- Pergunta: "Mostre meu progresso de estudos"
- Resposta mostrando:
  - Pontuação total
  - Conquistas desbloqueadas (🔥 Dedicado, 🎯 Multitask, etc.)
  - Estatísticas de estudo
  - Horas totais e aproveitamento

**Como capturar:**
1. No Playground
2. Digite: "Mostre meu progresso"
3. Capture o dashboard formatado
4. Salve como `dashboard-progresso.png`

---

### 6. ✅ Testes Automatizados Passando
**Arquivo:** `testes-37-passing.png`

**O que capturar:**
- Terminal/PowerShell
- Comando executado: `python -m pytest test_function.py -v`
- Resultado mostrando:
  - 37 testes executados
  - Todos PASSED (verde)
  - Tempo de execução (~1.47s)
  - Mensagem final: "37 passed"

**Como capturar:**
1. Abra PowerShell no diretório do projeto
2. Execute: `python -m pytest test_function.py -v`
3. Capture a saída completa
4. Salve como `testes-37-passing.png`

---

### 7. ✅ Azure Functions Deployadas
**Arquivo:** `azure-functions-deployed.png`

**O que capturar:**
- Azure Portal
- Function App aberta
- Lista de 5 funções visíveis:
  - buscar
  - gerar-cronograma
  - gerar-simulado
  - gerar-resumo
  - registrar-progresso
  - obter-dashboard
- Status: "Running"

**Como capturar:**
1. Acesse https://portal.azure.com
2. Abra seu Function App
3. Vá em "Functions"
4. Capture a lista completa
5. Salve como `azure-functions-deployed.png`

---

### 8. ✅ OpenAPI Spec Configurada
**Arquivo:** `openapi-actions-configured.png`

**O que capturar:**
- AI Foundry
- Seção "OpenAPI Actions"
- Arquivo `openapi-ai-foundry.json` carregado
- Lista de 6 operações visíveis:
  - buscarWeb
  - gerarCronograma
  - gerarSimulado
  - gerarResumo
  - registrarProgresso
  - obterDashboard

**Como capturar:**
1. No AI Foundry, aba do agente
2. Vá em "Tools" → "OpenAPI Actions"
3. Capture a lista de operações
4. Salve como `openapi-actions-configured.png`

---

## 🎯 Dica para Capturas de Tela:

- **Ferramenta:** Use Windows Snipping Tool (Win + Shift + S)
- **Resolução:** PNG de alta qualidade
- **Tamanho:** Máximo 2MB por imagem
- **Enquadramento:** Inclua contexto suficiente (URL, nome do projeto)
- **Texto legível:** Zoom adequado para leitura

---

## ✅ Checklist de Conclusão:

- [ ] 8 screenshots capturados
- [ ] Todos salvos nesta pasta (`screenshots/`)
- [ ] Nomes de arquivo corretos (sem espaços)
- [ ] README principal atualizado com links para as imagens
- [ ] Repositório pronto para submissão

---

**Prazo de entrega:** 21/11/2025 às 23:59

**Última atualização:** 13/11/2025
