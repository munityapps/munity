def get_request_lang(request):
    """Get the "lang" header from a request object. If the value is None or unsupported, return the default lang."""
    supported_languages = ["en", "fr"]
    default_language = "en"
    assert default_language in supported_languages

    language = request.data.get("lang")

    return language if language in supported_languages else default_language
