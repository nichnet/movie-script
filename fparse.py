from constants import ElementType
import re


def parse_line(line):
    trimmed = line.strip()

    if trimmed.isspace() or len(trimmed) == 0:
        return None
    
    #default, action/description, normal text.
    out = {
        'type': ElementType.ACTION,
        'value': trimmed.strip()
    }

    if trimmed.startswith('*'):
        out['type'] = ElementType.TITLE
        out['value'] = trimmed[1:]#.upper()
        #title
    if trimmed.startswith('##'):
        #transition
        out['type'] = ElementType.TRANSITION
        out['value'] = trimmed[2:]#.upper()
    elif trimmed.startswith('#'):
        #scene
        out['type'] = ElementType.SCENE

        startIndex = 1

        #interior/exterior scene
        if trimmed.startswith('#I'):
            out['int'] = True
            startIndex = 2
        elif trimmed.startswith('#E'):
            out['ext'] = True
            startIndex = 2

        out['value'] = trimmed[startIndex:].strip()#.upper()
    elif trimmed.startswith('@'):
        #speech 
        out['type'] = ElementType.DIALOGUE
        #ACTUAL speech is in quotes, outside is the speaker.
        pattern = r'@(\s*.*?)\s*\"(.*?)\"'
        matches = re.findall(pattern, trimmed)
        

        for match in matches:
            speaker, quoted = match
            out['speaker'] = speaker.strip()#.upper()
            out['value'] = quoted.strip()
   # else:
    #    out['value'] = trimmed.strip()
    
    return out

