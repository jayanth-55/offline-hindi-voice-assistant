def recognize_command(text):
    text = text.strip().lower()

    # Time
    if "समय" in text or "टाइम" in text:
        return "GET_TIME"

    # Date
    elif "तारीख" in text or "दिनांक" in text or "डेट" in text:
        return "GET_DATE"

    # Greeting
    elif "नमस्ते" in text or "हेलो" in text or "नमस्कार" in text:
        return "GREETING"

    # Intro
    elif "कौन" in text or "परिचय" in text:
        return "INTRO"

    # Thanks
    elif "धन्यवाद" in text or "थैंक" in text or "शुक्रिया" in text:
        return "THANKS"

    # Status
    elif "ठीक" in text or "कैसे हो" in text:
        return "STATUS"

    # Help
    elif "मदद" in text or "हेल्प" in text:
        return "HELP"

    # Play music
    elif ("संगीत" in text or "गाना" in text) and \
         ("चल" in text or "बजा" in text or "शुरू" in text):
        return "PLAY_MUSIC"

    # Stop music
    elif ("संगीत" in text or "गाना" in text) and \
         ("बंद" in text or "रोक" in text or "स्टॉप" in text):
        return "STOP_MUSIC"

    # Volume up
    elif "बढ़" in text or "बढ" in text or "तेज" in text or "ज्यादा" in text:
        return "VOLUME_UP"

    # Volume down
    elif "कम" in text or "घटा" in text or "धीमा" in text:
        return "VOLUME_DOWN"

    # Exit
    elif "बंद हो" in text or "बंद करो" in text or "रुक जाओ" in text or "एग्जिट" in text:
        return "EXIT"

    else:
        return "UNKNOWN"
