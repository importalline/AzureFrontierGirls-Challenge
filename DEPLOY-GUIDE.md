

5. **Testar uma função nova:**

```powershell
# Teste rápido do simulado
$url = "https://func-estudai-search-web-etbyaefhe7brateb.eastus2-01.azurewebsites.net/api/gerar-simulado"
$body = '{"materia": "Matematica", "num_questoes": 3, "dificuldade": "facil"}'
Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType "application/json; charset=utf-8" | ConvertTo-Json -Depth 10
```

Se retornar 3 questões de matemática → **DEPLOY OK!** ✅

---

## PASSO 2: Atualizar OpenAPI no AI Foundry

1. **Acesse o AI Foundry:**
   - Vá para: https://ai.azure.com
   - Abra seu projeto com o agente "Estudaí"

2. **Remover a ação antiga:**
   - Vá em: **Agent** → **Actions**
   - Localize a ação "PesquisaWeb" (versão 1.0.0)
   - Clique em: **Delete** ou **Remove**

3. **Adicionar a nova versão:**
   - Clique em: **Add Action**
   - Selecione: **OpenAPI**
   - Faça upload do arquivo: `C:\AzureFrontierGirls-Challenge\azure-function\openapi-ai-foundry.json`
   - **Authentication**: Selecione **Anonymous**
   - Clique em: **Save** / **Add**

4. **Verificar as 5 operações:**
   - Após salvar, você deve ver:
     - ✅ buscarWeb
     - ✅ gerarCronograma
     - ✅ gerarSimulado (NOVA)
     - ✅ gerarResumo (NOVA)
     - ✅ registrarProgresso (NOVA)
     - ✅ obterDashboard (NOVA)

---

## PASSO 3: Testar Todas as Funções no Playground

### 1. Teste de Busca Web

```
Você: Me busque recursos sobre técnicas de memorização para ENEM
```

Espera-se: Agente usa `buscarWeb` e retorna 5 resultados

### 2. Teste de Cronograma

```
Você: Crie um cronograma de 5 dias com Matemática, Física e Química, 3 horas por dia
```

Espera-se: Agente usa `gerarCronograma` e retorna cronograma semanal

### 3. Teste de Simulado (NOVO)

```
Você: Gere um simulado de 5 questões de Física, nível médio
```

Espera-se: Agente usa `gerarSimulado` e retorna 5 questões com alternativas

### 4. Teste de Resumo (NOVO)

```
Você: Me faça um resumo detalhado sobre fotossíntese
```

Espera-se: Agente usa `gerarResumo` e retorna resumo estruturado com mapa mental

### 5. Teste de Dashboard (NOVO)

```
Você: Mostre meu dashboard de progresso semanal
```

Espera-se: Agente usa `obterDashboard` e retorna estatísticas, conquistas e gráficos

### 6. Teste de Progresso (NOVO)

```
Você: Registre que estudei Matemática por 90 minutos, tópicos: equações e funções
```

Espera-se: Agente usa `registrarProgresso` e retorna pontos ganhos e mensagem motivacional

---

## PASSO 4: Capturar Screenshots

### Lista de Screenshots Necessários:

1. **01-ai-foundry-project.png**
   - Tela inicial do projeto no AI Foundry

2. **02-agent-overview.png**
   - Visão geral do agente "Estudaí"

3. **03-agent-tools.png**
   - Seção Tools mostrando as 3 ferramentas habilitadas

4. **04-code-interpreter.png**
   - Code Interpreter habilitado

5. **05-file-search.png**
   - File Search com arquivo `dicas-de-estudo.txt`

6. **06-openapi-actions.png**
   - OpenAPI Actions mostrando as 5 operações

7. **07-test-buscar.png**
   - Playground testando busca web

8. **08-test-cronograma.png**
   - Playground testando cronograma

9. **09-test-simulado.png**
   - Playground testando simulado (NOVO)

10. **10-test-resumo.png**
    - Playground testando resumo (NOVO)

11. **11-test-dashboard.png**
    - Playground testando dashboard (NOVO)

12. **12-azure-function-app.png**
    - Azure Portal mostrando o Function App

13. **13-functions-list.png**
    - Lista das 5 funções deployadas

14. **14-tests-passing.png**
    - Terminal mostrando 37 testes passando

15. **15-vscode-project.png**
    - VS Code com estrutura do projeto

### Como Capturar:

1. Use **Win + Shift + S** para capturar tela
2. Salve em: `C:\AzureFrontierGirls-Challenge\screenshots\`
3. Nomeie como indicado acima

---

## PASSO 5: Criar Repositório GitHub

1. **Criar novo repositório:**
   - Vá para: https://github.com/new
   - Nome: `AzureFrontierGirls-Challenge`
   - Descrição: "Assistente inteligente de estudos - Azure Frontier Girls Challenge 2024"
   - Visibilidade: **Public** ✅
   - Inicialize com: README (desmarque, vamos fazer upload do nosso)
   - Clique em: **Create repository**

2. **Preparar arquivos para upload:**

Estrutura que você vai fazer upload:

```
AzureFrontierGirls-Challenge/
├── azure-function/
│   ├── function_app.py
│   ├── test_function.py
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── host.json
│   ├── .funcignore
│   ├── openapi-ai-foundry.json
│   └── README.md
├── docs/
│   └── dicas-de-estudo.txt
├── screenshots/
│   ├── 01-ai-foundry-project.png
│   ├── 02-agent-overview.png
│   ├── ... (todas as 15 screenshots)
├── .gitignore
└── README.md (root)
```

4. **Upload via GitHub Desktop (FÁCIL) ou Git CLI:**

**Opção A: GitHub Desktop (Recomendado se não tem Git configurado)**
- Baixe: https://desktop.github.com/
- Clone o repositório que você criou
- Copie todos os arquivos para a pasta clonada
- Commit → Push

**Opção B: Git CLI**

```powershell
cd C:\AzureFrontierGirls-Challenge

git init
git add .
git commit -m "Initial commit: Estudaí - Assistente inteligente de estudos"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/AzureFrontierGirls-Challenge.git
git push -u origin main
```

5. **Verificar no GitHub:**
   - Acesse seu repositório
   - Verifique se README.md está sendo exibido
   - Confira se todas as pastas estão lá

---

## PASSO 6: Finalizar o Projeto

1. **Revisar checklist:**
   - ✅ Agente funcionando com 3 ferramentas (Code Interpreter, File Search, OpenAPI)
   - ✅ 5 funções Azure deployadas e testadas
   - ✅ 37 testes automatizados passando
   - ✅ Screenshots capturados
   - ✅ README completo
   - ✅ Repositório GitHub público

