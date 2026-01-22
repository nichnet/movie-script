from elements import ElementType
import re


# Time of day shortcuts
TIME_SHORTCUTS = {
    'D': 'DAY',
    'N': 'NIGHT',
    'DN': 'DAY/NIGHT',
    'ND': 'NIGHT/DAY',
}

# Valid location prefixes
VALID_LOCATIONS = {'I', 'E', 'IE', 'EI'}

# Regex to match valid scene prefixes: #, #I, #E, #IE, #EI, with optional /time
# Time can be single word (/DAY) or quoted multi-word (/"Soon after")
# Pattern: #(I|E|IE|EI)?(/(?:"[^"]*"|\S+))?\s+(.*)
SCENE_PREFIX_PATTERN = re.compile(
    r'^#(IE|EI|I|E)?(/(?:"[^"]*"|\S+))?\s+(.*)$',
    re.IGNORECASE
)


def parse_scene_heading(trimmed):
    """Parse a scene heading line starting with #.

    Returns dict with 'int', 'ext', 'time', 'int_first', 'value' keys,
    or None if it doesn't match a valid scene pattern.
    """
    match = SCENE_PREFIX_PATTERN.match(trimmed)

    if not match:
        # No valid prefix found - treat everything after # as scene name
        # This handles cases like "#MY HOUSE" or "#BLACK"
        scene_name = trimmed[1:].strip()
        return {
            'int': False,
            'ext': False,
            'time': None,
            'int_first': True,
            'value': scene_name
        }

    location_part = match.group(1) or ''  # I, E, IE, EI, or empty
    time_part = match.group(2)  # /D, /NIGHT, etc. or None
    scene_name = match.group(3)  # The rest

    result = {
        'int': False,
        'ext': False,
        'time': None,
        'int_first': True,
        'value': scene_name.strip()
    }

    # Parse location
    location_upper = location_part.upper()
    if location_upper == 'I':
        result['int'] = True
    elif location_upper == 'E':
        result['ext'] = True
    elif location_upper == 'IE':
        result['int'] = True
        result['ext'] = True
        result['int_first'] = True
    elif location_upper == 'EI':
        result['int'] = True
        result['ext'] = True
        result['int_first'] = False

    # Parse time (remove leading / and optional quotes, always uppercase)
    if time_part:
        time_val = time_part[1:]  # Remove the /
        # Strip quotes if present (for multi-word times like /"Soon after")
        if time_val.startswith('"') and time_val.endswith('"'):
            time_val = time_val[1:-1]
        time_val = time_val.upper()
        result['time'] = TIME_SHORTCUTS.get(time_val, time_val)

    return result


def parse_line(line):
    trimmed = line.strip()

    if trimmed.isspace() or len(trimmed) == 0:
        return None

    # Default: action/description
    out = {
        'type': ElementType.ACTION,
        'value': trimmed.strip()
    }

    # Title page elements: **T, **A, **C, **D
    if trimmed.startswith('**'):
        remainder = trimmed[2:]
        if remainder.startswith('T '):
            out['type'] = ElementType.TITLE_PAGE_TITLE
            out['value'] = remainder[2:].strip()
        elif remainder.startswith('A '):
            out['type'] = ElementType.TITLE_PAGE_AUTHOR
            out['value'] = remainder[2:].strip()
        elif remainder.startswith('C '):
            out['type'] = ElementType.TITLE_PAGE_COMMENT
            out['value'] = remainder[2:].strip()
        elif remainder.startswith('D '):
            out['type'] = ElementType.TITLE_PAGE_DATE
            out['value'] = remainder[2:].strip()
        return out

    # In-script title (single *)
    if trimmed.startswith('*') and not trimmed.startswith('**'):
        out['type'] = ElementType.TITLE
        out['value'] = trimmed[1:].strip()
        return out

    # Transition (##)
    if trimmed.startswith('##'):
        out['type'] = ElementType.TRANSITION
        out['value'] = trimmed[2:].strip()
        return out

    # Scene heading (#)
    if trimmed.startswith('#'):
        out['type'] = ElementType.SCENE
        scene_info = parse_scene_heading(trimmed)
        out['int'] = scene_info['int']
        out['ext'] = scene_info['ext']
        out['time'] = scene_info.get('time')
        out['int_first'] = scene_info.get('int_first', True)
        out['value'] = scene_info['value']
        return out

    # Dialogue (@)
    if trimmed.startswith('@'):
        out['type'] = ElementType.DIALOGUE
        # Use greedy match (.*) to capture everything up to the LAST quote
        pattern = r'@(\s*.*?)\s*\"(.*)\"'
        matches = re.findall(pattern, trimmed)

        for match in matches:
            speaker, quoted = match
            out['speaker'] = speaker.strip()
            out['value'] = quoted.strip()
        return out

    return out
