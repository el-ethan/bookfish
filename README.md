# Bookfish

Bookfish allows you to read Chinese novels from sites like http://www.kanunu8.com/ in plain text, rather than in the distracting, pop-up-filled browser environment.

To get the plain text of a novel, simply pass the url of a novel's index page to the Bookfish class:
    ```python
    >>> from bookfish import Bookfish
    >>> fish = Bookfish('http://www.kanunu8.com/book3/7198/159302.html')

Now you have your Bookfish instance `fish`, which you can do what you want with.
For example, `fish.book` will return the entire novel as a string. `fish.author` and `fish.title` will give the author and title, and `fish.charcount` will give you the length of the novel in characters. Additionally, when you instantiate your object, you can pass in `print_to_file=True` as a second argument, and this will print the entire novel to a file in your current working directory with a title matching the pattern `<title>_<author>.txt`. 
    ```python
    >>> Bookfish('http://www.kanunu8.com/book3/7193/', print_to_file=True)

Depending on the length of the novel you are processing, creating a Bookfish instance might take a while.
