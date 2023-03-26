# Inkwell

Inkwell is an open-source transcript authoring software written in Python that simplifies the process of editing transcripts. The software utilizes the PyQt library to provide a customizable user interface.

One of the unique features of Inkwell is its ability to format transcripts written in a simple markdown style automatically, saving users time and effort that would otherwise be spent on manual formatting. Additionally, Inkwell includes a range of editing tools to help users make quick and precise changes to their transcripts.

The software is constantly being updated with new features and improvements to enhance its user-friendliness and functionality. 

![Example](https://github.com/nichnet/movie-script/blob/master/example/example_1.png)

## Usage

Whilst in development: 
```python
python main.py
```

## Formatting


| Type | Prefix |
| --- | :---: |
|Title|\*|
|Transition|##|
|Scene|#|
|Action||
|Dialogue|@speaker "speech"|


*Star Trek
##FADE IN
#BLACK
Absolute Quiet. SOUND bleeds in. Low level b.g. NOISES of Enterprise bridge, clicking of relays, minor electronic effects. We HEAR A FEMALE voice.
@SAaVIK'S VOICE "Captain's log. Stardate 8130.3, Starship Enterprise on trianing mission to Gamma Hydra. Section 14, coordinates 22/87/4. Approaching Neutral Zone, all systems functioning."
#I ENTERPRISE BRIDGE
As the ANGEL WIDENS, we see the crew at stations; (screens and visual displays are in use): COMMANDER SULU at the helm, COMMANDER UHURA at the Comm Console, DR. BONES McCOY and SPOCK at his post. The Captain is new -- and unexpectedd LT. SAAVIK is young and beautiful. She is half Vulcan and half Romulan. In appearnace she is Vulcan with pointed ears, but her skin is fair and she has none of the expressionless facial immobility of a Vulcan.
@sulu "Leaving Section Fourteen for Section Fifteen."
@saavik "Project parabolic course to avoid entering Neutral Zone."
@sulu "Aye, Captain."
@uhura "Captain... I'm getting something on the distress channel. Minimal signal... but something..."
@Saavik"Can you amplify?"
@UHURA 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
