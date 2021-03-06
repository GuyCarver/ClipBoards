import sublime, sublime_plugin

selectionState = 0

class ColumnselectCommand( sublime_plugin.TextCommand ) :
  def run( self, edit ) :
    global selectionState
    selectionState = 0 if selectionState != 0 else 1

class LineselectCommand( sublime_plugin.TextCommand ) :
  def run( self, edit ) :
    global selectionState
    selectionState = 0 if selectionState != 0 else 2

class SelectionState( sublime_plugin.EventListener ) :
  def on_query_context(self, view, key, operator, operand, match_all):
    if key == "SelectionState.column" :
      return (selectionState == 1)
    elif key == "SelectionState.line" :
      return (selectionState == 2)
    else:
      return False

def ClearState( aView ) :
  global selectionState
  selectionState = 0

class Clipboards :
  def __init__( self ) :
    self.Current = 1
    self.LoadSettings()

  def LoadSettings( self ) :
    self.Clipboard_settings = sublime.load_settings("Clipboards.sublime-settings")
    self.Clipboards = [""] * int(self.Clipboard_settings.get("clipboards", 7))
    # print(self.Clipboards)

  def Push( self ) :
    self.Clipboards[self.Current] = sublime.get_clipboard()

  def Pull( self ) :
    sublime.set_clipboard(self.Clipboards[self.Current])

  def Set( self, Clip ) :
    prev = self.Current

    if (Clip != self.Current) and (Clip < len(self.Clipboards)) :
      try:
        self.Push()
      except:
        ()

      self.Current = Clip
      self.Pull()
#      print(self.Clipboards[self.Current])

    return prev

  def Restore( self, Clip ) :
    if (Clip != self.Current) and (Clip < len(self.Clipboards)) :
      self.Current = Clip
      self.Pull()

  def Append( self ) :
    cb = sublime.get_clipboard()
#    print("before " + self.Clipboards[self.Current])
    self.Clipboards[self.Current] = self.Clipboards[self.Current] + cb
    sublime.set_clipboard(self.Clipboards[self.Current])
#    print("after " + self.Clipboards[self.Current])

  def GetCurrent( self ) :
    return self.Current

Clips = None

class SetClipboardCommand( sublime_plugin.TextCommand ) :
  def run( self, edit, buffer ) :
    Clips.Set(buffer)

class PasteClipboardCommand( sublime_plugin.TextCommand ) :
  def run( self, edit, buffer, restore = False ) :
    prev = Clips.Set(buffer)
    self.view.run_command("paste")
    if restore :
      Clips.Restore(prev)

class AppendClipboardCommand( sublime_plugin.TextCommand ) :
  def run( self, edit, cmd ) :
    Clips.Push()
    self.view.run_command(cmd)
    Clips.Append()
    ClearState(self.view)

class ClipCutCommand( sublime_plugin.TextCommand ) :
  def run( self, edit ) :
    self.view.run_command("cut")
    ClearState(self.view)

class ClipCopyCommand( sublime_plugin.TextCommand ) :
  def run( self, edit ) :
    self.view.run_command("copy")
    ClearState(self.view)

class PasteAndSelectCommand( sublime_plugin.TextCommand ) :
  def run( self, edit ) :
    it = sublime.get_clipboard()
    rA = []
    if len(it) :
      vw = self.view
      for s in vw.sel() :
        chrs = vw.insert(edit, s.a, it)
        rA.append(sublime.Region(s.a, s.a + chrs))

      for r in rA :
        vw.sel().add(r)

def plugin_loaded(  ) :
  global Clips
  Clips = Clipboards()
