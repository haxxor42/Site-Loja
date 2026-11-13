# NexusCore - Sistema de Gerenciamento de Estoque (CRUD Genérico)

Sistema web completo em Python (Flask) e SQLite para controle e gestão de estoque de qualquer tipo de produto ou mercadoria.

## Funcionalidades do CRUD de Estoque

1. **Create (Cadastrar Produto)**:
   - Formulário completo para cadastrar qualquer produto: Nome, Preço Unitário (R$), Quantidade em Estoque e Descrição/Observações.
   - Acesso: `/loja/cadastrar` ou pelo botão "+ Cadastrar Novo Produto".

2. **Read (Painel e Consulta de Estoque)**:
   - Dashboard com KPIs em tempo real:
     - Total de Produtos Cadastrados
     - Unidades Físicas em Estoque
     - Valor Total Acumulado do Estoque (R$)
     - Alerta de Produtos Críticos / Esgotados
   - Tabela gerencial de produtos com pesquisa/filtro por nome ou descrição.
   - Status visual automático do estoque (Normal, Baixo, Esgotado).
   - Acesso: `/loja/` ou `/produtos`.

3. **Update (Editar e Movimentar Estoque)**:
   - **Edição Completa**: Tela dedicada para alterar nome, valor, quantidade e especificações (`/loja/editar/<id>`).
   - **Movimentação Rápida**: Botões diretos de entrada (`+`) e saída (`-`) de unidades na própria tabela.

4. **Delete (Excluir Produto)**:
   - Exclusão segura de itens com diálogo de confirmação.

5. **Módulo de Usuários**:
   - Autenticação e Login (`/login`)
   - Cadastro de Usuários (`/cadastro`)
   - Visualização e edição de perfil (`/user/dados`)

## Como Executar

```bash
cd BackEndmes06
python app.py
```
Ou dê dois cliques no arquivo `iniciar_site.bat` na raiz do projeto.
Acesse pelo navegador em: `http://127.0.0.1:5000`.
