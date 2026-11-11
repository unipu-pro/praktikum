# Blok A, vježba: kolaborativno programiranje u zajedničkom repozitoriju

Cilj: svaki student na svojoj grani doda jednu datoteku i jedan prazan commit, otvori pull request prema `main`, a nositelj spaja PR-ove različitim strategijama (rebase, squash, merge commit) tako da svi na istoj povijesti vide razliku. Vježba se radi u WSL-u ili na macOS-u/Linuxu iz tjedna 1.

| Sadržaj |
|---|
| 0. Priprema repozitorija (nositelj, prije termina) |
| 1. Kloniranje zajedničkog repozitorija |
| 2. Vlastita grana |
| 3. Skripta `add_contribution.sh` |
| 4. Push i pull request |
| 5. Spajanje uživo i `git log --graph` |
| 6. Zaostala grana: rebase i `--force-with-lease` (vježba) |

> **Windows:** ime datoteke sadrži `:` (npr. `2026-10-20T10:15:42.txt`), a dvotočka nije dopuštena u imenima datoteka na Windowsu. Kloniranje s Git for Windows (PowerShell, Git Bash, GitHub Desktop) završi greškom `error: invalid path '2026-10-20T10:15:42.txt'` i checkout ne uspije. Raditi isključivo u WSL-u (`~/`, ne `/mnt/c/...`), na macOS-u ili Linuxu.

## 0. Priprema repozitorija (nositelj, prije termina)
Repozitorij je prazan, samo s `README.md`, da grana `main` postoji i da se na nju može postaviti zaštita.
```bash
ORG=unipu-pro
REPO=shared-collab
TEAM=students            # team slug of the students in the organisation

gh repo create "$ORG/$REPO" --public --add-readme \
  --description "Week 2: collaborative programming exercise"
gh repo edit "$ORG/$REPO" --enable-merge-commit --enable-squash-merge \
  --enable-rebase-merge --delete-branch-on-merge

# RBAC: students may push branches and open PRs (Write = "push" in the API)
gh api -X PUT "orgs/$ORG/teams/$TEAM/repos/$ORG/$REPO" -f permission=push

# Branch protection on main: PR required, 1 approval, no force push, no deletion
gh api -X PUT "repos/$ORG/$REPO/branches/main/protection" --input - <<'JSON'
{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": { "required_approving_review_count": 1 },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
```
Skriptu `add_contribution.sh` podijeliti studentima (repozitorij kolegija ili poveznica), ne stavljati je u `shared-collab`.

`enforce_admins: false` znači da nositelj (Admin) može spojiti PR bez tuđeg odobrenja; studenti ne mogu odobriti vlastiti PR.

## 1. Kloniranje zajedničkog repozitorija
```bash
cd ~
gh repo clone unipu-pro/shared-collab
cd shared-collab
git log --oneline          # one commit: "Initial commit"
git branch -a              # local main + remote origin/main
```

## 2. Vlastita grana
Ime grane slijedi konvenciju `feature/<github-korisnik>`; tako se iz popisa grana odmah vidi tko na čemu radi.
```bash
GITHUB_USERNAME=$(gh api user -q .login)
git checkout -b "feature/$GITHUB_USERNAME"
git branch                 # * marks the current branch (HEAD)
```

## 3. Skripta `add_contribution.sh`
Kopirati skriptu u `~` (ne u repozitorij) i pokrenuti je iz repozitorija:
```bash
bash ~/add_contribution.sh
```
Skripta:
- odbija rad na `main` (prvo napraviti granu, korak 2),
- stvara datoteku s imenom trenutnog vremena u zoni Europe/Zagreb, ISO 8601 do sekunde, bez milisekundi i bez oznake zone: `TZ=Europe/Zagreb date +%Y-%m-%dT%H:%M:%S` → `2026-10-20T10:15:42.txt`,
- u datoteku upisuje korisničko ime (`$USER`),
- radi commit `feat: add contribution from <user>` i prazan commit `chore: empty commit from <user>` (`git commit --allow-empty`).

Provjera:
```bash
ls *.txt
cat 2026-*.txt                       # your $USER
git log --oneline --graph            # 2 new commits above "Initial commit"
git show --stat HEAD                 # empty commit: no files changed
```
Pitanje za grupu: zašto nema konflikata iako svi rade na istom repozitoriju? (Svatko dodaje drugu datoteku; ime je vrijeme do sekunde.)

## 4. Push i pull request
Prvo provjeriti da zaštita grane radi:
```bash
git push origin HEAD:main            # expected: rejected, "protected branch hook declined"
```
Zatim push vlastite grane i PR:
```bash
git push -u origin HEAD
gh pr create --base main \
  --title "feat: add contribution from $USER" \
  --body "Week 2 collaboration exercise"
gh pr view --web
```
Na stranici PR-a pogledati karticu **Commits** (2 commita) i **Files changed** (1 datoteka).

## 5. Spajanje uživo i `git log --graph`
Nositelj dijeli ekran, odobrava (Review → Approve) i spaja prva tri PR-a s tri različita gumba:

| PR | Gumb | Što se pojavi na `main` |
|---|---|---|
| 1 | Rebase and merge | 2 commita, s novim hashevima |
| 2 | Squash and merge | 1 commit (naslov PR-a postaje poruka) |
| 3 | Create a merge commit | 2 commita s grane + merge commit s dva roditelja |

Ostale PR-ove nositelj spaja strategijom kolegija: **fast-forward kad je moguć, inače merge commit**. Upravo to radi `git merge` bez opcija. GitHubov gumb *Create a merge commit* uvijek radi merge commit (`--no-ff`), pa se spaja lokalno. GitHub PR sam označi kao *merged* čim se njegovi commitovi pojave na `main`:
```bash
git fetch origin
git checkout main && git pull
git merge origin/feature/<github-korisnik>   # fast-forward if main has not moved, otherwise a merge commit
git push origin main                        # admin bypasses branch protection (enforce_admins: false)
```
Nakon svakog spajanja svi povlače `main`:
```bash
git checkout main
git pull                             # output says: Fast-forward
git log --graph --oneline --all
```
Usporediti graf s vizualizacijama iz predavanja: gdje je ravna linija, gdje je račvanje i merge commit, i koliko je commitova svaki PR dodao.

## 6. Zaostala grana: rebase i `--force-with-lease`
Svaki spojeni PR pomiče `main`, pa su ostale grane "iza". Na stranici PR-a vidi se *This branch is out-of-date with the base branch*. Za strategiju kolegija to nije problem (spajanje tada napravi merge commit), ali ovdje vježbamo rebase vlastite grane kao alternativu:
```bash
git checkout "feature/$GITHUB_USERNAME"
git log --oneline -2                 # note the two hashes
git fetch origin
git rebase origin/main               # replay your 2 commits on top of the new main
git log --oneline -2                 # same messages, NEW hashes
git push --force-with-lease          # a normal push is rejected: history was rewritten
```
`--force-with-lease` prepisuje granu samo ako na njoj u međuvremenu nema tuđih commitova; običan `--force` bi ih tiho obrisao. Rebase i force push rade se **samo na vlastitoj grani**, nikad na `main`.

## Predaja
Spojen PR u `shared-collab` s vlastitom datotekom (vidljivo u `git log --oneline -- 2026-*.txt`).

## Česti problemi
| Simptom | Rješenje |
|---|---|
| `error: invalid path '2026-...T..:..:...txt'` | Repozitorij je kloniran izvan WSL-a (Git for Windows). Klonirati u WSL-u u `~/` |
| `ERROR: you are on 'main'` | `git checkout -b feature/<github-korisnik>` pa ponovno pokrenuti skriptu |
| `protected branch hook declined` | Očekivano za push na `main`; pushati vlastitu granu i otvoriti PR |
| `gh pr create`: *must first push the current branch* | `git push -u origin HEAD` |
| `! [rejected] (non-fast-forward)` nakon rebasea | `git push --force-with-lease` |
| Rebase stane s konfliktom | Isto ime datoteke (isti trenutak): `git rebase --abort`, obrisati commitove s `git reset --hard origin/main` i ponovno pokrenuti skriptu |
| `403` pri pushu | Student nije u timu `students` ili tim nema Write na repozitoriju |
