# LAB 01

**WebSite Lab ID: daebe81f5a8d0f729c5e3f1c0d1e946faed22940**

  

**Analisando o website** [**www.businesscorp.com.br**](http://www.businesscorp.com.br/)

**Pergunta: Quais portas TCP estão abertas?**

Para identificar as portas TCP abertas em um site, utilizamos a ferramenta Nmap. Abaixo está o comando utilizado e o resultado obtido:

==nmap --open www.businesscorp.com.br -p- -Pn==  

**Resultado:**

![[/Untitled 19.png|Untitled 19.png]]

**Explicação:**

- O comando `**nmap**` é uma ferramenta de escaneamento de rede utilizada para descobrir hosts e serviços em uma rede.
- `**-open**` indica para o Nmap que ele deve mostrar apenas os hosts com portas abertas.
- `**www.businesscorp.com.br**` é o alvo do escaneamento.
- `**p-**` instrui o Nmap a verificar todas as portas.
- `**Pn**` desabilita o ping discovery, o que significa que o Nmap não irá verificar se os hosts estão online antes de escaneá-los.

Essa informação pode ser valiosa para entender a configuração do servidor e possíveis serviços em execução.

---

  

# LAB 02

  

**WebSite II Lab ID:** ec31dfc0de2d9ae049bed0a2a821c1d3a0adbeaf

  

**Análise do website** [**www.businesscorp.com.br**](http://www.businesscorp.com.br/)

**Pergunta:**  
Qual a versão do serviço DNS?

**Resposta:**  
Para determinar a versão do serviço DNS em execução no website [**www.businesscorp.com.br**](http://www.businesscorp.com.br/), utilizamos o utilitário Nmap com os seguintes comandos:

==nmap -p 53 -sV -Pn www.businesscorp.com.br==  

![[/Untitled 1 2.png|Untitled 1 2.png]]

Aqui está uma explicação detalhada dos comandos utilizados:

- `**nmap**`: Este é o comando principal para iniciar a ferramenta Nmap, que é amplamente utilizada para escanear e mapear redes, identificando hosts e serviços em execução.
- `**p 53**`: Este parâmetro especifica a porta que desejamos escanear, que no caso é a porta 53. A porta 53 é comumente associada a serviços DNS (Domain Name System).
- `**sV**`: Este parâmetro ativa a detecção de versão do serviço. Ele instrui o Nmap a tentar determinar a versão exata do serviço em execução na porta especificada.
- `**Pn**`: Este parâmetro indica ao Nmap para não realizar a detecção de hosts online. Isso significa que o Nmap não verificará se o host está ativo antes de realizar o escaneamento de portas.

Após a execução do comando, o Nmap forneceu a seguinte saída:

```Arduino

PORT   STATE SERVICE VERSION
53/tcp open  domain  ISC BIND 9.8.4-rpz2+rl005.12-P1

```

Essa saída nos informa que a porta 53 TCP está aberta e que o serviço DNS em execução utiliza a versão ==**ISC BIND 9.8.4-rpz2+rl005.12-P1**====.==

---

  

# LAB 03

  

**WebSite IIILab ID:** 2cb99839981c43da1f91b894318c41143dfa0391

  

**Análise do website** [**www.businesscorp.com.br**](http://www.businesscorp.com.br/)

**Pergunta:**  
Qual a versão do serviço de transferência de arquivos?

**Resposta:**  
Para determinar a versão do serviço de transferência de arquivos em execução no website [**www.businesscorp.com.br**](http://www.businesscorp.com.br/), utilizamos o utilitário Nmap com os seguintes comandos:

![[/Untitled 2 2.png|Untitled 2 2.png]]

  

Aqui está uma explicação detalhada dos comandos utilizados:

- `**nmap**`: Este é o comando principal para iniciar a ferramenta Nmap, que é amplamente utilizada para escanear e mapear redes, identificando hosts e serviços em execução.
- `**sV**`: Este parâmetro ativa a detecção de versão do serviço. Ele instrui o Nmap a tentar determinar a versão exata do serviço em execução na porta especificada.
- `**37.59.174.225**`: Este é o endereço IP do website que estamos analisando.
- `**p21**`: Este parâmetro especifica a porta que desejamos escanear, que no caso é a porta 21. A porta 21 é comumente associada ao serviço FTP (File Transfer Protocol).

Após a execução do comando, o Nmap forneceu a seguinte saída:

```Bash

PORT   STATE SERVICE VERSION
21/tcp open  ftp     ProFTPD 1.3.4a
Service Info: OS: Unix

```

Essa saída nos informa que a porta 21 TCP está aberta e que o serviço FTP em execução utiliza a versão **ProFTPD 1.3.4a**.

---

  

# LAB 04

  

**Lab ID:** 5d3b7d84f7c870a55bdb3cc9a000dbe7ee226002

  

**Realize um Ping Sweep na rede 172.30.0.0/24**

**Pergunta:**  
Quantos hosts respondem ICMP?

**Resposta:**

Para realizar um Ping Sweep na rede 172.30.0.0/24, utilizamos o utilitário `**fping**` com o seguinte comando:

```Shell

fping -c 1 -g 172.30.0.0/24 > ping1.txt | grep "64 bytes"

```

![[/Untitled 3 2.png|Untitled 3 2.png]]

Este comando executa uma varredura de ping na faixa de endereços IP de 172.30.0.1 a 172.30.0.254, enviando apenas um pacote de ping para cada host e redirecionando a saída para um arquivo chamado `**ping1.txt**`.

Aqui está uma explicação detalhada dos comandos utilizados:

- `**fping**`: Este é o comando principal para iniciar a ferramenta de ping avançada, que é usada para enviar pacotes ICMP para hosts em uma rede.
- `**c 1**`: Esse argumento especifica que será enviado apenas um pacote de ping para cada host.
- `**g 172.30.0.0/24**`: Esse argumento indica que a varredura de ping será realizada na faixa de endereços IP de 172.30.0.1 a 172.30.0.254.
- `**> ping1.txt**`: Este redirecionamento de saída (`**>**`) envia os resultados para o arquivo `**ping1.txt**` em vez de imprimi-los no terminal.
- `**| grep "64 bytes"**`: Este comando `**grep**` é usado para filtrar a saída e mostrar apenas as linhas que contêm a string "64 bytes", indicando que o ping foi bem-sucedido.

A saída do comando forneceu uma lista de hosts que responderam ao ping. Contando as linhas, podemos determinar quantos hosts responderam ICMP.

**Resposta:**  
Foram encontrados 22 hosts que responderam ICMP na rede 172.30.0.0/24.

Também foi fornecido outro comando alternativo usando um loop para pings sequenciais em uma faixa de IP e, em seguida, filtrando a saída para exibir apenas as linhas que contêm "64 bytes".

![[/Untitled 4 2.png|Untitled 4 2.png]]

Ambos os métodos atingem o mesmo resultado de determinar quantos hosts respondem ICMP na rede especificada.

> [!important] Pode ser feito um loop com o
> 
> **hping3**

---

  

# LAB 05

  

**Lab ID:** bf7e88fc633a0d2051aac1b97842f1b041d67a88

  

**Analise a rede 172.30.0.0/24**

**Pergunta:**  
Quantos hosts estão ativos na rede?

**Resposta:**

Para determinar quantos hosts estão ativos na rede 172.30.0.0/24, utilizamos o comando `**nmap**` com a opção `**-sn**` para fazer um "ping scan" (varredura de ping) e a opção `**-oG**` para salvar a saída em um formato greppable.

O comando utilizado foi:

```Shell

nmap -v -sn 172.30.0.0/24 -oG ativos.txt

```

Este comando executa uma varredura de ping em todos os hosts na faixa de endereços IP de 172.30.0.1 a 172.30.0.254 e salva os resultados no arquivo `**ativos.txt**`.

Em seguida, utilizamos o comando `**grep**` para filtrar a saída e mostrar apenas as linhas que contêm a string "Up", indicando que o host está ativo.

  

![[/Untitled 5 2.png|Untitled 5 2.png]]

Aqui está uma explicação detalhada dos comandos utilizados:

- `**nmap**`: Este é o comando principal para iniciar o utilitário de varredura de rede.
- `**v**`: Habilita o modo verbose (detalhado) para fornecer mais informações durante a execução do comando.
- `**sn**`: Essa opção indica ao `**nmap**` para fazer um "ping scan", que envia pacotes de ping para os hosts para determinar se estão ativos.
- `**172.30.0.0/24**`: Esse argumento especifica a faixa de endereços IP que será alvo da varredura.
- `**oG ativos.txt**`: Este argumento instrui o `**nmap**` a salvar os resultados em um arquivo chamado `**ativos.txt**` no formato greppable.

**Resposta:**  
Foram encontrados 23 hosts ativos na rede 172.30.0.0/24.

---

  

# LAB 06

  

**Lab ID:** 3ebba0716eeafafbf8dc2b912dcf44a05917961b

  

**Analise da rede 172.30.0.0/24**

**Pergunta:**  
Qual o endereço IP do host com sistema operacional Windows?

**Resposta:**

Para identificar o endereço IP do host com sistema operacional Windows na rede 172.30.0.0/24, utilizamos o comando `**nmap**` com a opção `**-Pn**` para desativar a verificação de host online e a opção `**-p445**` para varrer a porta 445, que é associada ao serviço de compartilhamento de arquivos do Windows.

O comando utilizado foi:

```Shell

nmap -Pn 172.30.0.0/24 -p445 --open

```

![[/Untitled 6 2.png|Untitled 6 2.png]]

Aqui está uma explicação detalhada do comando utilizado:

- `**nmap**`: Este é o comando principal para iniciar o utilitário de varredura de rede.
- `**Pn**`: Desativa a verificação de host online, permitindo a varredura de hosts que não respondem ao ping.
- `**172.30.0.0/24**`: Especifica a faixa de endereços IP que será alvo da varredura.
- `**p445**`: Indica ao `**nmap**` para varrer a porta 445, que é a porta padrão usada pelo serviço de compartilhamento de arquivos do Windows.
- `**-open**`: Mostra apenas os hosts com portas abertas.

O resultado da varredura mostrou um host com o endereço IP `**172.30.0.103**` e a porta `**445/tcp**` aberta. Isso indica que este host está executando um serviço de compartilhamento de arquivos do Windows.

**Resposta:**  
O endereço IP do host com sistema operacional Windows na rede 172.30.0.0/24 é `**172.30.0.103**`.

![[/Untitled 7 2.png|Untitled 7 2.png]]

---

  

# LAB 07

  

**Lab ID:** 1024755034671ec020b56260e1a4f2dc1049c8c7

  

**Análise da rede 172.30.0.0/24**

**Pergunta:**  
Quais portas TCP estão abertas no host com sistema operacional Windows?

**Resposta:**

Para identificar as portas TCP abertas no host com sistema operacional Windows na rede 172.30.0.0/24, utilizamos o comando `**nmap**` com as seguintes opções:

```Shell

nmap -sS -p- -Pn 172.30.0.103 --open -T5

```

![[/Untitled 8 2.png|Untitled 8 2.png]]

Aqui está uma explicação detalhada do comando utilizado:

- `**nmap**`: Este é o comando principal para iniciar o utilitário de varredura de rede.
- `**sS**`: Realiza um scan de TCP SYN. Esta opção é usada para detectar portas abertas.
- `**p-**`: Varre todas as 65535 portas TCP. O hífen indica que todas as portas devem ser escaneadas.
- `**Pn**`: Desativa a verificação de host online, permitindo a varredura de hosts que não respondem ao ping.
- `**172.30.0.103**`: Especifica o endereço IP do host alvo.
- `**-open**`: Mostra apenas os hosts com portas abertas.
- `**T5**`: Define o modo de velocidade da varredura para o máximo (mais agressivo).

O resultado da varredura mostrou as seguintes portas TCP abertas no host com sistema operacional Windows:

- `**135/tcp**`: MSRPC
- `**139/tcp**`: NetBIOS Session Service
- `**445/tcp**`: Microsoft-DS
- `**2810/tcp**`: NetSteward
- `**5985/tcp**`: WSMan
- `**8080/tcp**`: HTTP Proxy

Estas são as portas abertas no host com sistema operacional Windows na rede 172.30.0.0/24.

---

  

# LAB 08

  

**Lab ID:** 0bfcf348ad95674ac8f67c83fdf435c4cda1ef36

  

**Análise da rede 172.30.0.0/24**

**Pergunta:**  
Qual host na rede está executando serviço de envio de e-mails?

**Resposta:**

Para identificar o host na rede que está executando o serviço de envio de e-mails, utilizamos o comando `**nmap**` com as seguintes opções:

```Bash

nmap -Pn -sS -p25 172.30.0.0/24 --open

	
```

![[/Untitled 9 2.png|Untitled 9 2.png]]

Aqui está uma explicação detalhada do comando utilizado:

- `**nmap**`: Este é o comando principal para iniciar o utilitário de varredura de rede.
- `**Pn**`: Desativa a verificação de host online, permitindo a varredura de hosts que não respondem ao ping.
- `**sS**`: Realiza um scan de TCP SYN. Esta opção é usada para detectar portas abertas.
- `**p25**`: Especifica a porta 25, que é a porta padrão para o serviço de envio de e-mails (SMTP).
- `**172.30.0.0/24**`: Define o intervalo de endereços IP na rede a ser escaneada.
- `**-open**`: Mostra apenas os hosts com portas abertas.

O resultado da varredura mostrou que o host com o endereço ==IP 172.30.0.128== está executando o serviço de envio de e-mails na porta 25 (SMTP).

---

  

# LAB 09

  

**Lab ID:** d3e6a19e9636519726382a3799bf956a92656815

  

**Análise da rede 172.30.0.0/24**

**Pergunta:**  
Qual o nome do serviço de e-mail em execução no host encontrado anteriormente?

**Resposta:**

Para identificar o nome do serviço de e-mail em execução no host com o endereço IP 172.30.0.128, utilizamos o comando `**nmap**` com as seguintes opções:

```Shell

nmap -Pn -sSV -p25 172.30.0.128
	
```

![[/Untitled 10 2.png|Untitled 10 2.png]]

Aqui está uma explicação detalhada do comando utilizado:

- `**nmap**`: Este é o comando principal para iniciar o utilitário de varredura de rede.
- `**Pn**`: Desativa a verificação de host online, permitindo a varredura de hosts que não respondem ao ping.
- `**sSV**`: Realiza um scan de serviços e versões. Essa opção permite detectar informações detalhadas sobre os serviços em execução.
- `**p25**`: Especifica a porta 25, que é a porta padrão para o serviço de envio de e-mails (SMTP).
- `**172.30.0.128**`: Define o endereço IP do host a ser escaneado.

O resultado da varredura mostrou que o serviço de e-mail em execução no host 172.30.0.128 é o "==Postfix smtpd==." Além disso, o nome do host é "ubuntu.bloi.com.br."

## LAB 10

O resultado da varredura mostrou que o serviço de e-mail em execução no host 172.30.0.128 é o "==Postfix smtpd==." Além disso, o nome do host é "==ubuntu==.bloi.com.br."

![[/Untitled 10 2.png|Untitled 10 2.png]]

---

  

# LAB 11  
  

**Lab ID:** a32cd6136cb730483107a3ff4987339dc1ccc4d7

  

  

**Análise da rede 172.30.0.0/24**

**Pergunta:**  
Quais hosts estão executando o serviço do MySQL?

**Resposta:**

Para identificar os hosts que estão executando o serviço MySQL na rede 172.30.0.0/24, utilizamos o comando `**nmap**` com as seguintes opções:

```Shell

nmap -Pn -sSV -p3306 172.30.0.0/24 --open

	
```

![[/Untitled 11 2.png|Untitled 11 2.png]]

Aqui está uma explicação detalhada do comando utilizado:

- `**nmap**`: Este é o comando principal para iniciar o utilitário de varredura de rede.
- `**Pn**`: Desativa a verificação de host online, permitindo a varredura de hosts que não respondem ao ping.
- `**sSV**`: Realiza um scan de serviços e versões. Essa opção permite detectar informações detalhadas sobre os serviços em execução.
- `**p3306**`: Especifica a porta 3306, que é a porta padrão para o serviço MySQL.
- `**172.30.0.0/24**`: Define o intervalo de endereços IP a serem escaneados.

O resultado da varredura mostrou que dois hosts estão executando o serviço MySQL:

1. Host ==172.30.0.20== - Versão do MySQL não identificada.
2. Host ==172.30.0.104== - Executando MySQL versão 5.5.50-0ubuntu0.14.04.1.

---

  

# LAB 12

  

**Lab ID:** e0618228da49449d5141e1590b5126e870d80676

  

  

**Análise da rede 172.30.0.0/24**

**Pergunta:**  
Qual host está executando o serviço do Webmin?

**Resposta:**

Para identificar o host que está executando o serviço do Webmin na rede 172.30.0.0/24, utilizamos o comando `**nmap**` com as seguintes opções:

```Shell

nmap -sSV -Pn 172.30.0.0/24 --open -T5 -p10000

	
```

![[/Untitled 12 2.png|Untitled 12 2.png]]

Aqui está uma explicação detalhada do comando utilizado:

- `**nmap**`: Este é o comando principal para iniciar o utilitário de varredura de rede.
- `**sSV**`: Realiza um scan de serviços e versões. Essa opção permite detectar informações detalhadas sobre os serviços em execução.
- `**Pn**`: Desativa a verificação de host online, permitindo a varredura de hosts que não respondem ao ping.
- `**172.30.0.0/24**`: Define o intervalo de endereços IP a serem escaneados.
- `**-open**`: Mostra apenas os hosts com portas abertas.
- `**T5**`: Define o nível de agressividade da varredura. Neste caso, o valor 5 indica alta velocidade e agressividade.
- `**p10000**`: Especifica a porta 10000, que é a porta padrão para o serviço Webmin.

O resultado da varredura mostrou que o host ==172.30.0.15== está executando o serviço Webmin, com a porta 10000/tcp aberta e a versão MiniServ 0.01 (Webmin httpd).

---