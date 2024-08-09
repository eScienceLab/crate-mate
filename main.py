from pyld import jsonld
from linkml.validator import validate

import json
import logging

import argparse

example_path = "/workspace/example.json"
schema_path = "/workspace/schema.yaml"

def main(logger):
    # Load crate jsonld into json object
    with open(example_path, "r") as example_file, open(schema_path, "r") as schema_file:

        # ---------------------------------------------------------------------
        # Load json object from file
        logger.debug(f"Loading example file: {example_path}")

        try:
            crate_raw = json.load(example_file)
            logger.debug(f"Loaded example file: {example_path}")
        except Exception as e:
            print(f"Error: {e}")
            return

        logger.debug(f"Raw object: {json.dumps(crate_raw, indent=2)}")

        # ---------------------------------------------------------------------
        # Add a @base to the context
        logger.debug(f"Adding @base to context")
        
        uuid = "uuid-goes-here"
        base = f"arcp://uuid,{uuid}"            

        crate = {}
        crate['@context'] = {
            "@vocab": "https://w3id.org/ro/crate/1.1/context/",
            "@base": base
        }
        crate['@graph'] = crate_raw['@graph']

        logger.debug(f"Crate object after adding @base: {json.dumps(crate, indent=2)}")
        
        # ----------------------------------------------------------------------
        # Create a frame
        logger.debug(f"Creating frame")
        
        frame = {
            "@context": {
                "@vocab": "https://w3id.org/ro/crate/1.1/context",
            },
            "@id": f"ro-crate-metadata.json",
            "@embed": "@always"
        }
        options = {
            "base": base,
            "expandContext": crate['@context'],
            "extractAllScripts": False,
            "embed": "@always",
            "explicit": False,
            "omitDefault": False,
            "processingMode": "json-ld-1.1",
            "pruneBlankNodeIdentifiers": True,
            "requireAll": False,
        }

        logger.debug(f"Frame: {json.dumps(frame, indent=2)}")
        logger.debug(f"Options: {json.dumps(options, indent=2)}")
        
        # ---------------------------------------------------------------------
        # Apply framing
        logger.debug(f"Applying framing to {example_path}")
        
        framed = jsonld.frame(crate['@graph'], frame, options)

        logger.info(f"Framed object: {json.dumps(framed, indent=2)}")

        # ---------------------------------------------------------------------
        # Validate the framed object
        logger.debug(f"Validating the framed object")
        
        target_class = "Root"
        report = validate(framed, schema_path, target_class)

        logger.debug(f"Validation report: {report}")
        
        # ---------------------------------------------------------------------
        # Perform assertions
        logger.debug(f"Performing assertions")

        try:
            assert report.results == []
        except AssertionError as e:
            for result in report.results:
                logger.error(f"{result.message}")
            raise e

if __name__ == "__main__":

    # Parse command line agruments
    arg_parser = argparse.ArgumentParser(description="RO-Crate Framing Example")
    arg_parser.add_argument("--log", help="Set logging level", default="INFO")
    args = arg_parser.parse_args()

    # Set logging level
    logging.basicConfig(level=args.log)
    logger = logging.getLogger(__name__)
    
    main(logger)
 
