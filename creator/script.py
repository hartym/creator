import os
import subprocess

import pyjson5
from string import Template


class Script:
    def __init__(self, *, title, checks=None, steps=None, skip=False):
        self.title = title
        self.checks = checks or []
        self.steps = steps or []
        self.skip = skip


class JavascriptModuleFile:
    def __init__(self, path, /, *, json, preamble=None):
        self.path = path
        self.json = json
        self.preamble = preamble

    def execute(self, context):
        path = Template(self.path).substitute(context)
        with open(path, "w") as f:
            if self.preamble:
                f.write(self.preamble)
            f.write("export default ")
            f.write(pyjson5.dumps(self.json))
            f.write("\n")


class TextFile:
    def __init__(self, path, /, content, mkdir=False):
        self.path = path
        self.content = content
        self.mkdir = mkdir

    def execute(self, context):
        path = Template(self.path).substitute(context)

        if self.mkdir:
            subprocess.run(
                ["mkdir", "-p", os.path.dirname(path)], check=True, capture_output=True
            )

        with open(path, "w") as f:
            f.write(self.content)
            f.write("\n")


class JsonFileModify:
    def __init__(self, path, /, modifier):
        self.path = path
        self.modifier = modifier

    def execute(self, context):
        path = Template(self.path).substitute(context)
        with open(path, "r") as f:
            content = pyjson5.load(f)
        content = self.modifier(content)
        with open(path, "wb") as f:
            pyjson5.dump(content, f)
            f.write(b"\n")

        subprocess.run(["prettier", "--write", path], check=True, capture_output=True)
