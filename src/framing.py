import json
from pyld import jsonld

def apply_frame(logger, crate, frame):
    logger.debug(f"Applying framing to crate")

    # -------------------------------------------------------------------------
    # Set up framing 
    
    options = {
        "base": crate['@context']['@base'],
        "expandContext": crate['@context'],
        "extractAllScripts": False,
        "embed": "@never",
        "explicit": False,
        "omitDefault": False,
        "processingMode": "json-ld-1.1",
        "pruneBlankNodeIdentifiers": True,
        "requireAll": False,
    }

    logger.debug(f"Frame: {json.dumps(frame, indent=2)}")
    logger.debug(f"Options: {json.dumps(options, indent=2)}")

    # -------------------------------------------------------------------------
    # Apply framing
    
    framed = jsonld.frame(crate['@graph'], frame, options)
    
    logger.info(f"Framed object: {json.dumps(framed, indent=2)}")

    return framed

