# Kayla Laufer

import xmlrpc.client
import threading
import time

# In the cloud, update "localhost" to each nodes' corresponding internal IP
NODE_URL_A = "http://localhost:8000"  # Node for Client A
NODE_URL_B = "http://localhost:8001"  # Node for Client B
NODE_URL_C = "http://localhost:8002"  # Node for Client B

def client_submit(node_url, value, client_name, id = 0, case = 0):
    """Client submits a value to a node, without specifying a proposal ID."""
    try:
        with xmlrpc.client.ServerProxy(node_url) as node:
            print(f"[{client_name}] Submitting value '{value}' to {node_url}")
            result = node.submit_value(value, id, case)
            print(f"[{client_name}] Received result: {result}")
    except (ConnectionRefusedError, xmlrpc.client.ProtocolError, xmlrpc.client.Fault) as e:
        print(f"[{client_name}] Connection to {node_url} failed: {e}. Exiting.")

def simulate_two_clients(delay = 0.001, id_a = 0, id_b = 0, case = 0):
    # Client A submits a value to NODE_URL_A
    client_a = threading.Thread(target=client_submit, args=(NODE_URL_A, "A", "Client A", id_a, case))
    
    # Client B submits a different value to NODE_URL_B
    client_b = threading.Thread(target=client_submit, args=(NODE_URL_B, "B", "Client B", id_b, case))

    # Start both clients simultaneously
    client_a.start()
    time.sleep(delay)
    client_b.start()

    # Wait for both clients to finish
    client_a.join()
    client_b.join()

def simulate_three_clients(delay = 0.001, id_a = 0, id_b = 0, id_c = 0, case = 0):
    # Client A submits a value to NODE_URL_A
    client_a = threading.Thread(target=client_submit, args=(NODE_URL_A, "A", "Client A", id_a, case))
    
    # Client B submits a different value to NODE_URL_B
    client_b = threading.Thread(target=client_submit, args=(NODE_URL_B, "B", "Client B", id_b, case))

    # Client C submits a different value to NODE_URL_B
    client_c = threading.Thread(target=client_submit, args=(NODE_URL_C, "C", "Client C", id_c, case))

    # Start both clients simultaneously
    client_a.start()
    time.sleep(delay)
    client_b.start()
    time.sleep(1)
    client_c.start()

    # Wait for both clients to finish
    client_a.join()
    client_b.join()
    client_c.join()


def simulate_one_client():
    # Client A submits a value to NODE_URL_A
    client_a = threading.Thread(target=client_submit, args=(NODE_URL_A, "A", "Client A"))
    client_a.start()
    client_a.join()

if __name__ == "__main__":
    """Example when one client submits to the server. It will reach a consensus on the Client's value."""
    simulate_one_client()

    """Example of two clients submitting values to the server with random proposal IDs"""
    #simulate_two_clients(0.1) 

    """This demonstrates the case when a consensus has been reached by Client A, then Client B submits. The server
    will reach a consensus on Client A's value and inform Client B that no new values can be submitted after a 
    consensus has been reached"""
    #simulate_two_clients(6)

    """This simulates the case on slide 24 - Client A submits value A with proposal ID 3. ID 3 receives majority
    promises and begins the accept phase. Client B submits value B with proposal ID 4. It recognizes that the 
    majority agrees on value A and adopts it as well, but keeps its ID of 4. Before acceptance for ID 3 is reached, 
    ID 4 achieves majority promises and moves onto the accept phase. In this case, both proposers can succeed."""
    #simulate_two_clients(0.7, 3, 4, 1) 

    """This scenario simulates the case described on slide 25. Initially, Client A submits a proposal for Value A 
    with Proposal ID 3. Proposal ID 3 receives a majority of promises, allowing it to proceed. Before Client A's 
    proposal can reach full acceptance, however, Client B submits a new proposal for Value B with a higher Proposal 
    ID 4. During its prepare phase, Proposal ID 4 does not encounter any fully accepted values from Proposal ID 3, 
    so it proceeds with its own value, Value B. Proposal ID 4 quickly gathers a majority of promises and advances to 
    the accept phase. As a result, Proposal ID 4 reaches consensus on Value B, which effectively blocks Proposal ID 3 
    from completing, ensuring that all nodes converge on Value B.
    """
    #simulate_two_clients(0.4, 3, 4, 2) 

    """In this example, we simulate a livelock scenario in Paxos where multiple nodes—Node 0, Node 1, and Node 2—compete 
    to propose values nearly simultaneously, each with different proposal IDs. Initially, each node's proposal is blocked 
    by higher IDs from competing nodes, creating a cycle where none can reach consensus. To resolve this, we introduce a 
    randomized backoff: after each failed attempt, nodes wait for a random delay before retrying. This breaks the cycle of 
    constant interference, giving one node a chance to complete without interruption. Here, Node 0's randomized delay allowed 
    it to retry with a higher Proposal ID (8), gather the necessary promises, and reach consensus on value A. This example 
    illustrates how randomized backoff effectively prevents livelock, ensuring progress in the Paxos algorithm."""
    #simulate_three_clients(0.5, 3, 4, 5, 3) 

# Run by using the following command in the terminal:
# python3 KL_paxos_client.py
# Make sure the server file is running before running the client