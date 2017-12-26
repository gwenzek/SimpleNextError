import sublime

from sublime_plugin import WindowCommand

class SimpleNextError(WindowCommand):
  def run(self):
    window = self.window
    build_output = window.find_output_panel('exec')
    window.run_command('show_panel', args={'panel': 'output.exec'})
    cursor = build_output.sel()[0].end()
    error_linenumbers = build_output.find_by_selector('constant.numeric.linenumber.error')
    next_error = select_next_error(cursor, error_linenumbers)
    error_line = build_output.line(next_error)

    build_sel = build_output.sel()
    build_sel.clear()
    build_sel.add(error_line)
    build_output.show_at_center(error_line.begin())

    error_files = build_output.find_by_selector('entity.name.filename.error')
    filename = find_filename(build_output, error_line, error_files)
    linenumber = int(build_output.substr(next_error))
    filename = '%s:%d' % (filename, linenumber)
    window.open_file(filename, sublime.ENCODED_POSITION | sublime.TRANSIENT)


def select_next_error(cursor, error_linenumbers):
  for region in error_linenumbers:
    if region.begin() > cursor:
      return region
  return error_linenumbers[0]


def find_filename(view, error_line, error_files):
  i = 0
  for file_region in error_files:
    if error_line.contains(file_region):
      return view.substr(file_region)
    if error_line.begin() > file_region.end():
      break
    i += 1

  return view.substr(error_files[i])
