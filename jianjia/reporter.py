class Reporter:
    def __init__(self) -> None:
        self.had_error = False

    def error(self, line: int, message: str):
        self._report(line, "", message)

    def _report(self, line: int, where: str, message: str):
        self.had_error = True
        s = f"[line {line}] Error {where}: {message}"
        print(s)
