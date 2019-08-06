import game_state_tree as gtree
import extended_debug.error_test as err

class Command():
    SEP = ': '
    def __init__(self, keyword: str, desc: str, min_args: int, max_args: int):
        if not isinstance(keyword, str):
            raise TypeError('\'keyword\' must be a string, not a ' + str(type(keyword)))
        if not isinstance(desc, str):
            raise TypeError('\'desc\' must be a string, not a ' + str(type(desc)))
        if not isinstance(min_args, int):
            raise TypeError('\'min_args\' must be an integer, not a ' + str(type(min_args)))
        if not isinstance(max_args, int):
            raise TypeError('\'max_args\' must be an integer, not a ' + str(type(max_args)))
        if min_args < 0:
            raise ValueError('\'min_args\' must be greater than -1, not ' + str(min_args))
        if max_args < 0:
            raise ValueError('\'max_args\' must be greater than -1, not ' + str(max_args))
        if min_args > max_args:
            raise ValueError('\'max_args\' must be greater than or equal to \'min_args\', which is ' + str(min_args) + ', not ' + str(max_args))
        self.keyword = keyword
        self.desc = desc
        self.min_args = min_args
        self.max_args = max_args
        return
    def __repr__(self) -> str:
        return 'Command(' + repr(self.keyword) + ',' + repr(self.desc) + ',' + repr(self.min_args) + ',' + repr(self.max_args) + ')'
    def __str__(self) -> str:
        return self.keyword + Command.SEP + self.desc
    def __eq__(self, other) -> bool:
        if not isinstance(other, Command):
            raise TypeError('Command instances can only be compared to other Command instances, not ' + str(type(other)))
        return type(self) == type(other) and self.keyword == other.keyword and self.desc == other.desc and self.min_args == other.min_args and self.max_args == other.max_args
    def run(self, *args, **kw_args):
        raise NotImplementedError('Subclasses should override this function')
    
assert Command('fg', 'description', 0, 0) == Command('fg', 'description', 0, 0)
assert err.expect('Command(1, "description", 0, 0)', TypeError, global_variables={'Command':Command})
assert err.expect('Command("fg", 1, 0, 0,)', TypeError, global_variables={'Command':Command})
assert err.expect('Command("fg", "description", "0", 0)', TypeError, global_variables={'Command':Command})
assert err.expect('Command("fg", "description", 0, "0")', TypeError, global_variables={'Command':Command})
assert err.expect('Command("fg", "description", -1, 0)', ValueError, global_variables={'Command':Command})
assert err.expect('Command("fg", "description", 0, -1)', ValueError, global_variables={'Command':Command})
assert err.expect('Command("fg", "description", 2, 1)', ValueError, global_variables={'Command':Command})
assert repr(Command('fg', 'description', 1, 1)) == 'Command(\'fg\',\'description\',1,1)'
assert str(Command('fg', 'description', 0, 1)) == 'fg' + Command.SEP + 'description'
assert err.expect('Command("fg", "description", 0, 0) == "fg"', TypeError, global_variables={'Command':Command})
assert err.expect('Command("fg", "description", 0, 0).run()', NotImplementedError, global_variables={'Command':Command})

class Close(Command):
    KEYWORD = 'close'
    DESC = 'close this program'
    MIN_ARGS = 0
    MAX_ARGS = 0
    def __init__(self):
        Command.__init__(self, Close.KEYWORD, Close.DESC, Close.MIN_ARGS, Close.MAX_ARGS)
        return
    def __repr__(self) -> str:
        return 'Close()'
    def run(self):
        raise SystemExit

assert repr(Close()) == 'Close()'
assert err.expect('Close().run()', SystemExit, global_variables={'Close':Close, 'Command':Command})
assert str(Close()) == Close.KEYWORD + Command.SEP + Close.DESC

class Help(Command):
    KEYWORD = 'help'
    DESC = 'display this help message'
    MIN_ARGS = 0
    MAX_ARGS = 0
    def __init__(self):
        Command.__init__(self, Help.KEYWORD, Help.DESC, Help.MIN_ARGS, Help.MAX_ARGS)
        return
    def __repr__(self) -> str:
        return 'Help()'
    def run(self):
        class_list = Command.__subclasses__()
        output = ''
        for instance in class_list:
            output += str(instance) + '\n'
        print(output)
        return output
assert repr(Help()) == 'Help()'
assert str(Help()) == Help.KEYWORD + Command.SEP + Help.DESC

class Start(Command):
    KEYWORD = 'start'
    DESC = 'start a new game of connect-4'
    MIN_ARGS = 0
    MAX_ARGS = 1
    YES = 'y'
    NO = 'n'
    PROMPT_PREFIX = 'Would you like to go first ('
    PROMPT_JOIN = '/'
    PROMT_SUFFIX = ')?'
    RECOG_ERROR = 'Response not cognised! Try again.'
    def __init__(self, player_first: bool = None):
        if not isinstance(player_first, (bool, type(None))):
            raise TypeError('\'player_first\' must be a boolean or None, not a ' + str(type(player_first)))
        Command.__init__(self, Start.KEYWORD, Start.DESC, Start.MIN_ARGS, Start.MAX_ARGS)
        self.player_first = player_first
        return
    def __repr__(self) -> str:
        return 'Start(' + str(self.player_first) + ')'
    def __eq__(self, other) -> bool:
        return Command.__eq__(self, other) and self.player_first == other.player_first
    def run(self) -> gtree.DecisionNode:
        if self.player_first == None:
            while True:
                inp = input(Start.PROMPT_PREFIX + Start.YES + Start.PROMPT_JOIN + Start.NO + Start.PROMPT_SUFFIX)
                if inp == Start.YES:
                    self.player_first = True
                    break
                elif inp == Start.NO:
                    self.player_first = False
                    break
                else:
                    print(Start.RECOG_ERROR)
        return gtree.RootNode().traverse(self.player_first)
assert repr(Start()) == 'Start(None)'
assert repr(Start(True)) == 'Start(True)'
assert repr(Start(False)) == 'Start(False)'
assert Start() == Start()
assert Start(True).run() == gtree.RootNode().traverse(True)
assert Start(False).run() == gtree.RootNode().traverse(False)

class Insert(Command):
    KEYWORD = 'drop'
    DESC = 'drop one of your tokens into the board'
    MIN_ARGS = 0
    MAX_ARGS = 1
    PROMPT = 'Which column would you like to drop your token into (0 left-most, ' + str(gtree.Board.wdith) + ' right-most)?'
    RECOG_ERROR = 'Response not recognised as whole number! Try again.'
    RANGE_ERROR = 'You drop the token on the floor; there\'s no column there!'
    def __init__(self, col_i: int = None):
        if not isinstance(col_i, (int, type(None))):
            raise TypeError('\'col_i\' must be an integer or None, not a ' + str(type(col_i)))
        Command.__init__(self, Insert.KEYWORD, Insert.DESC, Insert.MIN_ARGS, Insert.MAX_ARGS)
        self.col_i = col_i
        return
    def __repr__(self) -> str:
        return 'Insert(' + str(self.col_i) + ')'
    def __eq__(self, other) -> bool:
        return Command.__eq__(self, other) and self.col_i == other.col_i
    def run(self, state: gtree.DecisionNode) -> gtree.DecisionNode:
        if not isinstance(state, gtree.DecisionNode):
            raise TypeError('\'state\' must be a DecisionNode, not a ' + str(type(state)))
        if not state.player_turn:
            raise ValueError('\'state.player_turn\' must be True, not ' + str(state.player_turn))
        if self.col_i == None:
            while True:
                inp = input(Insert.PROMPT)
                try:
                    self.col_i = int(inp)
                    break
                except ValueError:
                    print(Insert.RECOG_ERROR)
        try:
            self.state = self.state.traverse(self.col_i)
        except IndexError:
            print(Insert.RANGE_ERROR)
        return self.state
