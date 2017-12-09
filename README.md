# TypeThief

## How to Run?
    1. Create virtual environment:
        virtualenv venv --python=python2.7
    2. Install dependencies
        pip install -r requirements.txt
    3. Start the server:
        python run_server.py
    4. Start a client:
        python run_client.py [--host server_ip] [--port server_port]

## File organization:
- run_server.py: script for running the server
- run_client.py: script for running the client
- config.py: configurations for test, dev, stage, and prod
- ui/: ui components: logos, fonts
- typethief/: source code
    - shared/ 
        - Room.py: each game is represented by a Room class instance
            it is consists of:
            a. a game state representing the state of the game
                [playing, waiting, finished]
            b. functions for adding players, removing, and getting players
                in the room
        - Clock.py
            a global clock that keeps tracks of the duration of the game
        - Text.py: 
            implements the the text object the players are racing on, 
            it encapsulates 1) a string of text, 2) the position of the 
            current character, and 3) Character class which stores the 
            information of the claimer of the character, the position in
            the text, the value of the string and the score of the char.
        - Player.py:
            represents the player of the game, it contains: 
            1) player id, 2) player score, 3) an array of all the claimed
            Character class
        - Texts.txt: stores the text of the games 
    - client/
        - __init__.py: 
            contains the Client class, which is responsible for drawing 
            the Pygame UI, handling key down events; 
            it inherits SocketClient class and capsulates the following
            modules.
        - socketclient.py:
            SocketClient class is the module that sends client generated 
            messages to the server
            Client Namespace class is responsible for listening to server 
            response messages, and updates the client game state 
            accoringly.
        - button.py: 
            Button class and ButtonGroup class implement the buttons of the
            UI
        - gamewindow.py: game window UI
        - textutils.py: helper functions for drawing text on pygame window
    - server/
        - __init__.py:
            Server class runs the server and uses Flask_SocketIO for 
            handling network messaging 
            ServerNamespace Class keeps track of the global game states,
            which stores a dictionary of Rooms;
            it is also responsible for handling client events, including 
            start game, join room, and player inputs etc. It calls the 
            functions in RoomControl class for events handling. After the 
            events are handles, ServerNamespace will also generate
            response messages to send back to the clients.
        - roomcontrol.py:
            RoomControl class stores Room objects and player event queues, 
            it also has functions for updating the Room with events. 
            The class uses multithread event queue handling for processing
            game events.
        - eventqueue.py:
            EventQueue class stores the events generated by each player 
            marked by the timestamp created upon event generation; every 
            event has a timestamp, a player id, an input type and an input
            value
