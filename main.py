import streamlit as st
from functions import ideator
import json
import os
import sys
from datetime import datetime
from supabase import create_client, Client

#connect to supabase database
urL: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(urL, key)
data, count = supabase.table("bots_dev").select("*").eq("id", "inbound_sam").execute()
bot_info = data[1][0]

def main():

    # Create a title for the chat interface
    st.title("Inbound Sam Bot")

    st.write("These are standin variables to demonstrate the bot's ability to integrate variables into its instruction set.")
    
    #variables for system prompt
    name = "Sam"
    email = st.text_input("Lead Email", value="john@doe.com")
    phone = st.text_input("Lead Phone", value="282-222-3333")
    lastname = st.text_input("Lead Last Name", value="Doe")
    firstname = st.text_input("Lead First Name", value="John")
    what_is_your_age_ = st.text_input("Lead Age", value="")
    
    income_options = ["Unemployed", "$0 - $50K", "$50K - $100K", "$100K - $150K", "$150K - $225K", "$225K+"]
    what_is_your_current_annual_income_ = st.selectbox("Lead Annual Income", options=income_options, index=2)
    
    how_did_you_originally_hear_about_us_ = st.text_input("Lead Discovery Source", value="")
    which_job_title_do_you_most_identify_with_ = st.text_input("Lead Job Title", value="Director")

    paid_options = ["", "0", "1-10", "11-50", "50+"]
    how_many_times_have_you_been_paid_to_speak_ = st.selectbox("Times Paid to Speak", options = paid_options, index = 0)
    
    what_is_your_highest_level_of_education_completed = st.text_input("Lead Education Level", value="Bachelors")

    speaking_income = ["", "$0","Under $1,000","$1,000 - $5,000","$5,000 - $15,000","$15,000+"]
    how_much_do_you_currently_make_per_month_speaking_ = st.selectbox("Lead Monthly Speaking Income", options = speaking_income, index = 0)

    industry_options = ["","Government/Military","Non-Profit","Corporate","Association","Church/Faith-Based","College/University","Education (K-12)","Other"]
    what_industry_do_you_speak_in_or_hope_to_speak_in_ = st.selectbox("Lead Speaking Industry", options = industry_options, index = 0)
    
    please_list_your_speaking_website_or_linkedin_profile_here_ = st.text_input("Lead Speaking Website/LinkedIn", value="")

    desired_income = ["", "$1,000 - $5,000","$5,000 - $10,000","$10,000 - $20,000","$20,000+"]
    what_is_your_desired_monthly_income_from_speaking_what_is_your_goal_ = st.selectbox("Lead Desired Monthly Income from Speaking", options = desired_income, index = 0)
                                                                                       
    on_a_scale_of_1_10_how_commited_and_ready_are_you_to_invest_in_yourself_in_order_to_get_booked_and = st.text_input("Lead Commitment Level", value="")
    what_is_your_biggest_challenge_in_hitting_your_monthly_income_goal_of3_000___5_000_from_speaking = st.text_input("Lead Biggest Challenge to Hitting Monthly Goal", value="")

    prompt_variables = {
        "name": name,
        "email": email,
        "phone": phone,
        "lastname": lastname,
        "firstname": firstname,
        "what_is_your_age_": what_is_your_age_,
        "what_is_your_current_annual_income_": what_is_your_current_annual_income_,
        "how_did_you_originally_hear_about_us_": how_did_you_originally_hear_about_us_,
        "which_job_title_do_you_most_identify_with_": which_job_title_do_you_most_identify_with_,
        "how_many_times_have_you_been_paid_to_speak_": how_many_times_have_you_been_paid_to_speak_,
        "what_is_your_highest_level_of_education_completed": what_is_your_highest_level_of_education_completed,
        "how_much_do_you_currently_make_per_month_speaking_": how_much_do_you_currently_make_per_month_speaking_,
        "what_industry_do_you_speak_in_or_hope_to_speak_in_": what_industry_do_you_speak_in_or_hope_to_speak_in_,
        "please_list_your_speaking_website_or_linkedin_profile_here_": please_list_your_speaking_website_or_linkedin_profile_here_,
        "what_is_your_desired_monthly_income_from_speaking_what_is_your_goal_": what_is_your_desired_monthly_income_from_speaking_what_is_your_goal_,
        "on_a_scale_of_1_10__how_commited_and_ready_are_you_to_invest_in_yourself_in_order_to_get_booked_and": on_a_scale_of_1_10_how_commited_and_ready_are_you_to_invest_in_yourself_in_order_to_get_booked_and,
        "what_is_your_biggest_challenge_in_hitting_your_monthly_income_goal_of__3_000____5_000_from_speaking": what_is_your_biggest_challenge_in_hitting_your_monthly_income_goal_of3_000___5_000_from_speaking,
        "reschedule_link": "N/A"
    }

    system_prompt = bot_info['system_prompt']
    system_prompt = system_prompt.format(**prompt_variables)
    initial_text = bot_info['initial_text']
    initial_text = initial_text.format(**prompt_variables)

    
    if st.button('Click to Start or Restart'):
        st.write(initial_text)
        restart_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('database.jsonl', 'r') as db, open('archive.jsonl','a') as arch:
        # add reset 
            arch.write(json.dumps({"restart": restart_time}) + '\n')
        #copy each line from db to archive
            for line in db:
                arch.write(line)

        #clear database to only first two lines
        with open('database.jsonl', 'w') as f:
        # Override database with initial json files
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "assistant", "content": initial_text}            
            ]
            f.write(json.dumps(messages[0])+'\n')
            f.write(json.dumps(messages[1])+'\n')



    #initialize messages list and print opening bot message
    #st.write("Hi! This is Tara. Seems like you need help coming up with an idea! Let's do this. First, what's your job?")

    # Create a text input for the user to enter their message and append it to messages
    userresponse = st.text_input("Enter your message")
    

    # Create a button to submit the user's message
    if st.button("Send"):
        #prep the json
        newline = {"role": "user", "content": userresponse}

        #append to database
        with open('database.jsonl', 'a') as f:
        # Write the new JSON object to the file
            f.write(json.dumps(newline) + '\n')

        #extract messages out to list
        messages = []

        with open('database.jsonl', 'r') as f:
            for line in f:
                json_obj = json.loads(line)
                messages.append(json_obj)

        #generate OpenAI response
        messages, count = ideator(messages)

        #append to database
        with open('database.jsonl', 'a') as f:
                for i in range(count):
                    f.write(json.dumps(messages[-count + i]) + '\n')



        # Display the response in the chat interface
        string = ""

        for message in messages[1:]:
            string = string + message["role"] + ": " + message["content"] + "\n\n"
        st.write(string)
            

if __name__ == '__main__':
    main()
