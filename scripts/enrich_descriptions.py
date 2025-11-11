import json
import re
import ast
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sample_data" / "product_data.js"
OUT = ROOT / "sample_data" / "product_data.enriched.js"
OUT_JSON = ROOT / "sample_data" / "product_data.enriched.json"

PREFIX_RE = re.compile(r"^\s*module\.exports\s*=\s*", re.IGNORECASE)


def extract_json(js_text: str) -> str:
    text = PREFIX_RE.sub("", js_text, count=1)
    # strip only a single trailing semicolon if present
    if text.rstrip().endswith(";"):
        text = text.rstrip()[:-1]
    return text


def load_payload(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    json_text = extract_json(raw)
    # Try strict JSON first
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        # Fallback: tolerate JS-style single quotes or trailing commas
        try:
            return ast.literal_eval(json_text)
        except Exception as e:
            raise


def make_description(name: str, price, rating, main_category: str | None, subcategory: str | None, tags):
    name = name or "Product"
    mc = (main_category or "").strip()
    sc = (subcategory or "").strip()
    price_str = f" at ${float(price):.2f}" if price is not None else ""
    rating_str = f" (rated {float(rating):.1f}/5)" if rating is not None else ""
    cat_part = ""
    if mc and sc:
        cat_part = f" in the {mc} / {sc} category"
    elif mc:
        cat_part = f" in the {mc} category"
    elif sc:
        cat_part = f" in the {sc} category"

    # Pick a few tags to highlight
    t = [t for t in (tags or []) if isinstance(t, str)]
    features = []
    for tag in t[:5]:
        cleaned = tag.replace("_", "-")
        if cleaned.startswith("brand-"):
            features.append(cleaned.replace(
                "brand-", "brand ").replace("-", " "))
        elif cleaned.startswith("os-"):
            features.append(cleaned.replace(
                "os-", "").replace("-", " ").title())
        elif cleaned.startswith(("cpu-", "gpu-", "ram-", "ssd-", "panel-", "display-")):
            parts = cleaned.split("-")[1:]
            features.append(" ".join(p.upper() if p in {
                            "i3", "i5", "i7", "i9", "rtx"} else p.replace("ultra", "Ultra") for p in parts))
        else:
            features.append(cleaned.replace("-", " "))
    tag_part = f" featuring {', '.join(features)}" if features else ""

    return f"{name}{cat_part}{price_str}{rating_str}{tag_part}.".strip()


essential_fields = ("name", "price", "rating", "tags")


def enrich(payload: dict) -> dict:
    categories = payload.get("categories") or []
    for cat in categories:
        mc = cat.get("main_category")
        for sub in (cat.get("subcategories") or []):
            sc = sub.get("name")
            for p in (sub.get("products") or []):
                # Only add/replace when missing or empty
                if not p.get("description") or not str(p.get("description")).strip():
                    desc = make_description(
                        name=p.get("name"),
                        price=p.get("price"),
                        rating=p.get("rating"),
                        main_category=mc,
                        subcategory=sc,
                        tags=p.get("tags"),
                    )
                    p["description"] = desc
    return payload


PREFERRED_PRODUCT_ORDER = [
    "id",
    "external_id",
    "sku",
    "name",
    "description",
    "price",
    "rating",
    "tags",
    "image_url",
    "image_thumb_url",
    "image_attribution",
]


def reorder_product_keys(p: dict) -> dict:
    ordered = OrderedDict()
    # place preferred keys in order if present
    for k in PREFERRED_PRODUCT_ORDER:
        if k in p:
            ordered[k] = p[k]
    # append any remaining keys to preserve data
    for k, v in p.items():
        if k not in ordered:
            ordered[k] = v
    return ordered


def normalize_key_order(payload: dict) -> dict:
    categories = payload.get("categories") or []
    for cat in categories:
        for sub in (cat.get("subcategories") or []):
            products = sub.get("products") or []
            sub["products"] = [reorder_product_keys(p) for p in products]
    return payload


def write_js(payload: dict, path: Path) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    path.write_text(f"module.exports = {text};\n", encoding="utf-8")


def write_json(payload: dict, path: Path) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    path.write_text(text + "\n", encoding="utf-8")


def main():
    if not SRC.exists():
        raise SystemExit(f"Source file not found: {SRC}")
    data = load_payload(SRC)
    enriched = enrich(data)
    enriched = normalize_key_order(enriched)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    write_js(enriched, OUT)
    write_json(enriched, OUT_JSON)
    # Print a quick preview
    try:
        first = enriched["categories"][0]["subcategories"][0]["products"][0]
        print("Preview:", first.get("name"), "->", first.get("description"))
        print("Wrote:", OUT)
        print("Wrote:", OUT_JSON)
    except Exception:
        print("Wrote:", OUT)
        print("Wrote:", OUT_JSON)


if __name__ == "__main__":
    main()
