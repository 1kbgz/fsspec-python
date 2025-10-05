from pathlib import Path


class TestOpen:
    def test_open_read(self, open_hook):
        with open("in.txt", "r") as f:
            data = f.read()
            with open("out.txt", "w") as f:
                f.write(data)

        assert (Path(__file__).parent / "dump" / "out.txt").read_text() == "hello world"
