
### SEMANA 05 - INFORMATION GATHERING - INFRA

### LAB 01 - Netblock

---

**ID do Lab:** `817a3008ecf89361a605bf97ffc301c01d27439f`

**Pergunta:** Qual o netblock da businesscorp.com.br?

**Resposta:** Para descobrir o Netblock (o bloco/range de IPs), primeiro usamos o script `ResolvendoDNS.py` para descobrir o IP principal (37.59.174.225). Em seguida, usamos o comando `whois` para consultar o proprietário desse IP.

**Comando Utilizado (Whois):**

Bash

```
whois 37.59.174.225
```

**Explicação do Comando:**

- **`whois`**: Consulta registros públicos de alocação de IPs e domínios.
    
- **`37.59.174.225`**: O IP alvo que encontramos com nosso script.
    

**Resultado Obtido:** A consulta ao `whois` (especificamente no `whois.lacnic.net`) revela o Netblock (inetnum) alocado para este IP:

- **Netblock:** `37.59.174.224 - 37.59.174.239`
    

### Evidência (Print do Resultado)

![] (../assets/Pasted image 20251109235432.png)


---

### SEMANA 05 - INFORMATION GATHERING - INFRA

### LAB 02 - AS Provedor

---

**ID do Lab:** `cec4ca31572cc092f60aacb6e3cb285fe463687a`

**Pergunta:** Qual o AS do provedor utilizado pelo businesscorp.com.br?

**Resposta:** Usando o mesmo IP principal (37.59.174.225) que encontramos, consultamos o `whois` para identificar o "Autonomous System" (AS) que gerencia este bloco de rede.

**Comando Utilizado (Whois):**

Bash

```
whois 37.59.174.225
```

**Explicação do Comando:**

- **`whois`**: Consulta registros públicos. A informação do AS (origin-as) está contida no mesmo relatório do Netblock.
    

**Resultado Obtido:** A consulta ao `whois` revela o "origin-as" (AS de Origem) para este IP:

- **AS:** `AS16276`
    

### Evidência (Print do Resultado)

![] (../assets/Pasted image 20251109235508.png)

---

### SEMANA 05 - INFORMATION GATHERING - INFRA

### LAB 03 - Subdomínio Secreto

---

**ID do Lab:** `6baf1b94463986a7b0b90c41e8181248ecc2ccc6`

**Pergunta:** Realize o reconhecimento de DNS no businesscorp.com.br e encontre o subdomínio secreto.

**Resposta:** Utilizamos nosso script `ResolvendoDNS.py` que, em sua [ETAPA 4], realizou uma Transferência de Zona (AXFR) bem-sucedida contra o `ns2.businesscorp.com.br`.

**Comando Utilizado (Nosso Script):**

Bash

```
./ResolvendoDNS.py businesscorp.com.br
```

**Explicação do Comando:**

- O script identificou o `ns2` como vulnerável e "dumpou" a lista completa de todos os registros DNS, incluindo hosts que não são publicamente listados.
    

**Resultado Obtido:** Analisando a lista da Transferência de Zona, encontramos um subdomínio com nome suspeito:

- **Subdomínio Secreto:** `infrasecreta.businesscorp.com.br`
    

### Evidência (Print do Resultado)

![] (../assets/Pasted image 20251109235614.png)

---

### SEMANA 05 - INFORMATION GATHERING - INFRA

### LAB 04 - IP do Subdomínio Secreto

---

**ID do Lab:** `a3cd51af01b5835db42f68dc83348ff432c13251`

**Pergunta:** Qual o endereço IP do subdomínio encontrado anteriormente?

**Resposta:** A mesma Transferência de Zona (AXFR) da [ETAPA 4] do nosso script, que revelou o _nome_ do host, também revelou seu _registro A_ (seu endereço IP).

**Comando Utilizado (Nosso Script):**

Bash

```
./ResolvendoDNS.py businesscorp.com.br
```

**Explicação do Comando:**

- O script listou todos os registros DNS, incluindo os registros `A` (Endereço IPV4).
    

**Resultado Obtido:** A linha de saída do script para o host `infrasecreta` foi:

```
infrasecreta.businesscorp.com.br 3600    IN  A     37.59.174.225
```

- **IP:** `37.59.174.225`
    

### Evidência (Print do Resultado)

![] (../assets/Pasted image 20251109235642.png)

---

### SEMANA 05 - INFORMATION GATHERING - INFRA

### LAB 05 - DNS Reverso

---

**ID do Lab:** `4d290b3dff33d7717fba1c0fb84922762fe047a6`

**Pergunta:** Realize a pesquisa de DNS reverso no businesscorp.com.br e informe quais subdomínios foram encontrados.

**Resposta:** A Transferência de Zona (AXFR) que nosso script realizou na [ETAPA 4] é mais completa e já nos deu todos os nomes de host, incluindo aqueles que seriam encontrados em um reverso.

**Comando Utilizado (Nosso Script):**

Bash

```
./ResolvendoDNS.py businesscorp.com.br
```

**Resultado Obtido:** Analisando a lista completa do AXFR, encontramos os dois subdomínios específicos do lab:

- `rh.businesscorp.com.br`
    
- `piloto.businesscorp.com.br`
    

### Evidência (Print do Resultado)

![] (../assets/Pasted image 20251109235700.png)


---

### SEMANA 05 - INFORMATION GATHERING - INFRA

### LAB 06 - IPs do DNS Reverso

---

**ID do Lab:** `14291fa8ebc649fb20d6b61fff5e59e55f015e6e`

**Pergunta:** Informe quais os endereços IPs dos subdomínios encontrados anteriormente na pesquisa reversa de DNS.

**Resposta:** Novamente, a [ETAPA 4] (AXFR) do nosso script já nos forneceu os IPs (registros `A`) para esses hosts.

**Comando Utilizado (Nosso Script):**

Bash

```
./ResolvendoDNS.py businesscorp.com.br
```

**Resultado Obtido:** As linhas de saída do script para esses hosts foram:

```
rh.businesscorp.com.br         3600    IN  A     37.59.174.229
piloto.businesscorp.com.br     3600    IN  A     37.59.174.230
```

- **IPs:** `37.59.174.229` e `37.59.174.230`
    

### Evidência (Print do Resultado)

![] (../assets/Pasted image 20251109235710.png)


---

### SEMANA 05 - INFORMATION GATHERING - INFRA

### LAB 07 - Key (HINFO)

---

**ID do Lab:** `6286c8aebba26a24b645105b0fb71a24f5756bea`

**Pergunta:** Realize uma pesquisa DNS no businesscorp.com.br afim de descobrir mais informações do host e encontre a key para pontuar.

**Resposta:** A [ETAPA 4] (AXFR) do nosso script "dumpou" _todos_ os tipos de registro, não apenas registros `A` ou `CNAME`. Isso incluiu um registro `HINFO` (Host Information).

**Comando Utilizado (Nosso Script):**

Bash

```
./ResolvendoDNS.py businesscorp.com.br
```

**Resultado Obtido:** A saída do script incluiu a seguinte linha:

```
businesscorp.com.br          3600    IN  HINFO "SERVIDOR DELL" "DEBIAN - key:0989201883299"
```

- **Key:** `0989201883299`
    

### Evidência (Print do Resultado)

![] (../assets/Pasted image 20251109235729.png)


---

### SEMANA 05 - INFORMATION GATHERING - INFRA

### LAB 08 - Key (SPF)

---

**ID do Lab:** `874b1b71608f4358fa682b081efcb081c042bf1a`

**Pergunta:** Analise o SPF do businesscorp.com.br e encontre a key para pontuar.

**Resposta:** O SPF (Sender Policy Framework) é armazenado em um registro `TXT` no DNS. A [ETAPA 4] (AXFR) do nosso script também encontrou esse registro.

**Comando Utilizado (Nosso Script):**

Bash

```
./ResolvendoDNS.py businesscorp.com.br
```

**Resultado Obtido:** A saída do script incluiu a seguinte linha:

```
businesscorp.com.br          3600    IN  TXT   "v=spf1 include:key-9283947588214 ?all"
```

- **Key:** `9283947588214`
    

### Evidência (Print do Resultado)

![] (../assets/Pasted image 20251109235746.png)

---

### SEMANA 05 - INFORMATION GATHERING - INFRA

### LAB 09 - Subdomain Takeover

---

**ID do Lab:** `e2c8a198e85c28b4880f9e3db9e1ba98bb1a8dea`

**Pergunta:** Realize uma pesquisa por subdomain takeover e encontra a key para pontuar.

**Resposta:** A vulnerabilidade de Subdomain Takeover ocorre quando um registro `CNAME` aponta para um serviço externo que não está mais em uso. A [ETAPA 4] (AXFR) do nosso script encontrou o `CNAME` vulnerável.

**Comando Utilizado (Nosso Script):**

Bash

```
./ResolvendoDNS.py businesscorp.com.br
```

**Resultado Obtido:** A saída do script incluiu a seguinte linha:

```
admin.businesscorp.com.br      3600    IN  CNAME key.vlab.takeover.092935999311009.
```

O próprio _destino_ do CNAME continha a key.

- **Key:** `092935999311009`
    

### Evidência (Print do Resultado)

![] (../assets/Pasted image 20251109235814.png)
