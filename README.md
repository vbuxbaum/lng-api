# slack-writing-feedbacks

Integração com Slack para feedbacks sobre uso de termos específicos, que são indesejáveis no Workspace

# Instruções

## Requisitos

Python versão 3.6 ou mais recente

## Como rodar localmente

Crie um ambiente virtual utilizando o módulo [venv](https://docs.python.org/pt-br/3/library/venv.html)

```bash
python3 -m venv .venv-swf
```

Ative o ambiente virtual criados para

```bash
source .venv-swf/bin/activate
```

Instale as dependências

```bash
pip install -r dev-requirements
```

Instale o [NGROK](https://ngrok.com/download)