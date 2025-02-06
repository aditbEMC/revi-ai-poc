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

# Pre Prompts

prePrompt15 = """

    I want to generate detailed drip campaigns named below

    1. MISSED FIRST CLASS
    2. CLIENT COMPLETES LAST CREDIT OF ANY CLASS PACKAGE 
    3. CLIENT COMPLETES SINGLE CLASS CREDIT
    4. FIRST CLASS REMINDER
    5. LEAD ATTENDS FIRST CLASS USING INTRO OFFER
      
    You are going to generate the campaigns based on the questionnaire provided below.

    Here is the questionaire and its answers
    
    """

prePrompt610 = """

    I want to generate detailed drip campaigns named as below

    6. LEAD CLAIMS INTRO OFFER
    7. LEAD CONVERTS TO HIGHEST TIERED MEMBERSHIP
    8. LEAD CREATED
    9. LEAD CREATES TO LOWER OR MIDDLE TIER MEMBERSHIP
    10. LEADS ATTENDS FIRST CLASS USING DROP IN CREDIT FLOW
      
    You are going to generate the campaigns based on the questionnaire provided below.

    Here is the questionaire and its answers
     
    """

#prompts = [prePrompt13, prePrompt46, prePrompt710]
prompts = [prePrompt15, prePrompt610]

# Title of the app
st.title("Business Questionnaire Form")

# Business Profile Section
st.header("1. Business Profile")

name = st.text_input("What is your name")
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
seasonal_offerings = st.text_area("Are there any seasonal or promotional offerings you’d like to highlight?")
incentive_discounts = st.text_area("What incentive discounts do you offer to attract new members or retain existing ones?")
additional_classes = st.text_area("Do you offer any additional classes or programs?")
services_offered = st.text_area("What types of services and offerings does your business provide?")

# Customer Journey Section
st.header("3. Customer Journey")

member_locations = st.text_area("Where are the majority of your current members located?")
customer_lifecycle = st.text_area("What is the typical customer lifecycle for your business?")
key_milestones = st.text_area("What are the key milestones in your customer journey that you’d like to focus on?")

# Campaigns & Engagement Styles Section
st.header("4. Campaigns & Engagement Styles")

communication_tone = st.selectbox("What is your preferred tone of communication?", ["Friendly and casual", "Professional and motivational", "Other"])
brand_slogan = st.text_input("Do you have any preference as a slogan or phrases for your brand?")
campaign_frequency = st.text_input("How often would you like to send campaigns to customers?")
example_campaigns = st.text_area("Do you have any example campaigns that worked well previously? If yes, share the details.")
engage_inactive_customers = st.radio("Do you want campaigns to engage inactive customers?", ("Yes", "No"))
inactivity_days = st.number_input("If yes, after how many days of inactivity should we trigger a message?", min_value=0, step=1)
sms_focus_areas = st.text_area("Are there any specific areas you want to focus on or avoid in our SMS messaging?")
additional_info = st.text_area("Is there anything else you would like to share about your business that might help in customizing your SMS flows?")
include_links = st.radio("Do you want to include links to your website, app, or booking platform in messages?", ("Yes", "No"))

# Challenges & Targets Section
st.header("5. Challenges & Targets")

engagement_challenges = st.text_area("Are there any particular challenges you face in engaging leads or retaining members?")
target_demographic = st.text_area("Who is your target demographic for new members?")
campaign_goals = st.text_area("What is the main goal of your campaigns?")

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
        f"**Seasonal Offerings:** {seasonal_offerings}\n"
        f"**Incentive Discounts:** {incentive_discounts}\n"
        f"**Additional Classes/Programs:** {additional_classes}\n"
        f"**Services & Offerings:** {services_offered}\n\n"
        "3. Customer Journey\n"
        f"**Member Locations:** {member_locations}\n"
        f"**Customer Lifecycle:** {customer_lifecycle}\n"
        f"**Key Milestones:** {key_milestones}\n\n"
        "4. Campaigns & Engagement Styles\n"
        f"**Preferred Tone:** {communication_tone}\n"
        f"**Brand Slogan:** {brand_slogan}\n"
        f"**Campaign Frequency:** {campaign_frequency}\n"
        f"**Example Campaigns:** {example_campaigns}\n"
        f"**Engage Inactive Customers:** {engage_inactive_customers}\n"
        f"**Inactivity Days:** {inactivity_days}\n"
        f"**SMS Focus Areas:** {sms_focus_areas}\n"
        f"**Additional Info:** {additional_info}\n"
        f"**Include Links:** {include_links}\n\n"
        "5. Challenges & Targets \n"
        f"**Engagement Challenges:** {engagement_challenges}\n"
        f"**Target Demographic:** {target_demographic}\n"
        f"**Campaign Goals:** {campaign_goals}"
    )

    bedrock_runtime_client = boto3.client('bedrock-agent-runtime')

    # Specify the model ID and Alias ID you want to use
    agent_id = st.secrets["AGENT_ID"]
    agent_alias_id = st.secrets["AGENT_ALIAS_ID"]

    def invoke_agent(submitted_text):
        response = bedrock_runtime_client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            inputText=submitted_text,
            sessionId=uuid.uuid4().hex
        )
        return response
    
    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(invoke_agent, text + submitted_text) for text in prompts]
        results = [future.result() for future in futures]

    #response1, response2, response3 = results
    response1, response2 = results

    #st.write(response1, response2, response3)
    #st.write(response1, response2)

    completions = {}

    try:

        def process_completion(response, completion_key):
            completion_text = ""
            for event in response.get("completion"):
                chunk = event["chunk"]
                completion_text += chunk["bytes"].decode()
            completions[completion_key] = completion_text

        # Create threads for each response
        thread1 = threading.Thread(target=process_completion, args=(response1, 'completion1'))
        thread2 = threading.Thread(target=process_completion, args=(response2, 'completion2'))

        # start both threads simultaneously
        thread1.start()
        thread2.start()

        # Wait for both threads to finish
        thread1.join()
        thread2.join()

        completion1 = completions.get('completion1')
        completion2 = completions.get('completion2')

        result1 = completion1.split('2. CLIENT COMPLETES LAST CREDIT OF ANY CLASS PACKAGE')
        result2 = result1[1].split('3. CLIENT COMPLETES SINGLE CLASS CREDIT')
        result3 = result2[1].split('4. FIRST CLASS REMINDER')
        result4 = result3[1].split('5. LEAD ATTENDS FIRST CLASS USING INTRO OFFER')

        st.write(
            result1[0] + "\n\n" + "2. CLIENT COMPLETES LAST CREDIT OF ANY CLASS PACKAGE" + "\n\n" + 
            result2[0] + "\n\n" + "3. CLIENT COMPLETES SINGLE CLASS CREDIT" + "\n\n" + 
            result3[0] + "\n\n" + "4. FIRST CLASS REMINDER" + "\n\n" +
            result4[0] + "\n\n" + "5. LEAD ATTENDS FIRST CLASS USING INTRO OFFER" + "\n\n" +
            result4[1]
        )

        result5 = completion2.split('7. LEAD CONVERTS TO HIGHEST TIERED MEMBERSHIP')
        result6 = result5[1].split('8. LEAD CREATED')
        result7 = result6[1].split('9. LEAD CONVERTS TO LOWER OR MIDDLE TIER MEMBERSHIP')
        result8 = result7[1].split('10. LEADS ATTENDS FIRST CLASS USING DROP IN CREDIT FLOW')

        st.write(
            result5[0] + "\n\n" + "7. LEAD CONVERTS TO HIGHEST TIERED MEMBERSHIP" + "\n\n" + 
            result6[0] + "\n\n" + "8. LEAD CREATED" + "\n\n" + 
            result7[0] + "\n\n" + "9. LEAD CONVERTS TO LOWER OR MIDDLE TIER MEMBERSHIP" + "\n\n" +
            result8[0] + "\n\n" + "10. LEADS ATTENDS FIRST CLASS USING DROP IN CREDIT FLOW" + "\n\n" +
            result8[1]
        )

    except Exception as e:
        st.write("An error might occur. We know about the possibility of this bug occurring and we are working hard to ensure it does not in the near future !")