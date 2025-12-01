
# 🔐 Credenciais Comprometidas - Pentest

**Tags:** #pentest #credentials #loot #active-directory

---

## 🌐 1. Domínio Active Directory (ORIONSCORP2 / GBUSINESS)
*Credenciais válidas para movimentação lateral via SMB, RDP, WinRM ou Psexec.*

| Usuário | Senha | Privilégio / Contexto | Método de Obtenção |
| :--- | :--- | :--- | :--- |
| `Administrator` | `GBcorps3rv3r08` | **Domain Admin** | Dump de Memória (WCE) |
| `thenrique` | `dss!$#asdadm1n` | **Domain Admin** | Dump de Memória (Mimikatz) |
| `bernardo` | `1#bernard` | Usuário de Domínio | Dump de Memória (WCE) |
| `rogerio` | `Roger@10` | Usuário de Domínio | Dump de Memória (WCE) |
| `rlourdes` | `georgeorwell1984` | Usuário de Domínio | LLMNR Poisoning + Cracking |
| `lotavio` | `porche911.` | Usuário de Domínio | LLMNR Poisoning + Cracking |
| `camila` | `Apolo201` | Usuário de Domínio | Cache Dump + Cracking |
| `ti` | `it@LOCAL` | Usuário de Domínio | NTDS Dump + Cracking |
| `nicolas` | `23nick#@` | Usuário de Domínio | NTDS Dump + Cracking |
| `lucas` | `#1AriesBoss` | Usuário de Domínio | NTDS Dump + Cracking |
| `acosta` | `!amorloko!_15` | Usuário de Domínio | NTDS Dump + Cracking |
| `abeatriz` | `Beatboxman2K7` | Usuário de Domínio | NTDS Dump + Cracking |
| `sqlservice` | `#ptm@sql@kiero#` | Conta de Serviço | NTDS Dump + Cracking |
| `egabriel` | `Der#22Dwr#29` | Usuário de Domínio | NTDS Dump + Cracking |

---

## 🌍 2. Serviços Web & Aplicações
*Credenciais específicas de serviços rodando nas portas 8080 ou serviços legados.*

| Usuário | Senha | Serviço / Contexto | Método de Obtenção |
| :--- | :--- | :--- | :--- |
| `cpd` | `abc123` | **Tomcat Manager** (8080) | Hydra (Brute Force Online) |
| *N/A* | `4runner` | Hash Legado (Backup) | Hash Identifier + Lookup Online |

---

## 💻 3. Contas Locais (SAM Database)
*Credenciais extraídas das hives SAM locais de estações específicas via `reg save`.*

| Usuário | Senha | Contexto | Método de Obtenção |
| :--- | :--- | :--- | :--- |
| `DEV01` | `dev0105` | Local (Host 172.30...) | Reg Save (SAM/SYSTEM) + Cracking |
| `ADM01` | `admd0458` | Local (Host 172.30...) | Reg Save (SAM/SYSTEM) + Cracking |
| `CPD01` | `bk7cpd` | Local (Host 172.30...) | Reg Save (SAM/SYSTEM) + Cracking |

---

## 💀 4. Backdoors (Persistência)
*Usuários injetados no sistema durante a exploração.*

| Usuário | Senha | Onde foi criado | Método |
| :--- | :--- | :--- | :--- |
| `hacker` | `Password123!` | Servidor HPE iMC | Exploit Java Deserialization |
| `hacker` | `D3s3c_2025!` | Servidor HPE iMC | Exploit Java Deserialization (Senha Forte) |