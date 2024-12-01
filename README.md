To montando o front agr fds klkk

Só anotar aqui como faz pra rodar em linux pq esse sistema é foda
<!-- Cria o ambiente virtual -->
python3 -m venv venv 
<!-- Entra nele  -->
source venv/bin/activate
<!-- instala as depenencias -->
pip install flask pillow requests flet

<!-- So rodar essa bomba -->
python main.py
<!-- Tem um erro libmpv que pode ser que precise rodar esse comando-->
sudo apt update
sudo apt install libmpv-dev libmpv2 
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1