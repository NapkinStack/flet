# Legal scoping request — flet

> **This document is in French, by exception.** Its only purpose is to be sent to a lawyer,
> and the operator is established in France. The rest of the repository is in English. It is
> the deliverable of test **5.2 — viability (B)** of `discovery.md`, and it must be sent
> **before** the value test, because the value test performs the act this opinion is meant to
> qualify.
>
> **Version 2, 2026-09-21.** Version 1 described a single French community and was wrong: the
> product is an open platform any administrator installs (`discovery.md`, section 6, round 2).
> The questions below are not the same questions.

---

## Objet

Nous demandons une **opinion écrite de cadrage** sur la licéité, en droit français et
européen, du service décrit ci-dessous, **avant tout développement**. Nous ne demandons ni
montage, ni rédaction contractuelle : seulement une réponse aux huit questions de la
section 4.

## 1. Les faits

Chaque fait est marqué **[établi]** s'il est vérifié sur la documentation de la plateforme
d'exécution ou décidé par nous, **[hypothèse]** s'il reste à confirmer.

### Le produit

- **[établi]** flet est un **bot installable librement** sur n'importe quel serveur Discord
  ou canal Telegram. Ce n'est pas un service vendu à une communauté identifiée : c'est une
  plateforme que **n'importe quel administrateur de serveur peut installer de lui-même**.
- **[établi]** Une fois installé, **l'administrateur de ce serveur** — et non nous — établit
  la liste des traders que les membres de son serveur pourront copier. Les membres peuvent
  proposer et voter ; l'administrateur garde un droit de veto. **La liste finale est la
  sienne.**
- **[établi]** Ces administrateurs forment un **ensemble ouvert que nous ne choisissons pas
  et ne contrôlons pas**. Ils ne sont pas rémunérés et n'ont aucun lien contractuel avec nous
  au-delà des conditions d'utilisation du bot.
- **[établi]** Un membre choisit un trader dans la liste de son serveur. Les ordres de ce
  trader sont ensuite **répliqués automatiquement** sur le compte du membre, **sans
  intervention du membre à chaque ordre**.
- **[hypothèse]** Les membres résident dans des pays que nous **ne connaissons pas à
  l'avance** et que rien, en l'état, ne restreint. Le premier serveur visé est francophone,
  mais le produit est ouvert.

### L'exécution et l'argent

- **[établi]** Le lieu d'exécution est **Hyperliquid**, une plateforme de **contrats
  perpétuels** — instruments dérivés à effet de levier. Elle n'est ni établie ni agréée dans
  l'Union européenne.
- **[établi]** Les conditions de cette plateforme excluent des « Restricted Persons » :
  notamment les résidents des États-Unis et de l'Ontario, et les citoyens américains où
  qu'ils soient.
- **[établi]** **Aucune garde de fonds.** Les fonds restent sur le compte Hyperliquid du
  membre, ouvert à son nom. Le membre signe une autorisation unique, avec son portefeuille
  principal, enregistrant une **clé secondaire** que nous détenons et qui peut passer et
  annuler des ordres sur son compte. Le membre peut la révoquer à tout moment.
- **[hypothèse, solide]** Cette clé **ne peut pas retirer ni transférer** les fonds : le
  format des actions de retrait et de virement de la plateforme ne comporte aucun champ
  permettant d'agir pour le compte d'un tiers. Constat tiré de la documentation ; non vérifié
  par un essai.
- **[établi]** **Rémunération.** La plateforme d'exécution prélève elle-même une commission
  sur les ordres que nous routons et nous la crédite. Elle est **plafonnée à 0,1 % du
  notionnel**. Aucun flux financier ne transite par nous. Les administrateurs ne perçoivent
  rien.
- **[établi]** L'opérateur — nous — est une **personne physique établie en France, sans
  agrément**.

## 2. Les parties à qualifier

Trois, et nous avons besoin d'une réponse distincte pour chacune :

1. **L'opérateur de la plateforme** : fournit le logiciel, route les ordres, perçoit la
   commission. **Ne choisit aucun trader.**
2. **Chaque administrateur de serveur** : installe le bot et sélectionne les traders
   copiables. Bénévole. Ensemble ouvert.
3. **Les traders copiés** : tradent leur propre compte. Ils ne reçoivent rien de nous et
   n'ont, à ce stade, aucune relation avec nous.

## 3. Le contexte que nous croyons pertinent

Sans préjuger de votre analyse, pour que vous sachiez ce que nous avons déjà lu :

- La note de supervision de l'ESMA sur le copy trading (ESMA35-42-1428, 30 mars 2023) range
  ces services sous la **gestion de portefeuille ou le conseil en investissement**, et ses
  attentes portent notamment sur « les qualifications des traders dont les transactions sont
  copiées ».
- Les contrats perpétuels ne relèvent pas de MiCA mais de **MiFID II**.
- La promotion de services sur actifs numériques par un prestataire non enregistré est
  restreinte, et la loi n° 2023-451 du 9 juin 2023 a étendu ce régime aux réseaux sociaux.

## 4. Les questions

**Q1 — L'opérateur.** Fournissons-nous un **service d'investissement** alors que nous ne
sélectionnons aucun trader, que la sélection est faite par des tiers que nous ne contrôlons
pas, et que nous ne détenons ni les fonds ni la clé principale du client ? Sommes-nous
prestataire, ou fournisseur d'un outil technique ? Si prestataire : lequel, et quel agrément ?

**Q2 — Les administrateurs.** Chaque administrateur qui installe le bot et choisit les
traders copiables fournit-il lui-même un service d'investissement ? Le bénévolat change-t-il
la qualification ? Et surtout : **sommes-nous responsables de ce qu'ils font** — en tant que
fournisseur de l'outil, en tant que bénéficiaire économique de leur activité, ou pas du tout ?

**Q3 — La variante manuelle.** Si la copie n'était pas automatique, le membre validant chaque
ordre après notification, la qualification change-t-elle — et sort-elle du champ de
l'agrément, ou bascule-t-elle simplement du portefeuille au conseil ?

**Q4 — La territorialité, qui est notre question la plus lourde.** Le produit est ouvert : un
administrateur de n'importe quel pays peut l'installer, et ses membres résident où ils
veulent. **Quelles obligations en découlent pour nous ?** Devons-nous connaître le pays de
résidence de chaque membre, le restreindre, l'avertir ? Un agrément obtenu dans un seul État
membre nous couvrirait-il ailleurs par passeport européen, et à quelles conditions ?

**Q5 — Les exclusions de la plateforme d'exécution.** Celle-ci exclut les personnes
américaines et ontariennes. Devons-nous faire respecter cette exclusion pour notre propre
compte, et avec quels moyens — déclaration sur l'honneur, géoblocage, vérification
d'identité ?

**Q6 — La promotion par des tiers.** Chaque administrateur annonce le service à ses membres,
sans que nous le lui demandions et sans rémunération. Cette annonce relève-t-elle de la
publicité ou du démarchage pour un service non enregistré ? Le régime issu de la loi sur les
influenceurs s'y applique-t-il ? **Et sommes-nous responsables d'une promotion faite par des
tiers que nous n'avons pas mandatés ?**

**Q7 — Les aménagements.** Existe-t-il une construction praticable à l'échelle d'une
plateforme ouverte : restriction géographique à l'installation, changement de statut,
adossement à un établissement agréé ? Si vous en voyez une, un ordre de grandeur de coût et
de délai nous est très utile.

**Q8 — Le mode de rémunération, en tant que tel.** Nous prélevons une commission sur le
**volume routé**, jamais sur les gains du membre. C'est une décision arrêtée et nous
n'envisageons pas de partage des gains : la question n'est donc pas de choisir, mais de
savoir si **ce mode de rémunération contribue lui-même à la qualification**. Être payé à
l'acte de routage plutôt qu'à la performance change-t-il quelque chose au statut, dans un
sens ou dans l'autre ?

## 5. Ce que nous ne demandons pas

Pour tenir le périmètre et le budget : ni rédaction de conditions générales, ni montage de
structure, ni fiscalité, ni analyse pays par pays de l'Union. Une opinion écrite sur les huit
questions suffit à cette étape.

## 6. Ce que votre réponse décide

Rien n'est développé avant votre réponse. Une réponse « agrément requis », pour nous **ou**
pour les administrateurs, sans aménagement tenable dans notre budget, **arrête le projet** —
elle ne le reporte pas. C'est écrit comme tel dans notre document de découverte, et c'est
pourquoi nous vous écrivons avant d'avoir construit quoi que ce soit plutôt qu'après.
