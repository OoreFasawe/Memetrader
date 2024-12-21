# Helper function to process marketcap and volume
def process_value(value):
    """Remove 'k' and multiply by 1000, remove '$' and strip spaces."""
    return float(value.replace('k', '').replace('$', '').strip()) * 1000

# Helper function to convert age into seconds
def process_age(age):
    """Convert age (e.g., '3m ago', '1h ago', '2d ago') into seconds."""
    age_parts = age.split(' ')
    age_seconds = 0

    if len(age_parts) == 2:
        value = age_parts[0]

        if 'm' in value:  # minutes
            age_seconds = int(value[:-1]) * 60
        elif 'h' in value:  # hours
            age_seconds = int(value[:-1]) * 3600
        elif 'd' in value:  # days
            age_seconds = int(value[:-1]) * 86400
        elif 's' in value:  # seconds
            age_seconds = int(value[:-1])

    return age_seconds

def extract_data_from_element(element):
    """Extract link, marketcap, volume, and age from the anchor element."""
    link = element.get_attribute("href")
    img_tag = element.find_element("tag name", "img")
    name = img_tag.get_attribute("alt")
    # Get associated marketcap, volume, and age
    properties = element.text.split("\n")
    marketcap = properties[1]
    volume = properties[3]
    age = properties[4]

    # Process marketcap, volume, and age
    marketcap_processed = process_value(marketcap)
    volume_processed = process_value(volume)
    age_processed = process_age(age)

    return name, link, marketcap_processed, volume_processed, age_processed