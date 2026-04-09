import os
import json
from flask import Flask, render_template, request, jsonify, send_file, render_template_string
from aidemy import prep_class  
from google.cloud import pubsub_v1

app = Flask(__name__)
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

##ADD SEND PLAN EVENT FUNCTION HERE
def send_plan_event(teaching_plan:str):
    """
    Send the teaching event to the topic called plan
    
    Args:
        teaching_plan: teaching plan
    """
    publisher = pubsub_v1.PublisherClient()
    print(f"-------------> Sending event to topic plan: {teaching_plan}")
    topic_path = publisher.topic_path(PROJECT_ID, "plan")

    message_data = {"teaching_plan": teaching_plan} 
    data = json.dumps(message_data).encode("utf-8") 

    future = publisher.publish(topic_path, data)

    return f"Published message ID: {future.result()}"
@app.route('/', methods=['GET', 'POST'])
def index():
    subjects = ['English', 'Mathematics', 'Science', 'Computer Science']
    years = list(range(5, 8))

    if request.method == 'POST':
        selected_year = int(request.form['year'])
        selected_subject = request.form['subject']
        addon_request = request.form['addon']

        # Call prep_class to get teaching plan and assignment
        teaching_plan = prep_class(
            f"""For a year {selected_year} course on {selected_subject} covering {addon_request}, 
            Incorporate the school curriculum, 
            book recommendations, 
            and relevant online resources aligned with the curriculum outcome. 
            generate a highly detailed, day-by-day 3-week teaching plan, 
            return the teaching plan in markdown format
            """
        )

        ### ADD send_plan_event CALL
        send_plan_event(teaching_plan)
        return jsonify({'teaching_plan': teaching_plan})
    return render_template('index.html', years=years, subjects=subjects, teaching_plan=None, assignment=None)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
