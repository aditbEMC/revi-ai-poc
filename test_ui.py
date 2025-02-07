import streamlit as st
import boto3
import os
import uuid
import threading
from concurrent.futures import ThreadPoolExecutor

# Configure AWS credentials using environment variables
os.environ['AWS_ACCESS_KEY_ID'] = st.secrets['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = st.secrets['AWS_SECRET_ACCESS_KEY']
os.environ['AWS_DEFAULT_REGION'] = st.secrets['AWS_DEFAULT_REGION']

#prompts = [prePrompt13, prePrompt46, prePrompt710]
campaigns = [
    "1. MISSED FIRST CLASS", 
    "2. CLIENT COMPLETES LAST CREDIT OF ANY CLASS PACKAGE",
    "3. CLIENT COMPLETES SINGLE CLASS CREDIT",
    "4. FIRST CLASS REMINDER",
    "5. LEAD ATTENDS FIRST CLASS USING INTRO OFFER",
    "6. LEAD CLAIMS INTRO OFFER",
    "7. LEAD CONVERTS TO HIGHEST TIERED MEMBERSHIP",
    "8. LEAD CREATED",
    "9. LEAD CONVERTS TO LOWER OR MIDDLE TIER MEMBERSHIP",
    "10. LEADS ATTENDS FIRST CLASS USING DROP IN CREDIT FLOW"]

# Title of the app
st.title("Business Questionnaire Form")

# Business Profile Section
st.header("1. Business Profile")

name = st.text_input("What is your name?")
business_name = st.text_input("What is the name of your business?")
crm_used = st.text_input("Which CRM does your business currently use?")
business_location = st.text_input("What is your business location?")
website_url = st.text_input("Do you have a website? If yes, please provide the URL.")
business_style = st.text_area("How would you describe the atmosphere and style of your business?")
key_selling_points = st.text_area("What are the key selling points that attract your members?")
additional_amenities = st.text_area("Do you offer any additional amenities?")

# Memberships, Offers & Services Section
st.header("2. Memberships, Offers & Services")

membership_plans = st.text_area("What are the details of your membership plans?")
introductory_offers = st.text_area("Do you have any introductory offers for new members?")
incentive_discounts = st.text_area("What incentive discounts do you offer to attract new members or retain existing ones?")
additional_classes = st.text_area("Do you offer any additional classes or programs?")
services_offered = st.text_area("What types of services and offerings does your business provide?")

# Campaigns & Engagement Styles Section
st.header("3. Campaigns & Engagement Styles")

communication_tone = st.selectbox(
    "What is your preferred tone of communication?",
    ["Friendly and casual", "Professional and motivational", "Other"]
)
brand_slogan = st.text_input("Do you have any preference as a slogan or phrases for your brand?")
example_campaigns = st.text_area("Do you have any example campaigns that worked well previously? If yes, share the details.")
sms_focus_areas = st.text_area("Are there any specific areas you want to focus on or avoid in our SMS messaging?")
additional_info = st.text_area("Is there anything else you would like to share about your business that might help in customizing your SMS flows?")

# Challenges & Targets Section
st.header("4. Challenges & Targets")

engagement_challenges = st.text_area("Are there any particular challenges you face in engaging leads or retaining members?")
target_demographic = st.text_area("Who is your target demographic for new members?")
st.header("Which campaign do you want to generate")
selected_campaign = st.selectbox("Select a campaign:", campaigns)

if st.button("Submit"):
    
    # Create one big text with all submitted data
    submitted_text = (
        f"### Your Submitted Information:\n\n"
        "1. Business Profile\n"
        f"**Name:** {name}\n"
        f"**Business Name:** {business_name}\n"
        f"**CRM Used:** {crm_used}\n"
        f"**Location:** {business_location}\n"
        f"**Website:** {website_url}\n"
        f"**Atmosphere & Style:** {business_style}\n"
        f"**Key Selling Points:** {key_selling_points}\n"
        f"**Additional Amenities:** {additional_amenities}\n\n"
        "2. Memberships, Offers & Services \n"
        f"**Membership Plans:** {membership_plans}\n"
        f"**Introductory Offers:** {introductory_offers}\n"
        f"**Incentive Discounts:** {incentive_discounts}\n"
        f"**Additional Classes/Programs:** {additional_classes}\n"
        f"**Services & Offerings:** {services_offered}\n\n"
        "3. Campaigns & Engagement Styles\n"
        f"**Preferred Tone:** {communication_tone}\n"
        f"**Brand Slogan:** {brand_slogan}\n"
        f"**Example Campaigns:** {example_campaigns}\n"
        f"**SMS Focus Areas:** {sms_focus_areas}\n"
        f"**Additional Info:** {additional_info}\n\n"
        "4. Challenges & Targets \n"
        f"**Engagement Challenges:** {engagement_challenges}\n"
        f"**Target Demographic:** {target_demographic}\n\n"
    )

    bedrock_runtime_client = boto3.client('bedrock-agent-runtime')

    # Specify the model ID and Alias ID you want to use
    agent_id = st.secrets.agentDetails["AGENT_ID"]
    agent_alias_id = st.secrets.agentDetails["AGENT_ALIAS_ID"]

    drip_campaign = selected_campaign

    prePrompt = f"""

        I want to generate detailed drip campaign named below

        {drip_campaign}
        
        You are going to generate the campaigns based on the questionnaire provided below.

        Here is the questionaire and its answers
    
    """

    try:

        response = bedrock_runtime_client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            inputText=prePrompt + submitted_text,
            sessionId=uuid.uuid4().hex
        )

        completion_text = ""
        
        for event in response.get("completion"):
            chunk = event["chunk"]
            completion_text += chunk["bytes"].decode()
        
        st.write(completion_text + "\n\n")

    except Exception as e:
        st.write("A Bug occured. We know about this and are solving it in the backend")
        st.write(e)