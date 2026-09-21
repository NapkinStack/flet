---
title: "Pilot FAQ — what a member is told before they put in a euro"
status: accepted
written_on: 2026-09-21
grade: reported
---

# Pilot FAQ — what a member is told before they put in a euro

> **Provenance.** These exchanges were written by the framer as the questions a member would
> ask, then confirmed by the decider on 2026-09-21 as **representative of conversations that
> actually took place** with ten traders and twenty members. The real messages are private and
> were not disclosed, correctly. So: *reported*, not *primary*. Nothing here is a transcript,
> and no figure in this project rests on it.
>
> Its purpose is the opposite of evidence. It is the **onboarding text**: what an
> administrator tells a member before they put money in, and what the product must keep being
> able to answer honestly once it exists.

## Why all ten are kept

Each one carries a distinct warning. Removing any of them removes an honest answer, and the
charter's no-gos — never custody, never a promise of return — are only worth anything at the
moment a member is about to act.

---

**1. Tu prends une commission là-dessus ?**

Moi non, rien. C'est le dev du bot qui prend **0,1 % maximum du volume routé**, jamais un
pourcentage de tes gains. Concrètement, si le bot passe 1 000 € d'ordre pour toi, ça fait 1 €.
Tu payes quand ça trade, que tu gagnes ou que tu perdes — dis-toi bien que ça va dans les deux
sens.

**2. Le bot a accès à mes fonds ?**

Non, et c'est non négociable. Tes fonds restent sur **ton** compte Hyperliquid. Le bot a une
clé d'agent qui peut **passer des ordres et rien d'autre** — elle ne peut pas retirer, pas
transférer, pas sortir un centime. Tu la révoques quand tu veux, depuis ton compte, sans
demander la permission à personne.

**3. Et si le trader se plante ?**

Tu perds de l'argent. Pas « le bot amortit », pas « il y a un stop » : tu perds. Ce sont des
perps à levier, tu peux perdre **la totalité de ce que tu mets**. Je choisis des traders dont
je trouve le travail sérieux, ça ne veut pas dire qu'ils gagnent.

**4. Je mets combien ?**

Une somme dont la perte totale ne changerait rien à ta semaine. Pour la plupart d'entre vous
c'est entre 200 et 1 000 €. Et une contrainte technique : sous un certain montant, tes ordres
deviennent trop petits pour la plateforme et sont **refusés** — le bot te dira lequel avant que
tu commences, chiffre à l'appui.

**5. C'est légal ton truc ?**

Question honnête, réponse honnête : **personne ici n'est agréé**. Un avocat a été saisi sur le
sujet et l'avis n'est pas encore rendu. Ça veut dire que tu participes à un test avec cette
incertitude-là. Si ça te gêne, ne participe pas — c'est une raison parfaitement valable.

**6. Pourquoi ces traders-là ?**

Parce que je réponds d'eux, et c'est tout ce que ça veut dire. Ce n'est pas un classement de
performance : sélectionner sur la performance, ça sélectionne des scalpeurs dont les frais te
mangent. Le bot me sort pour chacun, en chiffres, **ce que ça te coûterait par mois en frais**
et **quelle part de ses ordres tu ne pourrais pas reproduire**. Je choisis avec ça sous les
yeux, pas avec un pourcentage de gains.

**7. Je peux arrêter quand ?**

Quand tu veux, tout de suite, sans prévenir. Tu révoques la clé et c'est fini. Tes positions
ouvertes restent à toi — c'est ton compte, tu les fermes comme tu veux.

**8. Ça coûte combien en frais au total ?**

Ça dépend entièrement de combien le trader trade. Un trader calme, c'est quelques pour cent par
an. Un trader très actif, ça peut dépasser **5 % par mois** — et à ce niveau ce sont les frais,
pas la stratégie, qui décident de ton résultat. Le bot affiche ce chiffre pour chaque trader
**avant** que tu choisisses, et refuse de dire « copiable » sans le signaler.

**9. Et si le bot bugue ou se déconnecte ?**

Tu te retrouves avec des positions ouvertes que plus rien ne suit. C'est le vrai risque et il
ne faut pas se raconter d'histoires : **ne mets rien que tu ne serais pas capable de gérer à la
main** si le bot s'arrêtait cette nuit.

**10. Pourquoi tu fais ça, toi ?**

Parce que des gens ici suivent des traders au hasard et se font rincer. Je ne gagne rien
dessus. Si ça ne marche pas, je le dirai ici et on arrêtera.

---

## What this commits the product to

Every one of these answers is a constraint on what gets built, not marketing copy:

| The answer | What the product must therefore do |
|---|---|
| 0.1% of routed volume, never a share of gains | PDR-0001, already decided |
| the key places orders and nothing else | the copying module holds an agent key with order permissions only, and the member revokes it from their own account |
| you can lose everything | no interface anywhere implies otherwise |
| the bot tells you the minimum ticket first | `screening` already does, with the refused share |
| nobody here is authorised | the notice is shown **before** a member acts, not in a footer |
| the monthly fee cost is shown before you choose | `screening` does, and `COPYABLE WITH RESERVATIONS (fees)` exists for exactly this |
| you revoke and it stops | revocation is a first-class path, not a support request |
| if the bot stops you are alone with open positions | said plainly at onboarding, and the operations playbook owes a rule for it |

Two of these are not built and are not in cycle 02: the **pre-action notice** and
**revocation**. They belong to the copying module, which is `critical`, and they are named
here so the module is framed with them rather than around them.
