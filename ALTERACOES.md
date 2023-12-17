## 🚀 Alterações na API para Melhorias de Segurança e Funcionalidade

### 1️⃣ Incrementos no Modelo de Dados

#### 1.1 📝 Campos de Auditoria
- **Objetivo:** Rastreabilidade e manutenção facilitada.
- **Implementação:** Adicionados `created_at` e `updated_at` em `User`.
  ```python
  created_at = fields.DatetimeField(auto_now_add=True)
  updated_at = fields.DatetimeField(auto_now=True)

#### 1.2 🏥 Modelo 'Plano' e Relacionamento com 'User'
- **Objetivo:** Gerenciar planos de saúde e associar usuários.
- **Implementação:** `Plano` para detalhes dos planos e `plano` em `User` para o vínculo.
  ```python
  class Plano(Model):
      # Detalhes do Plano
  class User(Model):
      plano = fields.ForeignKeyField('models.Plano', related_name='usuarios', null=True)

#### 1.3 🆔 Campo Único 'cpf' em 'User'
- **Objetivo:** Garantir que cada usuário tenha um CPF único.
- **Implementação:** Inclusão do campo `cpf` no modelo `User`, definido como único para evitar duplicatas.
  ```python
  cpf = fields.CharField(max_length=11, unique=True, null=False)

Este trecho destaca a importância do campo `cpf` como identificador único para cada usuário.
#### 1.4 🛠 Melhorias no Endpoint e Validação de Senha

- **Validação de Senha:**
  - **Objetivo:** Aumentar a segurança das contas dos usuários.
  - **Implementação:** Adicionei uma função no arquivo `validacao.py` para checar a complexidade das senhas, incluindo comprimento, uso de letras maiúsculas, minúsculas, números e símbolos especiais.
  - **Resultado:** Senhas que não atendem aos critérios são rejeitadas, aumentando a segurança da aplicação.

- **Endpoint `/health-check`:**
  - **Objetivo:** Verificar a saúde e disponibilidade da API.
  - **Implementação:** Adicionei um endpoint que retorna o status operacional da API, sem a necessidade de autenticação.
  - **Detalhes:**
    ```python
    @router.get("/health-check", status_code=status.HTTP_200_OK)
    async def health_check() -> dict:
        return {"status": "API operacional"}
    ```
  - **Benefício:** Essa funcionalidade é útil para monitoramento e garantia de que a API está funcionando corretamente.

- **Endpoint para Escolha de Plano de Saúde:**
  - **Objetivo:** Permitir que os usuários escolham ou alterem seus planos de saúde.
  - **Implementação:** Adicionei um endpoint que permite aos usuários associar um plano de saúde ao seu perfil.
  - **Detalhes:**
    ```python
    @router.post('/escolher-plano/{username}')
    async def escolher_plano(username: str, nome_plano: str):
        
    ```
  - **Impacto:** Facilita aos usuários a personalização e escolha de planos de saúde, melhorando a experiência do usuário.

### 📊 Resumo
As atualizações implementadas visam reforçar a segurança, a eficiência e a capacidade de personalização da API. 


