# respondeaY
Bot para responder uma _repetyda_ pergunta no Twitter.

## Inspiração

O artista [Juão Nin](https://twitter.com/juaonin) é fundador da banda Androide Sem Par e ativista em prol das comunidades indígenas. Em protesto a invisibilização da cultura indígena, ele passou a trocar a letra I pela Y em seus textos.
 
Os constantes questionamentos do seus seguidores nas redes sociais sobre o uso da letra Y o fizeram pensar em criar um bot para responder a essas perguntas. 

## Requisitos

- Python 3.6+
- `pip install -r requirements.txt`

## Configuração

Crie um app no Twitter e obtenha as variáveis de ambiente `CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_KEY` e `ACCESS_SECRET`.

Altere as respostas no arquivo `data/answers.txt`, observando o padrão de separação entre os textos e o limite de caracteres do Twitter.

## Funcionamento

Execute no terminal:
```
python bot.py
```

O projeto está pronto para funcionar no Heroku/Dokku, com a configuração de buildpacks e execução definidas nos arquivos `.buildpacks` e `Procfile`.