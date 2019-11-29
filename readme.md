[![Build][github-ci-image]][github-ci-link]
[![Package Control Downloads][pc-image]][pc-link]
![License][license-image]
# ApplySyntax

ApplySyntax is a plugin for Sublime Text 2 and 3 that allows you to detect and apply the syntax of files that might not otherwise be detected properly. For example, files with the `.rb` extension are usually Ruby files, but when they are found in a Rails project, they could be RSpec spec files, Cucumber step files, Ruby on Rails files (controllers, models, etc), or just plain Ruby files. This is actually the problem I was trying to solve when I started working on this plugin.

# Credits

DetectSyntax was originally created by phillipkoebbe.  In his words, these are his credits:

> It all started by forking the plugin created by JeanMertz [(1)][1]. I modified it quite extensively until I ended up with something entirely my own [(2)][2]. @maxim and @omarramos commented on the gist and suggested it should be part of Package Control. As I had created it solely for my own consumption, it seemed a bit "hard-coded" to be valuable as a package, but then I took a look at SetSyntax [(3)][3]. and saw how using settings would make it very flexible. That set me on the path that led to DetectSyntax.

[1]: https://gist.github.com/925008
[2]: https://gist.github.com/1497794
[3]: https://github.com/aparajita/SetSyntax

# Documentation

http://facelessuser.github.io/ApplySyntax/

# License

Raw Line Edit is released under the MIT license.

Copyright (c) phillipkoebbe.

Changes: Copyright (c) 2013 - 2019 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[github-ci-image]: https://github.com/facelessuser/ApplySyntax/workflows/build/badge.svg
[github-ci-link]: https://github.com/facelessuser/ApplySyntax/actions?workflow=build
[pc-image]: https://img.shields.io/packagecontrol/dt/ApplySyntax.svg?logo=sublime%20text&logoColor=cccccc
[pc-link]: https://packagecontrol.io/packages/ApplySyntax
[license-image]: https://img.shields.io/badge/license-MIT-blue.svg
