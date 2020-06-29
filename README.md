# Nlp- conference research project
This research is an independent study course under the guidance of Professor Andrew Petersen at University of Toronto Mississauga.

The goal of the research is to identify whether particular fields are open to minorities of various sorts (gender, ethnic background) by mining the major conferences for a field to see
(a) who is attending / presenting 
(b) who is placed in a position of responsibility or prominence (like a session chair, keynote speaker or author). 

This will require mining webpages of various sorts and using NLP to try to identify key pieces of information.

## scraping-adv.py
For using this software for pulling names and contextual information from two conference websites in the domain of Artificial Intelligence:

Make sure you have installed Python3.0 or higher and JAVA 8 (in order to use tika for parsing pdf) in your computer, as well as install and import all modules properly.
The conference websites are listed below:
AAAI Conference:
urls = ['https://aaai.org/Conferences/AAAI-20/',
        'https://aaai.org/Conferences/AAAI-19/',
        'https://aaai.org/Conferences/AAAI-18/',
        'https://aaai.org/Conferences/AAAI/aaai17.php',
        'https://aaai.org/Conferences/AAAI/aaai16.php',
        'https://aaai.org/Conferences/AAAI/aaai15.php',
        'https://aaai.org/Conferences/AAAI/aaai14.php',
        'https://aaai.org/Conferences/AAAI/aaai13.php']

APPLIED AI Summit:
urls = ['https://www.re-work.co/events/applied-ai-summit-san-francisco-2021',
         'https://www.re-work.co/events/applied-ai-summit-san-francisco-2020',
         'https://www.re-work.co/events/applied-ai-summit-san-francisco-2019',
         'https://www.re-work.co/events/applied-ai-summit-houston-2018']
         
         
