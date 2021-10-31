
from core.rules import Rule
from core import Color, board
from faronona.faronona_action import FarononaActionType, FarononaAction
MAX_SCORE = 22

class FarononaRules(Rule):

    def __init__(self, players):
        self.players = players
        self.current_player = -1 

    @staticmethod 
    def is_legal_move(state, action, player): 
        """Check if an action is a legal move.

        Args:
            state (FarononaState): A state object from the Faronona game.
            action (Action): An action object containing the move.
            player (int): The number of the player making the move.

        Returns:
            bool: True if the move is a legal one and False if else.
        """
        action = action.get_action_as_dict() 
        act_at = action['action']['at']
        act_to = action['action']['to']
        if state.get_next_player() == player:
            if action['action_type'] == FarononaActionType.MOVE:
                if state.get_board().get_cell_color(act_at) == Color(player):
                    effective_moves = FarononaRules.get_effective_cell_moves(state, act_at)
                    if effective_moves and act_to in effective_moves:
                        return True
                return False
            return False

    @staticmethod 
    def get_effective_cell_moves(state, cell):
        """Give the effective(Only the possible ones) moves a player can make regarding a piece on the board.

        Args:
            state (FarononaState): The current game state.
            cell ((int, int)): The coordinates of the piece on the board.
            player (int): The number of the player making the move.

        Returns:
            List: A list containing all the coordinates where the piece can go.
        """
        board = state.get_board()
        if board.is_cell_on_board(cell):
            possibles_moves = FarononaRules.get_rules_possibles_moves(cell, board.board_shape)
            effective_moves = []
            for move in possibles_moves:
                if board.is_empty_cell(move):
                    effective_moves.append(move)
            return effective_moves 

    @staticmethod #done
    def get_rules_possibles_moves(cell, board_shape):
        """Give all possibles moves for a piece according the game rules (Up, down, left, right, oblique).

        Args:
            cell ((int, int)): The coordinates of the piece on the board.
            board_shape ((int, int)): The board shape.

        Returns:
            List: A list containing all the coordinates where the piece could go.
        """
        if (cell[0]%2 == 0 and cell[1]%2 == 0) or (cell[0]%2 == 1 and cell[1]%2 == 1):
            return [(cell[0] + a[0], cell[1] + a[1])
                for a in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1)]
                if ((0 <= cell[0] + a[0] < board_shape[0]) and (0 <= cell[1] + a[1] < board_shape[1]))]
        elif (cell[0]%2 == 1 and cell[1]%2 == 0) or (cell[0]%2 == 0 and cell[1]%2 == 1):
            return [(cell[0] + a[0], cell[1] + a[1])
                for a in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if ((0 <= cell[0] + a[0] < board_shape[0]) and (0 <= cell[1] + a[1] < board_shape[1]))]

    @staticmethod 
    def make_move(state, action, player):
        """Transform the action of the player to a move. The move is made and the reward computed. 

        Args:
            state (FarononaState): A state object from the Faronona game.
            action (Action): An action object containing the move.
            player (int): The number of the player making the move.

        Returns: (next_state, done, next_is_reward): Gives the next state of the game along with the game status and
        the type of the next step.
        """
        board = state.get_board()
        json_action = action.get_json_action()
        action = action.get_action_as_dict()
        win = False 

        if action['action_type'] == FarononaActionType.MOVE:
            at = action['action']['at']
            to = action['action']['to']
            winby = action['winby']
        board.empty_cell(at)
        board.fill_cell(to, Color(player))

        approach = FarononaRules.is_win_approach_move(at, to, state, player)
        remote = FarononaRules.is_win_remote_move(at, to, state, player)

        if (approach is not None and len(approach) != 0) and (remote is not None and len(remote) != 0):
            if winby=="APPROACH":
                state.boring_moves = 0
                win = True
                for element in approach:
                    board.empty_cell(element)
                state.score[player] += len(approach)
                state.on_board[player*-1] -= len(approach) #modif
                state.captured = approach
            else:
                state.boring_moves = 0
                win = True
                for element in remote:
                    board.empty_cell(element)
                state.score[player] += len(remote)
                state.on_board[player*-1] -= len(remote) #modif
                state.captured = remote
        else:    
            if approach is not None and len(approach) != 0:
                state.boring_moves = 0
                win = True
                for element in approach:
                    board.empty_cell(element)
                state.score[player] += len(approach)
                state.on_board[player*-1] -= len(approach) #modif
                state.captured = approach

            elif remote is not None and len(remote) != 0:
                state.boring_moves = 0
                win = True
                for element in remote:
                    board.empty_cell(element)
                state.score[player] += len(remote)
                state.on_board[player*-1] -= len(remote) #modif
                state.captured = remote

        state.boring_moves += 1
        state.set_board(board)     
        state.rewarding_move = win
        state.set_latest_player(player)
        state.set_latest_move(json_action)
        if win:
            state.set_next_player(player)
            state.winmove = (at,to)
            if len(state.occuped) == 0:
                state.occuped.append(at)
                state.occupedplayer = player
            else: 
                if player == state.occupedplayer:
                    state.occuped.append(at)
                else: 
                    state.occuped = []
                    state.occuped.append(at)
                    state.occupedplayer = player

        else:
            state.set_next_player(player * -1)
            state.winmove = None
            state.captured = None
            state.occuped = []
            

        done = FarononaRules.is_end_game(state)
        return state, done

    @staticmethod
    def act(state, action, player): 
        """Take the state and the player's action and make the move if possible.

        Args:
            state (YoteState): A state object from the yote game.
            action (Action): An action object containing the move.
            player (int): The number of the player making the move.

        Returns:
            bool: True if everything goes fine and the move was made. False is else.
        """
        if FarononaRules.is_legal_move(state, action, player):
            return FarononaRules.make_move(state, action, player)
        else:
            return False

    @staticmethod
    def is_win_approach_move(at, to, state, player):
        board = state.get_board()
        opponent_pieces = board.get_player_pieces_on_board(Color(player * -1))
        i,j = at
        k,l = to
        captured = []

        if i == k:
            if (j-l == 1 and (i, l-1) in opponent_pieces):
                while (i, l-1) in opponent_pieces:
                    captured.append((i, l-1))
                    l=l-1
                return captured
            if (j-l == -1 and (i, l+1) in opponent_pieces):
                while (i, l+1) in opponent_pieces:
                    captured.append((i, l+1))
                    l=l+1
                return captured 
        elif j == l:
            if (i-k == 1 and (k-1, j) in opponent_pieces): 
                while (k-1, j) in opponent_pieces:
                    captured.append((k-1, j))
                    k=k-1
                return captured 
            if (i-k == -1 and (k+1, j) in opponent_pieces):
                while (k+1, j) in opponent_pieces:
                    captured.append((k+1, j))
                    k=k+1
                return captured 
        elif (k == i+1 and l == j+1 and (i+2, j+2) in opponent_pieces):
            while (i+2, j+2) in opponent_pieces:
                captured.append((i+2, j+2))
                i=i+1
                j=j+1
            return captured
        elif (k == i-1 and l == j-1 and (i-2, j-2) in opponent_pieces):
            while (i-2, j-2) in opponent_pieces:
                captured.append((i-2, j-2))
                i=i-1
                j=j-1
            return captured
        elif (k == i-1 and l == j+1 and (i-2, j+2) in opponent_pieces):
            while (i-2, j+2) in opponent_pieces:
                captured.append((i-2, j+2))
                i=i-1
                j=j+1
            return captured
        elif (k == i+1 and l == j-1 and (i+2, j-2) in opponent_pieces):
            while (i+2, j-2) in opponent_pieces:
                captured.append((i+2, j-2))
                i=i+1
                j=j-1
            return captured

    @staticmethod
    def is_win_remote_move(at, to, state, player):
        board = state.get_board()
        opponent_pieces = board.get_player_pieces_on_board(Color(player * -1))
        i,j = at
        k,l = to
        captured = []

        if i == k:
            if (j-l == 1 and (i, j+1) in opponent_pieces):
                while (i, j+1) in opponent_pieces:
                    captured.append((i, j+1))
                    j=j+1
                return captured 
            if (j-l == -1 and (i, j-1) in opponent_pieces):
                while (i, j-1) in opponent_pieces:
                    captured.append((i, j-1))
                    j=j-1
                return captured 
        elif j == l:
            if (i-k == 1 and (i+1, j) in opponent_pieces):
                while (i+1, j) in opponent_pieces:
                    captured.append((i+1, j))
                    i=i+1
                return captured 
            if (i-k == -1 and (i-1, j) in opponent_pieces):
                while (i-1, j) in opponent_pieces:
                    captured.append((i-1, j))
                    i=i-1
                return captured 
        elif (k == i+1 and l == j+1 and (i-1, j-1) in opponent_pieces):
            while (i-1, j-1) in opponent_pieces:
                captured.append((i-1, j-1))
                i=i-1
                j=j-1
            return captured
        elif (k == i-1 and l == j-1 and (i+1, j+1) in opponent_pieces):
            while (i+1, j+1) in opponent_pieces:
                captured.append((i+1, j+1))
                i=i+1
                j=j+1
            return captured
        elif (k == i-1 and l == j+1 and (i+1, j-1) in opponent_pieces):
            while (i+1, j-1) in opponent_pieces:
                captured.append((i+1, j-1))
                i=i+1
                j=j-1
            return captured
        elif (k == i+1 and l == j-1 and (i-1, j+1) in opponent_pieces):
            while (i-1, j+1) in opponent_pieces:
                captured.append((i-1, j+1))
                i=i-1
                j=j+1
            return captured

    @staticmethod 
    def get_player_actions(state, player):
        """Provide for a player and at a state all of his possible actions.

        Args:
            state (FarononaState): A state object from the Faronona game.
            player (int): The number of the player making the move.

        Returns:
            List[FarononaAction]: Contains all possible actions for a player at the given state.
        """
        actions, winacts, simpleacts = [], [], []
        board = state.get_board()
        empty_cells = board.get_all_empty_cells()
        player_pieces = board.get_player_pieces_on_board(Color(player))
        if state.winmove is not None:
            if player == state.get_latest_player() == state.get_next_player():
                at, to = state.winmove
                moves = FarononaRules.get_effective_cell_moves(state, to)
                if moves:
                    for move in moves:
                        if move in empty_cells and move not in state.occuped:
                            if move[0] != at[0] or move[1] != at[1] or ((move[0] != at[0] + 2 or move[0] != at[0] - 2) and (move[1] != at[1] + 2 or move[1] != at[1] - 2)):
                                if (FarononaRules.is_win_approach_move(to, move, state, player) is not None and len(FarononaRules.is_win_approach_move(to, move, state, player)) != 0) or (FarononaRules.is_win_remote_move(to, move, state, player) is not None and len(FarononaRules.is_win_remote_move(to, move, state, player)) != 0):
                                    actions.append(FarononaAction(action_type=FarononaActionType.MOVE, at=to, to=move))
                    return actions
        else:
            for piece in player_pieces:
                moves = FarononaRules.get_effective_cell_moves(state, piece)
                if moves:
                    for move in moves:
                        if move in empty_cells:
                            if (FarononaRules.is_win_approach_move(piece, move, state, player) is not None and len(FarononaRules.is_win_approach_move(piece, move, state, player)) != 0) or (FarononaRules.is_win_remote_move(piece, move, state, player) is not None and len(FarononaRules.is_win_remote_move(piece, move, state, player)) != 0):
                                winacts.append(FarononaAction(action_type=FarononaActionType.MOVE, at=piece, to=move))
                            else:
                                simpleacts.append(FarononaAction(action_type=FarononaActionType.MOVE, at=piece, to=move))
            if len(winacts) != 0:
                return winacts
            else:
                return simpleacts

    @staticmethod
    def moment_player(state, players):
        player = state.get_next_player() 
        if player == state.get_latest_player():
            if state.winmove is not None:
                action = FarononaRules.get_player_actions(state, player)
                if players[player].allow_combo is True and len(action) != 0:
                    return player
                else:
                    state.winmove = None 
                    state.set_next_player(player * -1) 
                    return player * -1
        return player 

    @staticmethod
    def random_play(state, player):
        """Return a random move for a player at a given state.

        Args:
            state (FarononaState): A state object from the Faronona game.
            player (int): The number of the player making the move.

        Returns:
            action : An action
        """
        import random
        actions = FarononaRules.get_player_actions(state, player)
        if len(actions) == 0:
            choice = None
        else:
            choice = random.choice(actions)
        return choice

    @staticmethod 
    def is_player_stuck(state, player):
        """Check if a player has the possibility to make a move

        Args:
            state (FarononaState): A state object from the Faronona game.
            player (int): The number of the player making the move.

        Returns:
            bool: True if a player can make a move. False if not.
        """
        if state.winmove is None: 
            return len(FarononaRules.get_player_actions(state, player)) == 0

    @staticmethod
    def is_end_game(state): 
        """Check if the given state is the last one for the current game.

        Args:
            state (FarononaState): A state object from the Faronona game.

        Returns:
            bool: True if the given state is the final. False if not.
        """
        if FarononaRules.is_player_stuck(state, state.get_next_player()) or FarononaRules.is_boring(state) : #
            return True
        latest_player_score = state.score[state.get_latest_player()]
        if latest_player_score >= MAX_SCORE:
            return True
        return False

    @staticmethod
    def is_boring(state):
        """Check if the game is ongoing without winning moves

        Args:
            state (FarononaState): A state object from the Faronona game.
        Returns:
            bool: True if the game is boring. False if else.
        """
        return state.boring_moves >= state.just_stop

    @staticmethod
    def get_results(state):  # TODO: Add equality case. a voir
        """Provide the results at the end of the game.

        Args:
            state (YoteState): A state object from the yote game.

        Returns:
            Dictionary: Containing the winner and the game score.
        """
        tie = False
        if state.score[-1] == state.score[1]:
            tie = True

        return {'tie': tie,  'winner': max(state.score, key=state.score.get),
                'score': state.score}