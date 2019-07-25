from extended_debug import error_test as err

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
            raise TypeError('\'state\' must be an integer, not a ' + repr(type(state)))
        if state > 1:
            raise ValueError('\'state\' must be lesser than 2, not ' + repr(state))
        if state < -1:
            raise ValueError('\'state\' must be greater than -2, not ' + repr(state))
        self.state = state
        return
    def __eq__(self, other) -> bool:
        if not isinstance(other, BoardPos):
            raise TypeError('BoardPos instances may only be compared to other BoardPos instances')
        return self.state == other.state
    def __repr__(self) -> str:
        return 'BoardPos(' + repr(self.state) + ')'
    def __str__(self) -> str:
        if self.state == 1:
            return BoardPos.player_symbol
        elif self.state == 0:
            return BoardPos.empty_symbol
        elif self.state == -1:
            return BoardPos.computer_symbol
        else:
            raise ValueError('\'state\' must be either 1, 0, or -1, not ' + repr(state))
    def full(self) -> bool:
        '''Tests occupacy of this space.'''
        return self.state != 0
    def capture(self, player: bool = False):
        '''Attempts to occupy this space.'''
        if not isinstance(player, bool):
            raise TypeError('\'player\' must be a boolean, not a ' + repr(type(player)))
        if self.full():
            raise Exception('cannot capture already occupied space')
        if player:
            self.state = 1
        else:
            self.state = -1
        return self
assert BoardPos().state == 0
assert err.expect('BoardPos(\'0\')', TypeError, global_variables={'BoardPos':BoardPos})
assert err.expect('BoardPos(2)', ValueError, global_variables={'BoardPos':BoardPos})
assert err.expect('BoardPos(-2)', ValueError, global_variables={'BoardPos':BoardPos})
assert BoardPos() == BoardPos()
assert err.expect('BoardPos() == 0', TypeError, global_variables={'BoardPos':BoardPos})
assert repr(BoardPos()) == 'BoardPos(0)'
assert str(BoardPos()) == BoardPos.empty_symbol
assert str(BoardPos(1)) == BoardPos.player_symbol
assert str(BoardPos(-1)) == BoardPos.computer_symbol
assert BoardPos().full() == False
assert BoardPos(1).full() == True
assert BoardPos(-1).full() == True
assert BoardPos().capture().state == -1
assert BoardPos().capture(True).state == 1
assert err.expect('BoardPos(1).capture()', Exception, global_variables={'BoardPos':BoardPos})

class BoardColumn():
    '''A list representing a single column on a connect-4 board.
            0th index is bottom
            last index is top'''
    height = 6 #number of spaces in a column on the board
    def __init__(self, spaces: tuple = ()):
        if not isinstance(spaces, tuple):
            raise TypeError('\'spaces\' must be a tuple, not a ' + repr(type(spaces)))
        if len(spaces) > BoardColumn.height:
            raise IndexError('\'spaces\' must be no longer than ' + repr(BoardColumn.height) + ', ' + repr(len(spaces)) + ' is too long')
        column = []
        for item in spaces:
            if isinstance(item, BoardPos):
                column.append(item)
            else:
                column.append(BoardPos(item))
        while len(column) < BoardColumn.height:
            column.append(BoardPos())
        self.items = tuple(column)
        return
    def __eq__(self, other) -> bool:
        if not isinstance(other, BoardColumn):
            raise TypeError('BoardColumn instances may only be compared to other BoardColumn instances, not ' + repr(type(other)))
        return self.items == other.items
    def __repr__(self) -> str:
        result = 'BoardColumn(('
        i = 0
        while i < BoardColumn.height:
            result += repr(self.items[i]) + ','
            i += 1
        return result[0:-1] + '))'
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
    def addToken(self, player: bool = False):
        '''Attempts to slide a token into this column'''
        if not isinstance(player, bool):
            raise TypeError('\'player\' must be a boolean, not a ' + repr(type(player)))
        if self.full():
            raise Exception('cannot add token to full column')
        i = 0
        while i < BoardColumn.height:
            if not self.items[i].full():
                self.items[i].capture(player)
                return self
            i += 1
        raise IndexError('could not find an empty BoardPos to put a token into')
assert len(BoardColumn().items) == BoardColumn.height
assert BoardColumn().items == tuple([BoardPos()] * BoardColumn.height)
assert BoardColumn((1,1,1,-1)).items == (BoardPos(1),BoardPos(1),BoardPos(1),BoardPos(-1),BoardPos(),BoardPos())
assert err.expect('BoardColumn(0)', TypeError, global_variables={'BoardColumn':BoardColumn})
assert err.expect('BoardColumn(' + repr(tuple([0] * (BoardColumn.height + 1))) + ')', IndexError, global_variables={'BoardColumn':BoardColumn})
assert BoardColumn() == BoardColumn()
assert err.expect('BoardColumn() == 0', TypeError, global_variables={'BoardColumn':BoardColumn,'BoardPos':BoardPos})
assert BoardColumn() != BoardColumn(tuple([1]))
assert repr(BoardColumn()) == 'BoardColumn(' + repr(tuple([BoardPos(0)] * BoardColumn.height)).replace(' ','') + ')'
assert str(BoardColumn((1,-1,1))) == BoardPos.player_symbol + BoardPos.computer_symbol + BoardPos.player_symbol + BoardPos.empty_symbol + BoardPos.empty_symbol + BoardPos.empty_symbol
assert BoardColumn(tuple([1])).full() == False
assert BoardColumn((1,1,1,-1,-1,-1)).full() == True
assert BoardColumn().addToken() == BoardColumn(tuple([-1]))
assert BoardColumn((-1,1)).addToken(True) == BoardColumn((-1,1,1))
assert err.expect('BoardColumn((1,1,1,-1,-1,-1)).addToken()', Exception, global_variables={'BoardColumn':BoardColumn,'BoardPos':BoardPos})

class Board():
    '''2D tuple representing a whole connect-4 board.
            0th index is far left
            last index is far right'''
    width = 7 #number of columns on the board
    def __init__(self, columns: tuple = ()):
        if not isinstance(columns, tuple):
            raise TypeError('\'columns\' must be a tuple, not a ' + repr(type(columns)))
        if len(columns) > Board.width:
            raise IndexError('\'columns\' must be no longer than ' + repr(Board.width) + ', not ' + repr(len(columns)))
        board = []
        for item in columns:
            if isinstance(item, BoardColumn):
                board.append(item)
            else:
                board.append(BoardColumn(item))
        while len(board) < Board.width:
            board.append(BoardColumn())
        self.columns = tuple(board)
        return
    def __eq__(self, other) -> bool:
        if not isinstance(other, Board):
            raise TypeError('Board instances must only be compared to other Board instances, not ' + repr(type(other)))
        return self.columns == other.columns
    def __repr__(self) -> str:
        result = 'Board(('
        for column in self.columns:
            result += repr(column) + ','
        return result[0:-1] + '))'
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
            raise TypeError('\'col_i\' must an integer, not a ' + repr(type(col_i)))
        if not isinstance(player, bool):
            raise TypeError('\'player\' must be a boolean, not a ' + repr(type(coll_i)))
        if col_i < 0:
            raise IndexError('\'col_i\' must be greater than -1, not ' + repr(col_i))
        if col_i >= Board.width:
            raise IndexError('\'col_i\' must be lesser than ' + repr(Board.width) + ', not ' + repr(col_i))
        self.columns[col_i].addToken(player)
        return
assert Board().columns == tuple([BoardColumn()] * Board.width)
assert Board(((1,1),(-1,-1))).columns == (BoardColumn((1,1)),BoardColumn((-1,-1)),BoardColumn(),BoardColumn(),BoardColumn(),BoardColumn(),BoardColumn())
assert err.expect('Board(1)', TypeError, global_variables={'Board':Board})
assert err.expect('Board((1,-1))', TypeError, global_variables={'Board':Board,'BoardColumn':BoardColumn})
assert err.expect('Board((1,1,1,-1,-1,-1,1,-1))', IndexError, global_variables={'Board':Board})
assert Board() == Board()
assert Board(((1,1),(-1,-1))) != Board()
assert err.expect('Board() == 0', TypeError, global_variables={'Board':Board})
assert repr(Board()) == 'Board(' + repr(tuple([BoardColumn()] * Board.width)).replace(' ','') + ')'
assert str(Board()) == str(BoardColumn()) * Board.width
assert str(Board(((1,1),(-1,-1)))) == str(BoardColumn((1,1))) + str(BoardColumn((-1,-1))) + str(BoardColumn()) * (Board.width - 2)
assert Board().full() == False
assert Board(tuple([tuple([1])])).full() == False
assert Board(tuple([tuple([1] * BoardColumn.height)] * Board.width)).full() == True

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
    def traverse(col_i: int):
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
