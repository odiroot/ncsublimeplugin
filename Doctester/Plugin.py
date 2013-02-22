import sublime, sublime_plugin
import subprocess
import threading


class ExampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        # Get absolute path of currently edited file.
        path = view.file_name()

        result = run_file_doctests(path)
        if result:
            sublime.message_dialog("Doctest run results:\n%s" % result)


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
    ext_command = "python -m doctest -v"

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
        command = "%s %s" % (self.ext_command, self.path)

        # Execute external command, catch stdout/stderr.
        self.process = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)

        # Store results of external command run.
        self.result, self.error = self.process.communicate()

    def kill(self):
        self.process.kill()
