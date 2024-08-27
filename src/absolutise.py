import json

def absolutise(logger, input_crate):
    """
    Add a @base to the context of the input crate and return the updated crate.

    :param logger: The logger object.
    :type logger: logging.Logger
    
    :param input_crate: The input crate to add a @base to.
    :type input_crate: dict
    
    :return: The updated crate with a @base added to the context.
    """
    logger.debug(f"Adding @base to context")
        
    uuid = "uuid-goes-here"
    base = f"arcp://uuid,{uuid}"            

    crate = {}
    crate['@context'] = {
        "@vocab": "https://w3id.org/ro/crate/1.1/context/",
        "@base": base
    }
    crate['@graph'] = input_crate['@graph']

    logger.debug(f"Crate object after adding @base: {json.dumps(crate, indent=2)}")
    return crate
