import re

# Pattern for fulltext links in transformed xml
# Captures the URL
fulltext_pattern = re.compile(r'<fulltext-url>(.*)</fulltext-url>')
# Pattern for xml header (e.g. <?xml version="1.0" encoding="UTF-8"?>)
xml_header_pattern = re.compile(r'<\?xml(.+?)\?>')