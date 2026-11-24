# Tjedan 6: CI/CD workflowi i cloud provideri

Termin: blok A, CI vježba (80 min) + pauza + blok B, predavanje o cloud providerima (40 min) i vježba s cjenicima (40 min).

> **Ishod vježbe:** u osobnom repozitoriju `praktikum-<github-korisnik>` spojen PR s grane `feature/cicd`: stari workflowi obrisani, a `ci.yml` (`test-module`, `test-container`, `build-image`), `deploy.yml` (`build-image`, `deploy`) i `release.yml` (`build-image`, `call-deploy`) napisani iz početka; slike `:<grana>`, `:dev`, `:vX.Y.Z`, `:latest` i `:<SHA>` na `ghcr.io/unipu-pro/praktikum-llm-<github-korisnik>`; okruženja `dev` i `prod`. Kriteriji prihvaćanja su na vrhu [blok-a-vjezba.md](blok-a-vjezba.md).

| Datoteka | Sadržaj |
|---|---|
| [blok-a-vjezba.md](blok-a-vjezba.md) | Vježba: 0. brisanje starih workflowa; 1. `ci.yml` s tri joba i ruleset; 2. `deploy.yml`, okruženja `dev` i `prod`, grana `dev`, cache sa `:dev`; 3. `release.yml`, most iz `release_please.yml`, izdanje s tri taga i isporuka u `prod`; dva pitanja za razumijevanje |
| [cicd-workflows.png](cicd-workflows.png) | Dijagram tri workflowa, njihovih jobova i taga slike koji svaki job objavljuje (izvor: `cicd-workflows.svg`) |
| [cicd-lab/](cicd-lab/) | Rješenje: stanje repozitorija nakon vježbe (`.github/workflows/ci.yml`, `deploy.yml`, `release.yml`, `release_please.yml`) |
| [blok-b-predavanje.pptx](blok-b-predavanje.pptx) | Predavanje (40 min): data centri, zone i regije, iste usluge na GCP-u, AWS-u i Azureu (VM, tajne, baza, kontejneri bez poslužitelja), latencija, replikacija i disaster recovery, Portal/CLI/REST/HCL, demo izrade VM-a u portalu, provjera razumijevanja |
| [blok-b-vjezba.md](blok-b-vjezba.md) | Vježba (40 min): zahtjevi statične Next.js stranice, procjena diska, propusnosti i odlaznog prometa, izbor VM-a u GCP kalkulatoru (`europe-west8`) i istog ranga u AWS kalkulatoru (`eu-south-1`); domaća zadaća: usporedba cijena VM-ova pet rangova na GCP-u, AWS-u i Azureu |
| [vm-usporedba-predlozak.xlsx](vm-usporedba-predlozak.xlsx) | Predložak za domaću zadaću: list *Usporedba* (cijene, mjesečni iznos i $ po GB RAM-a računaju se sami) i list *Pitanja* |

## Raspored vježbe (80 min)
| Korak u [blok-a-vjezba.md](blok-a-vjezba.md) | Okvirno |
|---|---|
| 0. Polazište: brisanje starih workflowa | 5 min |
| 1. `ci.yml`: testovi modula, testovi u kontejneru, slika grane; ruleset | 25 min |
| 2. `deploy.yml`: okruženja, grana `dev`, cache sa `:dev` | 20 min |
| 3. `release.yml`: izdanje s tri taga, isporuka u `prod` | 25 min |
| Rezerva | 5 min |

## Raspored vježbe u bloku B (40 min)
| Korak u [blok-b-vjezba.md](blok-b-vjezba.md) | Okvirno |
|---|---|
| 1. Zahtjevi sustava | 3 min |
| 2. Procjena resursa | 10 min |
| 3. GCP: odabir VM-a u kalkulatoru | 10 min |
| 4. AWS: isti rang VM-a | 10 min |
| 5. Usporedba i pitanja | 7 min |

## Priprema
- **Studenti:** `gh auth refresh -s workflow,read:packages`; PR iz tjedna 5 spojen ili zatvoren.
- Polazište je `main` osobnog repozitorija s `Dockerfile`, `Dockerfile.test`, testovima i rulesetom `protect-main` iz tjedna 5.

## Predaja (praktični zadatak 6)
Spojen PR iz `feature/cicd` s odgovorima na pitanja za razumijevanje u opisu PR-a; uspješna pokretanja `ci`, `deploy` (grana `dev`) i `release-please` s izdanjem i isporukom u `prod`.

Vježba u bloku B: PR iz `feature/vm-procjena` s `docs/vm-procjena.md` (procjena, izbor VM-a na GCP-u i AWS-u, poveznice na izračune, odgovori na pitanja). Domaća zadaća: `docs/vm-usporedba.xlsx` u istom PR-u, do sljedećeg termina.
