# Vježba (40 min): koliko košta jedan VM za statičnu stranicu

Na predavanju smo vidjeli da GCP, AWS i Azure nude istu uslugu pod različitim imenima. Danas biramo stvarni VM za jedan (izmišljeni) sustav: najprije iz zahtjeva izračunamo koliko resursa treba, zatim nađemo najjeftiniji odgovarajući VM u GCP kalkulatoru i isti rang VM-a u AWS kalkulatoru.

> ### 🎯 Ishod vježbe
> U osobnom repozitoriju `praktikum-<github-korisnik>` otvoren je PR s grane `feature/vm-procjena` koji dodaje datoteku `docs/vm-procjena.md`: procjenu resursa iz zahtjeva, odabrani VM na GCP-u i njegov par na AWS-u s mjesečnom cijenom VM-a, diska i odlaznog prometa, poveznice na oba spremljena izračuna i odgovore na tri pitanja s kraja vježbe.
>
> **Kriteriji prihvaćanja:**
> 1. Tablica procjene (korak 2) ima disk, vršnu propusnost i mjesečni odlazni promet za oba scenarija (vlastiti streaming i YouTube embed), s računom, ne samo rezultatom.
> 2. GCP: VM iz serije E2 u regiji `europe-west8` (Milano), on-demand, 730 sati mjesečno; obrazloženo zašto nije manji i zašto nije veći tip.
> 3. AWS: VM iz obitelji `t3` (ili `t4g`) u regiji `eu-south-1` (Milano) s istim brojem vCPU-a i istom količinom RAM-a, uz provjerenu mrežnu propusnost.
> 4. Za oba providera posebno su navedene cijene VM-a, diska i odlaznog prometa, te ukupni mjesečni iznos.
> 5. Poveznice na spremljene izračune iz [GCP Pricing Calculatora](https://cloud.google.com/products/calculator) i [AWS Pricing Calculatora](https://calculator.aws/) (*Share*).
> 6. Odgovori na tri pitanja iz koraka 5.
>
> **Predaja:** PR iz `feature/vm-procjena` u `main`. Spaja ga nastavnik nakon pregleda.

| Sadržaj | Okvirno |
|---|---|
| 1. Zahtjevi sustava | 3 min |
| 2. Procjena resursa | 10 min |
| 3. GCP: odabir VM-a u kalkulatoru | 10 min |
| 4. AWS: isti rang VM-a | 10 min |
| 5. Usporedba i pitanja | 7 min |

---

## 1. Zahtjevi sustava

Klijent ima statičnu web stranicu i želi je poslužiti s jednog VM-a.

| Zahtjev | Vrijednost |
|---|---|
| Aplikacija | Next.js, statički export (`next build` s `output: "export"`): samo HTML, CSS, JS i mediji, bez Node.js poslužitelja |
| Broj stranica | najviše 20 |
| Videi | ukupno 1,4 GB, gledaju se kao stream u 1080p, oko 5 Mbit/s po gledatelju |
| Slike | ukupno 600 MB |
| Korisnici | najviše 100 dnevno, svi u New Yorku |
| Vršno opterećenje | najviše 20 istovremenih korisnika |
| Arhitektura | jedan VM, bez redundancije, bez CDN-a, bez load balancera |
| Rast sadržaja | nema, sadržaj je fiksan |
| Model plaćanja | on-demand (bez rezervacija, bez *committed use* i *spot* popusta) |
| Regija | najbliža Zagrebu |
| Alternativa | videi se ne poslužuju s VM-a, nego su ugrađeni s YouTubea (*YouTube embed*) |

Na VM-u radi samo web poslužitelj (npr. `nginx`) koji šalje gotove datoteke.

## 2. Procjena resursa

Popunite tablicu u `docs/vm-procjena.md`. Pokažite račun.

| Resurs | Kako izračunati | Vaša procjena |
|---|---|---|
| **Disk** | operacijski sustav + sadržaj (1,4 GB + 0,6 GB + build); zaokružiti na veličinu koju provider nudi | ~3 GB (Debian) + 2 GB sadržaja ≈ 5 GB → **20 GB** (10 GB je minimum i dovoljan, 20 GB ostavlja rezervu za logove i nadogradnje) |
| **Vršna propusnost** | istovremeni korisnici × bitrate videa | 20 × 5 Mbit/s = **100 Mbit/s** |
| **Odlazni promet mjesečno, streaming** | korisnici dnevno × podaci po korisniku × 30 dana | 100 × 2 GB × 30 = **6 000 GB** (~5 590 GiB) |
| **Odlazni promet mjesečno, YouTube embed** | isto, ali bez videa | 100 × 0,6 GB × 30 = **1 800 GB** (~1 680 GiB) |
| **vCPU** | koliko posla ima `nginx` koji šalje statične datoteke? | malo: `nginx` šalje gotove datoteke (`sendfile`), 100 Mbit/s je mali promet → **1 vCPU** ili shared-core dovoljan |
| **RAM** | OS + `nginx`; pomaže li da sadržaj stane u RAM (*page cache*)? | OS + `nginx` < 0,5 GB → **1–2 GB**; s 2 GB veći dio sadržaja ostaje u page cacheu (bonus, ne nužnost) |

**Pretpostavka za odlazni promet:** u najgorem slučaju svaki korisnik pogleda sve stranice i sve videe jednom, dakle preuzme sav sadržaj (2 GB sa streamingom, 0,6 GB s YouTube embedom). Ako pretpostavite nešto drugo, napišite što i zašto.

> 💡 Provjera: koliko minuta videa stane u 1,4 GB pri 5 Mbit/s? (1 GB = 8 000 Mbit.) Ako vam je rezultat manji od minute ili veći od deset sati, negdje je zalutala jedinica.
>
> **Rješenje:** 1,4 × 8 000 = 11 200 Mbit; 11 200 / 5 = 2 240 s ≈ **37 minuta** videa.

**Zašto je odlazni promet važan:** provideri ne naplaćuju dolazni promet, ali naplaćuju svaki GB koji VM pošalje na internet (*egress*). Kod streaminga videa to je obično najveća stavka na računu, veća od samog VM-a.

## 3. GCP: odabir VM-a u kalkulatoru

1. Otvorite [cloud.google.com/products/calculator](https://cloud.google.com/products/calculator) → *Add to estimate* → **Compute Engine**.
2. Postavite:
   - **Region:** `europe-west8` (Milano), najbliža Zagrebu.
   - **Operating system:** *Free: Debian, CentOS, ...*
   - **Provisioning model:** *Regular* (on-demand).
   - **Machine family:** *General purpose*, **Series:** `E2`.
   - **Hours per day:** 24, **Days per week:** 7 (oko 730 sati mjesečno).
   - **Boot disk:** *Balanced persistent disk*, veličina iz koraka 2.
3. Krenite od najmanjeg tipa (`e2-micro`) i idite prema većem (`e2-small`, `e2-medium`) dok tip ne zadovolji procjenu iz koraka 2. Za svaki pogledani tip zapišite vCPU, RAM i mjesečnu cijenu.
4. Dodajte odlazni promet: *Add to estimate* → **Networking** (*Cloud Networking / Network Service Tiers*), odlazni promet na internet iz `europe-west8`, količina iz koraka 2 (streaming). Usporedite **Standard** i **Premium** tier.
5. **Share** → kopirajte poveznicu u `docs/vm-procjena.md`.

> 💡 Sve cijene u vježbi pišemo u **USD**. Ako GCP kalkulator prikazuje drugu valutu, prebacite je na USD (izbornik valute); AWS kalkulator ionako prikazuje samo USD.

> 💡 Shared-core tipovi (`e2-micro`, `e2-small`, `e2-medium`) imaju 2 vCPU-a, ali trajno smiju koristiti samo dio njih (12,5 %, 25 %, 50 %) i kratko "puknuti" (*burst*) do punih 2 vCPU-a. Za `nginx` koji šalje statične datoteke to je obično dovoljno; zapišite zašto.

> ⚠️ Besplatni `e2-micro` (*Free Tier*) postoji samo u nekoliko američkih regija. U Milanu se plaća.

## 4. AWS: isti rang VM-a

1. Otvorite [calculator.aws](https://calculator.aws/) → *Create estimate* → **Amazon EC2**.
2. **Region:** *Europe (Milan)* `eu-south-1`.
3. **Operating system:** Linux; **Workload:** *Constant usage*, 730 h/mjesečno; **Pricing model:** *On-Demand*.
4. **Instance type:** u filteru upišite broj vCPU-a i količinu RAM-a vašeg GCP VM-a i odaberite najjeftiniji tip iz obitelji `t3` (Intel) ili `t4g` (ARM, Graviton). Ako izaberete `t4g`, provjerite postoji li u Milanu.
5. **Mrežna propusnost:** u [opisu tipova instanci](https://aws.amazon.com/ec2/instance-types/t3/) piše *Up to 5 Gigabit*. To je vršna vrijednost; burstable tipovi imaju i nižu **baznu** propusnost (*baseline*). Nađite baznu propusnost odabranog tipa u [dokumentaciji EC2](https://docs.aws.amazon.com/ec2/latest/instancetypes/gp.html#gp_network) i usporedite je s vršnom propusnošću iz koraka 2. Ako je bazna manja, uzmite veći tip i zapišite zašto.
6. **Storage:** EBS `gp3`, veličina iz koraka 2.
7. **Data transfer:** *Outbound Data Transfer → Internet*, količina iz koraka 2 (streaming).
8. **Share** → poveznica u `docs/vm-procjena.md`.

## 5. Usporedba i pitanja

Dodajte tablicu i odgovorite u `docs/vm-procjena.md`:

| | GCP | AWS |
|---|---|---|
| Tip VM-a (vCPU, RAM) | `e2-small` (2 vCPU shared, 2 GB) | `t3.small` (2 vCPU, 2 GiB) |
| VM mjesečno | ~$15 (`europe-west8`; provjeriti u kalkulatoru) | $0,0240/h × 730 = **$17,52** |
| Disk mjesečno | 20 GB balanced PD ≈ $2–2,5 | 20 GB gp3 ≈ $1,7–2 |
| Odlazni promet mjesečno, streaming | Standard tier: (5 590 − 200 GiB besplatno) × $0,085 ≈ **$458** | (6 000 − 100 GB besplatno) × ~$0,09 ≈ **$531** |
| Odlazni promet mjesečno, YouTube embed | (1 680 − 200) × $0,085 ≈ **$126** | (1 800 − 100) × ~$0,09 ≈ **$153** |
| **Ukupno, streaming** | **≈ $475** | **≈ $550** |
| **Ukupno, YouTube embed** | **≈ $145** | **≈ $172** |

Zašto `e2-small` i `t3.small`: `e2-micro` ima dovoljno CPU-a, ali `t3.micro` ima baznu mrežnu propusnost oko 64 Mbit/s, manje od potrebnih 100 Mbit/s; `t3.small` ima oko 128 Mbit/s. Da bi par bio istog ranga, na GCP-u uzimamo `e2-small`. Veći tip (`e2-medium`, `t3.medium`) nije potreban jer ni CPU ni RAM nisu usko grlo.

> Cijene su snimka od 24. 11. 2026. (USD, on-demand, Linux) i služe kao orijentir; vaše brojke iz kalkulatora mogu se razlikovati.

1. **Koja je stavka najskuplja i koliko puta je skuplja od VM-a?** Što bi se dogodilo s računom da stranica postane popularna (1 000 korisnika dnevno)?

   **Odgovor:** odlazni promet, ~$460–530 mjesečno, oko 25–30 puta više od VM-a (~$15–18). Uz 1 000 korisnika dnevno promet raste na ~60 TB mjesečno (~$4 000–5 000), a vršna propusnost na 200 × 5 Mbit/s = 1 Gbit/s, što jedan mali VM ne može poslužiti. Rješenje tada nije veći VM, nego CDN ili video platforma.
2. **Svi korisnici su u New Yorku, a VM je u Milanu.** Koliko otprilike iznosi latencija (slajd 13; izmjerite na [gcping.com](https://gcping.com))? Smeta li to gledanju videa koji se bufferira? Smeta li učitavanju stranice? Što biste preporučili klijentu i koji razlog bi mogao opravdati regiju u Europi?

   **Odgovor:** oko 90–110 ms RTT. Video koji se bufferira to jedva osjeti (samo pri pokretanju i premotavanju), ali učitavanje stranice osjeti svaki round trip (TCP, TLS, HTML, resursi), pa je stranica sporija za ~0,3–0,5 s. Preporuka je regija uz korisnike, npr. `us-east4` (Sjeverna Virginija), koja je obično i jeftinija. Europu bi mogla opravdati obveza da podaci ostanu u EU ili tim i ostala infrastruktura u EU; za javni statični sadržaj to je slab razlog.
3. **Što se mijenja s YouTube embedom?** Koliko se smanjuje račun, mijenja li se tip VM-a i disk, i što klijent gubi tom odlukom?

   **Odgovor:** odlazni promet pada za ~70 % (s ~$460–530 na ~$125–155), pa ukupni račun pada s ~$475–550 na ~$145–170. Disk treba samo ~1 GB sadržaja, a VM može pasti na najmanji tip jer više ne šalje video. Klijent gubi kontrolu: YouTube reklame i preporuke uz video, kolačiće trećih strana (GDPR), ovisnost o uvjetima YouTubea i vlastitu analitiku gledanja.

---

## Domaća zadaća: usporedba cijena VM-ova u Excelu

Predložak: [vm-usporedba-predlozak.xlsx](vm-usporedba-predlozak.xlsx).

U list **Usporedba** za svaki od pet rangova upišite tip VM-a, vCPU, RAM i cijenu po satu na GCP-u, AWS-u i Azureu. Stupci *mjesečno* i *$ po GB RAM-a* računaju se sami. Rangovi:

| Rang | Opis | Prijedlog tipova (GCP / AWS / Azure) |
|---|---|---|
| 1. Najmanji | najmanji burstable VM s 1 GB RAM-a | `e2-micro` / `t3.micro` / `B1s` ili `B2ats_v2` |
| 2. Mali | 2 vCPU, 4 GB | `e2-medium` / `t3.medium` / `B2s` ili `B2als_v2` |
| 3. Opći | 2 vCPU, 8 GB, ne burstable | `e2-standard-2` ili `n4-standard-2` / `m7i.large` / `D2s_v5` |
| 4. Memorijski | 2 vCPU, 16 GB | `e2-highmem-2` ili `n4-highmem-2` / `r7i.large` / `E2s_v5` |
| 5. Najmanji GPU | najjeftiniji VM s jednim GPU-om | `n1-standard-4` + `T4` ili `g2-standard-4` (L4) / `g4dn.xlarge` (T4) / `NC4as_T4_v3` (T4) |

Pravila:
- Cijene u **USD**, **on-demand**, **Linux**, bez popusta.
- Regija: Milano (`europe-west8`, `eu-south-1`, *Italy North*). Ako tip ondje ne postoji (čest slučaj s GPU-ovima), uzmite najbližu europsku regiju u kojoj postoji i upišite je u stupac *Regija*.
- U stupac *Izvor* upišite URL stranice s cijenom, a u *Datum* dan kad ste je pročitali. Cijene se mijenjaju.
- Prijedlozi tipova nisu obvezni: smijete uzeti drugi tip, ako je istog ranga (vCPU, RAM) i to napišete u napomeni.

U listu **Pitanja** odgovorite (2 do 4 rečenice, uz brojke iz tablice):
1. Koji provider nudi najjeftiniji VM?
2. Kod kojeg providera je najjeftinije iznajmiti najmanji GPU?
3. Kod kojeg providera je najbolje iznajmiti memory-efficient VM i zašto?

**Predaja:** `docs/vm-usporedba.xlsx` u istom PR-u (`feature/vm-procjena`), prije sljedećeg termina.
