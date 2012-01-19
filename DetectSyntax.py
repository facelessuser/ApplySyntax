import sublime, sublime_plugin
import os, string, re

class DetectSyntaxCommand(sublime_plugin.EventListener):
	def __init__(self):
		super(DetectSyntaxCommand, self).__init__()
		self.first_line = None
		self.file_name = None
		self.view = None
		self.syntaxes = None
		self.plugin_name = 'DetectSyntax'
		self.plugin_dir = sublime.packages_path() + os.path.sep + self.plugin_name
		self.user_dir = sublime.packages_path() + os.path.sep + 'User'


	def on_load(self, view):
		self.detect_syntax(view)

	
	def on_post_save(self, view):
		self.detect_syntax(view)
	  

	def detect_syntax(self, view):
		if view.is_scratch() or not view.file_name: # buffer has never been saved
			return

		self.reset_cache_variables(view)
		self.load_syntaxes()
		for syntax in self.syntaxes:
			# stop on the first syntax that matches
			if self.syntax_matches(syntax):
				self.set_syntax(syntax)
				break


	def reset_cache_variables(self, view):
		self.view = view
		self.file_name = view.file_name()
		self.first_line = view.substr(view.line(0))
		self.syntaxes = []


	def set_syntax(self, syntax):
		name = syntax.get("name")

		dirs = name.split(os.path.sep)
		name = dirs.pop()
		path = os.path.sep.join(dirs)

		if not path:
			path = name
	 
		new_syntax = 'Packages' + os.path.sep + path + os.path.sep + name + '.tmLanguage'
		current_syntax = self.view.settings().get('syntax')

		# only set the syntax if it's different
		if new_syntax != current_syntax:
			self.view.set_syntax_file(new_syntax)


	def load_syntaxes(self):
		settings = sublime.load_settings(self.plugin_name + '.sublime-settings')
		self.syntaxes = settings.get("syntaxes")


	def syntax_matches(self, syntax):
		rules = syntax.get("rules")

		for rule in rules:
			if 'function' in rule:
				result = self.function_matches(rule)
			else:
				result = self.regexp_matches(rule)

			# return on first match. don't return if it doesn't
			# match or else the remaining rules won't be applied
			if result:
				return True

		return False # there are no rules or none match


	def function_matches(self, rule):
		function = rule.get("function")
		path_to_file = function.get("source")
		function_name = function.get("name")

		# is path_to_file absolute?
		if not os.path.isabs(path_to_file):
			# it's not, so look in Packages/User
			if os.path.exists(self.user_dir + os.path.sep + path_to_file):
				path_to_file = self.user_dir + os.path.sep + path_to_file
			else:
				# now look in the plugin's directory
				path_to_file = self.plugin_dir + os.path.sep + path_to_file

		# I originally had error handling in here that would just return
		# False, but I decided to take it out in favor of letting the
		# exceptions bubble up so the end user will know something happened
		# in their function. So if the file doesn't exist, boom! If there is
		# an error in the code in the file, boom! If something else bombs
		# when calling the function (or the use provides the wrong function name),
		# boom! Either way, the user will get valuable feedback.

		with open(path_to_file, 'r') as the_file:
			function_source = the_file.read()

		exec(function_source)
		return eval(function_name + '(\'' + self.file_name + '\')')


	def regexp_matches(self, rule):
		if "first_line" in rule:
			subject = self.first_line
			regexp = rule.get("first_line")
		elif "file_name" in rule:
			subject = self.file_name
			regexp = rule.get("file_name")
		else:
			return False

		if regexp and subject:
			return re.match(regexp, subject) != None
		else:
			return False
