# 📑 GCS Automation: Terraform + Python + Docker

Este repositório contém uma solução de **Infraestrutura efêmera** para jobs de dados no Google Cloud Platform (GCS). O objetivo é provisionar um bucket, executar um script Python de ingestão e permitir o descomissionamento da infraestrutura de forma isolada e segura.

---

## 🚀 Arquitetura da Solução

O projeto utiliza o conceito de "Infraestrutura Just-in-Time" encapsulada em um ambiente imutável:

1.  **Orquestração:** Um script `entrypoint.sh` coordena o ciclo de vida.
2.  **IaC:** O Terraform provisiona o Bucket GCS.
3.  **App:** O Python executa a lógica de negócio (upload de dados).
4.  **Isolamento:** Docker garante que todas as ferramentas (TF, Python, Cloud SDK) funcionem em qualquer máquina.



---

## 🛠️ Estrutura de Arquivos

* `main.tf`: Configuração dos recursos GCP.
* `script.py`: Script Python para manipulação de dados no GCS.
* `Dockerfile`: Definição da imagem com Terraform + Python.
* `entrypoint.sh`: Maestro do container (TF Apply -> Python Run).
* `requirements.txt`: Dependências do SDK do Google Cloud.

---

## 🏁 Como Executar

### 1. Pré-requisitos
Certifique-se de ter o Docker instalado e estar autenticado no GCP localmente:
```bash
gcloud auth application-default login