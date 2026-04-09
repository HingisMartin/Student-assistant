import os
import json
import base64
import random
from google.cloud import storage
import functions_framework

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from gemini import gen_assignment_gemini,combine_assignments
from deepseek import gen_assignment_deepseek
from typing import TypedDict

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
ASSIGNMENT_BUCKET = os.environ.get("ASSIGNMENT_BUCKET","")


class State(TypedDict):
    teaching_plan: str
    model_one_assignment: str
    model_two_assignment: str
    final_assignment: str

def create_assignment(teaching_plan: str):
    print(f"create_assignment---->{teaching_plan}")
    builder = StateGraph(State)
    builder.add_node("gen_assignment_gemini", gen_assignment_gemini)
    builder.add_node("gen_assignment_deepseek", gen_assignment_deepseek)
    builder.add_node("combine_assignments", combine_assignments)
    
    builder.add_edge(START, "gen_assignment_gemini")
    builder.add_edge("gen_assignment_gemini", "gen_assignment_deepseek")
    builder.add_edge("gen_assignment_deepseek", "combine_assignments")
    builder.add_edge("combine_assignments", END)

    graph = builder.compile()
    state = graph.invoke({"teaching_plan": teaching_plan})

    return state["final_assignment"]

@functions_framework.cloud_event
def generate_assignment(cloud_event):
    print(f"CloudEvent received: {cloud_event.data}")

    try:
        if isinstance(cloud_event.data.get('message', {}).get('data'), str): 
            data = json.loads(base64.b64decode(cloud_event.data['message']['data']).decode('utf-8'))
            teaching_plan = data.get('teaching_plan')
        elif 'teaching_plan' in cloud_event.data: 
            teaching_plan = cloud_event.data["teaching_plan"]
        else:
            raise KeyError("teaching_plan not found") 

        assignment = create_assignment(teaching_plan)

        print(f"Assignment---->{assignment}")

        #Store the return assignment into bucket as a text file
        storage_client = storage.Client()
        bucket = storage_client.bucket(ASSIGNMENT_BUCKET)
        file_name = f"assignment-{random.randint(1, 1000)}.txt"
        blob = bucket.blob(file_name)
        blob.upload_from_string(assignment)

        return f"Assignment generated and stored in {ASSIGNMENT_BUCKET}/{file_name}", 200

    except (json.JSONDecodeError, AttributeError, KeyError) as e:
        print(f"Error decoding CloudEvent data: {e} - Data: {cloud_event.data}")
        return "Error processing event", 500

    except Exception as e:
        print(f"Error generate assignment: {e}")
        return "Error generate assignment", 500

# import unittest

# class TestCreateAssignment(unittest.TestCase):
#     def test_create_assignment(self):
#         test_teaching_plan = "Week 1: 2D Shapes and Angles - Day 1: Review of basic 2D shapes (squares, rectangles, triangles, circles). Day 2: Exploring different types of triangles (equilateral, isosceles, scalene, right-angled). Day 3: Exploring quadrilaterals (square, rectangle, parallelogram, rhombus, trapezium). Day 4: Introduction to angles: right angles, acute angles, and obtuse angles. Day 5: Measuring angles using a protractor. Week 2: 3D Shapes and Symmetry - Day 6: Introduction to 3D shapes: cubes, cuboids, spheres, cylinders, cones, and pyramids. Day 7: Describing 3D shapes using faces, edges, and vertices. Day 8: Relating 2D shapes to 3D shapes. Day 9: Identifying lines of symmetry in 2D shapes. Day 10: Completing symmetrical figures. Week 3: Position, Direction, and Problem Solving - Day 11: Describing position using coordinates in the first quadrant. Day 12: Plotting coordinates to draw shapes. Day 13: Understanding translation (sliding a shape). Day 14: Understanding reflection (flipping a shape). Day 15: Problem-solving activities involving perimeter, area, and missing angles."
#         initial_state = {"teaching_plan": test_teaching_plan, "model_one_assignment": "", "model_two_assignment": "", "final_assignment": ""}
#         updated_state = create_assignment(initial_state)
        
#         print(updated_state)


# if __name__ == '__main__':
#     unittest.main()


