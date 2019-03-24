# MD 2 HTML PARSER #
Made by Dmitri Qiu.
## Description
MD2HTML parser is a easy to use [Markdown](https://daringfireball.net/projects/markdown/ "About Markdown") parser/renderer written in Python. It's extendable, fast, and user friendly.
## Usage
Import MD2HTML to your project by `import MD2HTML as m2h` and then write the following code:
```python
with open("Your md doc.md") as doc:
    renderer = m2h.Renderer()
    result = renderer.render(doc, False, True, "Your/Image/Folder") # The first boolean is for not displaying line count
                                                                    # The second is for return as file object
    result.close()
```
Then, you will see a file named `"Your md doc.html"` show up in your project folder.
Congrats! You rendered a MD file to html using M2H for the first time!
## Licensing
MD2HTML is licensed under [GNU GPL V3.0](https://choosealicense.com/licenses/gpl-3.0/ "The license")  
(The license is longer than my code dude tf)

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