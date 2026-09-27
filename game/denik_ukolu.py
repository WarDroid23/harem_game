"""Přehled aktivních a dokončených úkolů napříč herními systémy."""

from config import CYAN, DIM, GOLD, GREEN, MAGENTA, NC, YELLOW
from game.npc_questy import NPC_QUESTY
from game.svet import LOKACE, NPC
from utils.vypis import clear, hlavicka, menu_cara


def _nazev_lokace(hra, lokace_id):
    if not lokace_id:
        return "bez určené lokace"
    data = LOKACE.get(lokace_id)
    if data and lokace_id in hra.svet.odhalene_lokace:
        return data.get("nazev", lokace_id)
    return f"skrytá lokace ({lokace_id})"


def _zobraz_bezny_quest(hra):
    quest = hra.questy.aktivni_quest
    if not quest:
        print(f"  {DIM}Nemáš aktivní běžný úkol.{NC}")
        return
    print(f"  {YELLOW}📜 {quest.get('nazev', 'Neznámý úkol')}{NC}")
    print(f"     {quest.get('popis', '')}")
    print(
        f"     Zbývá dní: {hra.questy.dny_zbyva} | "
        f"Odměna: {quest.get('odmena_zlato', 0)} zl. | "
        f"Riziko: {int(quest.get('riziko', 0) * 100)} %"
    )
    print(f"     Místo: {_nazev_lokace(hra, quest.get('lokace'))}")


def _zobraz_npc_ukoly(hra):
    system = hra.npc_questy
    print(f"\n{MAGENTA}Aktivní úkoly NPC{NC}")
    if not system.aktivni:
        print(f"  {DIM}Žádný přijatý NPC úkol.{NC}")
    for npc_id, zaznam in system.aktivni.items():
        data_npc = NPC.get(npc_id, {})
        jmeno_npc = data_npc.get("jmeno", npc_id)
        quest = zaznam.get("quest") if isinstance(zaznam, dict) else None
        if not isinstance(quest, dict):
            zaklad = NPC_QUESTY.get(npc_id, {})
            quest = (
                zaklad.get("navazujici")
                if int(system.dokoncene.get(npc_id, 0)) >= 1
                else zaklad
            ) or zaklad
        print(f"  {YELLOW}🤝 {quest.get('nazev', 'Neznámý úkol')}{NC} — {jmeno_npc}")
        print(f"     {quest.get('popis', '')}")
        print(
            f"     Odměna: {quest.get('odmena', 0)} zl. | "
            f"Požadovaný vztah: {quest.get('pozadavek', '?')}"
        )
        print(
            f"     Zadavatel: {jmeno_npc} — "
            f"{_nazev_lokace(hra, data_npc.get('lokace'))}"
        )

    dostupne = system.dostupne(hra)
    print(f"\n{GREEN}Další dostupné NPC úkoly: {len(dostupne)}{NC}")
    if not dostupne:
        print(f"  {DIM}Zatím není dostupný žádný další úkol.{NC}")
    for npc_id, quest in dostupne:
        data_npc = NPC.get(npc_id, {})
        jmeno_npc = data_npc.get("jmeno", npc_id)
        lokace = _nazev_lokace(hra, data_npc.get("lokace"))
        print(
            f"  • {quest.get('nazev', 'Neznámý úkol')} — "
            f"{jmeno_npc} ({lokace})"
        )


def zobraz_denik_ukolu(hra):
    clear()
    hlavicka("Deník úkolů", "Aktivní cíle, odměny a postup")

    kapitola = hra.kampan.aktualni()
    print(f"{CYAN}Hlavní kampaň{NC}")
    if kapitola:
        print(
            f"  📖 Kapitola {hra.kampan.kapitola + 1}: "
            f"{kapitola.get('nazev', 'Neznámá kapitola')}"
        )
        print(f"     {kapitola.get('popis', '')}")
        print(
            f"     Cíl: navštiv {_nazev_lokace(hra, kapitola.get('lokace'))}"
        )
    else:
        print(f"  {GREEN}Kampaň je dokončena.{NC}")

    menu_cara()
    print(f"\n{GOLD}Běžný úkol{NC}")
    _zobraz_bezny_quest(hra)

    menu_cara()
    _zobraz_npc_ukoly(hra)

    historie = getattr(hra.questy, "historie", [])
    npc_dokonceno = sum(
        max(0, int(pocet)) if str(pocet).lstrip("-").isdigit() else 0
        for pocet in hra.npc_questy.dokoncene.values()
    )
    print(
        f"\n{DIM}Dokončené běžné úkoly: {hra.questy.dokonceno} "
        f"({sum(1 for zaznam in historie if isinstance(zaznam, dict) and zaznam.get('uspech'))} úspěšně) | "
        f"Dokončené NPC úkoly: {npc_dokonceno}{NC}"
    )
