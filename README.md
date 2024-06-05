# About
Python files to download scans from the https://scanvf.org/ website and convert them to pdf.
# Usage
Run the ```main.py```file, it will guide you through the process.

The downloads are outputed into the ```./outputs/TITLE/CHAPTER/``` folder.

*I made the functions' input and output folders all optional arguments that default to ```./outputs/```, but feel free to customize pass the arguments suiting your own needs.*
***
Running the ```combine_to_pdf.py``` file will output into ```./outputs/TITLE - PDF/CHAPTER.pdf``` *by default*.

*Note : the TITLE notation stands for the manga's title and the CHAPTER notation stands for a chapter/volume used in the folders.*
# Running
**Installing dependencies**

```python -m pip install -r requirements.txt```

**Running the downloader**

```python main.py```

**Running the PDF combiner**

```python combine_to_pdf.py```
