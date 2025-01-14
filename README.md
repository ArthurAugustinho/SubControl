
# SubControl

Projeto feito com python puro com interface no prompt, com o intuito de organizar os gastos com assinaturas mensais onde você pode **adicionar** assinatura, **remover** assinaturas, **visualizar** o valor gasto mensalmente e nos **ultimos 12 meses**, e marcar como **pago** a assinatura.

## Deploy
Logo apos criar e ativar seu ambiente virtual **(venv)** rode o seguintes comandos para instalar as dependencias do codigo:

```bash
  pip install -r requirements.txt
```
 
Apos isto rode este comando para criar as tabelas do banco de dados:

```bash
  python .\models\database.py
```
 
E por fim execulte este comando para entrar na interface e usar a aplicação:

```bash
  python .\templates\app.py
```
 
## Autor

- [ArthurAugustinho] - (https://github.com/ArthurAugustinho)