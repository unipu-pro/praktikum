# Tjedan 4: Docker Compose i testovi

Termin: 180 min = blok A (80 min) + pauza (20 min) + blok B (80 min). Blok C (Ollama i Open WebUI u Composeu, 80 min) je zaseban blok vježbi koji se nastavlja na blok B.
Ishodi učenja koje tjedan pokriva: 1 (prepoznati koncepte i alate: Docker Compose, mreže, volumeni), 2 (razlikovati okruženja: isti testovi protiv Ollame na hostu i u kontejneru, konfiguracija iz okoline), 5 (evaluirati rješenje: izlazni kod testova, izloženost portova, trajnost podataka).

> **Ishod bloka A:** student zna objasniti kako iz koda nastaje slika i kada je treba ponovno izgraditi i objaviti, zašto više kontejnera opisujemo u `compose.yaml`, kako se servisi pronalaze na mreži (host, zadani bridge, korisnička mreža i DNS), gdje podaci prežive kontejner (bind mount, imenovani volumen) i po čemu se razlikuju dugoživući i kratkoživući kontejneri.
>
> **Ishod bloka B:** otvoren pull request `feature/compose` u `praktikum-<github-korisnik>`: slika se gradi iz jednostavnog `Dockerfile`a (jedna faza), student pokaže razliku između koda u slici, bind mounta i imenovanog volumena te podatke u imenovanom volumenu pročita iz praznog alpine kontejnera, alat i testovi su servisi u `compose.yaml` na host mreži, testovi se pokreću iz jednostavnog `Dockerfile.test`, uz unit testove postoje 3 integracijska testa protiv prave Ollame; student zna objasniti razliku između unit i integracijskih testova i pokazati da integracijski testovi padaju kad backend ne radi. Kriteriji prihvaćanja su na vrhu [blok-b-vjezba.md](blok-b-vjezba.md).
>
> **Ishod bloka C:** otvoren pull request `feature/compose-ollama`: Ollama (`ollama-server`), jednokratno preuzimanje modela (`ollama-pull`) i Open WebUI rade u Composeu na korisničkoj mreži `backend`; testovi i alat Ollamu traže po DNS imenu `ollama-server` i preko `depends_on` čekaju da backend bude zdrav, a modeli su u imenovanom volumenu. Kriteriji prihvaćanja su na vrhu [blok-c-vjezba.md](blok-c-vjezba.md).

| Datoteka | Sadržaj |
|---|---|
| [blok-a-predavanje.pptx](blok-a-predavanje.pptx) | Ponavljanje (jednostavni Dockerfile, od koda do slike u registru, SHA-256 i nepromjenjivost slike), Docker Compose (zašto, anatomija `compose.yaml`, projekt/servis/kontejner, naredbe, `depends_on` i `healthcheck`), umrežavanje (host, zadani bridge, korisnička mreža, DNS, objavljeni portovi), volumeni (sloj kontejnera, bind mount, imenovani volumen, životni vijek), dugoživući i kratkoživući kontejneri, `restart` i izlazni kod |
| [blok-b-vjezba.md](blok-b-vjezba.md) | Vježba: višefazni u jednostavni `Dockerfile`; `compose.yaml` s host mrežom; kod u slici vs bind mount vs imenovani volumen, podaci u imenovanom volumenu pregledani iz alpine kontejnera i prednosti u produkciji (`compose.storage.yaml`); `Dockerfile.test`; unit vs integracijski testovi i marker; testovi u Composeu i ovisnost o backendu (što kad Ollama ne radi); predaja kao PR |
| [blok-c-vjezba.md](blok-c-vjezba.md) | Vježba: `ollama-server` s volumenom i `healthcheck`; zadani bridge vs korisnička mreža; `ollama-pull` i `depends_on`; testovi po DNS imenu i lanac ovisnosti `tests` → `ollama-pull` → `ollama-server`; Open WebUI; volumeni i `down`; predaja kao PR |
| [docker-lab/blok-b/](docker-lab/blok-b/) | Rješenje bloka B (modul): jednostavni `Dockerfile`, `compose.yaml`, `compose.storage.yaml`, `Dockerfile.test`, `pytest.ini`, `tests/` |
| [docker-lab/blok-c/](docker-lab/blok-c/) | Rješenje bloka C (modul): konačni `compose.yaml` s Ollamom i Open WebUI-jem |
| [docker-lab/paket/](docker-lab/paket/) | Isto za repozitorij koji je nakon tjedna 3 Python paket: `Dockerfile.test`, `pyproject.toml`, `tests/test_integration.py`, `compose.yaml` bloka B |

## Raspored bloka A (80 min)
| Cjelina | Slajdovi | Okvirno |
|---|---|---|
| Naslov, ishod, sadržaj | 1–3 | 3 min |
| Ponavljanje (Dockerfile, od koda do registra, SHA-256) | 4–7 | 15 min |
| Docker Compose: kako i zašto | 8–13 | 19 min |
| Umrežavanje | 14–18 | 16 min |
| Volumeni | 19–21 | 11 min |
| Dugoživući i kratkoživući kontejneri, ciljna arhitektura | 22–26 | 13 min |
| Provjera razumijevanja | 27 | 3 min |

## Raspored bloka B (80 min)
| Korak u [blok-b-vjezba.md](blok-b-vjezba.md) | Okvirno |
|---|---|
| Ishod vježbe, 0. Grana i priprema | 4 min |
| 1. Od višefaznog do jednostavnog Dockerfilea | 6 min |
| 2. Od `docker run` do `compose.yaml` | 8 min |
| 3. Odakle kontejneru kod i gdje žive podaci (slika, bind mount, imenovani volumen, alpine) | 24 min |
| 4. Jednostavni Dockerfile za testove | 8 min |
| 5. Integracijski testovi | 10 min |
| 6. Testovi u Composeu i ovisnost o backendu | 12 min |
| 7. Provjere, commit i pull request | 8 min |

## Raspored bloka C (80 min)
| Korak u [blok-c-vjezba.md](blok-c-vjezba.md) | Okvirno |
|---|---|
| Ishod vježbe, 0. Grana i slike | 5 min |
| 1. Servis `ollama-server` | 10 min |
| 2. Mreže: zadani bridge, mreža projekta, korisnička mreža | 15 min |
| 3. `ollama-pull` i `depends_on` | 10 min |
| 4. Testovi protiv Ollame u kontejneru | 10 min |
| 5. Open WebUI | 10 min |
| 6. Volumeni | 5 min |
| 7. Provjere, commit i pull request | 15 min |

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
- Blok B: otvoren pull request iz `feature/compose` u `main`, s `compose.txt` i `storage.txt` koji potvrđuju kriterije 1–6 (kriterij 7 provjerava se iz poruke commita i naslova PR-a).
- Blok C: otvoren pull request iz `feature/compose-ollama` (prema `feature/compose` dok PR iz bloka B nije spojen), s `compose.txt` koji potvrđuje kriterije 1–5 i snimkom zaslona Open WebUI-ja u opisu (kriterij 6 provjerava se iz poruke commita i naslova PR-a).

PR-ove ne spajati sami; ostaju otvoreni za pregled.
