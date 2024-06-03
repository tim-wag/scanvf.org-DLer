# About
A python file to download scans from the https://scanvf.org/ website and convert them to pdf.
# Usage
The downloads are outputed into the ```./outputs/TITLE/CHAPTER/``` folder.

Running the ```combine_to_pdf.py``` will output into ```./outputs/TITLE - PDF/CHAPTER.pdf```

*Note : the CHAPTER notation in the folders stands for a chapter/volume, depending on the manga. TITLE stands for the manga's title*
# Running
**Installing dependencies**

```python -m pip install -r requirements.txt```

**Running the downloader**

```python main.py```

**Running the PDF combiner**

```python combine_to_pdf.py```
