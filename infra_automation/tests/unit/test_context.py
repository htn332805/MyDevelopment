from orchestrator.context import Context

def test_set_get_and_history():
    ctx = Context()
    assert ctx.get("foo") is None
    ctx.set("foo", 123, who="step1")
    assert ctx.get("foo") == 123
    hist = ctx.get_history()
    assert len(hist) == 1
    rec = hist[0]
    assert rec["step"] == "step1"
    assert rec["key"] == "foo"
    assert rec["before"] is None
    assert rec["after"] == 123
