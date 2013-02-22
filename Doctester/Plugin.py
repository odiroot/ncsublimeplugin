import json
import sublime
import sublime_plugin
import subprocess
import threading
from sublime import Region
from os.path import abspath, dirname, join


_this_file  = __file__
_this_dir = abspath(dirname(_this_file))


class ExampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        # Get absolute path of currently edited file.
        path = view.file_name()
        if not path:
            return

        result = run_file_doctests(path)
        if result:
            display_errors(view, json.loads(result))


def display_errors(view, error_def):
    clearErrorMarks(view)

    lines = [int(row["line"]) - 1 for row in error_def]
    view.set_status('test-error-status', error_def[0]["explanation"])

    markErrorLines(view, lines)


def markErrorLines(view, lines):
    regions = []
    for line in lines:
        region = view.line(view.text_point(line, 0))
        regions.append(region)
    view.add_regions("error-liner", regions, "keyword", "bookmark",
        sublime.DRAW_OUTLINED)


def clearErrorMarks(view):
    view.erase_regions("error-liner")
    view.erase_status('test-error-status')


def run_file_doctests(path):
    u"Run doctests of a single Python module."
    # Create threaded executor for given path.
    executor = DoctestExecutor(path)
    # Run executor and wait one second for results.
    executor.start()
    executor.join(1)

    # If executor is still running forcibly kill it.
    if executor.isAlive():
        executor.kill()

    # Some error handling.
    if executor.error:
        sublime.error_message("Error during doctests running:\n%s"
            % executor.error)
        return None

    return executor.result


class DoctestExecutor(threading.Thread):
    test_command = "python -m doctest -v"
    parse_command = "python %s" % join(_this_dir, "docparser.py")

    def __init__(self, file_path):
        self.path = file_path
        # For external command output.
        self.result = None
        # For external command error.
        self.error = None
        self.process = None
        super(DoctestExecutor, self).__init__()

    def run(self):
        # Run command on given file path.
        command = "%s %s | %s" % (self.test_command, self.path,
            self.parse_command)

        # Execute external command, catch stdout/stderr.
        self.process = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

        # Store results of external command run.
        self.result, self.error = self.process.communicate()

    def kill(self):
        self.process.kill()


class CleanMarksOnSave(sublime_plugin.EventListener):
    def on_post_save(self, view):
        clearErrorMarks(view)
