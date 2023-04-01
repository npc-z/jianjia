from jianjia.reporter import Reporter
from jianjia.scanner import Scanner


class JianJia:
    def __init__(self) -> None:
        self._reporter = Reporter()

    def run(self, path: str = ""):
        if path != "":
            self._run_file(path)
        else:
            self._run_prompt()

    def _run_file(self, path: str):
        code = ""
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        self._run(code)

        # Indicate an error in the exit code.
        if self._reporter.had_error:
            exit(65)

    def _run_prompt(self):
        while True:
            line = ""
            try:
                line = input("> ")
            except EOFError:
                break

            self._run(line)

            # 在交互式循环中, 如果用户输入有误, 也不应终止整个会话.
            self._reporter.had_error = False

    def _run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        # Just print the tokens now
        for token in tokens:
            print(token)
