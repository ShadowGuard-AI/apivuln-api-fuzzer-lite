![Hands tying the twine on a brown paper parcel at a worn depot bench, a blank cobalt blue tag lying flat against the parcel and facing the camera, scissors and a twine ball beside it, parcels stacked behind](intro-banner.png)

# apivuln-api-fuzzer-lite

![Inside a parcel sorting depot: workers carrying and checking brown paper parcels tied with twine, every parcel carrying a blank cobalt blue tag, among shelving and rolling cages](banner.png)

![A plain brown paper parcel tied with natural twine in a neat bow, a blank cobalt blue tag hanging from the twine below the parcel against the blurred racks of a sorting depot, the heading plate](logo.png)

![Veranda scene: the frog throat pouch swells and relaxes while the frog holds its post](scene.svg)


# apivuln-API-Fuzzer-Lite
A spec driven fuzzer that sends random, type shaped values to the endpoints declared in a provided OpenAPI/Swagger specification (JSON). Generated values are substituted for path, query, and header parameters and for request bodies. When an operation declares a 200 response schema, the response body is checked against that schema with `jsonschema`, and a failed check is logged as a warning. The closing line of a run counts the requests attempted, succeeded, failed, and validated, and a run in which no request succeeded exits 1 (a `--dry-run` run sends nothing and is exempt). This tool does not test for injection flaws, broken authentication, or data exposure, and it does not validate requests against the schema.


![Major section divider](sep-heavy.svg)

## Install

> Field note, pinned to the bench: the clone line above names the ShadowStrikeHQ account, while this repository lives under ShadowGuard-AI. The line is kept as written.

`git clone https://github.com/ShadowStrikeHQ/apivuln-api-fuzzer-lite`


![Minor section divider](sep-light.svg)

## Usage

> Field note, pinned to the bench: the usage line names no specification argument, even though the tool runs from a provided OpenAPI or Swagger specification. No flag is invented here to fill that gap.

`./apivuln-api-fuzzer-lite [params]`


![Major section divider](sep-heavy.svg)

## Parameters

> Field note, pinned to the bench: a dry run sends nothing and is exempt from the exit 1 rule that ends a run in which no request succeeded.

- `-h`: Show help message and exit
- `--requests`: Number of requests to send per endpoint. Defaults to 10.
- `--dry-run`: Perform a dry run without sending actual requests.


![Minor section divider](sep-light.svg)

## License
Copyright (c) ShadowStrikeHQ
