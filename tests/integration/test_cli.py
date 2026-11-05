import io
from unittest.mock import patch

import pytest

from futurizer.cli import main

_SAMPLE = "Forse perché della fatal quïete\ntu sei l'immago a me sì cara vieni"


@pytest.fixture
def sample_file(tmp_path):
    f = tmp_path / "input.txt"
    f.write_text(_SAMPLE, encoding="utf-8")
    return f


def test_file_input(sample_file):
    code, out, err = _run([str(sample_file), "--seed", "1"])
    assert code == 0
    assert len(out.strip()) > 0
    assert err == ""


def test_stdin_input():
    code, out, err = _run(["-", "--seed", "1"], stdin=_SAMPLE)
    assert code == 0
    assert len(out.strip()) > 0
    assert err == ""


def test_file_not_found():
    code, out, err = _run(["nonexistent.txt"])
    assert code == 1
    assert "not found" in err
    assert out == ""


def test_empty_file(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("", encoding="utf-8")
    code, _, err = _run([str(f)])
    assert code == 1
    assert "empty" in err


def test_whitespace_only_file(tmp_path):
    f = tmp_path / "blank.txt"
    f.write_text("   \n\n  ", encoding="utf-8")
    code, _, err = _run([str(f)])
    assert code == 1
    assert "empty" in err


def test_empty_stdin():
    code, _, err = _run(["-"], stdin="")
    assert code == 1
    assert "empty" in err


def test_lang_italian(sample_file):
    code, _, err = _run([str(sample_file), "--lang", "it", "--seed", "1"])
    assert code == 0
    assert err == ""


def test_lang_english(tmp_path):
    f = tmp_path / "input.txt"
    f.write_text(
        "Every Night and every Morn\nSome to Misery are Born.", encoding="utf-8"
    )
    code, _, err = _run([str(f), "--lang", "en", "--seed", "1"])
    assert code == 0
    assert err == ""


def test_invalid_lang(tmp_path):
    f = tmp_path / "input.txt"
    f.write_text("Il treno corre", encoding="utf-8")
    # argparse rejects unknown choices before main() logic runs
    with pytest.raises(SystemExit) as exc:
        _run([str(f), "--lang", "zz"])
    assert exc.value.code != 0


def test_seed_reproducibility(sample_file):
    _, out1, _ = _run([str(sample_file), "--seed", "42"])
    _, out2, _ = _run([str(sample_file), "--seed", "42"])
    # Same seed must produce identical output
    assert out1 == out2


def test_different_seeds_differ(sample_file):
    _, out1, _ = _run([str(sample_file), "--seed", "42"])
    _, out2, _ = _run([str(sample_file), "--seed", "99"])
    # Different seeds should produce different output
    assert out1 != out2


def test_noise_zero_still_produces_output(sample_file):
    code, out, _ = _run([str(sample_file), "--noise", "0.0", "--seed", "1"])
    assert code == 0
    assert len(out.strip()) > 0


def test_noise_max_still_produces_output(sample_file):
    code, out, _ = _run([str(sample_file), "--noise", "1.0", "--seed", "1"])
    assert code == 0
    assert len(out.strip()) > 0


def _run(args, stdin=None):
    """Helper function to run the CLI with mocked stdin, stdout, and stderr."""

    stdout = io.StringIO()
    stderr = io.StringIO()

    stdin_mock = io.StringIO(stdin) if stdin is not None else io.StringIO("")

    with (
        patch("sys.stdout", stdout),
        patch("sys.stderr", stderr),
        patch("sys.stdin", stdin_mock),
    ):
        code = main(args)

    return code, stdout.getvalue(), stderr.getvalue()
