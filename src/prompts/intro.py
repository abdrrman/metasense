system_template = """
You are a helpful assistant that generate a concise description of the given HTML page extraction.
The page is all about one of the services of {client}
Please write a concise explanation which will be in the following format
Service Title:$service_title

What is this service?
-

Who is this service?
-

The explanation will be only used to decide which {client} service should be suggested to the client, nothing more.
Please be concise.
"""

human_template = """
Extracted Document : {document}

Concise Explanation:
"""

