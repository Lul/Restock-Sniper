# Restock-Sniper
This program was created with the intention to providing a solution to anyone seeking to snipe the restocking of an item which is sold out.\
**definitions.txt** and **supportedsites.txt** will be updated as I discover more websites to support.\
Any questions, or if there are websites you want added, feel free to email me at *johnthiell@gmail.com*.

# Usage
**1)** Install **Selenium**. `pip3 install selenium`\
**2)** Download the appropriate webdriver from *https://pypi.org/project/selenium/* for the matching browser of your choice. Move this file into the same folder as this program. ***WARNING: SAFARI NOT SUPPORTED***\
**3)** Create a file named **websites.txt**, this will serve as the list of items you want sniped.\
**4)** Insert the direct URLs of the items in which you want to be notified about upon restock.

Your **websites.txt** is backed up as **websites.bak** upon execution of this program.

# Creating Your Own Definitions
To create your own definition, you first need to examine the 'sold out' element on the webpage of the item you are trying to snipe.\
This program works by **class names**, and these belong inside the **definitions.txt** file.\
Additionally, add the website to the **supportedsites.txt** file in the format of **"website.com"**.
