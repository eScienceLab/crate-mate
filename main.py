from pyld import jsonld
from linkml.validator import validate

import argparse
import json
import logging

import absolutise
import framing

example_path = "/workspace/example.json"
schema_path = "/workspace/schema.yaml"

def main(logger):
    # Load crate jsonld into json object
    with open(example_path, "r") as example_file:

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

        crate = absolutise.absolutise(logger, crate_raw)
        
        # ----------------------------------------------------------------------
        # Apply framing
        
        frame = {
            "@id": f"ro-crate-metadata.json",
        }

        framed = framing.apply_frame(logger, crate, frame)

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

    # ---------------------------------------------------------------------
    # Parse command line agruments
    
    arg_parser = argparse.ArgumentParser(description="RO-Crate Framing Example")
    arg_parser.add_argument("--log", help="Set logging level", default="INFO")
    args = arg_parser.parse_args()

    # ---------------------------------------------------------------------
    # Set logging level
    
    logging.basicConfig(level=args.log)
    logger = logging.getLogger(__name__)
    
    main(logger)
 
