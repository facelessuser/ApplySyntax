[![Unix Build Status][travis-image]][travis-link]
[![Package Control Downloads][pc-image]][pc-link]
# ApplySyntax
ApplySyntax is a plugin for Sublime Text 2 and 3 that allows you to detect and apply the syntax of files that might not otherwise be detected properly. For example, files with the `.rb` extension are usually Ruby files, but when they are found in a Rails project, they could be RSpec spec files, Cucumber step files, Ruby on Rails files (controllers, models, etc), or just plain Ruby files. This is actually the problem I was trying to solve when I started working on this plugin.

### Note
It forces predefined extensions, always overriding the user settings on the usual extension setting files as `PHP.sublime-settings`. To use different extensions, you must edit the package settings by yourself going on `Preferences -> Packages Settings -> ApplySyntax`. For example, if you need only `*.inc` files being used as anything else than PHP.

# Credits
DetectSyntax was originally created by phillipkoebbe.  In his words, these are his credits:

> It all started by forking the plugin created by JeanMertz [(1)][1]. I modified it quite extensively until I ended up with something entirely my own [(2)][2]. @maxim and @omarramos commented on the gist and suggested it should be part of Package Control. As I had created it solely for my own consumption, it seemed a bit "hard-coded" to be valuable as a package, but then I took a look at SetSyntax [(3)][3]. and saw how using settings would make it very flexible. That set me on the path that led to DetectSyntax.

[1]: https://gist.github.com/925008
[2]: https://gist.github.com/1497794
[3]: https://github.com/aparajita/SetSyntax

# Documentation
http://facelessuser.github.io/ApplySyntax/

[travis-image]: https://img.shields.io/travis/facelessuser/ApplySyntax/master.svg
[travis-link]: https://travis-ci.org/facelessuser/ApplySyntax
[pc-image]: https://img.shields.io/packagecontrol/dt/ApplySyntax.svg
[pc-link]: https://packagecontrol.io/packages/ApplySyntax
