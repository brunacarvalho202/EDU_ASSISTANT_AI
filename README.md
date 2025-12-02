# 📚 EDU ASSISTANT AI: Seu Chatbot de Estudo Pessoal

Bem-vindo ao repositório do **EDU ASSISTANT AI**, um assistente estudantil inteligente desenvolvido para otimizar sua jornada de aprendizado. Este projeto é um chatbot interativo que utiliza o poder do **Gemini LLM (Large Language Model)** para fornecer respostas, explicações e suporte de estudo em tempo real.

---

## 🛠️ Tecnologias Utilizadas

### Backend e Linguagem
* **Python:** Linguagem principal do projeto.
* **Google Gemini API:** O modelo de linguagem grande (LLM) que alimenta a inteligência do chatbot.
* **FastAPI:** Framework moderno e rápido para construir a API.
* **Streamlit:** Biblioteca para criar a interface de usuário web.

### Infraestrutura e DevOps (AWS)
* **AWS Secrets Manager:** Utilizado para armazenar e gerenciar a chave de API de forma segura.
* **AWS ECR (Elastic Container Registry):** Repositório para armazenar a imagem Docker da aplicação.
* **AWS ECS (Elastic Container Service):** Serviço de orquestração de containers para executar e gerenciar a aplicação na internet.
* **Docker:** Para conteinerização da aplicação.
* **Pipeline CI/CD (GitHub Actions/AWS):** Para automação da construção, teste e implantação da aplicação.

## ⚙️ Fluxo do Pipeline CI/CD

O processo de Integração Contínua e Entrega Contínua (CI/CD) é estruturado em um fluxo robusto que envolve três *branches* principais: `main`, `dev` e `staging`.

| Branch | Propósito | Gatilho do Pipeline |
| :--- | :--- | :--- |
| `dev` | Desenvolvimento e testes iniciais de novas funcionalidades. | **Commit** (Executa testes unitários/integração) |
| `staging` | Ambiente de pré-produção para revisão e aprovação final. | **Merge/Pull Request** de `dev` |
| `main` | Código pronto para produção e responsável pelo deploy final. | **Pull Request Aprovado** de `staging` |

### Detalhamento do Fluxo

1.  **Início em `dev`:** O fluxo se inicia com um *commit* na *branch* `dev`. O pipeline executa automaticamente todos os testes (unitários e de integração).
2.  **Transição para `staging`:** Se os testes passarem, o código pode ser movido para a *branch* `staging`.
3.  **Revisão e Aprovação:** Na `staging`, o código é revisado. A aprovação final para o deploy na infraestrutura de produção é feita através de um **Pull Request (PR) aprovado** para a *branch* `main`.
4.  **Deploy em `main`:** O *merge* do PR para a `main` desencadeia o *workflow* final, que inclui:
    * Construção da imagem Docker.
    * Upload da imagem para o **AWS ECR**.
    * Atualização do serviço no **AWS ECS** (deploy na infraestrutura da AWS).
