import os
import requests
import json
import networkx as nx
from utils.base_agent import BaseAgent
from agents.final_agent import FinalAgent
from agents.analyze import AnalyzeAgent
from agents.expand import ExpandAgent
from dotenv import load_dotenv
from utils.reddit_fetch import RedditMonitor


def write_to_file(prompt, filename='output.txt'):
    with open(filename, 'a') as f:
        f.write("=== Iteration Output ===\n")
        f.write("Message:\n")
        f.write(prompt.get('message', '') + "\n\n")



def main():
    load_dotenv()

    # Initialize Modules
    reddit_monitor = RedditMonitor()
    if not reddit_monitor.username:
        logging.error("Reddit authentication failed. Exiting application.")
        return

    reddit_content = reddit_monitor.fetch_all_recent_activity(limit=10)
    print(f"Fetched {len(reddit_content)} recent posts and comments.")
    




    # Initialize agents
    agents = {
     
        'Expand': ExpandAgent(),
        'Analyze': AnalyzeAgent(),
        'Final': FinalAgent()
        
    }

    # Create a directed graph to model the flow of data between agents
    G = nx.DiGraph()

    # Add nodes
    G.add_nodes_from(agents.keys())

    # Define edges to represent the flow between agents
    G.add_edges_from([
        ('Expand', 'Analyze'), 
        ('Analyze', 'Final')
        
    ])

    # Read initial prompt from 'initial_prompt.txt'

    prompt = reddit_content

    iteration = 0
    max_iterations = 1  # Safety to prevent infinite loops
    is_complete = False

    while iteration < max_iterations and not is_complete:
        iteration += 1
        print(f"--- Iteration {iteration} ---")

        # Process the prompt through the agents according to the graph
        for node in nx.topological_sort(G):
            if node != 'Final':
                agent = agents[node]
                try:
                    print(f"Processing with {node}Agent")
                    prompt = agent.process(prompt)
                    write_to_file(prompt)
                except Exception as e:
                    print(f"An error occurred in {node}Agent: {e}")
                    return  # Exit if there's an error
            else:
                # Check if the process is complete using the FinalAgent
                is_complete = agents['Final'].process(prompt)
                if is_complete:
                    print("Process is complete.")
                else:
                    print("Process is not yet complete. Continuing to next iteration.")

    # After the loop ends
    if not is_complete:
        print("Reached maximum iterations without completion.")
        print("Outputting the final progress as if the process is complete.")

    # Output the final progress
    with open('final_output.txt', 'w') as f:
        f.write("=== Final Output ===\n")
        f.write("Message:\n")
        f.write(prompt.get('message', '') + "\n\n")
        f.write("="*50 + "\n\n")

    print("Final progress has been saved to 'final_output.txt'.")

if __name__ == "__main__":
    main()