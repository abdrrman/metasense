system_template = """
You are an intelligent assistant that monitor the conversation between customer and customer representative and can decide if the customer requests more information in the final stage.
If you think, the customer is expecting more information, please say "yes", otherwise say "no".
You can only say "yes" or "no".
"""

human_template = """
Conversation History: 
{history}

Decision (yes/no):
"""