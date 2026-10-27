Atividade Classe 04 — Sockets UDP
RA: 2403862

Objetivo
--------
Adaptar o Servidor/Cliente da Prática 8 (UDP) para que:
- o cliente envie um arquivo de imagem;
- o servidor receba esse arquivo via datagrama.

Arquivos
--------
servidor_udp.py   -> servidor que reconstitui a imagem
cliente_udp.py    -> cliente que fatia e envia a imagem
neymar.png        -> imagem de exemplo usada no envio

Como executar
-------------
1. Abra um terminal e rode o servidor:
   python3 servidor_udp.py

2. Abra OUTRO terminal, na mesma pasta, e rode o cliente:
   python3 cliente_udp.py

3. O servidor grava o arquivo recebido como:
   recebido_neymar.png

Observação
----------
HOST = 127.0.0.1 e PORTA = 45405 (iguais à Prática 8).
Cada datagrama tem no máximo 512 bytes, como no recvfrom(512) da aula.
