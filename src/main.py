from pyld import jsonld
import linkml.validator as lmval

import argparse
import json
import logging
import os

from src import absolutise
from src import framing

example_path = "/workspace/example.json"
schema_dir = "/workspace/schema"

def main(logger=None, input_path=None):
    # Load crate jsonld into json object
    with open(example_path, "r") as example_file:

        # ---------------------------------------------------------------------
        # Load json object from file
        logger.debug(f"Loading example file: {example_path}")

        try:
            crate_raw = json.load(example_file)
            logger.debug(f"Loaded example file: {example_path}")
        except Exception as e:
            logger.error(f"Error: {e}")
            return False

        logger.debug(f"Raw object: {json.dumps(crate_raw, indent=2)}")

        # ---------------------------------------------------------------------
        # Add a @base to the context
        logger.debug("Performing absolution")

        crate = absolutise.absolutise(logger, crate_raw)

        # ---------------------------------------------------------------------
        # Iterate over the schema directory, loading each schema file and frame

        for directory in os.listdir(schema_dir):
            logger.debug(f"Processing directory: {directory}")

            # ------------------------------------------------------------------
            # Construct schema path variable
            
            schema_path = os.path.join(schema_dir, directory, "schema.yaml")

            # ------------------------------------------------------------------
            # Load the frame file
            logger.debug(f"Loading grame file")
            
            frame_file = os.path.join(schema_dir, directory, "frame.json")
            try:
                with open(frame_file, "r") as frame:
                    frame = json.load(frame)
            except Exception as e:
                logger.error(f"Error: {e}")
                return False

            # ------------------------------------------------------------------
            # Apply framing
            logger.debug(f"Applying framing")
        
            framed = framing.apply_frame(logger, crate, frame)

            # ------------------------------------------------------------------
            # Validate the framed object
            logger.debug(f"Validating the framed object")
            
            try:
                target_class = "ROCrateMetadata"
                report = lmval.validate(instance=framed,
                                        schema=schema_path,
                                        target_class=target_class,
                                        strict=True
                                        )
            except Exception as e:
                logger.error(f"Error: {e}")
                return False

            logger.info(f"Validation report: {report}")
        
            # ---------------------------------------------------------------------
            # Perform assertions
            logger.debug(f"Performing assertions")

            try:
                assert report.results == []
                logger.info(f"Validation passed")
            except AssertionError as e:
                for result in report.results:
                    logger.error(f"{result.message}")
                raise e

            # ---------------------------------------------------------------------
            # Return success
            
            return True

if __name__ == "__main__":

    # ---------------------------------------------------------------------
    # Parse command line agruments
    
    arg_parser = argparse.ArgumentParser(description="RO-Crate Framing Example")
    arg_parser.add_argument("--log", help="Set logging level", default="INFO")
    arg_parser.add_argument("--input", help="Path to input file", default="/workspace/example.json")
    args = arg_parser.parse_args()

    # ---------------------------------------------------------------------
    # Set logging level
    
    logging.basicConfig(level=args.log)
    logger = logging.getLogger(__name__)
    logger.setLevel(args.log)
    
    main(logger=logger,
         input_path=args.input)
 
