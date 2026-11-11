# Tjedan 4: Docker Compose i testovi

Termin: 180 min = blok A (80 min) + pauza (20 min) + blok B (80 min). Blok C (Ollama, Open WebUI i testovi u Composeu, 80 min) je zaseban blok vježbi koji se nastavlja na blok B.
Ishodi učenja koje tjedan pokriva: 1 (prepoznati koncepte i alate: Docker Compose, mreže, volumeni), 2 (razlikovati okruženja: isti alat protiv Ollame na hostu i u kontejneru, konfiguracija iz okoline), 5 (evaluirati rješenje: izlazni kod testova, izloženost portova, trajnost podataka).

> **Ishod bloka A:** student zna objasniti kako iz koda nastaje slika i kada je treba ponovno izgraditi i objaviti, zašto više kontejnera opisujemo u `compose.yaml`, kako se servisi pronalaze na mreži (host, zadani bridge, korisnička mreža i DNS), gdje podaci prežive kontejner (bind mount, imenovani volumen) i po čemu se razlikuju dugoživući i kratkoživući kontejneri.
>
> **Ishod bloka B:** otvoren pull request `feature/compose` u `praktikum-<github-korisnik>`: slika se gradi iz jednostavnog `Dockerfile`a (jedna faza), alat je servis `llm` u `compose.yaml` na host mreži, a student pokaže razliku između koda u slici, bind mounta i imenovanog volumena te podatke u imenovanom volumenu pročita iz praznog alpine kontejnera. Pomoćni `compose.storage.yaml` na kraju bloka briše. Kriteriji prihvaćanja su na vrhu [blok-b-vjezba.md](blok-b-vjezba.md).
>
> **Ishod bloka C:** otvoren pull request `feature/compose-ollama`: Ollama (`ollama-server`), jednokratno preuzimanje modela (`ollama-pull`) i Open WebUI rade u Composeu na korisničkoj mreži `backend`; alat Ollamu traži po DNS imenu `ollama-server`. Unit testovi se pokreću iz jednostavnog `Dockerfile.test` kao kratkoživući servis `tests` (rezultat je izlazni kod), a alat preko lanca `depends_on` čeka da backend bude zdrav. Blok završava pregledom svih DevOps datoteka u korijenu repozitorija. Kriteriji prihvaćanja su na vrhu [blok-c-vjezba.md](blok-c-vjezba.md).

| Datoteka | Sadržaj |
|---|---|
| [blok-a-predavanje.pptx](blok-a-predavanje.pptx) | Ponavljanje (jednostavni Dockerfile, od koda do slike u registru, SHA-256 i nepromjenjivost slike), Docker Compose (zašto, anatomija `compose.yaml`, projekt/servis/kontejner, naredbe, `depends_on` i `healthcheck`), umrežavanje (host, zadani bridge, korisnička mreža, DNS, objavljeni portovi), volumeni (sloj kontejnera, bind mount, imenovani volumen, životni vijek), dugoživući i kratkoživući kontejneri, `restart` i izlazni kod |
| [blok-b-vjezba.md](blok-b-vjezba.md) | Vježba: višefazni u jednostavni `Dockerfile`; `compose.yaml` s host mrežom; kod u slici vs bind mount vs imenovani volumen, podaci u imenovanom volumenu pregledani iz alpine kontejnera i prednosti u produkciji (`compose.storage.yaml`, na kraju se briše); predaja kao PR |
| [blok-c-vjezba.md](blok-c-vjezba.md) | Vježba: `ollama-server` s volumenom i `healthcheck`; zadani bridge vs korisnička mreža; `ollama-pull` i `depends_on`; lanac ovisnosti `llm` → `ollama-pull` → `ollama-server`; unit testovi u kontejneru (`Dockerfile.test`, servis `tests`, izlazni kod); Open WebUI; volumeni i `down`; predaja kao PR; pregled DevOps datoteka u korijenu repozitorija |
| [docker-lab/blok-b/](docker-lab/blok-b/) | Rješenje bloka B (modul): jednostavni `Dockerfile`, `compose.yaml` sa servisom `llm` |
| [docker-lab/blok-c/](docker-lab/blok-c/) | Rješenje bloka C (modul): konačni `compose.yaml` s Ollamom, Open WebUI-jem i servisom `tests`, `Dockerfile.test` |
| [docker-lab/paket/](docker-lab/paket/) | Isto za repozitorij koji je nakon tjedna 3 Python paket, stanje nakon bloka C: `Dockerfile`, `Dockerfile.test`, `pyproject.toml`, `compose.yaml` |

## Raspored bloka A (80 min)
| Cjelina | Slajdovi | Okvirno |
|---|---|---|
| Naslov, sadržaj | 1–2 | 3 min |
| Ponavljanje (Dockerfile, od koda do registra, SHA-256) | 3–6 | 15 min |
| Docker Compose: kako i zašto | 7–12 | 19 min |
| Umrežavanje | 13–17 | 16 min |
| Volumeni | 18–20 | 11 min |
| Dugoživući i kratkoživući kontejneri, ciljna arhitektura | 21–25 | 13 min |
| Provjera razumijevanja | 26 | 3 min |

## Raspored bloka B (80 min)
| Korak u [blok-b-vjezba.md](blok-b-vjezba.md) | Okvirno |
|---|---|
| Ishod vježbe, 0. Grana i priprema | 5 min |
| 1. Od višefaznog do jednostavnog Dockerfilea | 8 min |
| 2. Od `docker run` do `compose.yaml` | 12 min |
| 3. Odakle kontejneru kod i gdje žive podaci (slika, bind mount, imenovani volumen, alpine) | 40 min |
| 4. Pospremanje (`compose.storage.yaml`), provjere, commit i pull request | 15 min |

## Raspored bloka C (80 min)
| Korak u [blok-c-vjezba.md](blok-c-vjezba.md) | Okvirno |
|---|---|
| Ishod vježbe, 0. Grana i slike | 4 min |
| 1. Servis `ollama-server` | 7 min |
| 2. Mreže: zadani bridge, mreža projekta, korisnička mreža | 11 min |
| 3. `ollama-pull`, `depends_on` i lanac ovisnosti | 12 min |
| 4. Unit testovi u kontejneru: `Dockerfile.test` | 10 min |
| 5. Servis `tests` | 9 min |
| 6. Open WebUI | 8 min |
| 7. Volumeni | 4 min |
| 8. Provjere, commit i pull request | 9 min |
| 9. Pregled DevOps datoteka u korijenu repozitorija | 6 min |

## Priprema
- **Studenti, prije termina** (oko 5 GB preuzimanja, ne na nastavi):
  ```bash
  docker pull python:3.13-alpine alpine:3.24
  docker pull ollama/ollama:0.40.13
  docker pull ghcr.io/open-webui/open-webui:v0.7.2
  ollama pull llama3.2:1b        # Ollama on the host, for block B
  ```
- **Docker Desktop:** uključiti *Settings → Resources → Network → Enable host networking* (Docker Desktop 4.34+), potrebno za blok B.
- Polazište je stanje osobnog repozitorija nakon PR-a iz tjedna 3 (višefazni `Dockerfile` s fazama `base`, `test`, `runtime`, koji u koraku 1 bloka B postaje jednostavan, `requirements*.txt`, `tests/`, `version.txt`).

## Predaja (praktični zadatak 4)
- Blok B: otvoren pull request iz `feature/compose` u `main`, s `compose.txt` i `storage.txt` koji potvrđuju kriterije 1–5 (kriterij 6 provjerava se iz poruke commita i naslova PR-a).
- Blok C: otvoren pull request iz `feature/compose-ollama` (prema `feature/compose` dok PR iz bloka B nije spojen), s `compose.txt` koji potvrđuje kriterije 1–5 i snimkom zaslona Open WebUI-ja u opisu (kriterij 6 provjerava se iz poruke commita i naslova PR-a).

PR-ove ne spajati sami; ostaju otvoreni za pregled.
