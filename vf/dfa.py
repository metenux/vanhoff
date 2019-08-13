from accepts import accepts

'''
@auth meten 2019.01.08
'''


@accepts(str)
def to_c_list(s):
    c_list = []
    for c in s:
        c_list.append(c)
    return c_list


class Node:
    def __init__(self, c, child_set=None, end=False):
        if not c:
            raise Exception('c is None')
        if child_set is None:
            child_set = set()
        self.__c = c
        self.__child_set = child_set
        self.__end = end

    def add_child(self, child):
        self.__child_set.add(child)

    def get_child_set(self):
        return self.__child_set

    def get_c(self):
        return self.__c

    def get_end(self):
        return self.__end

    @accepts(object, bool)
    def set_end(self, end):
        self.__end = end


class DfaFilter:
    @accepts(object, Node)
    def __init__(self, head):
        self.__head = head
        self.__bad_word_map = dict()
        self.__bad_word_list = list()
        self.__content = None
        self.__idx = 0

    @accepts(object, str)
    def filter_word(self, word):
        self.__content = word
        self.search_word()
        self.__content = None
        return set(self.__bad_word_map.keys())

    def search_word(self):
        if not self.__content:
            return
        c_list = to_c_list(self.__content)
        cur_node = self.__head
        while self.__idx < len(c_list):
            cur_node = self.search_node(cur_node, c_list[self.__idx])
            if not cur_node:
                cur_node = self.__head
                self.__idx = self.__idx - len(self.__bad_word_list)
                self.__bad_word_list.clear()
            elif cur_node.get_end():
                self.__bad_word_list.append(c_list[self.__idx])
                bad_word = ''.join(self.__bad_word_list)
                self.__bad_word_map[bad_word] = None
                self.__idx = self.__idx - len(self.__bad_word_list) + 1
                self.__bad_word_list.clear()
                cur_node = self.__head
            else:
                self.__bad_word_list.append(c_list[self.__idx])
            self.__idx = self.__idx + 1

    @accepts(object, Node, str)
    def search_node(self, node, c):
        if not node:
            return None
        node_childs = node.get_child_set()
        for nc in node_childs:
            if nc.get_c() == c:
                return nc
        return None


class Dfa:
    def __init__(self):
        self.__head = Node('E')
        pass

    def get_head(self):
        return self.__head

    @classmethod
    @accepts(object, set)
    def create_dfa_head(cls, word_set):
        dfa = Dfa()
        dfa.create_dfa(word_set)
        return dfa.get_head()

    def create_dfa(self, word_list):
        for word in word_list:
            c_list = to_c_list(word)
            if 0 < len(c_list):
                self.add_nodes(self.__head, c_list, 0)
                pass

    @accepts(object, Node, list, int)
    def add_nodes(self, node, c_list, idx):
        c = c_list[idx]
        cur_node = self.get_node(node, c)
        if not cur_node:
            cur_node = Node(c)
            node.add_child(cur_node)

        if (len(c_list) - 1) == idx:
            cur_node.set_end(True)

        idx = idx + 1

        if idx < len(c_list):
            self.add_nodes(cur_node, c_list, idx)

    @accepts(object, Node, str)
    def get_node(self, node, c):
        for n in node.get_child_set():
            if c == n.get_c():
                return n
        return None


if __name__ == '__main__':
    #构建一个敏感词库
    bad_word_set = {'vanhoff', 'meten'}
    dfa_filter = DfaFilter(Dfa.create_dfa_head(bad_word_set))
    print(dfa_filter.filter_word('hello vanhoff, hello meten'))
