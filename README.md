# Inkwell

Inkwell is an open-source transcript authoring software that simplifies the process of editing transcripts. The software is written in Python and utilizes the PyQt library.

One of the unique features of Inkwell is its ability to format transcripts written in a simple markdown style automatically, saving users time and effort that would otherwise be spent on manual formatting. Additionally, Inkwell includes a range of editing tools to help users make quick and precise changes to their transcripts.

The software is constantly being updated with new features and improvements to enhance its user-friendliness and functionality. 

![Example](https://github.com/nichnet/movie-script/blob/master/example/example_1.png)


## Usage
```python
python main.py
```


## Features
- Simple markdown style editor, and page preview
- Also supports tags like <b>, <i>, etc.
- Saving/Loading files
- Printing to PDF


## Formatting

| Type | Prefix | Example |
| --- | :---: | :--- |
|Title|\*| \*Star Trek|
|Transition|##| ##FADE IN |
|Scene|#| #BLACK
|Scene, Interior |#I | #I ENTERPRISE BRIDGE
|Scene, Exterior |#E | #SPACE
|Action||Absolute quiet. SOUND bleeds in...|
|Dialogue|@speaker "speech"| @SAAVIK'S VOICE "Captain's log. Stardate 8130..." |


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
