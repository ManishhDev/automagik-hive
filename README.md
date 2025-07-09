# Sistema Multi-Agente PagBank

Sistema sofisticado de atendimento ao cliente multi-agente desenvolvido com o framework Agno, projetado especificamente para as necessidades do mercado brasileiro do PagBank.

## 🚀 Início Rápido

### Método 1: Interface Web Moderna (Recomendado)

```bash
# 1. Inicie o backend do sistema PagBank
uv run python playground.py

# 2. Em outro terminal, inicie a interface web
cd agent-ui
pnpm install
pnpm dev
```

A interface web estará disponível em: http://localhost:3000  
O backend estará disponível em: http://localhost:7777

### Método 2: Playground Básico do Agno

```bash
# Execute apenas o demo do Agno Playground (interface básica)
uv run python playground.py
```

## 📋 Visão Geral do Sistema

O Sistema Multi-Agente PagBank utiliza orquestração avançada de IA para fornecer atendimento ao cliente inteligente em cinco domínios especializados:

### Times Especialistas
- **Time de Cartões** 💳 - Problemas com cartões de crédito/débito, limites, faturas
- **Time de Conta Digital** 🏦 - PIX, transferências, saldo, extratos
- **Time de Investimentos** 💰 - CDB, produtos de investimento, compliance
- **Time de Crédito** 💸 - Empréstimos, FGTS, proteção contra fraudes
- **Time de Seguros** 🛡️ - Produtos de seguro, sinistros, coberturas

### Recursos Principais
- 🇧🇷 Suporte nativo ao português brasileiro com correção de erros de digitação
- 🚨 Detecção avançada de fraudes e prevenção de golpes
- 😤 Detecção de frustração e escalação para atendimento humano
- 🧠 Memória persistente e reconhecimento de padrões
- 📚 Filtragem de conhecimento específico por time
- ⚡ Otimização de tempo de resposta <2s

### Interface Web Moderna
- 💬 **Interface de Chat Moderna**: Design limpo com suporte a streaming em tempo real
- 🧩 **Suporte a Chamadas de Ferramentas**: Visualiza chamadas de ferramentas do agente e seus resultados
- 🧠 **Etapas de Raciocínio**: Exibe o processo de raciocínio do agente (quando disponível)
- 📚 **Suporte a Referências**: Mostra fontes utilizadas pelo agente
- 🖼️ **Suporte Multimodal**: Lida com vários tipos de conteúdo, incluindo imagens, vídeo e áudio
- 🎨 **UI Personalizável**: Construída com Tailwind CSS para facilitar estilização

## 🏗️ Arquitetura

### Visão Geral do Sistema

```mermaid
graph TB
    UI[🌐 Interface Web<br/>Next.js + TypeScript] --> API[🔄 API Playground<br/>FastAPI]
    API --> ORCH[🎯 Orquestrador Principal<br/>Modo Route]
    
    ORCH --> PREP[📝 Pré-processamento]
    PREP --> NORM[🔧 Normalização de Texto]
    PREP --> FRUST[😤 Detecção de Frustração]
    PREP --> ROUT[🎯 Lógica de Roteamento]
    
    ORCH --> MEM[🧠 Gerenciamento de Memória]
    MEM --> SQLITE[(🗄️ SQLite<br/>Sessões & Padrões)]
    
    ORCH --> TEAMS[👥 Times Especialistas]
    TEAMS --> CARDS[💳 Time de Cartões]
    TEAMS --> ACCOUNT[🏦 Time de Conta Digital]
    TEAMS --> INVEST[💰 Time de Investimentos]
    TEAMS --> CREDIT[💸 Time de Crédito]
    TEAMS --> INSUR[🛡️ Time de Seguros]
    
    ORCH --> ESC[⚠️ Sistemas de Escalação]
    ESC --> HUMAN[👤 Escalação Humana]
    ESC --> TECH[🔧 Escalação Técnica]
    ESC --> TICK[🎫 Sistema de Tickets]
    
    TEAMS --> KB[📚 Base de Conhecimento<br/>CSV + Filtros]
    KB --> VECTOR[(🎯 Embeddings<br/>Similaridade Vetorial)]
    
    style UI fill:#e1f5fe
    style ORCH fill:#fff3e0
    style TEAMS fill:#f3e5f5
    style ESC fill:#ffebee
    style KB fill:#e8f5e8
```

### Fluxo de Processamento de Mensagens

```mermaid
sequenceDiagram
    participant U as 👤 Cliente
    participant UI as 🌐 Interface Web
    participant O as 🎯 Orquestrador
    participant P as 📝 Pré-processamento
    participant T as 👥 Time Especialista
    participant M as 🧠 Memória
    participant E as ⚠️ Escalação
    
    U->>UI: Mensagem do cliente
    UI->>O: Requisição HTTP
    O->>P: Processa mensagem
    P->>P: Normaliza texto
    P->>P: Detecta frustração
    P->>P: Determina roteamento
    
    alt Frustração alta
        P->>E: Escala para humano
        E->>UI: Resposta de escalação
    else Roteamento normal
        O->>T: Direciona para time
        T->>M: Consulta contexto
        M-->>T: Retorna histórico
        T->>T: Processa com conhecimento
        T->>O: Resposta especializada
    end
    
    O->>M: Atualiza memória
    O->>UI: Resposta final
    UI->>U: Exibe resposta
```

## 🛠️ Stack Técnico

### Backend
- **Framework**: Agno (Orquestração Multi-Agente)
- **LLM**: Claude Sonnet 4 (claude-sonnet-4-20250514)
- **Base de Conhecimento**: CSV com embeddings PgVector
- **Memória**: Agno Memory v2 com SqliteMemoryDb
- **Linguagem**: Python 3.12+
- **Armazenamento**: SQLite para sessões e memória

### Frontend (Interface Web)
- **Framework**: Next.js 15 com App Router
- **Linguagem**: TypeScript
- **Estilização**: Tailwind CSS
- **Componentes**: shadcn/ui + Radix UI
- **Animações**: Framer Motion
- **Gerenciamento Estado**: Zustand
- **Renderização Markdown**: react-markdown

## 📁 Estrutura do Projeto

```
pagbank/
├── agent-ui/             # Interface web moderna (Next.js + TypeScript)
│   ├── src/
│   │   ├── app/                   # Páginas da aplicação Next.js
│   │   ├── components/            # Componentes React
│   │   │   ├── playground/        # Interface do playground
│   │   │   │   ├── ChatArea/      # Área de chat
│   │   │   │   └── Sidebar/       # Barra lateral
│   │   │   └── ui/                # Componentes UI reutilizáveis
│   │   ├── hooks/                 # Hooks React customizados
│   │   ├── lib/                   # Utilitários e configurações
│   │   └── types/                 # Definições TypeScript
│   ├── package.json              # Dependências Node.js
│   └── tailwind.config.ts        # Configuração Tailwind CSS
├── orchestrator/          # Roteamento e orquestração principal
│   ├── main_orchestrator.py       # Orquestrador principal
│   ├── routing_logic.py           # Lógica de roteamento
│   ├── frustration_detector.py    # Detector de frustração
│   ├── text_normalizer.py         # Normalizador de texto
│   ├── clarification_handler.py   # Manipulador de esclarecimentos
│   └── state_synchronizer.py      # Sincronizador de estado
├── teams/                 # Implementações dos times especialistas
│   ├── base_team.py              # Classe base dos times
│   ├── cards_team.py             # Time de cartões
│   ├── digital_account_team.py   # Time de conta digital
│   ├── investments_team.py       # Time de investimentos
│   ├── credit_team.py            # Time de crédito
│   ├── insurance_team.py         # Time de seguros
│   └── team_tools.py             # Ferramentas compartilhadas
├── knowledge/            # Base de conhecimento e filtragem
│   ├── csv_knowledge_base.py     # Base de conhecimento CSV
│   ├── agentic_filters.py        # Filtros agênticos
│   └── pagbank_knowledge.csv     # Dados de conhecimento
├── memory/               # Memória e detecção de padrões
│   ├── memory_manager.py         # Gerenciador de memória
│   ├── pattern_detector.py       # Detector de padrões
│   └── session_manager.py        # Gerenciador de sessões
├── escalation_systems/   # Escalação humana e técnica
│   ├── escalation_manager.py     # Gerenciador de escalação
│   ├── technical_escalation_agent.py  # Agente escalação técnica
│   ├── ticket_system.py          # Sistema de tickets
│   └── feedback_human_systems/   # Sistemas de feedback humano
├── config/               # Configuração e definições
│   ├── settings.py               # Configurações principais
│   ├── models.py                 # Modelos de dados
│   └── database.py               # Configuração do banco
├── utils/                # Utilitários e formatadores
├── data/                 # Dados de sessão e memória
├── tests/                # Testes unitários e integração
├── playground.py         # Demo do Agno Playground
└── docs/                 # Documentação
    ├── DEMO_SCRIPT.md            # Scripts de demonstração completos
    ├── DEMO_INSTRUCTIONS.md      # Instruções de demo
    └── DEVELOPMENT_GUIDELINES.md # Diretrizes de desenvolvimento
```

## 🔧 Configuração

Configurações principais em `config/settings.py`:
- Timeout de roteamento de time: 30s
- Máximo de turnos de conversa: 20
- Limite de frustração: Nível 3
- Timeout de sessão: 30 minutos

## 🔒 Recursos de Segurança

- Detecção de golpes de antecipação de pagamentos
- Proteção de clientes vulneráveis
- Reconhecimento de padrões de fraude
- Avisos de compliance para investimentos
- Manuseio seguro de credenciais

## 🧠 Sistema de Memória

- **Memória Persistente**: Contexto do usuário mantido entre sessões
- **Detecção de Padrões**: Reconhecimento de comportamentos recorrentes
- **Insights Contextuais**: Análise de histórico de interações
- **Sincronização de Estado**: Coordenação entre times especialistas

## 🎯 Recursos Avançados

- **Normalização de Texto**: Correção automática de erros de português
- **Detecção de Frustração**: Identificação de sinais de insatisfação
- **Esclarecimentos Inteligentes**: Perguntas contextuais para consultas ambíguas
- **Escalação Automática**: Transferência para atendimento humano quando necessário
- **Filtragem de Conhecimento**: Acesso específico por domínio de especialização

## 👥 Equipe

Desenvolvido com o Framework Agno pelas equipes **Namastex Labs** e **Yaitech**

## 📝 Licença

Proprietário - PagBank 2025