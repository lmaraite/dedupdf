# dedupdf
Remove duplicated pages from PDF files (like animations in PDF export slides).
Some slides which get exported to PDF and handed out to attendees of a presentation 
may contain duplications if the presenter used animations. 
This can be pretty annoying if you want to take notes in the PDF or just want to 
skim the slides.


With `dedupdf` you can automatically remove those duplications. It does so by checking the
headings and first lines of each slide and removing those which are duplicated. 

### Installation

#### Conda
To install via conda you need conda as a prerequisite. 
* https://www.anaconda.com/docs/getting-started/miniconda/install

Once you have conda installed you can clone the repo and create the environment:
```
git clone https://github.com/lmaraite/dedupdf.git
cd dedupdf
conda env create -f environment.yaml
```

### Run

#### Conda
Use the help manual for detailed information:

```
conda run python main.py --help
```

Examples:

```
conda run python main.py test.pdf
```

```
conda run python main.py test.pdf -o test-clean.pdf
```