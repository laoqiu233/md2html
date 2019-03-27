# MD 2 HTML PARSER #
Made by Dmitri Qiu.
## Description
MD2HTML parser is a easy to use [Markdown](https://daringfireball.net/projects/markdown/ "About Markdown") parser/renderer written in Python. It's extendable, fast, and user friendly.
---
# Usage
Import MD2HTML to your project by `import MD2HTML as m2h` and then write the following code:
```python
with open("Your md doc.md") as doc:
    renderer = m2h.Renderer()
    result, metadata = renderer.render(doc, False, True, "Your/Image/Folder") # The first boolean is for not displaying line count
                                                                              # The second is for return as file object
    result.close()
```
Then, you will see a file named `"Your md doc.html"` show up in your project folder.
Congrats! You rendered a MD file to html using M2H for the first time!
## Custom tags
Adding custom tags in m2h is as easy as writing a simple parsing function!
Your function will need to look like this:
```python
def your_func(self, line, file, line_count):
    # Parsing
    return (parsed_text, line_count + 1)
```
And then just use a decorator or a function to add your custom parsing function into the renderer!
```python
# Using a function
renderer.addBlockElem(r"Your regex pattern", your_func)

# Using a decorator
@renderer.addBlockElem(r"Your regex pattern")
def your_func(self, line, file, line_count):
    # Parsing
    return (parsed_text, line_count + 1)
```
After adding your custom function, you can just render like you usually do.
## Examples
The example is a really simple custom md tag that renders text in a `<code>` element but the text inside it is all red.
First, we need to create a parsing function.
```python
renderer = m2h.Renderer()
# Make the function a custom tag parser.
@renderer.addBlockElem(r"\|\|\|\n?")
def redCode(self, line, file, line_count):
    """
        'self' argument is the renderer itself, use self to access functions in renderers, or variables like emphasis_tags, md_tags.
        'line' argument is the first matched line of your regex pattern.
        'file' argument is the file that the renderer is parsing.
        'line_count' argument is the line count of the line matched, don't forget to add 1 to this argument everytime you use the file.readline() function, and if the next line isn't matching your md tag, you should subtract 1 from line_count.
        All parsing function should have this four arguments(Including 'self'). 
    """
    # Currently 'line' should be our first matched text, which is '|||'(The regex pattern is r"\|\|\|\n?")
    result = "<pre><code>\n" # Open the html tags
    # Make a loop to parse until eof or not matching text
    while True:
        # Read a new line and add the line_count
        line = file.readline()
        line_count += 1
        # Check if it's the eof our end of element
        if line == "" or re.match(r"\|\|\|\n?", line): break
        # If not add the line to our parsed text
        result += line
    result += "</code></pre>\n" # Close the html tags
    return (result, line_count + 1)
    """
        The returned value should be a tuple containing the parsed text and the line count of the first line after this md element. 
    """
```
Now let's try adding a custom emphasis parser that makes a span of text red and bold.
```python
renderer = m2h.Renderer()
@renderer.addEmphasis(r"\|(.+)\|")
def redText(self, match):
    """
        The 'self' argument is the same as the block element parser.
        'match' argument is the match or your regexr pattern.
    """
    # In emphasis parsers you only need to return the rendered text.
    return "<span style=\"color:red; font-weight:bold;\">%s</span>" %(match.group(0))
```
Emphasis and block element parsers all can be written in a lambda function, as long as they have the correct arguments and return types:
```python
renderer = m2h.Renderer()
redText = lambda self, match: "<span style=\"color:red; font-weight:bold;\">%s</span>" %(match.group(0))
renderer.addEmphasis(r"\|(.+)\|", redText) 
```
---
## Licensing
MD2HTML is licensed under [GNU GPL V3.0](https://choosealicense.com/licenses/gpl-3.0/ "The license")  
(The license is longer than my code dude tf)
---
# Everything down below is written for *testing purposes*
## Capybara facts
* Capybaras are cute!  
#![Capybara image](https://media1.fdncms.com/orlando/imager/u/blog/2516965/sfds.jpg?cb=1471435085 "A capybara")#

* Capybaras come in diffrent colors:
    1. Yellow
    2. Capybara color
    3. Spikey dude  
#![Spikey dude](https://a-z-animals.com/media/animals/images/180x170/capybara1.jpg "This is a spikey dude")#

* Capybaras are chill af

* Capybaras are generally cool dudes to hang out with

## Cool cats
Shuchi senpai  
![best boi](https://static.tvtropes.org/pmwiki/pub/images/cat_6.jpg "Id smash")  
Maxwell the cat  
![maxwell the cat](Maxwell.png "qt3.14")  
^ This won't render on github because this uses the dedicated image folder feature in the parser

    This is code
    This is the second line of the code
``` 
This is code too
```

>A great philosopher once said:
>>~~**Yiff** me daddy *uwu*~~  
>>And then he wrote this piece of code:  
>```python
>cat = 1
>def yiff():
>    print ("Owo whats dis?")
>    # Aww yes give me the good ***y e e f s***
>```

|Table|Test|Henlo|
|:---|---:|:---:|---|
henlo|this|is test
|*This*|**is**|~~test~~|
|with|~~emphasis~~|heaw ya my chigga|
^I don't know why this table doesn't render properly on github, it works fine using my parser