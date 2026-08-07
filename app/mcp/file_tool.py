from pathlib import Path


class FileTool:

    def read_file(self, file_path):

        try:

            return Path(file_path).read_text()

        except Exception:

            return "Unable to read file."