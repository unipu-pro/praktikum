# Tjedan 5: GitHub Actions

Termin: blok A (predavanje, 80 min) + pauza + vježbe (90 min: uvod i dva dijela).
Ishodi učenja koje tjedan pokriva: 1 (prepoznati koncepte i alate: CI/CD, GitHub Actions, runneri, artefakti, registar slika), 2 (razlikovati okruženja: lokalno, runner na GitHubu, kontejner), 3 (primijeniti alate na vlastitom repozitoriju: workflowi za testove i Docker sliku na `ghcr.io`), 5 (evaluirati rješenje: sigurnost autentikacije i akcija, status provjera na PR-u, trošak minuta).

> **Ishod bloka A:** student zna objasniti što je kontinuirana integracija i gdje je GitHub Actions među CI/CD alatima u 2026., procijeniti trošak minuta, pročitati i napisati workflow (događaji, runneri, efemerni strojevi, jobovi, koraci, ulazi i izlazi, artefakti), odabrati siguran način autentikacije (`GITHUB_TOKEN`, tajne, OIDC) i procijeniti kada koristiti gotov softver (Open WebUI), a kada forkati OSS projekt.
>
> **Ishod vježbi:** u osobnom repozitoriju `praktikum-<github-korisnik>` dva pull requesta: `feature/actions-hello` (Open WebUI `v0.13.3` i workflow `hello`, spojen) i `feature/ci` (`Dockerfile.test` i workflow `ci`, otvoren, sve provjere zelene, slika `ghcr.io/unipu-pro/praktikum-llm-<github-korisnik>:<SHA commita>` objavljena; ruleset `protect-main`). Kriteriji prihvaćanja su na vrhu svakog dijela u [blok-b-vjezba.md](blok-b-vjezba.md).

| Datoteka | Sadržaj |
|---|---|
| [blok-a-predavanje.pptx](blok-a-predavanje.pptx) | Ponavljanje (četiri pitanja o `compose.yaml` i odgovori na jednoj slici), CI i CI/CD/CD, karta CI/CD alata u 2026., cjenik GitHub Actions, anatomija workflowa, događaji, runneri (hosted, larger, self-hosted), efemerni strojevi, jobovi (`needs`, matrica, `if`), ulazi i izlazi (koraci, jobovi, `workflow_dispatch`, `workflow_call`), konteksti i script injection, autentikacija (`GITHUB_TOKEN`, tajne, OIDC), artefakti i cache, često korištene akcije, lanac opskrbe (zapinjanje, Dependabot), Open WebUI kao tuđi softver, fork OSS-a, provjera razumijevanja |
| [blok-b-vjezba.md](blok-b-vjezba.md) | Vježbe: 0. pregled svih datoteka u repozitoriju; 0b. Open WebUI `v0.7.2` → `v0.13.3` (bilješke izdanja, sigurnosna kopija volumena); 1. anatomija workflowa (`hello.yml`); 2. Python CI, Docker build, testovi u slici i push slike na `ghcr.io` s tagom SHA commita (`ci.yml`, `GITHUB_TOKEN`, `packages: write`), ruleset: merge tek uz zelen CI |
| [actions-lab/](actions-lab/) | Rješenje: stanje repozitorija nakon oba dijela (`.github/workflows/hello.yml`, `ci.yml`, `Dockerfile.test`, `compose.yaml` s Open WebUI `v0.13.3`) |

## Raspored bloka A (80 min)
| Cjelina | Slajdovi | Okvirno |
|---|---|---|
| Naslov, sadržaj | 1–2 | 3 min |
| Ponavljanje: četiri pitanja i odgovori | 3–5 | 10 min |
| CI i alati u 2026., cjenik | 6–10 | 14 min |
| Anatomija GitHub Actions | 11–20 | 22 min |
| Autentikacija, artefakti | 21–24 | 12 min |
| Gotove akcije i lanac opskrbe | 25–27 | 8 min |
| Tuđi softver i OSS, što gradimo | 28–31 | 8 min |
| Provjera razumijevanja | 32 | 3 min |

## Raspored vježbi (90 min)
| Korak u [blok-b-vjezba.md](blok-b-vjezba.md) | Okvirno |
|---|---|
| 0. Polazište i pregled svih datoteka u repozitoriju | 8 min |
| 0b. Open WebUI: pregled zadnjih slika i nadogradnja na `v0.13.3` | 7 min |
| 1. Anatomija workflowa: hello world, kontekst, izlazi, PR, spajanje, `workflow_dispatch` | 25 min |
| 2. `Dockerfile.test`, `ci.yml` (testovi, Docker, push na `ghcr.io`), crveno pa zeleno, ruleset: merge tek uz zelen CI | 50 min |

## Priprema
- **Studenti, prije termina:**
  - `docker pull ghcr.io/open-webui/open-webui:v0.13.3` (oko 1,5 GB),
  - `gh auth refresh -s workflow` (bez opsega `workflow` push datoteka u `.github/workflows/` bude odbijen).
- Polazište je `main` osobnog repozitorija s spojenim PR-ovima iz tjedna 4 (`compose.yaml` s `ollama-server`, `ollama-pull`, `open-webui`, `llm` na mreži `backend`). Dodatni zadatak s paketom iz tjedna 3 (`src/praktikum_llm`) ovaj tjedan se ne koristi.

## Predaja (praktični zadatak 5)
- Dio 1: spojen PR iz `feature/actions-hello`; uspješna pokretanja `hello` za `push`, `pull_request` i `workflow_dispatch`.
- Dio 2: **otvoren** PR iz `feature/ci` sa zelenim provjerama `test` i `docker` te crvenim pokretanjima u povijesti; slika `ghcr.io/unipu-pro/praktikum-llm-<github-korisnik>:<SHA commita>` u *Packages*; aktivan ruleset `protect-main` (obavezan PR, obavezne provjere `test` i `docker`). Taj PR ne spajati sami.

PR iz dijela 1 se spaja jer `workflow_dispatch` radi samo s datotekom workflowa na zadanoj grani.
