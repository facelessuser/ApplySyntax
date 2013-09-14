ApplySyntax
============

Description
-----------

ApplySyntax is a plugin for Sublime Text 2 and 3 that allows you to detect and apply the syntax of files that might not otherwise be detected properly. For example, files with the `.rb` extension are usually Ruby files, but when they are found in a Rails project, they could be RSpec spec files, Cucumber step files, Ruby on Rails files (controllers, models, etc), or just plain Ruby files. This is actually the problem I was trying to solve when I started working on this plugin.

Installation
------------

ApplySyntax can be installed in a variety of ways:

* Through [wbond](https://sublime.wbond.net)'s Package Control at [https://sublime.wbond.net](https://sublime.wbond.net)

	Open Package Control
	Select 'Install Package'
	Find and select 'ApplySyntax'

* By cloning this repository in Packages
	
	```bash
	# cd into your Packages folder
	git clone git://github.com/facelessuser/ApplySyntax.git .
	
	# if sublime 3
	git clone -b ST3 git://github.com/facelessuser/ApplySyntax.git .
	```

* By downloading the files and placing them in a directory under Packages, such as ApplySyntax or User

	If you don't put the files in Packages/User (you *can*, but probably shouldn't), make sure they live in Packages/ApplySyntax. If you download and extract a compressed archive from GitHub, the directory will be `facelessuser-ApplySyntax`. Remove `facelessuser-`.

Usage
-----

ApplySyntax is based on the idea that there are rules for selecting a certain syntax. You define the rules, the plugin checks them. The first one to pass wins. If you have need of multiple conditions that must be met, you should use the function rule. See the default settings file for more on function rules.

Create your own rules in `Packages/User/ApplySyntax.sublime-settings`. The easiest way to get started is to just copy the default settings file found in `Packages/ApplySyntax/ApplySyntax.sublime-settings` to your user directory and modify it to meet your needs. Make sure you rename the `default_syntaxes` key to just `syntaxes`. If you don't, you will overwrite the default syntaxes and they will not work.

See the default settings file for examples and comments related to creating rules.

Credits
-------

[@facelessuser](https://github.com/facelessuser) is the current maintainer of ApplySyntax (originally [DetectSyntax](https://github.com/phillipkoebbe/DetectSyntax))

DetectSyntax was created by [@phillipkoebbe](https://github.com/phillipkoebbe). The following quote from him summarizes the motivation and history of the package:

> It all started by forking the plugin created by [@JeanMertz](https://github.com/JeanMertz)¹. I modified it quite extensively until I ended up with something entirely my own². [@maxim](https://github.com/maxim) and [@omarramos](https://github.com/omarramos) commented on the gist and suggested it should be part of [Package Control](https://github.com/wbond/sublime_package_control). As I had created it solely for my own consumption, it seemed a bit "hard-coded" to be valuable as a package, but then I took a look at SetSyntax³ and saw how using settings would make it very flexible. That set me on the path that led to DetectSyntax.

1. [https://gist.github.com/925008](https://gist.github.com/925008)
2. [https://gist.github.com/1497794](https://gist.github.com/1497794)
3. [https://github.com/aparajita/SetSyntax](https://github.com/aparajita/SetSyntax) *(no longer exists)*

Contributing
------------

* Fork the project.
* Use topic branch.
* Make pull request.

History
-------

2013-01-11

* Corrected location of Blade PHP files.

2013-01-05

* Added support for Blade PHP files.

2012-11-18

* Added support for zsh config files. [Thanks Benjamin Smith]

2012-10-25

* Added ability to match all rules. [Thanks for the idea Kirk Strauser]

2012-10-20

* Added jbuilder to the Ruby rule. [Thanks Aaron Crespo]
* Expanded Vagrantfile rule to catch extensions (like Vagrantfile.local).

2012-09-01

* Removed Puppet files from Ruby syntax. See https://github.com/phillipkoebbe/DetectSyntax/issues/11 for details.
* Added some more files to YAML, PHP, XML, INI, and ShellScript. [Thanks Chris Jones]

2012-08-13

* User-defined syntax rules get processed first now. [Closes #11]

2012-08-07

* Added rule to Ruby syntax for Puppet (pp) files.

2012-07-12

* Added support for .simplecov (https://github.com/colszowka/simplecov#using-simplecov-for-centralized-config) [Closes #9, thanks Andrey Botalov]
* Added Preferences menu [Closes #8, thanks Kirk Strauser]
* Create a bare-bones user settings file if one doesn't exist

2012-07-02

* Fixed improper handling of directories with non-ascii characters [Closes #5, thanks Andrew Dryga]

2012-06-28

* Better handling of file defining a function potentially not existing.

2012-06-26

* Added new_file_syntax so new files can have a syntax applied immediately.

2012-06-20

* Added rule for *.thor (thanks Magnus Rex).

2012-04-13

* Renamed the `syntaxes` key to `default_syntaxes` so it is no longer necessary to duplicate default rules in User/DetectSyntax.sublime-settings.

2012-03-23

* Added rule type of 'binary' which builds a shebang regexp for the user.

2012-03-22

* Check to make sure the syntax file exists before trying to set it. [Closes #3, thanks tito]
