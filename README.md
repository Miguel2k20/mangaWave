To montando o front agr fds klkk

Só anotar aqui como faz pra rodar em linux pq esse sistema é foda
<!-- Cria o ambiente virtual -->
python3 -m venv venv 
<!-- Entra nele  -->
source venv/bin/activate
<!-- instala as depenencias -->
pip install flask
pip install pillow
pip install requests
<!-- So rodar essa bomba -->
python main.py

<!-- Caso eu va usar o flet -->

pip install flet

sudo apt update
sudo apt install libmpv-dev libmpv2 
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1