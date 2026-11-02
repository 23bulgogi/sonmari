from translator import Translator

def run(labels):
    t = Translator(); words = []
    for l in labels:
        w, s = t.step(l)
        if w: words.append(w.strip())
    return words, s

def test_one_shot():
    assert run(["head", "", "sick"])[1] == "머리 아프다"

def test_continuous():
    assert run(["cold1", "cold1", "", "cold2"])[1] == "감기"

def test_three_step_and_reverse():
    assert run(["hospitalization1", "hospitalization2", "hospitalization3"])[1] == "입원"
    assert run(["hospitalization3", "hospitalization2", "hospitalization1"])[1] == "퇴원"

def test_recovery_vs_better():
    assert run(["recovery1", "recovery2", "recovery3"])[1] == "완쾌"
    assert run(["recovery3"])[1] == "낫다"

def test_reset():
    assert run(["head", "reset"])[1] == ""

if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f(); print("ok", name)
