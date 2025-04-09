# Py-Agent-Voice

Py-Agent-Voice é um projeto baseado em Python para lidar com interações entre humano e agente de I.A. permitindo a leitura e análise de dados de um arquivo CSV.

## Funcionalidades

- Análise de dados
- Reconhecimento e transcrição de voz
- Interação por voz com Agente de I.A.

## Instalação

```bash
git clone https://github.com/estevan-ulian/py-agent-voice.git
cd py-agent-voice
pip install -r requirements.txt
```

## Uso
- Crie um arquivo nomeado como `.env` e insira sua chave `OPENAI_API_KEY`. Acesse [OpenAI API Keys](https://platform.openai.com/settings/organization/api-keys) para obter sua chave de API.
- Insira seu arquivo CSV no diretório `datasets`.
- Acesse o arquivo `app.py`, vá até a linha 124, onde a classe TalkingLLM é instanciada e defina o nome do seu arquivo CSV. Por padrão é utilizado o arquivo `df_rent.csv` como exemplo.
- Execute o script principal para iniciar a aplicação:
```bash
python app.py
```
- Aguarde a inicialização.
- Pressione `<caps_lock>` para iniciar a gravação do seu áudio.
- Faça sua pergunta e pressione `<caps_lock>` novamente para parar a gravação.
- O agente irá processar sua pergunta e gerar uma resposta.
- O áudio da resposta será reproduzido automaticamente.
- Aguarde a conclusão do agente para fazer uma nova pergunta.

Você pode alterar a tecla de gravação na instância da classe TalkingLLM alterando o parâmetro `key_press`, definido como `<caps_lock>` por padrão. Confira a documentação do `pynput` para mais opções de teclas: [documentação do pynput](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key).

Para sair do programa pressione `ctrl + c` se estiver em um ambiente Windows ou `cmd + c` se estiver em um ambiente MacOS.

## Licença

Este projeto está licenciado sob a Licença MIT.
