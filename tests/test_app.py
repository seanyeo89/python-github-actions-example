# DATABASE
# Columns: | Player Id | Player Name | Team Name | Age | Average Score | 
from random import randrange
Database={
    1:["FB", "A", 23, 58],
    2:["AMZN", "B", 22, 60],
    3:["AAPL", "C", 23, 56],
    4:["TSLA", "D", 24, 53]
        }



# API simulation of READ operation

# Input Payload
'''
    payload={
            "Player_id": id
        }
'''

def read_player(payload):
    id = payload["Player_id"]
    if id in Database:
        entry=Database[id]
        return {"Code":200, 
                "Response":{"Name":entry[0],"Team":entry[1],"Age":entry[2],"Average":entry[3]},
                "Message":"Read Operation Succesful"}

    else:
        return {"Code":404,"Message":"Player does not exists"}



# API Testing Function
# Code deployment will fail some time due to random range theoratically.
# Testing function

test_payload={
        "Player_id": randrange(5)
    }

def test_read_player():
    response=read_player(test_payload)
    assert response.get("Code")==200