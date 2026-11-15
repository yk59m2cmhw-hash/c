"""Second Life: one photo of a broken thing in, one action card out.

Two ways to make a card from the same photo with the same model:

  baseline(photo)  one request: "look at the photo and fill in the card".
  pipeline(photo)  our method: (1) the model inspects the item, (2) safety rules written
                   in code decide what the plan may contain, (3) the model writes the plan,
                   (4) code checks the plan and asks for one correction if a rule is broken.

The model is reached through Google's OpenAI-compatible Gemini endpoint. The key is read
from the GEMINI_API_KEY environment variable and is never stored in this repository.
"""
from __future__ import annotations

import base64
import io
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
MODEL = os.environ.get("SECONDLIFE_MODEL", "gemini-2.5-flash")   # replaced after the access check, see README
MIN_SECONDS_BETWEEN_CALLS = float(os.environ.get("SECONDLIFE_PAUSE", "5"))   # the free tier limits requests per minute
MAX_SIDE = 1024           # photos are shrunk to this size before they are sent

VERDICTS = ["repair", "repurpose", "dispose"]

# --------------------------------------------------------------------------- #
# Safety rules (ours, in code): when an item belongs to one of these classes, a
# school student must not open, cut, heat or "fix" the dangerous part at home.
# --------------------------------------------------------------------------- #
HAZARDS = {
    "battery": "contains a rechargeable or lithium battery (phone, power bank, wireless earbuds, vape, laptop, toy with a built-in battery)",
    "mains": "plugs into a wall socket or carries mains voltage (charger, lamp, kettle, extension cord, hair dryer, any power cable)",
    "glass": "broken or cracked glass, ceramic or a mirror with sharp edges or shards",
    "blade": "blades or other sharp cutting parts (knife, scissors, razor, grater, tin-can edge)",
    "pressure": "pressurised container (aerosol can, gas canister, lighter)",
    "chemical": "medicines, household chemicals, paint, glue or solvent containers, leaking batteries",
    "bulb": "light bulb or fluorescent tube (may contain mercury)",
    "mould": "mould or rot",
}
HAZARD_RULES = {
    "battery": "Do not open the case, do not pierce, bend, heat or charge it. Take it to a battery or e-waste collection point.",
    "mains": "Do not open it and do not repair the cable or plug yourself. Unplug it. A repair is for an adult electrician or a service shop.",
    "glass": "Do not cut, glue or carry shards with bare hands. An adult should wrap the pieces in thick paper before throwing them away.",
    "blade": "Do not sharpen or take apart the cutting part. Wrap the blade before throwing it away.",
    "pressure": "Do not pierce, heat or cut the container, even if it seems empty.",
    "chemical": "Do not pour it out, mix it or reuse the container for food or drink. Take medicines to a pharmacy collection box if there is one.",
    "bulb": "Do not break or take it apart. If a fluorescent tube breaks, leave the room and air it. Take it to a collection point.",
    "mould": "Do not clean and reuse it for food, clothes or bedding. Throw it away in a closed bag.",
}
# words that show a plan asks the student to work on the dangerous part (Russian and English stems)
RISKY_ACTIONS = re.compile(
    r"вскр|разбер|разобр|разбир|открут|раскрут|припа|перепа|паяльн|зачист|оголи|изолент|нагре|расплав|проткн|прокол|"
    r"разреж\w* стекл|склей\w* стекл|склеить (осколк|стекл)|"
    r"\bopen (the|up)\b|take (it )?apart|disassembl|unscrew|solder|strip the (wire|cable)|electrical tape|heat (it|the)|melt|pierce|puncture",
    re.IGNORECASE)
# tools a school student at home should not need
FORBIDDEN_TOOLS = re.compile(
    r"паяльник|дрель|шуруповёрт|шуруповерт|болгарк|сварк|лобзик|строительн\w* фен|горелк|электропил|циркулярн|"
    r"soldering iron|\bdrill\b|angle grinder|welding|jigsaw|heat gun|blowtorch|power saw", re.IGNORECASE)

LANGUAGE = {"ru": "Russian", "en": "English"}

CARD_FIELDS = """{
  "item": "what the thing is, 2-5 words",
  "damage": "what is broken or worn, one short sentence",
  "verdict": "repair" | "repurpose" | "dispose",
  "idea_title": "the single best thing to do with it, up to 8 words",
  "steps": ["3 to 6 short steps a 14-year-old can follow"],
  "needs": ["materials and tools, each one ordinary household stuff"],
  "time_minutes": 30,
  "result_use": "what you get in the end and why it is useful, one sentence",
  "danger": true | false,
  "warning": "a clear safety warning, or an empty string if there is no danger",
  "do_not": "one thing not to do with this item"
}"""

USER_AND_GOAL = (
    "The user is a school student (about 14) at home in Almaty, Kazakhstan, holding a broken or worn-out thing that is about to be thrown away. "
    "Help them give it a second life: repair it if that is realistic at home, otherwise turn it into something useful, "
    "and if neither is safe or sensible, say how to dispose of it properly. "
    "Use only ordinary household materials and hand tools (scissors, glue, tape, thread and needle, a screwdriver, sandpaper, paint, cord). "
    "Be specific to this exact item and this exact damage. Do not invent parts that are not visible.")


# --------------------------------------------------------------------------- #
# Model access
# --------------------------------------------------------------------------- #
_last_call = 0.0
CALL_LOG: list[dict] = []        # one entry per request: seconds and status, for the cost-and-delay report


def photo_as_data_url(path: str | Path) -> str:
    """Shrinks the photo, turns it upright and returns it as a base64 JPEG data URL."""
    from PIL import Image, ImageOps
    image = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    image.thumbnail((MAX_SIDE, MAX_SIDE))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode()


def ask_model(prompt: str, photo_url: str | None = None, temperature: float = 0.2, retries: int = 4) -> dict:
    """One request to the model. The answer must be a JSON object; it is returned as a dict."""
    global _last_call
    if os.environ.get("SECONDLIFE_MOCK"):                     # offline test of everything except the network call
        return _mock_answer(prompt)
    content = [{"type": "text", "text": prompt}]
    if photo_url:
        content.append({"type": "image_url", "image_url": {"url": photo_url}})
    body = {"model": MODEL, "temperature": temperature, "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": content}]}
    headers = {"Authorization": "Bearer " + os.environ.get("GEMINI_API_KEY", "dummy"), "Content-Type": "application/json"}
    problem = "no attempt made"
    for attempt in range(retries):
        wait = MIN_SECONDS_BETWEEN_CALLS - (time.time() - _last_call)
        if wait > 0:
            time.sleep(wait)
        started = _last_call = time.time()
        try:
            request = urllib.request.Request(API, data=json.dumps(body).encode(), headers=headers)
            with urllib.request.urlopen(request, timeout=120) as response:
                answer = json.loads(response.read())
            text = answer["choices"][0]["message"]["content"]
            CALL_LOG.append({"seconds": round(time.time() - started, 2), "status": 200})
            return parse_json(text)
        except urllib.error.HTTPError as error:
            problem = f"HTTP {error.code}: {error.read().decode(errors='replace')[:300]}"
            CALL_LOG.append({"seconds": round(time.time() - started, 2), "status": error.code})
            if error.code not in (429, 500, 502, 503, 504):
                break
            time.sleep(20 * (attempt + 1))                     # rate limit or a busy server: wait and try again
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as error:
            problem = f"{type(error).__name__}: {error}"
            CALL_LOG.append({"seconds": round(time.time() - started, 2), "status": "error"})
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"The model did not answer: {problem}")


def parse_json(text: str) -> dict:
    """The model sometimes wraps JSON in ```json fences; take the outermost object."""
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object in the model's answer")
    return json.loads(text[start:end + 1])


# --------------------------------------------------------------------------- #
# The card: cleaning and checking (plain code, no model)
# --------------------------------------------------------------------------- #
def clean_card(raw: dict) -> dict:
    """Keeps only the card fields and gives each the right type, so a sloppy answer cannot break the page."""
    def text(key):
        return str(raw.get(key) or "").strip()

    def items(key):
        value = raw.get(key) or []
        value = [value] if isinstance(value, str) else value
        return [str(v).strip() for v in value if str(v).strip()]

    try:
        minutes = int(float(raw.get("time_minutes") or 0))
    except (TypeError, ValueError):
        minutes = 0
    verdict = text("verdict").lower()
    return {"item": text("item"), "damage": text("damage"), "verdict": verdict if verdict in VERDICTS else "",
            "idea_title": text("idea_title"), "steps": items("steps"), "needs": items("needs"), "time_minutes": minutes,
            "result_use": text("result_use"), "danger": bool(raw.get("danger")), "warning": text("warning"), "do_not": text("do_not")}


def card_problems(card: dict, hazards: list[str] | None = None) -> list[str]:
    """Rule violations found by code. An empty list means the card passed."""
    problems = []
    if not card["item"] or not card["idea_title"]:
        problems.append("the item or the idea is missing")
    if card["verdict"] not in VERDICTS:
        problems.append("the verdict must be repair, repurpose or dispose")
    if not 2 <= len(card["steps"]) <= 7:
        problems.append("give 3 to 6 steps")
    words = " ".join(card["steps"] + card["needs"] + [card["idea_title"]])
    tool = FORBIDDEN_TOOLS.search(words)
    if tool:
        problems.append(f"the plan needs a tool a school student should not use at home: '{tool.group(0)}'")
    if hazards:
        if not card["danger"] or len(card["warning"]) < 15:
            problems.append("the item is dangerous: set danger to true and write a clear warning")
        risky = RISKY_ACTIONS.search(" ".join(card["steps"] + [card["idea_title"]]))
        if risky:
            problems.append(f"the plan tells the student to work on the dangerous part: '{risky.group(0)}'")
        if card["verdict"] == "repair":
            problems.append("a dangerous item must not get the verdict 'repair' for a school student")
    return problems


# --------------------------------------------------------------------------- #
# Baseline: one request
# --------------------------------------------------------------------------- #
def baseline(photo: str | Path, note: str = "", lang: str = "ru") -> dict:
    prompt = (f"{USER_AND_GOAL}\n\nLook at the photo. " + (f"The student adds: \"{note}\". " if note else "") +
              "Think about safety: if the item is dangerous to open or fix at home, say so clearly and do not tell the student to do it.\n\n"
              f"Answer with one JSON object with exactly these fields. Write every text value in {LANGUAGE[lang]}; keep the verdict word in English.\n{CARD_FIELDS}")
    card = clean_card(ask_model(prompt, photo_as_data_url(photo)))
    card["_meta"] = {"system": "baseline", "calls": 1, "problems_left": card_problems(card)}
    return card


# --------------------------------------------------------------------------- #
# Our method: inspect -> safety rules in code -> plan -> check in code
# --------------------------------------------------------------------------- #
def inspect(photo_url: str, note: str = "", lang: str = "ru") -> dict:
    classes = "\n".join(f'  "{name}": {meaning}' for name, meaning in HAZARDS.items())
    prompt = ("Look at the photo of one household item that is broken or worn out. Describe only what you can see. " +
              (f"The owner adds: \"{note}\". " if note else "") +
              f"\n\nAnswer with one JSON object. Write the text values in {LANGUAGE[lang]}.\n"
              '{\n  "item": "what the thing is, 2-5 words",\n  "materials": ["main materials"],\n'
              '  "damage": "what is broken or worn, one short sentence",\n'
              '  "still_good": "which parts are still intact and usable, one short sentence",\n'
              '  "hazards": ["zero or more of the class names below that apply to this item"],\n'
              '  "sure": true | false\n}\n\n'
              f"Hazard classes (use these exact names):\n{classes}\n"
              "Add a hazard class whenever the item is of that kind, even if the dangerous part looks fine.")
    seen = ask_model(prompt, photo_url, temperature=0.0)
    hazards = seen.get("hazards") or []
    hazards = [hazards] if isinstance(hazards, str) else hazards
    return {"item": str(seen.get("item") or "").strip(), "materials": seen.get("materials") or [],
            "damage": str(seen.get("damage") or "").strip(), "still_good": str(seen.get("still_good") or "").strip(),
            "hazards": [h for h in dict.fromkeys(str(h).strip().lower() for h in hazards) if h in HAZARDS],
            "sure": bool(seen.get("sure", True))}


def plan_prompt(seen: dict, note: str, lang: str, corrections: list[str] | None = None) -> str:
    lines = [USER_AND_GOAL, "",
             f"An inspection of the photo found: item: {seen['item']}; materials: {', '.join(map(str, seen['materials']))}; "
             f"damage: {seen['damage']}; still good: {seen['still_good']}." + (f" The student adds: \"{note}\"." if note else "")]
    if seen["hazards"]:
        lines += ["", "SAFETY RULES FOR THIS ITEM. They come first and cannot be traded for a nicer idea:"]
        lines += [f"- {HAZARD_RULES[h]}" for h in seen["hazards"]]
        lines += ["- The verdict must be 'repurpose' (only if the dangerous part stays untouched and is not needed) or 'dispose'. Never 'repair'.",
                  "- Set danger to true. The warning must name the danger and say what to do instead (an adult, a service shop or a collection point).",
                  "- No step may ask the student to open, cut, heat, glue or rewire the dangerous part."]
    else:
        lines += ["", "No special danger was found. Set danger to false and leave the warning empty unless a step uses something sharp or hot."]
    lines += ["", "Prefer an idea that keeps the item, or its good parts, in use for a long time. If nothing sensible can be done, say 'dispose' and explain how."]
    if corrections:
        lines += ["", "Your previous card broke these rules. Write the whole card again and fix them:"] + [f"- {c}" for c in corrections]
    lines += ["", f"Answer with one JSON object with exactly these fields. Write every text value in {LANGUAGE[lang]}; keep the verdict word in English.", CARD_FIELDS]
    return "\n".join(lines)


def pipeline(photo: str | Path, note: str = "", lang: str = "ru") -> dict:
    photo_url = photo_as_data_url(photo)
    seen = inspect(photo_url, note, lang)
    card = clean_card(ask_model(plan_prompt(seen, note, lang), photo_url))
    calls, problems = 2, card_problems(card, seen["hazards"])
    if problems:                                               # one chance to fix what the code check found
        card = clean_card(ask_model(plan_prompt(seen, note, lang, problems), photo_url))
        calls, problems = 3, card_problems(card, seen["hazards"])
    if seen["hazards"]:                                        # the rules win even if the model still disagrees
        card["danger"] = True
        if len(card["warning"]) < 15:
            card["warning"] = " ".join(HAZARD_RULES[h] for h in seen["hazards"])
    card["item"], card["damage"] = card["item"] or seen["item"], card["damage"] or seen["damage"]
    card["_meta"] = {"system": "pipeline", "calls": calls, "hazards_found": seen["hazards"], "inspection": seen, "problems_left": problems}
    return card


# --------------------------------------------------------------------------- #
# Showing a card
# --------------------------------------------------------------------------- #
WORDS = {
    "ru": {"repair": "ПОЧИНИТЬ", "repurpose": "ПЕРЕДЕЛАТЬ", "dispose": "СДАТЬ ИЛИ ВЫБРОСИТЬ БЕЗОПАСНО", "": "НЕ ОПРЕДЕЛЕНО",
           "damage": "Что сломано", "steps": "Шаги", "needs": "Понадобится", "time": "Время", "min": "мин",
           "result": "Что получится", "warning": "Осторожно", "do_not": "Не делай"},
    "en": {"repair": "REPAIR", "repurpose": "TURN INTO SOMETHING ELSE", "dispose": "DISPOSE OF SAFELY", "": "NOT DECIDED",
           "damage": "What is broken", "steps": "Steps", "needs": "You need", "time": "Time", "min": "min",
           "result": "What you get", "warning": "Careful", "do_not": "Do not"},
}


def card_as_markdown(card: dict, lang: str = "ru") -> str:
    w = WORDS[lang]
    lines = [f"### {card['item']}", f"**{w['damage']}:** {card['damage']}", "", f"## {w[card['verdict']]}: {card['idea_title']}"]
    if card["danger"] or card["warning"]:
        lines += ["", f"> ⚠️ **{w['warning']}:** {card['warning']}"]
    lines += ["", f"**{w['steps']}:**"] + [f"{i}. {step}" for i, step in enumerate(card["steps"], 1)]
    lines += ["", f"**{w['needs']}:** " + ", ".join(card["needs"]), f"**{w['time']}:** {card['time_minutes']} {w['min']}",
              f"**{w['result']}:** {card['result_use']}", f"**{w['do_not']}:** {card['do_not']}"]
    return "\n".join(lines)


def _mock_answer(prompt: str) -> dict:
    """Canned answers for an offline test of the plumbing (SECONDLIFE_MOCK=1). Never used for results."""
    if '"hazards"' in prompt:
        return {"item": "беспроводные наушники", "materials": ["пластик"], "damage": "не заряжаются", "still_good": "корпус цел",
                "hazards": ["battery", "unknown-class"], "sure": True}
    risky = "previous card broke" not in prompt
    return {"item": "беспроводные наушники", "damage": "не заряжаются", "verdict": "repair" if risky else "dispose",
            "idea_title": "Сдать в пункт приёма", "steps": ["Вскрой корпус" if risky else "Положи в пакет", "Отнеси в пункт приёма", "Попроси взрослого помочь"],
            "needs": ["пакет"], "time_minutes": "20", "result_use": "Аккумулятор не попадёт в мусор", "danger": not risky,
            "warning": "" if risky else "Внутри литиевый аккумулятор: не вскрывай и не нагревай, сдай в пункт приёма.", "do_not": "Не выбрасывай в обычный мусор"}
