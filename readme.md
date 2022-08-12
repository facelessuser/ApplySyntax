[![Donate via PayPal][donate-image]][donate-link]
[![Discord][discord-image]][discord-link]
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

https://facelessuser.github.io/ApplySyntax/

# License

ApplySyntax is released under the MIT license.

[github-ci-image]: https://github.com/facelessuser/ApplySyntax/workflows/build/badge.svg?branch=master&event=push
[github-ci-link]: https://github.com/facelessuser/ApplySyntax/actions?query=workflow%3Abuild+branch%3Amaster
[discord-image]: https://img.shields.io/discord/678289859768745989?logo=discord&logoColor=aaaaaa&color=mediumpurple&labelColor=333333
[discord-link]: https://discord.gg/TWs8Tgr
[pc-image]: https://img.shields.io/packagecontrol/dt/ApplySyntax.svg?labelColor=333333&logo=sublime%20text
[pc-link]: https://packagecontrol.io/packages/ApplySyntax
[license-image]: https://img.shields.io/badge/license-MIT-blue.svg?labelColor=333333
[donate-image]: https://img.shields.io/badge/Donate-PayPal-3fabd1?logo=paypal
[donate-link]: https://www.paypal.me/facelessuser
