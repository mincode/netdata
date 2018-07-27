import networkx
import sys
import os
import silk
from subprocess import Popen
import string
import random
import sqlparse
from protocol_graph import ProtocolGraph


def id_generator(size=8, chars=string.ascii_letters):
    """
    Generate random string.
    size: size of the string to be generated.
    chars: list of letters for the string.
    :return: random string generated.
    """
    L = []
    for _ in range(size):
        L.append(random.choice(chars))
    return ''.join(L)
    # return ''.join(random.choice(chars) for _ in range(size))

def sql_parse_no_ws(s):
    """
    Parse sql statement skipping whitespaces.
    :param s: string with one sql statement.
    :return: list of sqlparse.tokens for sql statement without the whitespaces.
    """
    parsed = sqlparse.parse(s)
    tokens = parsed[0].tokens
    cleaned = [t for t in tokens if t.ttype != sqlparse.tokens.Token.Text.Whitespace]
    return cleaned


def tokens_select_all(tokens):
    """
    Check if tokens of sql statement is a 'select * from table;' statement.
    :param tokens: list of sqlparse.tokens representing sql statment.
    :return: table name or empty string if no such statement.
    """
    table = ''
    token_type = sqlparse.tokens.Token
    if tokens[0].ttype == token_type.Keyword.DML and \
       tokens[0].value.lower() == 'select':
        if tokens[1].ttype == token_type.Wildcard and tokens[1].value == '*':
            if tokens[2].ttype == token_type.Keyword and tokens[2].value.lower() == 'from':
                if tokens[4].ttype == token_type.Punctuation and tokens[4].value == ';':
                    table = tokens[3].value
    return table


def tokens_select_frame(tokens):
    """
    Check if tokens of sql statement is a
    'select * from table where (%s<=stime_epoch_secs and stime_epoch_secs<%s);'
    statement
    :param tokens: list of sqlparse.tokens representing sql statment.
    :return: table name or empty string if not such a statement; currently only
    checks whether a where clause is present.
    """
    table = ''
    token_type = sqlparse.tokens.Token
    if tokens[0].ttype == token_type.Keyword.DML and \
       tokens[0].value.lower() == 'select':
        if tokens[1].ttype == token_type.Wildcard and tokens[1].value == '*':
            if tokens[2].ttype == token_type.Keyword and tokens[2].value.lower() == 'from':
                if tokens[4].ttype == sqlparse.sql.where:
                    table = tokens[3].value
    return table


class FlowCursor:
    """
    Cursor for data access.
    """
    _connection = None  # database connection
    _sql_params = tuple() # tuple of sql parameters

    def __init__(self, connection):
        self._connection = connection

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        """
        Next record in iterator.
        :return: named record like in silk.
        """
        pass

    def execute(self, sql, params=tuple()):
        """
        Execute sql statment to select the data.
        :param sql: string of sql statement.
        :param params: tuple (start, end).
        """
        pass


class IPFIXCursor(FlowCursor):
    """
    Cursor for data access.
    """
    def __init__(self, connection):
        super(IPFIXCursor, self).__init__(connection)

    def __next__(self):
        record = self._connection.__next__()
        valid = False
        while record and not valid:
            if self._sql_params:
                (start, end) = self._sql_params
                valid = start <= record.stime_epoch_secs and record.etime_epoch_secs < end
            else:
                valid = True
        return record

    def execute(self, sql, params=tuple()):
        """
        Execute sql statment to select the data;
        currently only fetch_all and fetch_frame implemented.
        :param sql: string of sql statement.
        :param params: tuple (start, end).
        """
        tokens = sql_parse_no_ws(sql)
        table = tokens_select_all(tokens)
        self._sql_params = tuple()
        if not table:
            table = tokens_select_frame(tokens)
            if table:
                self._sql_params = params


class FlowConnection:
    """
    Connection to flow data.
    """
    _connection = None  # connection handle to flow data
    _cursor_constructor = None  # function to construct cursor object

    def __init__(self, cursor_constructor, *args):
        """
        Initialize.
        """
        self._cursor_constructor = cursor_constructor

    def __enter__(self):
        """
        Enter with context.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit with context.
        """
        pass

    def open(self):
        """
        Open the database connection.
        """
        pass

    def close(self):
        """
        Close connection.
        """
        pass

    def cursor(self):
        """
        :return: cursor to access data.
        """
        return self._cursor_constructor(self._connection)


class IPFIXConnection(FlowConnection):
    """
    Connection to an IPFIX file.
    """
    _ipfix_file = '' # name of the ipfix input file
    _silk_file = None  # silk file pipe

    def __init__(self, ipfix_file):
        """
        Create a connection to an IPFIX file.
        :param ipfix_file: file name.
        """
        super(IPFIXConnection, self).__init__(IPFIXCursor)
        self._ipfix_file = ipfix_file

    def open(self):
        super(IPFIXConnection, self).open()
        self._silk_file = '/tmp/' + os.path.basename(self._ipfix_file) + id_generator() + '.rw'
        # print('Temporary file: ' + self._silk_file)
        os.mkfifo(self._silk_file)
        Popen(['rwipfix2silk', '--silk-output='+self._silk_file, self._ipfix_file])
        self._connection = silk.silkfile_open(self._silk_file, silk.READ)

    def close(self):
        if self._connection:
            # It seems the connection is closed automatically.
            # self._connection.close()
            # only need to remove the temporary silk file.
            os.remove(self._silk_file)
        super(IPFIXConnection, self).close()
