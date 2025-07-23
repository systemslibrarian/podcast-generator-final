import yaml # Import the PyYAML package
import xml.etree.ElementTree as xml_tree # Import the ElementTree module from the xml.etree package
import sys # Import sys for exiting gracefully

# --- Configuration and File Loading ---
FEED_YAML_FILE = 'feed.yaml'
OUTPUT_XML_FILE = 'podcast.xml'

# Load YAML data from file with error handling
try:
    with open(FEED_YAML_FILE, 'r') as file:
        yaml_data = yaml.safe_load(file) # Use the safe_load() function to load the YAML data from the file
except FileNotFoundError:
    print(f"Error: '{FEED_YAML_FILE}' not found. Please ensure it exists in the root directory.")
    sys.exit(1) # Exit with an error code
except yaml.YAMLError as exc:
    print(f"Error parsing '{FEED_YAML_FILE}': {exc}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred while loading '{FEED_YAML_FILE}': {e}")
    sys.exit(1)

# --- Input Validation ---
# Define required top-level keys in the YAML file
required_top_level_keys = [
    'link', 'format', 'title', 'subtitle', 'author', 'description',
    'image', 'language', 'category', 'item'
]

for key in required_top_level_keys:
    if key not in yaml_data or yaml_data[key] is None:
        print(f"Error: Missing or empty required top-level key '{key}' in '{FEED_YAML_FILE}'.")
        sys.exit(1)

# Ensure 'item' is a list and not empty
if not isinstance(yaml_data['item'], list) or not yaml_data['item']:
    print(f"Error: 'item' must be a non-empty list in '{FEED_YAML_FILE}'.")
    sys.exit(1)

# Define required keys for each podcast item
required_item_keys = ['title', 'description', 'duration', 'published', 'file', 'length']

# --- XML Generation ---
# Create RSS element with appropriate attributes and namespaces
rss_element = xml_tree.Element('rss', {
    'version': '2.0',
    'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
})

channel_element = xml_tree.SubElement(rss_element, 'channel') # Create channel element as a child of the RSS element
link_prefix = yaml_data['link'] # Store the link prefix in a variable for convenience

# Add subelements to the channel element using data from the YAML file
# Using a helper function to add elements safely
def add_subelement_text(parent, tag, text, attributes=None):
    """Helper to add a subelement with text, handling None values."""
    if text is not None:
        elem = xml_tree.SubElement(parent, tag, attributes if attributes else {})
        elem.text = str(text) # Convert to string to avoid potential issues

add_subelement_text(channel_element, 'link', link_prefix)
add_subelement_text(channel_element, 'format', yaml_data.get('format'))
add_subelement_text(channel_element, 'title', yaml_data.get('title'))
add_subelement_text(channel_element, 'subtitle', yaml_data.get('subtitle'))
add_subelement_text(channel_element, 'itunes:author', yaml_data.get('author'))
add_subelement_text(channel_element, 'description', yaml_data.get('description'))

# itunes:image requires an 'href' attribute
if 'image' in yaml_data and yaml_data['image'] is not None:
    xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data['image']})
else:
    print("Warning: 'image' key is missing or empty. iTunes image will not be set.")

add_subelement_text(channel_element, 'language', yaml_data.get('language'))
# Note: The 'link' element is added twice in the original, keeping for fidelity
add_subelement_text(channel_element, 'link', link_prefix)

# Create an 'itunes:category' subelement
if 'category' in yaml_data and yaml_data['category'] is not None:
    xml_tree.SubElement(channel_element, 'itunes:category', {'text': yaml_data['category']})
else:
    print("Warning: 'category' key is missing or empty. iTunes category will not be set.")

# Loop through each item in the YAML file's 'item' section
for i, item in enumerate(yaml_data['item']):
    item_element = xml_tree.SubElement(channel_element, 'item')

    # Validate each item's required keys
    for key in required_item_keys:
        if key not in item or item[key] is None:
            print(f"Error: Missing or empty required key '{key}' in item {i+1} of '{FEED_YAML_FILE}'.")
            sys.exit(1)

    add_subelement_text(item_element, 'title', item.get('title'))
    add_subelement_text(item_element, 'itunes:author', yaml_data.get('author')) # Author from top-level
    add_subelement_text(item_element, 'description', item.get('description'))
    add_subelement_text(item_element, 'itunes:duration', item.get('duration'))
    add_subelement_text(item_element, 'pubDate', item.get('published'))

    # Add an 'enclosure' subelement
    enclosure_url = link_prefix + item.get('file', '')
    enclosure_length = str(item.get('length', 0)) # Ensure length is a string
    xml_tree.SubElement(item_element, 'enclosure', {
        'url': enclosure_url,
        'type': 'audio/mpeg', # Assuming audio/mpeg, could be made configurable
        'length': enclosure_length
    })

# Write the created XML tree to a file
try:
    output_tree = xml_tree.ElementTree(rss_element) # Create an ElementTree object from the RSS element
    # Pretty print the XML for readability
    xml_tree.indent(output_tree, space="  ", level=0)
    output_tree.write(OUTPUT_XML_FILE, encoding='UTF-8', xml_declaration=True) # Write the XML tree to a file
    print(f"Successfully generated '{OUTPUT_XML_FILE}'")
except Exception as e:
    print(f"Error writing XML to '{OUTPUT_XML_FILE}': {e}")
    sys.exit(1)
