# LAB 01

**Lab ID:** d4e17e1d388d22ed5faa00dd4d7c4351e3ea88fa

  

**Recon**

**Analisando o mail.businesscorp.com.br**

**Pergunta:**  
Quais portas TCP estão abertas?

**Resposta:**

Para identificar as portas TCP abertas no host mail.businesscorp.com.br, utilizamos o comando `**nmap**` com as seguintes opções:

```Shell

nmap -Pn -sSV -p- mail.businesscorp.com.br --open -T5

	
```

![[Untitled.png]]

Aqui está uma explicação detalhada do comando utilizado:

- `**nmap**`: Este é o comando principal para iniciar o utilitário de varredura de rede.
- `**Pn**`: Desativa a verificação de host online, permitindo a varredura de hosts que não respondem ao ping.
- `**sSV**`: Realiza um scan de serviços e versões. Essa opção permite detectar informações detalhadas sobre os serviços em execução.
- `-``**p-**`: Varre todas as 65535 portas TCP.
- `**mail.businesscorp.com.br**`: Especifica o host alvo da varredura.
- `**-open**`: Mostra apenas os hosts com portas abertas.
- `**T5**`: Define o nível de agressividade da varredura. Neste caso, o valor 5 indica alta velocidade e agressividade.

O resultado da varredura mostrou que o host mail.businesscorp.com.br possui as seguintes portas TCP abertas:

- ==21/tcp: FTP (ProFTPD 1.3.5)==
- ==80/tcp: HTTP (Apache httpd 2.4.10 (Debian))==
- ==110/tcp: POP3 (Courier pop3d)==
- ==143/tcp: IMAP (Courier Imapd - versão lançada em 2011)==

Além disso, foi identificado que o sistema operacional do host é ==Unix.==

---

  

# LAB 02

  

**Lab ID:** cd80018932136b6804afc03404755d6e2403e20a

  

**Recon II**

**Analisando o mail.businesscorp.com.br**

**Pergunta:**  
Quais portas UDP estão/está aberta?

**Resposta:**

Para identificar as portas UDP abertas no host mail.businesscorp.com.br, utilizamos o comando `**nmap**` com as seguintes opções:

```Shell

nmap -Pn -sUV --top-ports=10 mail.businesscorp.com.br --open -T5

	
```

![[Untitled 1.png]]

Aqui está uma explicação detalhada do comando utilizado:

- `**nmap**`: Este é o comando principal para iniciar o utilitário de varredura de rede.
- `**Pn**`: Desativa a verificação de host online, permitindo a varredura de hosts que não respondem ao ping.
- `**sUV**`: Realiza um scan de serviços e versões para protocolos UDP. Essa opção permite detectar informações detalhadas sobre os serviços em execução no protocolo UDP.
- `**-top-ports=10**`: Varre as 10 portas UDP mais comuns.
- `**mail.businesscorp.com.br**`: Especifica o host alvo da varredura.
- `**-open**`: Mostra apenas os hosts com portas abertas.
- `**T5**`: Define o nível de agressividade da varredura. Neste caso, o valor 5 indica alta velocidade e agressividade.

O resultado da varredura mostrou que o host mail.businesscorp.com.br possui as seguintes portas UDP abertas:

- ==53/udp: Serviço de domínio (domain?)== ==Open==
- ==135/udp: MS RPC (Microsoft Remote Procedure Call)== ==filtered==
- ==137/udp: NetBIOS Name Service (netbios-ns)== ==filtered==
- ==138/udp: NetBIOS Datagram Service (netbios-dgm)== ==filtered==
- ==445/udp: Microsoft-DS (Microsoft Directory Services)== ==filtered==

Algumas das portas estão marcadas como "open|filtered", o que indica que o estado da porta não pôde ser determinado com certeza devido a filtragem.

---

  

# LAB 03

  

**Lab ID:** 5e1c51a7dd4c5cc22bbaef665ffb1a4b7c450b59

  

**Recon III**

**Analisando o mail.businesscorp.com.br**

**Pergunta:**  
Qual a key no banner da porta UDP identificada?

**Resposta:**

Para identificar a "key" no banner da porta UDP identificada (porta 53), utilizamos o comando `**nc**` para conectar-se ao serviço DNS na porta 53 e observar a resposta do banner.

```Shell

nc -uv mail.businesscorp.com.br 53

	
```

![[Untitled 2.png]]

Aqui está uma explicação detalhada do comando utilizado:

- `**nc**`: Este é o comando utilizado para iniciar a ferramenta de conexão de rede.
- `**uv**`: Opções que especificam que queremos usar o protocolo UDP (`**u**`) e ativar o modo de verificação reversa para resolução de DNS (`**v**`).
- `**mail.businesscorp.com.br**`: Especifica o host alvo para a conexão.
- `**53**`: Especifica o número da porta que queremos conectar (no caso, a porta UDP 53 para DNS).

O resultado da conexão mostrou o banner do serviço DNS, que inclui a key identificada como:

```Plain
Copy code
DESEC DNS SERVER 901238127-1281321-d192919

```

Essa é a "key" encontrada no banner da porta UDP 53 no host mail.businesscorp.com.br.

---

  

# LAB 04

  

**Lab ID:** f7506c0fb77e7d8ffc6b8faae173b2eeb843674f

  

**OSINT**

**Informação Encontrada:**

Durante a fase de Information Gathering, foi possível identificar um vazamento de dados de e-mail do domínio businesscorp.com.br. Após a investigação, foram encontrados os seguintes dados:

- **Usuário:** camila
- **Senha:** ca123456

**Passos Realizados:**

1. Identificação dos servidores de nomes (NS) do domínio businesscorp.com.br:
    
    ```Shell
    
    host -t ns businesscorp.com.br | cut -d " " -f4
    ```
    
    ![[Untitled 3.png]]
    
      
    
2. Realização de uma transferência de zona (AXFR) para obter informações sobre os registros do domínio:
    
    ```Bash
    
    host -l -a businesscorp.com.br ns2.businesscorp.com.br
    ```
    
    ![[Untitled 4.png]]
    

  

1. Acesso ao site do Trello indicado na resposta do laboratório:
2. ==[**https://trello.com/b/kaqiIGDl/businesscorpcombr**](https://trello.com/b/kaqiIGDl/businesscorpcombr)====.==

![[Untitled 5.png]]

1. Acesso ao link do Pastebin contendo as credenciais vazadas: ==[**https://pastebin.com/57J3tLmc**](https://pastebin.com/57J3tLmc)====.==

![[Untitled 6.png]]

**Informação Obtida:**

- ==**Usuário:**== ==camila==
- ==**Senha:**== ==ca123456==

Estas são as credenciais encontradas no vazamento de dados do domínio businesscorp.com.br durante a fase de Information Gathering.

---

  

# LAB 05

  

**Lab ID:** a94c482b6350083881ea19393ec1ba423a0086fd

  

**OSINT II**

**Informação Encontrada:**

Durante a análise do serviço de e-mail hospedado no host mail.businesscorp.com.br, foi possível identificar o nome do serviço de e-mail utilizado:

- **Nome do Serviço de E-mail: ==Postfix==**

**Passos Realizados:**

1. Conexão ao serviço de e-mail no host mail.businesscorp.com.br na porta 110 usando o protocolo POP3:
    
    ```Plain
    
    nc -v mail.businesscorp.com.br 110
    	
    ```
    
    ![[Untitled 7.png]]
    
2. Autenticação no serviço de e-mail com as credenciais obtidas anteriormente:
    
    ```Bash
    
    USER camila
    PASS ca123456
    ```
    
    ![[Untitled 8.png]]
    
3. Utilização do comando LIST para listar os e-mails disponíveis:
    
    ```Plain
    
    LIST
    ```
    
    ![[Untitled 9.png]]
    
4. Para visualizar o conteúdo do e-mail, foi utilizado o comando RETR seguido do número do e-mail:
    
    ```Plain
    
    RETR 1
    ```
    
    ![[Untitled 10.png]]
    
    O conteúdo do e-mail foi exibido, incluindo informações sobre o remetente, destinatário, assunto e corpo da mensagem.
    
5. O procedimento foi repetido para outros e-mails, como no caso do comando RETR 2, para obter informações adicionais.

![[Untitled 11.png]]

**Informação Obtida:**

O serviço de e-mail utilizado é o ==**POSTFIX**==, como evidenciado nos cabeçalhos dos e-mails.

Exemplo de cabeçalho do e-mail: ==Received: by== ==[businesscorp.com.br](http://businesscorp.com.br/)== ==(Postfix, from userid 33)==

![[Untitled 12.png]]

Esta é a informação sobre o serviço de e-mail utilizado no host mail.businesscorp.com.br.

---

  

# LAB 06

  

**Lab ID:** 5951994a8e5899becc82db06c6b0c8cb3c090798

  

**OSINT III**

Durante a análise do host mail.businesscorp.com.br, foi possível identificar o serviço utilizado para webmail:

- **Serviço de Webmail Utilizado: ==SquirrelMail==**

O SquirrelMail foi identificado nos cabeçalhos dos e-mails, como no exemplo abaixo:

```Makefile

User-Agent: SquirrelMail/1.4.23 [SVN]
```

![[Untitled 13.png]]

Esta é a informação sobre o serviço de webmail utilizado no host mail.businesscorp.com.br.

### LAB 7

  

Lab ID: d6122d2498ed54e03ed511ba3765be726cb8dfce

**OSINT IV**

Durante a análise do host mail.businesscorp.com.br, foi possível identificar a versão do serviço utilizado para webmail:

  

- Versão **Serviço de Webmail Utilizado:** ==SquirrelMail/1.4.23==

---

# LAB 08

  

Lab ID: 96e960bf324552b9bd259c4ba4f282810c1a91ca

OSINT V

  

- O e-mail corporativo enviado para a colaboradora Camila foi de ==jotafsantos@businesscorp.com.br==

---

# LAB 09

  

Lab ID: 0814ccb8677c278e6467fb7f84d256b90d3f142e

OSINT VI

  

- A primeira mensagem foi : ==09/10/2018==

---

  

# LAB 10

  

Lab ID: 48e3a108b96624fe432acd5ebe21ad1a6564e29b

OSINT VII

  

- O IP que enviou a primeira mensagem : ==189.29.146.62==

---

  

# LAB 11

  

Lab ID: 51a3ca114c9c7d2dfbcae794a0f5a77e88873aa1

OSINT VIII

  

**Passos Realizados:**

1. Conexão ao serviço de e-mail no host mail.businesscorp.com.br na porta 143 usando o protocolo IMAP:
    
    ![[Untitled 14.png]]
    
    1. `**nc -v mail.businesscorp.com.br 143**`:
        
        - `nc`: É o comando para iniciar uma conexão de rede. Neste caso, estamos usando `nc` para iniciar uma conexão TCP.
        - `v`: Ativa o modo verbose, o que significa que irá exibir informações detalhadas sobre a conexão à medida que ela acontece.
        - `mail.businesscorp.com.br`: É o endereço do servidor ao qual estamos nos conectando.
        - `143`: Este é o número da porta usado para comunicações IMAP (Internet Message Access Protocol). É onde o serviço IMAP estará ouvindo no servidor.
        
        **Explicação**: Com esse comando, estamos iniciando uma conexão com o servidor de e-mail `mail.businesscorp.com.br` na porta 143, que é a porta padrão para o protocolo IMAP.
        
    2. `**a LOGIN camila ca123456**`:
        
        - `a`: Esta é uma tag arbitrária que usamos para identificar os comandos enviados. No IMAP, os comandos são identificados por tags.
        - `LOGIN`: Este é o comando IMAP para autenticar um usuário.
        - `camila`: É o nome de usuário usado para fazer login na conta de e-mail.
        - `ca123456`: É a senha associada à conta de e-mail.
        
        **Explicação**: Com este comando, estamos autenticando na conta de e-mail com o nome de usuário `camila` e a senha `ca123456`.
        
    3. `**a LIST "*"**`:
        
        - `LIST`: Este comando é usado para listar as caixas de correio disponíveis no servidor IMAP.
        - `"*"`: É um argumento usado para listar todas as caixas de correio.
        
        **Explicação**: Com este comando, estamos solicitando uma lista de todas as caixas de correio disponíveis na conta.
        
    4. `**a STATUS INBOX.Sent**`:
        
        - `STATUS`: Este comando é usado para obter o status de uma caixa de correio específica.
        - `INBOX.Sent`: É o nome da caixa de correio para a qual queremos obter o status.
        
        **Explicação**: Este comando é usado para obter informações sobre a caixa de correio "Sent".
        
    5. `**a SEARCH FROM "camila"**`:
        
        - `SEARCH`: Este comando é usado para realizar uma busca dentro da caixa de correio.
        - `FROM "camila"`: Este é um critério de busca para encontrar e-mails enviados por "camila".
        
        **Explicação**: Estamos procurando todos os e-mails na caixa de correio que foram enviados por "camila".
        
    6. `**a FETCH 2 (BODY[1.1])**`:
        
        - `FETCH`: Este comando é usado para recuperar informações sobre uma mensagem específica.
        - `2`: É o número da mensagem que queremos recuperar.
        - `(BODY[1.1])`: Este é um argumento para especificar que queremos recuperar o corpo da mensagem.
        
        **Explicação**: Com este comando, estamos recuperando o corpo da segunda mensagem na caixa de correio.
        
    
    Esses comandos permitem que você se autentique na conta de e-mail, liste as caixas de correio disponíveis, obtenha informações sobre a caixa de correio "Sent", realize uma busca por e-mails enviados por "camila" e, por fim, obtenha o corpo de uma mensagem específica. O conteúdo dessa mensagem contém a ==senha "bj9384221-==", conforme solicitado.
    
    ![[Untitled 15.png]]
    
    ---
    
      
    
    # LAB 12
    
    Lab ID: dbfc1186829c76cc4fd0791c854a4be479cc846b
    
    OSINT IX
    
      
    
    - O email corporativo foi encontrado ao usar o comando `RETR 2` para ler a segunda mensagem do inbox e o email encontrado foi : **==dev@businesscorp.com.br==**
    
      
    
    ---
    
      
    
    # LAB 13
    
    Lab ID: ad86e1a8e8da9e3392964eab7203677e4963ad7e
    
    OSINT X
    
      
    
    1. Acesse essa URL [mail.businesscorp.com.br](http://mail.businesscorp.com.br/)
        
        ![[Untitled 16.png]]
        
    2. Faça a autenticação  
        Usuario: camila  
        senha: bj9384221
        
        ![[Untitled 17.png]]
        
    
    ---
    
      
    
    # LAB 14
    
    Lab ID: 2a609e861ddb928e22e19a2f70b83c936124f2f5
    
    OSINT XI
    
      
    
    ![[Untitled 18.png]]