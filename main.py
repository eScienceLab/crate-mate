from pyld import jsonld
from linkml.validator import validate

import json

example_path = "/workspace/example.json"
schema_path = "/workspace/schema.yaml"

def main():
    # Load crate jsonld into json object
    with open(example_path, "r") as example_file, open(schema_path, "r") as schema_file:

        # ---------------------------------------------------------------------
        # Load json object from file

        try:
            crate_raw = json.load(example_file)
        except Exception as e:
            print(f"Error: {e}")
            return

        # ---------------------------------------------------------------------
        # Add a @base to the context
        
        uuid = "uuid-goes-here"
        base = f"arcp://uuid,{uuid}/"            

        print(crate_raw)
        print(crate_raw['@context'])
        crate_raw['@context'] = {
            "@vocab": "https://w3id.org/ro/crate/1.1/context",
            "@base": base
        }

        # ----------------------------------------------------------------------
        # Create a frame
        
        frame = {
            "@context": {
                "@vocab": "https://w3id.org/ro/crate/1.1/context",
                "@base": base
            },
            "@id": "http://ro-crate-metadata.json",
            "@embed": "@always"
        }
        options = {}

        # ---------------------------------------------------------------------
        # Apply framing
        
        framed = jsonld.frame(crate_raw, frame, options)
        print(json.dumps(framed, indent=2))

        # ---------------------------------------------------------------------
        # Validate the framed object
        
        target_class = "Root"
        report = validate(framed, schema_path, target_class)

        # ---------------------------------------------------------------------
        # Perform assertions

        try:
            assert report.results == []
        except AssertionError as e:
            for result in report.results:
                print(f"{result.message}")
            raise e

if __name__ == "__main__":
    main()
 
