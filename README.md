# fast_file_search
A Tkinter based file search inspired by my onion_file_search


Inspired by my previous project [onion_file_search](https://github.com/jimbob88/onion_file_search), this is a file searching utility that drops the cascading design of onion_file_search, and returns a more [Catfish](https://launchpad.net/catfish-search) style return result.

An example of the program running is shown below:

![Example of Program Running](https://user-images.githubusercontent.com/9913366/114072689-74639180-989a-11eb-9878-b03f1865bf47.png)


It is intended to by lightweight and fast to try and serve as a replacement for the ever slower explorer search.
This software relies on the amazing [scandir_rs](https://github.com/brmmm3/scandir-rs), which provides extremely fast search speeds on Windows, and the Linux speeds aren't anything to laugh at either! I personally realised its glorious speeds under my documention of file searching, [python_file_hunting](https://github.com/jimbob88/python_file_hunting), and since then added its featureset to `onion_file_search` and now `fast_file_search` relies entirely on the speeds that `scandir_rs` gives the community!
