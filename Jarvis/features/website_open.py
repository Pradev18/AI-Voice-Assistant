import webbrowser

# Common sites dictionary to handle popular websites without needing ".com"
COMMON_SITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
    "amazon": "https://www.amazon.com",
    "wikipedia": "https://www.wikipedia.org"
}

def website_opener(domain):
    try:
        # Check if domain is in COMMON_SITES; if so, use the associated URL
        if domain in COMMON_SITES:
            url = COMMON_SITES[domain]
        else:
            # Append '.com' if no extension is provided
            if not (domain.endswith('.com') or domain.endswith('.org') or domain.endswith('.net')):
                domain += '.com'
            url = 'https://www.' + domain
        
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Error opening {domain}: {e}")
        return False
