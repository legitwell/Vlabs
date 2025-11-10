# Semana 06 - Mecanismo de Defesa

  

## Laboratório 1: Identificação de Portas

### Descrição

Neste laboratório, o objetivo era identificar portas abertas em um host específico.

### Passos Realizados

1. Utilizei o comando `nmap -v -sS --top-ports=10 -Pn 172.16.1.59` para realizar a identificação de portas abertas.
2. Nesse caso fiz na tentativa e erro até descobrir que era a porta 443
![](../assets/Untitled%2020.png)


Foi utilizado o Nmap para realizar uma varredura de portas no host 172.16.1.59. Os parâmetros usados foram:

- `**v**`: Ativa o modo verboso, fornecendo mais detalhes durante a execução.
- `**sS**`: Realiza uma varredura TCP SYN, que é mais rápida e stealth.
- `**-top-ports=10**`: Escaneia as 10 portas mais comuns, proporcionando uma varredura rápida.
- `**Pn**`: Ignora a descoberta de host e considera todos os hosts como online.

### Conclusão

Foi possível identificar que a porta 443 estava aberta no host 172.16.1.59.

## Laboratório 2: Bypass na Porta 443

### Descrição

Neste laboratório, o objetivo era encontrar uma forma de contornar a segurança na porta 443.

  

### Passos Realizados

1. Fiz um `nmap -v -sSV --top-ports=100 -Pn -g 443 172.16.1.59`
    
    ![](../assets/Untitled%201%203.png)
    
2. Utilizei a porta 443 para estabelecer uma conexão com o host 172.16.1.59.
3. Após a conexão, enviei um comando GET.


![](../assets/Untitled%202%203.png)
### Conclusão

O bypass na porta 443 foi bem-sucedido, permitindo a comunicação com o host.

  

Utilizou-se o Netcat (nc) para iniciar uma conexão TCP na porta 443 do host 172.16.1.59. Os parâmetros utilizados foram:

- `**v**`: Ativa o modo verboso, exibindo informações detalhadas sobre a conexão.
- `**p 443**`: Define a porta local como 443.
- `**172.16.1.59**`: Endereço IP do host de destino.
- `**8080**`: Número da porta do serviço.

---

**Laboratório 3: Identificação de Portas Abertas**

- **Host Analisado:** [intranet.businesscorp.com.br](http://intranet.businesscorp.com.br/)
- **Comando Utilizado:** nmap -v -D RND:50 -sS --top-ports=400 -Pn [intranet.businesscorp.com.br](http://intranet.businesscorp.com.br/)

![](../assets/Untitled%203%203.png)
- **Portas TCP Abertas:** 80, 2222, 10000 **Laboratório 4: Identificação do Sistema Operacional**
![](../assets/Untitled%204%203.png)


Novamente, foi utilizado o Nmap para realizar uma varredura de portas, desta vez no host intranet.businesscorp.com.br. Os parâmetros utilizados foram:

- `**v**`: Modo verboso ativado.
- `**D RND:20**`: Gera endereços IP aleatórios na tentativa de contornar possíveis mecanismos de defesa.
- `**sS**`: Escaneia portas usando TCP SYN.
- `**-top-ports=400**`: Escaneia as 400 portas mais comuns.
- `**Pn**`: Ignora a descoberta de host.
    
    ---
    
- **Host Analisado:** [intranet.businesscorp.com.br](http://intranet.businesscorp.com.br/)
- **Comando Utilizado:** nmap -v -D RND:20 -sSV -p 80,2222,10000 -Pn [intranet.businesscorp.com.br](http://intranet.businesscorp.com.br/)
- `**-sSV**`: Escaneia todos os portos e realiza detecção de serviço e versão.

![](../assets/Untitled%205%203.png)
- Sistema operacional encontrado : Debian 4
- Versão do Serviço Remoto : OpenSSH 6.0p1
- Serviço de gerenciamento web do servidor : MiniServ 0.01
- **Métodos de Autenticação Aceitos:**
    
    - Para o serviço na porta 80 (HTTP), não foram identificados métodos de autenticação específicos, o que é típico para serviços web.
    - Para o serviço na porta 2222 (EtherNetIP-1), foram identificados os seguintes métodos de autenticação:
        - `publickey`
        - `password`
    
      
    
    - Para o serviço na porta 10000 (snet-sensor-mgmt), não foram identificados métodos de autenticação específicos.
- **Possível Sistema Operacional:**
    - Debian (Baseado na versão do Apache identificada)