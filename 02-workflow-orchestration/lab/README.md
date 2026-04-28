# Pipeline de Ingestão de Dados de Movimentação Aeroportuária (ANAC) ✈️
Este projeto utiliza o Kestra para orquestrar um pipeline de dados (ETL) que extrai informações de movimentação aeroportuária da API de Dados Abertos da ANAC, realiza o tratamento de dados e os carrega de forma resiliente em um banco de dados PostgreSQL.

### 🚀 Tecnologias Utilizadas
- Orquestrador: Kestra (Declarativo em YAML)

- Banco de Dados: PostgreSQL

- Linguagem de Manipulação: SQL (PostgreSQL Dialect) e Shell Script

- Fonte de Dados: ANAC (Sistemas de Dados Abertos)

### 🏗️ Arquitetura do Pipeline
O workflow foi desenhado seguindo as melhores práticas de engenharia de dados, dividido em camadas:

1. Ingestão (Extract): Download dinâmico do CSV baseado nos inputs de year e month.

2. Staging Area: Os dados brutos são carregados em uma tabela intermediária (movimentacao_aeroportuaria_staging) com todos os campos como TEXT para evitar falhas de carga.

3. Limpeza e Transformação (Transform):  Criação de uma View de Limpeza (vw_movimentacao_aeroportuaria_limpa) que realiza o cast de tipos (Date, Time, Numeric).

    - Tratamento de valores nulos e strings inconsistentes.

    - Geração de um id_movimento único via Hash MD5 para garantir a unicidade.

4. Carga Final (Load): Utilização do comando MERGE (Upsert) para garantir a idempotência do pipeline, atualizando registros existentes e inserindo novos.

### 📊 Visualização do Fluxo
Grafo gerado automaticamente pelo Kestra demonstrando a sequência de tasks e logs de auditoria.

### 🛠️ Como Executar
Pré-requisitos
- Instância do Kestra rodando (Docker recomendado).

- Banco de Dados PostgreSQL acessível.

- Variáveis de ambiente (KV Store no Kestra) configuradas:

- POSTGRES_USERNAME

- POSTGRES_PASSWORD

Instalação
1. Crie um novo Flow no seu painel do Kestra.

2. Copie e cole o conteúdo do arquivo pipeline_flight_anac.yaml.

3. Execute o workflow selecionando o mês e ano desejados nos inputs.

### 🧠 Destaques Técnicos
- Idempotência: O pipeline pode ser executado múltiplas vezes para o mesmo período sem gerar duplicidade de dados.

- Resiliência: A separação entre Staging e Production permite que erros de tipagem no arquivo da ANAC não quebrem a tabela final de análise.

- Auditoria: Cada linha inserida contém a data de ingestão (dh_ingestao) e o nome do arquivo de origem (nome_arquivo).