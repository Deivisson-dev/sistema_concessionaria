# Sistema para Concessionária 🚗

Projeto acadêmico desenvolvido com Django, Docker e PostgreSQL. O sistema é responsável por gerenciar operações relacionadas a uma concessionária.


## 🚀 Começando

### Pré-requisitos
- [Docker](https://docs.docker.com/engine/install/) 
- [Docker Compose](https://docs.docker.com/compose/install/) 
- [Git](https://git-scm.com/)

### 📥 Instalação
1. Clone o repositório:
```bash
git clone https://github.com/Deivisson-dev/sistema_concessionaria.git
cd sistema_concessionaria
```

2. Configure as variáveis de ambiente:
```bash
touch .env
```

3. Inicie os containers:
```bash
 docker compose up -d --build
```

4. Execute as migrations:
```bash
  docker compose exec web python app/manage.py migrate
```

5. (Opcional) Crie um superusuário:
```bash
  docker compose exec web python app/manage.py createsuperuser
```
