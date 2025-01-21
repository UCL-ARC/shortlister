# Shortlister

Light-weight program that assists with shortlisting candidates in a management setting.  

## Quick start

Run the following script from terminal:

```bash
shortlist <role_directory>
# <role_directory> : the path to your folder containing both:
# 1.criteria(.csv file) - see test_role folder for formatting examples
# 2.candidate CVs(.pdf files)
``` 
Optional arguments avaliable which offers additional functionalities:

```bash
shortlist <role_directory> -w
# deploys webview for pdf files
```

## Functionalities

```?``` for help (list avaliable key options in the current view)

*Note*: keys are case sensitive, ```r``` is different to ```R```

#### Sorting applicants
- Alphabetical
- Score (Ascending/Descending)
- Interactive comparison sort
#### Filtering
- allow users to enter their own expressions
- up/down arrow keys for filtering templates 
- allow regex expressions

#### Mark applicant
- select a criterion and give an appropiate score
- create notes on selected applicant
#### Ranking
- Quickly compare a list of applicant
#### Export excel spreadsheet
- Export the applicant table to an Excel spreadsheet 
#### PDF Webview
- Open pdfs automatically in webview if viewing details for a specific applicant 
#### REPL:
- Open a Python REPL within the terminal
- Developer mode (full control to the program)
