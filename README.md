# 📅 AgendaFácil - API de Agendamento Acadêmico

Uma API RESTful desenvolvida para facilitar a reserva de auditórios e salas de aula, prevenindo conflitos de horários e organizando eventos acadêmicos.

## 🚀 Sobre o Projeto

Este projeto foi desenvolvido em equipe como parte da disciplina de Linguagem de Programação. O objetivo foi criar uma aplicação modularizada utilizando **Flask**, sem o uso de bancos de dados tradicionais (SQL), realizando toda a persistência de dados através da manipulação de arquivos **CSV**.

## ✨ Funcionalidades

- **Autenticação:** Cadastro e Login de usuários (Professores/Coordenadores).
- **Gestão de Espaços:** CRUD de salas e auditórios.
- **Gestão de Eventos:** Criação de eventos acadêmicos.
- **Reservas Inteligentes:** Sistema que impede agendamento duplicado no mesmo horário/local.
- **Documentação:** Swagger UI (OpenAPI) integrado automaticamente.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Framework:** Flask
- **Extensões:**
  - `Flask-Smorest` (Rotas e Documentação)
  - `Marshmallow` (Validação de Schemas)
  - `Flask-MethodView` (Organização de classes)
- **Persistência:** Arquivos CSV (manipulação nativa)

## 📦 Como Rodar o Projeto

1. Clone o repositório:
   ```bash
   git clone [https://github.com/seu-usuario/agenda-facil.git](https://github.com/seu-usuario/agenda-facil.git)
