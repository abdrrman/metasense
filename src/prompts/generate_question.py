system_template = """
You are a helpful assistant that is good at transforming the conversation history to a question from the customer's point of view.
Transform the customer's latest intent to a well-defined question to ask it to the customer representative from scratch.
This question will be answered by customer representative so ask like the customer.
It is like summarizing the intent of customer and transform it to a well-defined question.
"""

human_template = """
Example Conversation History :
Customer: Hello, I'm old and I got some surgery. After returning hospital I will need some assistance in the home for my health.
Customer Rep: Hi I'm sorry to hear that. We can help you with assistance in returning home after hospitalization service. Would you like me to explain more.
Customer: Sure, go ahead.
##################################################
Example Question: Could you give detailed explanation about Assistance in Returning Home After Hospitalization service. 
##################################################
Conversation History:
{history}
##################################################
Question:
"""