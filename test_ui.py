import streamlit as st
import boto3
import os
import uuid

# Configure AWS credentials using environment variables
os.environ['AWS_ACCESS_KEY_ID'] = st.secrets['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = st.secrets['AWS_SECRET_ACCESS_KEY']
os.environ['AWS_DEFAULT_REGION'] = st.secrets['AWS_DEFAULT_REGION']

# Prompt Prefix
prePrompt13 = """I want to generate detailed drip campaigns named as below

    1) MISSED FIRST CLASS
    2) CLIENT COMPLETES LAST CREDIT OF ANY CLASS PACKAGE 
    3) CLIENT COMPLETES SINGLE CLASS CREDIT
      
    You are going to generate the campaigns based on the questionnaire provided below. You will reference the knowledge base that contains 10 predefined campaigns and their structures. The goal is to generate campaigns that use the same names as those found in the knowledge base, but personalize the content based on the answers to the questionnaire. Please ensure that the output is detailed and complete for every campaign.

For each campaign, follow these steps:

Name of the Campaign: Use the same name as found in the knowledge base.

Messages:
-Craft minimum of 2-3 messages for each campaign.
-Messages should be engaging, aligned with the tone described in the questionnaire (e.g., friendly, professional), and include clear calls-to-action (CTAs).
-The content should be personalized using the answers provided in the questionnaire (e.g., mention the business name, highlight the key selling points, refer to specific services or offers).

Timing:
-Specify the exact timing for when each message should be sent (e.g., number of days after the event, time of day, and specific times of the year, such as "1 day after the first class," "3 days after joining," or "during the summer months").
-Ensure the timing aligns with the context of the business’s engagement strategy and customer journey.

Additional Instructions:
-Ensure that all 10 campaigns have detailed, fully fleshed-out messages. Do not omit any part of the campaign, especially for the last 6-7 campaigns, which tend to be shorter in previous outputs.
-The output should not exceed 4096 tokens, so if the response starts to become too lengthy, ensure each campaign’s content is divided into manageable sections. If necessary, break the message into smaller parts without losing the integrity of the campaign.
-If the content reaches the token limit, consider splitting the messages into multiple outputs, ensuring that every campaign is complete.
-Focus on generating engaging, personalized, and effective communication flows based on the business’s profile, membership plans, and offers.
-Add 2 blank lines before starting generation for next campaign

Here is the questionaire and its answers """

prePrompt46 = """I want to generate detailed drip campaigns named as below

    4) FIRST CLASS REMINDER
    5) LEAD ATTENDS FIRST CLASS USING INTRO OFFER
    6) LEAD CLAIMS INTRO OFFER
      
    You are going to generate the campaigns based on the questionnaire provided below. You will reference the knowledge base that contains 10 predefined campaigns and their structures. The goal is to generate campaigns that use the same names as those found in the knowledge base, but personalize the content based on the answers to the questionnaire. Please ensure that the output is detailed and complete for every campaign.

For each campaign, follow these steps:

Name of the Campaign: Use the same name as found in the knowledge base.

Messages:
-Craft minimum of 2-3 messages for each campaign.
-Messages should be engaging, aligned with the tone described in the questionnaire (e.g., friendly, professional), and include clear calls-to-action (CTAs).
-The content should be personalized using the answers provided in the questionnaire (e.g., mention the business name, highlight the key selling points, refer to specific services or offers).

Timing:
-Specify the exact timing for when each message should be sent (e.g., number of days after the event, time of day, and specific times of the year, such as "1 day after the first class," "3 days after joining," or "during the summer months").
-Ensure the timing aligns with the context of the business’s engagement strategy and customer journey.

Additional Instructions:
-Ensure that all 10 campaigns have detailed, fully fleshed-out messages. Do not omit any part of the campaign, especially for the last 6-7 campaigns, which tend to be shorter in previous outputs.
-The output should not exceed 4096 tokens, so if the response starts to become too lengthy, ensure each campaign’s content is divided into manageable sections. If necessary, break the message into smaller parts without losing the integrity of the campaign.
-If the content reaches the token limit, consider splitting the messages into multiple outputs, ensuring that every campaign is complete.
-Focus on generating engaging, personalized, and effective communication flows based on the business’s profile, membership plans, and offers.
-Add 2 blank lines before starting generation for next campaign

Here is the questionaire and its answers """

prePrompt710 = """I want to generate detailed drip campaigns named as below

    7) LEAD CONVERTS TO HIGHEST TIERED MEMBERSHIP
    8) LEAD CREATED
    9) LEAD CREATES TO LOWER OR MIDDLE TIER MEMBERSHIP
    10) LEADS ATTENDS FIRST CLASS USING DROP IN CREDIT FLOW
      
    You are going to generate the campaigns based on the questionnaire provided below. You will reference the knowledge base that contains 10 predefined campaigns and their structures. The goal is to generate campaigns that use the same names as those found in the knowledge base, but personalize the content based on the answers to the questionnaire. Please ensure that the output is detailed and complete for every campaign.

For each campaign, follow these steps:

Name of the Campaign: Use the same name as found in the knowledge base.

Messages:
-Craft minimum of 2-3 messages for each campaign.
-Messages should be engaging, aligned with the tone described in the questionnaire (e.g., friendly, professional), and include clear calls-to-action (CTAs).
-The content should be personalized using the answers provided in the questionnaire (e.g., mention the business name, highlight the key selling points, refer to specific services or offers).

Timing:
-Specify the exact timing for when each message should be sent (e.g., number of days after the event, time of day, and specific times of the year, such as "1 day after the first class," "3 days after joining," or "during the summer months").
-Ensure the timing aligns with the context of the business’s engagement strategy and customer journey.

Additional Instructions:
-Ensure that all 10 campaigns have detailed, fully fleshed-out messages. Do not omit any part of the campaign, especially for the last 6-7 campaigns, which tend to be shorter in previous outputs.
-The output should not exceed 4096 tokens, so if the response starts to become too lengthy, ensure each campaign’s content is divided into manageable sections. If necessary, break the message into smaller parts without losing the integrity of the campaign.
-If the content reaches the token limit, consider splitting the messages into multiple outputs, ensuring that every campaign is complete.
-Focus on generating engaging, personalized, and effective communication flows based on the business’s profile, membership plans, and offers.
-Add 2 blank lines before starting generation for next campaign

Here is the questionaire and its answers """

# Title of the app
st.title("Business Profile & Membership Information Form")

# Business Profile Section
st.header("1. Business Profile")

business_name = st.text_input("What is the name of your business?")
crm_used = st.text_input("Which CRM does your business currently use?")
business_location = st.text_input("What is your business location?")
website_url = st.text_input("Do you have a website? If yes, please provide the URL.")
business_atmosphere = st.text_area("How would you describe the atmosphere and style of your business?")
key_selling_points = st.text_area("What are the key selling points that attract your members?")
additional_amenities = st.text_area("Do you offer any additional amenities?")

# Memberships, Offers & Services Section
st.header("2. Memberships, Offers & Services")

membership_plans = st.text_area("What are the details of your membership plans?")
introductory_offers = st.text_area("Do you have any introductory offers for new members?")
incentive_discounts = st.text_area("What incentive discounts do you offer to attract new members or retain existing ones?")
additional_classes = st.text_area("Do you offer any additional classes or programs?")
services_offerings = st.text_area("What types of services and offerings does your business provide?")

# Campaigns & Engagement Styles Section
st.header("3. Campaigns & Engagement Styles")

preferred_tone = st.selectbox("What is your preferred tone of communication?", ["Friendly and casual", "Professional and motivational", "Other"])
brand_slogan = st.text_input("Do you have any preference as a slogan or phrases for your brand?")
successful_campaigns = st.text_area("Do you have any example campaigns that worked well previously? If yes, share the details.")
sms_focus_areas = st.text_area("Are there any specific areas you want to focus on or avoid in our SMS messaging?")
additional_info = st.text_area("Is there anything else you would like to share about your business that might help in customizing your SMS flows?")

# Challenges & Targets Section
st.header("4. Challenges & Targets")

engagement_challenges = st.text_area("Are there any particular challenges you face in engaging leads or retaining members?")
target_demographic = st.text_area("Who is your target demographic for new members?")

if st.button("Submit"):
    # Create one big text with all submitted data
    submitted_text = (
        f"### Your Submitted Information:\n\n"
        "1. Business Profile\n"
        f"**Business Name:** {business_name}\n"
        f"**CRM Used:** {crm_used}\n"
        f"**Location:** {business_location}\n"
        f"**Website:** {website_url}\n"
        f"**Atmosphere & Style:** {business_atmosphere}\n"
        f"**Key Selling Points:** {key_selling_points}\n"
        f"**Additional Amenities:** {additional_amenities}\n\n"
        "2. Memberships, Offers & Services \n"
        f"**Membership Plans:** {membership_plans}\n"
        f"**Introductory Offers:** {introductory_offers}\n"
        f"**Incentive Discounts:** {incentive_discounts}\n"
        f"**Additional Classes/Programs:** {additional_classes}\n"
        f"**Services & Offerings:** {services_offerings}\n\n"
        "3. Campaigns & Engagement Styles\n"
        f"**Preferred Tone:** {preferred_tone}\n"
        f"**Brand Slogan:** {brand_slogan}\n"
        f"**Successful Campaigns:** {successful_campaigns}\n"
        f"**SMS Focus Areas:** {sms_focus_areas}\n"
        f"**Additional Info:** {additional_info}\n\n"
        "4. Challenges & Targets \n"
        f"**Engagement Challenges:** {engagement_challenges}\n"
        f"**Target Demographic:** {target_demographic}"
    )

    bedrock_runtime_client = boto3.client('bedrock-agent-runtime')

    # Specify the model ID and Alias ID you want to use
    

    # Specify the model ID and Alias ID you want to use
    agent_id = st.secrets["AGENT_ID"]
    agent_alias_id = st.secrets["AGENT_ALIAS_ID"]

    # Call the Bedrock model via runtime endpoint
    response1 = bedrock_runtime_client.invoke_agent(
        agentId = agent_id,     # Your specific agent ID
        agentAliasId = agent_alias_id, # agent alias ID
        inputText = prePrompt13 + submitted_text,      # The input text or data
        sessionId = uuid.uuid4().hex
    )

    # Parse and print the response from the model
    completion1 = ""
    for event in response1.get("completion"):
        chunk = event["chunk"]
        completion1 += chunk["bytes"].decode()

    response2 = bedrock_runtime_client.invoke_agent(
        agentId = agent_id,     # Your specific agent ID
        agentAliasId = agent_alias_id, # agent alias ID
        inputText = prePrompt46 + submitted_text,      # The input text or data
        sessionId = uuid.uuid4().hex
    )

    # Parse and print the response from the model
    completion2 = ""
    for event in response2.get("completion"):
        chunk = event["chunk"]
        completion2 += chunk["bytes"].decode()

    response3 = bedrock_runtime_client.invoke_agent(
        agentId = agent_id,     # Your specific agent ID
        agentAliasId = agent_alias_id, # agent alias ID
        inputText = prePrompt710 + submitted_text,      # The input text or data
        sessionId = uuid.uuid4().hex
    )

    # Parse and print the response from the model
    completion3 = ""
    for event in response3.get("completion"):
        chunk = event["chunk"]
        completion3 += chunk["bytes"].decode()

    # Display the combined text
    st.write("Generated Text", completion1+"\n\n"+ completion2 + "\n\n" + completion3)
    #st.text_area("Submitted Information", response['output']['text'])