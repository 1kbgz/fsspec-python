from pathlib import Path


class TestOpen:
    def test_open_read(self, open_hook):
        with open("in.txt", "r") as f:
            data = f.read()
            with open("out.txt", "w") as f:
                f.write(data)

        assert (Path(__file__).parent / "dump" / "out.txt").read_text() == "hello world"

    def test_open_passthrough(self, open_hook):
        # Open pyproject.toml
        with open("pyproject.toml", "r") as f:
            assert f.read()
