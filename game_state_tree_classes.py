class BoardPos():
    '''An enumeration representing a single space on a connect-4 board.
            -1 = belongs to computer
            0 = empty
            1 = belongs to player'''
    player_symbol = '@' #string representation of player's tokens
    empty_symbol = ' ' #string representation of empty space
    computer_symbol = '%' #string representation of computer's tokens
    def __init__(self, state: int = 0):
        if not isinstance(state, int):
            raise TypeError
        if state > 1:
            raise ValueError
        if state < -1:
            raise ValueError
        self.state = state
        return
    def __eq__(self, other) -> bool:
        if not isinstance(other, BoardPos):
            raise TypeError
        return self.state == other.state
    def __repr__(self) -> str:
        return 'BoardPos(' + self.state + ')'
    def __str__(self) -> str:
        if self.state == 1:
            return BoardPos.player_symbol
        elif self.state == 0:
            return BoardPos.empty_symbol
        elif self.state == -1:
            return BoardPos.computer_symbol
        else:
            raise Exception
    def full(self) -> bool:
        '''Tests occupacy of this space.'''
        return self.state != 0
    def capture(player: bool = False):
        '''Attempts to occupy this space.'''
        if not isinstance(player, bool):
            raise TypeError
        if self.full():
            raise Exception('cannot capture already occupied space')
        if player:
            self.state = 1
        else:
            self.state = -1
        return

class BoardColumn():
    '''A list representing a single column on a connect-4 board.
            0th index is bottom
            last index is top'''
    height = 6 #number of spaces in a column on the board
    def __init__(self, spaces: tuple):
        if not isinstance(spaces, tuple):
            raise TypeError
        if len(spaces) > BoardColumn.height:
            raise IndexError
        column = []
        i = 0
        while i < len(spaces):
            if isinstance(spaces[i], BoardPos):
                column[i] = spaces[i]
            else:
                column[i] = BoardPos(spaces[i])
            i += 1
        while i < BoardColumn.height:
            column[i] = BoardPos()
            i += 1
        self.items = tuple(column)
        return
    def __eq__(self, other) -> bool:
        if not isinstance(other, BoardColumn):
            raise TypeError
        return self.items == other.items
    def __repr__(self) -> str:
        result = 'BoardColumn(('
        i = 0
        while i < BoardColumn.height:
            result += repr(self.items[i]) + ','
            i += 1
        return result + '))'
    def __str__(self) -> str:
        result = ''
        i = 0
        while i < BoardColumn.height:
            result += str(self.items[i])
            i += 1
        return result
    def full(self) -> bool:
        '''Tests the occupancy of this column'''
        for item in self.items:
            if not item.full():
                return False
        return True
    def addToken(player: bool = False):
        '''Attempts to slide a token into this column'''
        if self.full():
            raise Exception('cannot add token to full column')
        i = 0
        while i < BoardColumn.height:
            if not self.items[i].full():
                self.items[i].capture(player)
                return
            i += 1
        return

class Board():
    '''2D tuple representing a whole connect-4 board.
            0th index is far left
            last index is far right'''
    width = 7 #number of columns on the board
    def __init__(self, columns: tuple):
        if not isinstance(columns, tuple):
            raise TypeError
        if len(columns) > Board.width:
            raise IndexError
        board = []
        i = 0
        while i < len(columns):
            if isinstance(columns[i], BoardColumn):
                board.append(columns[i])
            else:
                board.append(BoardColumn(columns[i]))
            i += 1
        while i < Board.width:
            board.append(BoardColumn())
            i += 1
        self.columns = board
        return
    def __eq__(self, other) -> bool:
        if not isinstance(other, Board):
            raise TypeError
        return self.columns == other.columns
    def __repr__(self) -> str:
        result = 'Board(('
        for column in columns:
            result += repr(column) + ','
        return result + '))'
    def __str__(self) -> str:
        strings = []
        for col in columns:
            strings.append(str(col).reverse())
            result = ''
        i = 0
        while i < BoardColumn.height:
            j = 0
            while j < Board.width:
                result += str(self.strings[j][i])
                j += 1
            result += '\n'
            i+= 1
        return result
    def full(self) ->  bool:
        '''Tests occupacy of this board'''
        for col in self.columns:
            if not col.full():
                return False
        return True
    def addToken(col_i: int, player: bool = False):
        '''Attempts to slide a token into one indexed column.'''
        if not isinstance(col_i, int):
            raise TypeError
        if not isinstance(player, bool):
            raise TypeError
        if col_i < 0:
            raise IndexError
        if col_i >= Board.width:
            raise IndexError
        self.columns[col_i].addToken(player)
        return

class VictoryState():
    '''An enumeration representing the victory condition of a connect-4 board.
            1 = player victory
            0 = stalemate
            -1 = computer victory
            -2 = no victory yet'''
    def __init__(self, state: (int, Board)):
        if isinstance(state, int):
            if state > 1:
                raise ValueError
            if state < -2:
                raise ValueError
            self.state = state
            return
        elif not isinstance(state, (Board, tuple)):
            raise TypeError
        elif isinstance(state, tuple):
            board = Board(state)
        else:
            board = state
        if self.win(board, True):
            self.state = 1
        elif self.win(board, False):
            self.state = -1
        elif board.full():
            self.state = 0
        else:
            self.state = -2
        return
    def __eq__(self, other) -> bool:
        if not isinstance(other, VictoryState):
            raise TypeError
        return self.state == other.state
    def __repr__(self) -> str:
        return 'VictoryState(' + self.state + ')'
    def win(self, board: Board, player: bool = False) -> bool:
        '''Determines whether the player/computer has won.'''
        if not isinstance(board, Board):
            raise TypeError
        if not isinstance(player, bool):
            raise TypeError
        if player:
            target = BoardPos(1)
        else:
            target = BoardPos(-1)
        i = 0
        while i < Board.width:
            j = 0
            while j < BoardColumn.height:
                if self.search(board, i, j, target):
                    return True
                j += 1
            i += 1
        return False
    def search(self, board: Board, x: int, y: int, target: BoardPos) -> bool:
        '''Searches for a line of tokens matching the target on the board.
                targeting empty spaces makes no sense'''
        if not isinstance(board, Board):
            raise TypeError
        if not isinstance(x, int):
            raise TypeError
        if not isinstance(y, int):
            raise TypeError
        if not isinstance(target, BoardPos):
            raise TypeError
        if not isinstance(length, int):
            raise TypeError
        #(up-right, center-right, down-right, up-center, down-center, up-left, center-left, down-left)
        mods_x = (1,1,1,0,0,-1,-1,-1) #sequence of x modifiers (length should = mods_y length)
        mods_y = (1,0,-1,1,-1,1,0,-1) #sequence of y modifiers (length should = mods_x length
        i = 0
        while i < len(mods_x):
            if self.line_search(board, x, y, target, mods_x[i], mods_y[i]):
               return True
            i += 1
        return False
    def line_search(self, board: Board, x: int, y: int, target: BoardPos, mod_x: int, mod_y: int, length: int = 4) -> bool:
        '''Recursively searches a line of tokens on the board for for each to match the target.
                targeting empty spaces makes no sense'''
        if not isinstance(board, Board):
            raise TypeError
        if not isinstance(x, int):
            raise TypeError
        if not isinstance(y, int):
            raise TypeError
        if not isinstance(target, BoardPos):
            raise TypeError
        if not isinstance(mod_x, int):
            raise TypeError
        if not isinstance(mod_y, int):
            raise TypeError
        if not isinstance(length, int):
            raise TypeError
        if length < 0:
            raise ValueError
        if board.columns[x].items[y] != target:
            return False
        elif length == 0:
            return True
        else:
            return self.line_search(board, x + mod_x, y + mod_y, target, mod_x, mod_y, length - 1)

class DecisionNode():
    '''A single node of the game state tree.'''
    def __init__(self, board: Board, player_turn: bool = False):
        if not isinstance(board, Board):
            raise TypeError
        if not isinstance(player_turn, bool):
            raise TypeError
        self.board = board
        self.player_turn = player_turn
        self.state = VictoryState(board)
        dependents = []
        if self.state == -2:
            i = 0
            while i < Board.width:
                try:
                    dependent = DecisionNode(board.addToken(i, player_turn), not player_turn)
                    weight = 1
                except:
                    dependent = None
                    weight = 0
                dependents.append(dependent)
                lots.append(weight)
                i += 1
            for dependent in dependents:
                if not isinstance(dependent, type(None)):
                    break
            else:
                raise Exception
            self.dependents = dependents
        return
    def __eq__(self, other) -> bool:
        if not isinstance(other, DecisionNode):
            raise TypeError
        return self.board == other.board and self.player_turn == other.player_turn and self.dependents == other.dependents
    def __repr__(self) -> str:
        return 'DecisionNode(' + repr(self.board) + ',' + repr(self.player_turn) + ')'
    def traverse(col_i: int) -> DecisionNode:
        if not isinstance(col_i, int):
            raise TypeError
        if col_i < 0:
            raise IndexError
        if coll_i >= len(self.dependents):
            raise IndexError
        return self.dependents[col_i]
    
class RootNode():
    '''The root node of the game state tree.'''
    def __init__(self):
        self.player = DecisionNode(Board(), True)
        self.computer = DecisionNode(Board(), False)
        return
    def __eq__(self, other) -> bool:
        if not isinstance(other, RootNode):
            raise TypeError
        return self.player == other.player and self.computer == other.computer
    def __repr__(self) -> str:
        return 'RootNode(' + repr(self.difficulty) + ')'
    def traverse(player_first: bool = True):
        if player_first:
            return self.player
        else:
            return self.computer
