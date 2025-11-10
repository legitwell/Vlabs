
```markdown
## Lab 01 – Portas Abertas
**Desafio #1 – “Portas Abertas”**  
- **Lab ID:** `beee791354a71ca0daad919ba87993d7a44f160b`  
- **Fonte:** `monitoramento.pcap`

### Objetivo
Identificar todas as portas TCP **abertas** no host monitorado.

### Procedimento
1. Abrir o arquivo `monitoramento.pcap` no Wireshark.  
2. Aplicar o filtro de display:  
   ```wireshark
   tcp.flags.syn == 1 && tcp.flags.ack == 1
```


![](assets/Pasted%20image%2020251101193530.png)

3. Anotar os números de porta dos pacotes **SYN-ACK**.

### Resultado

- **Portas abertas (ordem crescente):**  
    `33024, 33054, 43001, 44289, 49222`

---

## Lab 02 – Coleta de Banners

**Lab ID:** `7aa8c0052252b06629659ff9bb33e6bd38e64639`

### Objetivo

Analisando as portas encontradas anteriormente foi possível obter alguma key?
Verificar se alguma das 5 portas descobertas expõe uma chave, coletando banners.

### Comando

```bash
nmap -Pn -sV -sC --script=banner 172.16.1.3 \
     -p 33024,33054,43001,44289,49222 \
     --max-retries 0
```


![](assets/Pasted%20image%2020251101193644.png)

### Saída resumida

|porta|banner retornado|
|---|---|
|todas|`172.16.1.55 port 44905 Key - b4nn3rgr4bbing122938842`|

- **Chave extraída:** `b4nn3rgr4bbing122938842`

---

## Lab 03 – Socket Final

### Objetivo

Qual o socket encontrado?
Concatenar os banners e descobrir o socket secreto.

### Comando

```bash
nmap -Pn -sV -sC --script=banner \
     -p 33024,33054,43001,44289,49222 \
     --max-retries 0 172.16.1.3 | grep banner
```

### Saída bruta

```
|_banner: 172.
|_banner: 16.1
|_banner: .55
|_banner: port 44905
|_banner: Key - b4nn3rgr4bbing122938842
```

### Conclusão

- **Socket secreto:** `172.16.1.55:44905`
- **Chave de autenticação:** `b4nn3rgr4bbing122938842`


### Relatório – Lab 04: 
id: `cd15eea6c2342839a83f4f08351e864fd8932f3f`

> Dispositivo-alvo ativo: **172.16.1.55:44905**

### Comando executado
```bash
nc -vn -w1 172.16.1.55 44905
````

![](assets/Pasted%20image%2020251101195217.png)

![](assets/Pasted%20image%2020251101195232.png)

### Pacote IP – Dissecação byte-a-byte

| Campo (offset)                           | Hex           | Valor / Interpretação                             |
| ---------------------------------------- | ------------- | ------------------------------------------------- |
| **Versão** (0)                           | `45`          | **4** (IPv4)                                      |
| **Header Length** (0)                    | `45`          | **5** × 4 = **20 bytes**                          |
| **Explicit Congestion Notification** (1) | `00`          | **0x00** (ECN não utilizado)                      |
| **Total Length** (2-3)                   | `00 4c`       | **76 bytes**                                      |
| **Identification** (4-5)                 | `d1 b4`       | **0xd1b4**                                        |
| **Flags + Fragment Offset** (6-7)        | `40 00`       | Flags: **DF** (Don’t Fragment) setado; Offset = 0 |
| **TTL** (8)                              | `40`          | **64**                                            |
| **Protocolo** (9)                        | `01`          | **ICMP**                                          |
| **Checksum** (10-11)                     | `4e a3`       | **0x4ea3**                                        |
| **IP Origem** (12-15)                    | `ac 10 01 37` | **172.16.1.55**                                   |
| **IP Destino** (16-19)                   | `ac 10 01 02` | **172.16.1.2**                                    |


### Payload ICMP (ASCII)




![](assets/Pasted%20image%2020251101195901.png)



```
dst http port 80 /malware.txt - KEY:00298417172
```

### Chave extraída

![](assets/Pasted%20image%2020251101200021.png)




