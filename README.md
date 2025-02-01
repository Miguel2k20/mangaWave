# MangaWave

MangaWave é um projeto de desenvolvimento pessoal, sem fins lucrativos, projetado para otimizar a leitura e o download de mangás em formatos PDF e .mobi, proporcionando uma experiência de leitura ideal para dispositivos Kindle.

## Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

- **Linguagem de Programação:** Python
- **Framework de Interface:** Flet
- **API:** [MangaDex API](https://api.mangadex.org/docs/)

## Configuração do Ambiente e Execução

### Linux
Para configurar o ambiente no Linux, siga os seguintes passos:

1. Crie e ative um ambiente virtual:

```sh
python3 -m venv venv
source venv/bin/activate
```

2. Instale as dependências necessárias:

```sh
pip install flask pillow requests flet
```

3. Atualize o sistema e instale as bibliotecas exigidas:

```sh
sudo apt update
sudo apt install libmpv-dev libmpv2
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1
```

4. Execute o projeto:

```sh
flet run main.py -r
```

### Windows
Para configurar o ambiente no Windows, siga os passos abaixo:

1. Instale as dependências do projeto:

```sh
pip install flask pillow requests flet
```

2. Execute o projeto:

```sh
python main.py
```

## Considerações Finais

O MangaWave foi criado para aprimorar a experiência de leitura de mangás, fornecendo uma solução prática para download e organização dos arquivos. Sinta-se à vontade para contribuir ou sugerir melhorias! 🚀

