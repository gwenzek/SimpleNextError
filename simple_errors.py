import sublime

import os

from sublime_plugin import WindowCommand

LOGGING = True


def log(*args):
  if LOGGING:
    print("[SimpleNextError]:", *args)


class SimpleNextError(WindowCommand):
  """Jump to the next build error.

  The error will be selected in the build output,
  and the relevant file will be opened if it exists.
  """

  def run(self):
    window = self.window
    build_output = window.find_output_panel("exec")
    if not build_output:
      return log("No Build ouptut found.")
    window.run_command("show_panel", args={"panel": "output.exec"})

    cursor = build_output.sel()[0].end()
    error_line = find_error_line(build_output, after=cursor)
    if not error_line:
      return log("No error found.")

    center(build_output, build_output.line(error_line))
    file_path = resolve_file(build_output,
                             find_error_file(build_output, error_line))
    if not file_path:
      return log("Unable to resolve filename:", filename)

    linenumber = int(build_output.substr(error_line))
    open_file(window, file_path, linenumber)


def center(view, region):
  """Center the view on the given region."""
  view.sel().clear()
  view.sel().add(region)
  view.show_at_center(region)


def find_error_line(view, after):
  """Returns the first error after the given point."""
  error_linenumbers = view.find_by_selector("constant.numeric.linenumber.error")
  if not error_linenumbers:
    return None

  for region in error_linenumbers:
    if region.begin() > after:
      return region
  # Go back to the first error.
  return error_linenumbers[0]


def find_error_file(view, error_line):
  """Returns the filename that comes just before the given error line region."""
  error_files = view.find_by_selector("entity.name.filename.error")
  if not error_files:
    return None

  error_eol = view.line(error_line).end()
  for i, file_region in enumerate(error_files):
    if file_region.end() > error_eol:
      # The filename is after the error line, return the previous one.
      return error_files[i - 1]

  return error_files[-1]


def resolve_file(view, filename):
  """Returns the full path of the given file, or None if no valid file found."""
  filename = view.substr(filename)
  # result_base_dir is set by the Default/exec.py plugin which runs Build commands.
  base_dir = view.settings().get("result_base_dir", "")
  localized = os.path.join(base_dir, filename)
  if os.path.exists(localized):
    return localized
  elif os.path.exists(filename):
    return filename
  else:
    return None


def open_file(window, file_path, linenumber):
  window.open_file("%s:%d" % (file_path, linenumber),
                   sublime.ENCODED_POSITION | sublime.TRANSIENT)
