  

# LAB 01

Lab ID: 29c597cc4c9c5146fe5cddf248270e767eba39df

  

Database

Analise o segmento de rede 172.16.1.1 até 172.16.1.100 (o host 172.16.1.5 está fora do escopo) e responda:

Existe algum host com o serviço MySql ativo na rede?

Resposta : 172.16.1.33

```CSS
nmap -p 3306 172.16.1.1-100 --open
```
![](../assets/Untitled%2021.png)


  

# LAB 2

**Database**

Lab ID: 5ea4aabba6c8aee74471553be462fc7cca14777a

Qual a versão do MySQL no Host encontrado anteriormente?

Resposta : 5.1.73-1
![](../assets/Untitled%201%204.png)


Esse comando é usado para se conectar a um servidor MySQL hospedado no IP 172.16.1.33 usando o usuário "root". Aqui está a explicação detalhada do comando:

- `**mysql**`: É o programa cliente do MySQL usado para se conectar ao servidor MySQL.
- `**h 172.16.1.33**`: Especifica o host (IP) do servidor MySQL ao qual você deseja se conectar. Nesse caso, o IP é 172.16.1.33.
- `**u root**`: Define o usuário que está sendo usado para se conectar ao servidor MySQL. Neste caso, está sendo usado o usuário "root".
- Ao executar esse comando, o MySQL tentará se conectar ao servidor MySQL no IP 172.16.1.33 usando o usuário "root". Se a conexão for bem-sucedida, você poderá interagir com o servidor MySQL por meio da linha de comando do MySQL.

O servidor MySQL está executando a **versão 5.1.73-1** no sistema operacional Debian.

  

# LAB 3

**Database**

Lab ID: a25ed3540040e482db1e1ad25e85bacad572c9e4

Realize a enumeração no MySQL do host encontrado anteriormente e consiga a key no banco de dados encontrado.

  
![](../assets/Untitled%202%204.png)


Para obter a key no banco de dados `**vlab**` do host MySQL 172.16.1.33, você fez a enumeração corretamente. Aqui está o passo a passo simplificado:

1. Conecte-se ao MySQL no host 172.16.1.33:
    
    ```Plain
    mysql -h 172.16.1.33 -u root -p
    ```
    
2. Liste os bancos de dados disponíveis:
    
    ```SQL
    SHOW DATABASES;
    ```
    
3. Use o banco de dados `**vlab**`:
    
    ```SQL
    USE vlab;
    ```
    
4. Liste as tabelas no banco de dados `**vlab**`:
    
    ```SQL
    SHOW TABLES;
    ```
    
5. Exiba o conteúdo da tabela `**ativa**`:
    
    ```SQL
    SELECT * FROM ativa;
    ```
    

Isso deve retornar a chave `**KEY 662102538896**`

  

# LAB 04

**SSH**

Lab ID: b8be5661a77ea2c5ed5344d7b06eb26a1dfffc7b

Neste mesmo host analisado anteriormente existe um serviço de SSH.

Quais os métodos de autenticação aceitos no serviço de SSH?

Resposta : publickey,password

![](../assets/Untitled%203%204.png)


O erro **"no matching host key type found"** indica que o cliente SSH não conseguiu encontrar um tipo de chave de host compatível com o oferecido pelo servidor SSH no host 172.16.1.33. Isso geralmente ocorre quando o servidor SSH oferece tipos de chave de host que não são suportados pelo cliente SSH.

# LAB 05

  

**NFS - PARTE I**

Lab ID: 2ba03ce463bc0a07c288203bd7060ad074db19fd

Explore o serviço de NFS do servidor 172.16.1.31 e consiga a key.

  
![](../assets/Untitled%204%204.png)


1. **Identificar o serviço NFS**: O comando `**rpcinfo -p 172.16.1.31 | grep nfs**` é usado para listar os serviços RPC (Remote Procedure Call) disponíveis no servidor 172.16.1.31 e filtrar apenas as entradas relacionadas ao NFS (Network File System). Isso nos permite identificar que o NFS está sendo executado na porta 2049.
2. **Verificar os diretórios compartilhados**: O comando `**showmount -e 172.16.1.31**` é usado para listar os diretórios compartilhados disponíveis no servidor NFS (172.16.1.31). Ele nos informa que o diretório `**/home/camila**` está sendo compartilhado.
3. **Criar um diretório local para montagem**: O comando `**mkdir nfs**` é usado para criar um diretório local chamado `**nfs**` onde o compartilhamento NFS será montado. Este diretório servirá como um ponto de montagem para o compartilhamento remoto.
4. **Montar o compartilhamento NFS**: O comando `**mount -t nfs -o nfsvers=3 172.16.1.31:/home/camila nfs**` é usado para montar o compartilhamento NFS remoto no diretório local `**nfs**`. A opção `**t nfs**` especifica o tipo de sistema de arquivos como NFS, e `**o nfsvers=3**` define a versão do NFS a ser usada como 3.
5. **Acessar o diretório NFS montado**: O comando `**cd nfs**` é usado para entrar no diretório `**nfs**` onde o compartilhamento NFS foi montado. Isso nos permite acessar os arquivos e diretórios dentro do compartilhamento remoto.
6. **Verificar o conteúdo do diretório NFS**: O comando `**ls**` é usado para listar o conteúdo do diretório NFS montado, permitindo-nos verificar se o compartilhamento foi montado corretamente e se o arquivo `**key.txt**` está presente.
7. **Visualizar o conteúdo do arquivo key.txt**: O comando `**cat key.txt**` é usado para exibir o conteúdo do arquivo `**key.txt**`, que contém a chave necessária para habilitar um ponto no VLAB.

Esses comandos são usados em conjunto para acessar e obter a chave no compartilhamento NFS do servidor 172.16.1.31.

# LAB 06

  

**NFS - PARTE II**

Lab ID: 9f032acb136f7bb9ff090a227f9a495fcf02c685

Consiga acesso ao shell ao host 172.16.1.31 através de manipulação de chaves ssh para obter a key.

  

1. **Gerar a chave SSH:**
    
    - Execute o comando `**ssh-keygen -t rsa**` para gerar uma chave SSH. Isso criará um par de chaves pública e privada.
    
    ![](../assets/Untitled%205%204.png)
    
2. **Montar o diretório NFS:**
    
    - Utilize o comando `**mount -t nfs -o nfvers=3 172.16.1.31:/home/camila /home/nfs**` para montar o diretório NFS remoto em sua máquina local.
    
    ![](../assets/Untitled%206%203.png)
    
3. **Acessar a pasta SSH e adicionar a chave pública:**
    
    - Navegue até a pasta `**~/.ssh/**` em seu sistema local.
    - Abra o arquivo `**authorized_keys**` e insira a chave pública gerada na etapa 1.
    
    ![](../assets/Untitled%207%203.png)
    
![](../assets/Untitled%208%203.png)


1. **Conectar-se ao servidor SSH:**
    
    - Use o comando `**ssh camila@172.16.1.31 -i id_rsa -o HostKeyAlgorithms=+ssh-dss -o PubkeyAcceptedAlgorithms=+ssh-rsa**` para se conectar ao servidor SSH. Substitua `**id_rsa**` pelo caminho da sua chave privada.
    ![](../assets/8f07c411-8a6d-4cd0-8bae-142e364176d0.png)
    
    
2. **Explorar o sistema de arquivos:**
    
    - Após se conectar, use o comando `**pwd**` para verificar o diretório atual.
    
    ![](../assets/Untitled%209%203.png)
    
    - Use `**cd ../..**` para voltar à pasta raiz.
    - Procure pelo arquivo `**key.txt**` usando `**ls -la**` para listar todos os arquivos, incluindo os ocultos.
3. **Encontrar a resposta do VLAB:**
    
    - Abra o arquivo `**key.txt**` encontrado no passo anterior para encontrar a resposta do VLAB, que é `**999675754423**`.
    
    ![](../assets/Untitled%2010%203.png)
    

Certifique-se de substituir os caminhos e nomes de arquivos conforme necessário para corresponder à sua configuração específica.

# LAB 07 | 08 | 09

  

**NFS II**

ID do laboratório: f73439e67146fa142f759d17d9f320c34df54355

ID do laboratório: 8b6f2fe04ee2f74dccc93bd2dcb0fc9d205277f8

ID do laboratório: 17c69319942b2da4295a3547bf2fc10ca3b0943a

  

Utilize as técnicas de enumeração NFS no host 172.16.1.251 e informe quais as versões NFS suportadas.

  
![](../assets/Untitled%2011%203.png)


  

# LAB 10

  

**FTP**

ID do laboratório: cdcad4766b40276231f58d0825b5b1f7b9a62470

Enumere o serviço de FTP do host: 172.16.1.31 e encontre uma chave para pontuar.

  
![](../assets/Untitled%2012%203.png)


  

# LAB 11

  

**FTP - PARTE I**

Lab ID: 243ac57079c67f699cc4fb5d4f1194aa5ea7de0e

Utilize as técnicas de enumeração no host 172.16.1.251 e informe a versão do serviço FTP encontrada.

Resposta : ProFTPD1.3.5
![](../assets/Untitled%2013%202.png)


  

# LAB 12

  

**FTP - PARTE II**

Lab ID: 73e7e0bf78736e9ce093713e726947bacf4254c5

Ganhe acesso ao serviço de FTP no host 172.16.1.251 e consiga a key para pontuar.

Resposta: ce6cfad1ff11b600bef6da1aa844996a

  
![](../assets/Untitled%2014%202.png)


  

# LAB 13

  

**SMB**

Lab ID: 7b581af4c9208ce84bab830e23567ef64655bb87

Enumere o serviço de SMB e consiga a chave para pontuar.
![](../assets/Untitled%2015%202.png)


- `**smbclient**`: é o comando para acessar recursos compartilhados em servidores SMB.
- `**L**`: é o parâmetro para listar recursos compartilhados.
- `**//172.16.1.4/**`: especifica o endereço IP do servidor e o nome do compartilhamento. No caso, `**172.16.1.4**` é o endereço IP do servidor e `**/**` indica que queremos listar todos os compartilhamentos disponíveis no servidor.
- `**N**`: indica que queremos fazer a conexão sem especificar um nome de usuário ou senha.

Este comando retornará uma lista dos compartilhamentos disponíveis no servidor SMB com o endereço IP `**172.16.1.4**`.
![](../assets/Untitled%2016%202.png)

![](../assets/Untitled%2017%202.png)


  

# LAB 14

  

**SNMP**

Lab ID: 7dca58db46ecb2efbc629f69b32fc468435067af

Enumere o serviço de SNMP e consiga a KEY para pontuar.

  
![](../assets/Untitled%2018%202.png)


- `**snmpwalk**`: comando para caminhar pela árvore de informações SNMP.
- `**c public**`: especifica a comunidade SNMP a ser usada. A comunidade SNMP é semelhante a uma senha e é usada para autenticar o acesso ao dispositivo SNMP. Aqui, a comunidade é "public", que é comumente usada para acesso de leitura (read-only).
- `**v1**`: especifica a versão do SNMP a ser usada. Neste caso, é a versão 1 do SNMP.
- `**172.16.1.4**`: endereço IP do dispositivo SNMP que será consultado.
- `**1.3.6.1.4.1.77.1.2.25**`: identificador de objeto (OID) que representa a parte da árvore SNMP que desejamos consultar. No caso, parece estar relacionado a informações de usuários do sistema.

As linhas retornadas pelo comando representam as informações recuperadas do dispositivo SNMP, como o nome dos usuários. A chave (KEY) mencionada no final parece ser uma resposta ao seu pedido específico. Portanto, a resposta seria: `**KEY298700191820**`.

  

# LAB 15

  

**SNMP II**

Lab ID: f142b53623052d1c9395beca20bca731c15f8439

Utilize as técnicas de análise SNMP no host: 172.30.0.103 e informe qual a community utilizada no serviço.
![](../assets/Untitled%2019%202.png)


- `**onesixtyone**`: o nome do comando utilizado para iniciar a ferramenta.
- `**c /usr/share/wordlists/metasploit/snmp_default_pass.txt**`: especifica o caminho para o arquivo contendo as strings que serão usadas para brute force nas comunidades SNMP. Neste caso, a ferramenta está usando o arquivo `**snmp_default_pass.txt**` que contém senhas padrão comumente usadas em comunidades SNMP.
- `**172.30.0.103**`: o endereço IP do alvo que será escaneado em busca de comunidades SNMP vulneráveis.

O comando escaneia o host `**172.30.0.103**` em busca de comunidades SNMP vulneráveis usando senhas padrão listadas no arquivo `**snmp_default_pass.txt**`. No exemplo dado, foi encontrada uma comunidade SNMP chamada `**Secret**` no host `**172.30.0.103**`.

  

# LAB 16

  

**SNMP II**

Lab ID: 8e993cde6c1d62fef19e51cbce068613422127d4

Utilize as técnicas de análise SNMP no host:172.30.0.103 e informe qual o hostname.

  
![](../assets/Untitled%2020%202.png)


- `**snmp-check**`: o nome do comando utilizado para iniciar a ferramenta.
- `**172.30.0.103**`: o endereço IP do dispositivo remoto que será enumerado.
- `**c Secret**`: especifica a comunidade SNMP a ser utilizada durante a enumeração. Neste caso, a comunidade é `**Secret**`.

A saída do comando fornece diversas informações sobre o dispositivo remoto:

- `**Hostname**`: o nome do host, que neste caso é `**SRV01**`.

  

# LAB 17

  

**SNMP II**

Lab ID: 4290653214d09bc7150226b2b1f3670c2a146545

Utilize as técnicas de análise SNMP no host:172.30.0.103 e encontre a chave para pontuar em informações sobre o armazenamento do discos do host.

  
![](../assets/Untitled%2020%202.png)

![](../assets/Untitled%2021%202.png)


  

# LAB 18

  

**SNMP II**

Lab ID: 198cac2b229c544247ecf1fd8a9f8ecb9a2df46b

Utilize as técnicas de análise SNMP no host:172.30.0.103 e informe quais usuários foram encontrados.
![](../assets/131e63d5-70b0-4c4d-949b-0ae7cf82ae09.png)

![](../assets/66d4941f-5964-42f0-8016-3e22abaf02fa.png)


`**snmpwalk -c Secret -v1 172.30.0.103 1.3.6.1.4.1.77.1.2.25**`: Este comando realiza uma caminhada no dispositivo SNMP para obter informações sobre os usuários. Ele especifica a comunidade SNMP "Secret", a versão SNMPv1 e o OID (Object Identifier) 1.3.6.1.4.1.77.1.2.25, que é usado para consultar informações sobre usuários.
![](../assets/Untitled%2022.png)
