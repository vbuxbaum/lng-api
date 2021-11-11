# slack-writing-feedbacks

Integração com Slack para feedbacks sobre uso de termos específicos, que são indesejáveis no Workspace

# Instruções

## Como alterar / criar feedbacks

### Alterando o texto padrão

No arquivo `data/feedbacks.json` temos 3 pedaços de texto dentro da seção `"default_text"`, que representam a estrutura base da mensagem que o robô envia quando dá um feedback:
- `intro`: Pequena saudação marcando (`<@<user_id>>`) a pessoa que escreveu a mensagem original, e citando (`<found_word>`) a expressão que foi usada indevidamente
- `explanation`: Pequeno início para o parágrafo (`<feedback>`) que explica a motivação do feedback àquela expressão.
- `goodbye`: Finalização da mensagem

Cada uma dessas partes da mensagem será, por padrão, separada por 1 linha em branco na mensagem final.

Para alterar esses textos, basta alterar o arquivo tendo cuidado para manter a formatação padrão do JSON. Faça suas alterações, nomeie e conclua o commit criando uma nova branch. Prossiga criando o Pull Request, e aguarde que sua sugestão seja revisada pelo time responsável.

### Criando / Alterando um feedback

No arquivo `data/feedbacks.json` temos a seção `"feedbacks"` que é a relação `expressão a ser evitada` <> `feedback para a expressão, quando usada`.

No exemplo abaixo, as expressões `denegrir`, `denegrindo` e `denegriu` terão o mesmo texto de feedback (representado por `denegrir`), e a expressão `os estudantes` terá outro texto de feedback (representado por `os_estudantes`).

```json
"feedbacks": {
    "denegrir": "denegrir.slack",
    "denegrindo": "denegrir.slack",
    "denegriu": "denegrir.slack",
    "os estudantes": "os_estudantes.slack"
}
```

Os termos `os_estudantes.slack` e `denegrir.slack` fazem referência aos arquivos `data/os_estudantes.slack` e `data/denegrir.slack`, que armazenam o texto que será usado como feedback na resposta do robô.

O texto nos arquivos com final `.slack` podem conter [formatação](https://api.slack.com/reference/surfaces/formatting) como negrito, itálico, emojis, links, etc.

Para alterar esses textos, você precisa:
- alterar a seção `"feedbacks"` no arquivo `data/feedbacks.json`, tendo cuidado para manter a formatação padrão do JSON.
- alterar / criar o arquivo com final `.slack` correspondente

Faça suas alterações, nomeie e conclua o commit criando uma nova branch. Prossiga criando o Pull Request, e aguarde que sua sugestão seja revisada pelo time responsável.

## Como rodar localmente

### Tokens de acesso no Slack

Para que a aplicação consiga (mesmo rodando localmente) enviar mensagens para o Slack, é necessário 2 tokens de acesso: `SLACK_BOT_TOKEN` e `SLACK_SIGNING_SECRET`

Procure uma das pessoas colaboradoras do projeto para obter esses Tokens.

### Rodando a aplicação
> Requisito: Python versão 3.6 ou mais recente

Crie um ambiente virtual utilizando o módulo [venv](https://docs.python.org/pt-br/3/library/venv.html)

```bash
python3 -m venv .venv-swf
```

Ative o ambiente virtual criado

```bash
source .venv-swf/bin/activate
```

Instale as dependências

```bash
pip install -r dev-requirements
```

Para testar a função `listen_messages` (responsável por escutar as mensagens do Slack):

```bash
python3 -i app.py
 * Serving Flask app 'app' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:3000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 322-576-941
 |
```

Nesse momento o REPL (terminal interativo do Python) foi aberto. Aperte `ctrl+C` para cancelar a execução do app, mas sem sair do terminal do Python.

Você verá o indicativo `>>>` para inserir um comando do Python, e então poderá utilizar o comando abaixo. 
- Substitua `SEU_USER_ID` pelo seu [ID de usuário do Slack](https://www.workast.com/help/articles/61000165203/) entre aspas. 
- Substitua `SUA_MENSAGEM` pelo texto da mensagem que gostaria de testar.

```python
>>> listen_messages({"event":{"user": SEU_USER_ID, "text": SUA_MENSAGEM}})
```


