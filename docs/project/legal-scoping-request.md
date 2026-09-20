# Legal scoping request — flet

> **This document is in French, by exception.** Its only purpose is to be sent to a lawyer
> qualified in French law, and the launch country is France (`discovery.md`, section 6,
> round 2). The rest of the repository is in English. It is the deliverable of test
> **5.2 — viability (B)** of the discovery, and it must be sent **before** the value test,
> because the value test performs the act this opinion is meant to qualify.

---

## Objet

Nous demandons une **opinion écrite de cadrage** sur la licéité, en droit français, d'un
service décrit ci-dessous, **avant tout développement**. Nous ne demandons ni montage, ni
rédaction contractuelle : seulement une réponse aux six questions de la section 4.

## 1. Les faits

Chaque fait est marqué : **[établi]** quand il est vérifié sur la documentation de la
plateforme ou décidé par nous ; **[hypothèse]** quand il reste à confirmer.

- **[établi]** Le produit est un bot installé dans le serveur Discord d'une communauté
  existante. Il n'a pas d'existence hors de ce serveur.
- **[établi]** Le lancement vise une communauté dont les membres résident majoritairement en
  France. Une extension à l'étranger est envisagée plus tard et **n'entre pas** dans cette
  demande.
- **[établi]** Le lieu d'exécution est Hyperliquid, une plateforme de **contrats perpétuels**
  — donc des instruments dérivés à effet de levier. Elle n'est pas établie dans l'Union
  européenne et n'y est pas agréée. Ses conditions d'utilisation excluent notamment les
  personnes résidant aux États-Unis et en Ontario.
- **[établi]** L'**administrateur** du serveur — un membre de la communauté, bénévole —
  établit et tient la liste des traders que les membres sont autorisés à copier. Il la tient
  explicitement pour écarter les escrocs. Les membres peuvent proposer des traders et voter,
  mais l'administrateur conserve un **droit de veto** : la liste finale est la sienne.
- **[établi]** Les traders de la liste sont eux-mêmes membres de la communauté. Ils tradent
  leur propre compte ; le produit se contente de lire leurs positions, publiques sur la
  chaîne.
- **[établi]** Un membre choisit un ou plusieurs traders de la liste. Les ordres de ces
  traders sont ensuite **répliqués automatiquement** sur le compte du membre, **sans
  intervention du membre à chaque ordre**.
- **[établi]** **Aucune garde de fonds.** Les fonds restent sur le compte Hyperliquid du
  membre, ouvert à son nom. Le membre signe une autorisation unique, avec son portefeuille
  principal, qui enregistre une **clé secondaire** détenue par le produit ; cette clé peut
  passer et annuler des ordres sur son compte. Le membre peut la révoquer à tout moment.
- **[hypothèse, solide]** Cette clé secondaire **ne peut pas retirer ni transférer** les
  fonds du membre : le format des actions de retrait et de virement de la plateforme ne
  comporte aucun champ permettant d'agir pour le compte d'un tiers. Constat tiré de la
  documentation de la plateforme ; non vérifié par un essai.
- **[établi]** **Rémunération.** La plateforme prélève elle-même une commission sur les
  ordres routés par le produit et la crédite à celui-ci. Elle est **plafonnée à 0,1 % du
  notionnel** échangé. Aucun flux financier ne transite par le produit.
- **[établi]** L'**opérateur** — celui qui exploite le service et perçoit la commission — est
  une **personne physique, sans agrément**.
- **[établi]** L'**administrateur ne perçoit rien**. Il fournit la curation gratuitement, à
  sa propre communauté.

## 2. Les deux parties à qualifier

Nous avons besoin d'une réponse **distincte pour chacune** :

1. **L'opérateur** : exploite le bot, perçoit la commission, est l'interlocuteur du membre.
2. **L'administrateur** : choisit les traders copiables, bénévolement, et annonce le service
   à ses membres.

## 3. Le contexte réglementaire que nous croyons pertinent

Sans préjuger de votre analyse, et pour que vous sachiez ce que nous avons déjà lu :

- L'ESMA a publié une note de supervision sur le copy trading (ESMA35-42-1428, 30 mars 2023)
  qui range ces services sous la **gestion de portefeuille ou le conseil en investissement**,
  et dont les attentes portent notamment sur « les qualifications des traders dont les
  transactions sont copiées ».
- Les contrats perpétuels ne relèvent pas de MiCA mais de **MiFID II**.
- La promotion de services sur actifs numériques par un prestataire non enregistré fait
  l'objet de restrictions, étendues aux réseaux sociaux par la loi n° 2023-451 du 9 juin 2023.

## 4. Les questions

**Q1.** L'opérateur fournit-il un **service d'investissement** ? Si oui, lequel — gestion de
portefeuille pour le compte de tiers, réception-transmission d'ordres, conseil en
investissement, autre — et quel agrément est requis, auprès de quelle autorité ?

**Q2.** **L'administrateur** fournit-il lui aussi un service d'investissement, ou une
prestation réglementée à un autre titre, en sélectionnant les traders copiables ? Le fait
qu'il ne soit **pas rémunéré** change-t-il la qualification ?

**Q3.** Si la copie n'était **pas automatique** — le membre validant chaque ordre après
notification — la qualification change-t-elle, et dans quel sens ? Cette variante sort-elle du
champ de l'agrément, ou bascule-t-elle simplement d'une catégorie à une autre ?

**Q4.** L'annonce du service par l'administrateur à ses propres membres, dans un serveur
Discord, constitue-t-elle une **publicité ou un démarchage** pour un service non enregistré ?
Le régime issu de la loi sur les influenceurs s'applique-t-il à un administrateur bénévole ?

**Q5.** Le fait que la plateforme d'exécution ne soit **ni établie ni agréée dans l'Union**
aggrave-t-il l'exposition de l'opérateur ou de l'administrateur, ou est-il indifférent ?

**Q6.** Existe-t-il un **aménagement praticable** — restriction géographique de l'accès,
changement de statut, adossement à un établissement agréé, modification du produit — qui
rende l'activité licite à une échelle compatible avec un revenu plafonné à 0,1 % du notionnel
échangé ? Si vous en voyez un, son coût d'ordre de grandeur nous est utile.

## 5. Ce que nous ne demandons pas

Pour tenir le périmètre et le budget : ni rédaction de conditions générales, ni montage de
structure, ni fiscalité, ni analyse d'un autre pays que la France. Une opinion écrite sur les
six questions suffit à cette étape.

## 6. Ce que votre réponse décide

Cette demande est le test le plus lourd d'une découverte produit en cours, et rien n'est
développé avant votre réponse. Une réponse « agrément requis » pour l'une **ou** l'autre
partie, sans aménagement tenable dans notre budget, **arrête le projet** — elle ne le reporte
pas. C'est écrit comme tel dans notre document de découverte, et c'est pour cela que nous vous
écrivons avant d'avoir construit quoi que ce soit plutôt qu'après.
