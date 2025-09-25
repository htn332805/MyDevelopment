def summarize(ctx_dict: dict) -> str:
    # very simple summary
    lines = []
    for k, v in ctx_dict.items():
        lines.append(f"{k}: {v}")
    return "\\n".join(lines)
