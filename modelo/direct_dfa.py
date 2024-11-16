from pythomata import SimpleDFA
from graphviz import Digraph
from modelo.utils import WriteToFile
from pprint import pprint

RAW_STATES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'#definimos la lista de los estados del DFA. osea los circulitos

"""Esta clase utiliza directamente el algoritmo basado en seguir posiciones, 
derivado del árbol sintáctico de la expresión regular."""
class DDFA:
    def __init__(self, tree, symbols, regex):

    
        self.nodes = list()#Una lista que almacenará los nodos del árbol

        # propiedades del FA. Al igual que en el dfa definimos los simbolos, lista de estados,los diccionarios y el conjunt
        # de estados de aceptacion y estado inicial
        self.symbols = symbols
        self.states = list()
        self.trans_func = dict()
        self.accepting_states = set()
        self.initial_state = 'A'

        # Esta parte obtendremos el arbol sintactico, la cadena y por ultimo la variable donde almacenaremos  el estado finalDFA
        # y un contador para asignar identificadores unicos a los nodos
        self.tree = tree
        self.regex = regex
        self.augmented_state = None
        self.iter = 1

        self.STATES = iter(RAW_STATES)# esta linea buscamos iterar la lista que dfinimos en la parte superior para asignar nombres a los estados(A,B...)
        try:
            self.symbols.remove('e')#eliminamos el epsilon ya que el DFA no lo necesita
        except:
            pass

        # Aqui hacemos el llamado de los metodos para la construccion de DFA a partir del arbol
        self.ParseTree(self.tree)
        self.CalcFollowPos()

    def CalcFollowPos(self):
        for node in self.nodes:
            if node.value == '*':# si el nodo representa un klenp los nodos es su ultima posicion apuntan a la primera posicion
                for i in node.lastpos:
                    child_node = next(filter(lambda x: x._id == i, self.nodes))
                    child_node.followpos += node.firstpos
            elif node.value == '.':#representa concatenacion
                for i in node.c1.lastpos:
                    child_node = next(filter(lambda x: x._id == i, self.nodes))
                    child_node.followpos += node.c2.firstpos

        # generacion de los estados
        initial_state = self.nodes[-1].firstpos # primera posicion, osea la raiz del arbol

        # Filtrar los nodos que tienen un símbolo.
        self.nodes = list(filter(lambda x: x._id, self.nodes))
        self.augmented_state = self.nodes[-1]._id

        # Recursion construir los estados del DFA recursivamente
        self.CalcNewStates(initial_state, next(self.STATES))

     # esta funcion nos permite contruir recursivamente los estados y transiciones del DFA
    def CalcNewStates(self, state, curr_state):

        if not self.states:
            self.states.append(set(state))
            if self.augmented_state in state:
                self.accepting_states.update(curr_state)

        # Iteramos por cada símbolo
        for symbol in self.symbols:

            # Obtenga todos los nodos con el mismo símbolo en followpos
            same_symbols = list(
                filter(lambda x: x.value == symbol and x._id in state, self.nodes))

            # Crea un nuevo estado con los nodos.
            new_state = set()
            for node in same_symbols:
                new_state.update(node.followpos)

            #El nuevo estado no está en la lista de estados.
            if new_state not in self.states and new_state:

                # Obtenga los nuevos estados de las letras
                self.states.append(new_state)
                next_state = next(self.STATES)

                # Agregar estado a la función de transición
                try:
                    self.trans_func[next_state]
                except:
                    self.trans_func[next_state] = dict()

                try:
                    existing_states = self.trans_func[curr_state]
                except:
                    self.trans_func[curr_state] = dict()
                    existing_states = self.trans_func[curr_state]

                # Agregar la referencia
                existing_states[symbol] = next_state
                self.trans_func[curr_state] = existing_states

                # Preguntamos si ¿Es un estado de aceptación?
                if self.augmented_state in new_state:
                    self.accepting_states.update(next_state)

                # Repetir con este nuevo estado.
                self.CalcNewStates(new_state, next_state)

            elif new_state:
                #El estado ya existe... ¿cuál es?
                for i in range(0, len(self.states)):

                    if self.states[i] == new_state:
                        state_ref = RAW_STATES[i]
                        break

                #  Añadir el simbolo de transicion
                try:
                    existing_states = self.trans_func[curr_state]
                except:
                    self.trans_func[curr_state] = {}
                    existing_states = self.trans_func[curr_state]

                existing_states[symbol] = state_ref
                self.trans_func[curr_state] = existing_states

    def ParseTree(self, node):
        method_name = node.__class__.__name__ + 'Node'
        method = getattr(self, method_name)
        return method(node)

    def LetterNode(self, node):
        new_node = Node(self.iter, [self.iter], [
                        self.iter], value=node.value, nullable=False)
        self.nodes.append(new_node)
        return new_node

    def OrNode(self, node):
        node_a = self.ParseTree(node.a)
        self.iter += 1
        node_b = self.ParseTree(node.b)

        is_nullable = node_a.nullable or node_b.nullable
        firstpos = node_a.firstpos + node_b.firstpos
        lastpos = node_a.lastpos + node_b.lastpos

        self.nodes.append(Node(None, firstpos, lastpos,
                               is_nullable, '|', node_a, node_b))
        return Node(None, firstpos, lastpos, is_nullable, '|', node_a, node_b)

    def AppendNode(self, node):
        node_a = self.ParseTree(node.a)
        self.iter += 1
        node_b = self.ParseTree(node.b)

        is_nullable = node_a.nullable and node_b.nullable
        if node_a.nullable:
            firstpos = node_a.firstpos + node_b.firstpos
        else:
            firstpos = node_a.firstpos

        if node_b.nullable:
            lastpos = node_b.lastpos + node_a.lastpos
        else:
            lastpos = node_b.lastpos

        self.nodes.append(
            Node(None, firstpos, lastpos, is_nullable, '.', node_a, node_b))

        return Node(None, firstpos, lastpos, is_nullable, '.', node_a, node_b)

    def KleeneNode(self, node):
        node_a = self.ParseTree(node.a)
        firstpos = node_a.firstpos
        lastpos = node_a.lastpos
        self.nodes.append(Node(None, firstpos, lastpos, True, '*', node_a))
        return Node(None, firstpos, lastpos, True, '*', node_a)

    def PlusNode(self, node):
        node_a = self.ParseTree(node.a)

        self.iter += 1

        node_b = self.KleeneNode(node)

        is_nullable = node_a.nullable and node_b.nullable
        if node_a.nullable:
            firstpos = node_a.firstpos + node_b.firstpos
        else:
            firstpos = node_a.firstpos

        if node_b.nullable:
            lastpos = node_b.lastpos + node_a.lastpos
        else:
            lastpos = node_b.lastpos

        self.nodes.append(
            Node(None, firstpos, lastpos, is_nullable, '.', node_a, node_b))

        return Node(None, firstpos, lastpos, is_nullable, '.', node_a, node_b)

    def QuestionNode(self, node):
        # Node_a is epsilon
        node_a = Node(None, list(), list(), True)
        self.iter += 1
        node_b = self.ParseTree(node.a)

        is_nullable = node_a.nullable or node_b.nullable
        firstpos = node_a.firstpos + node_b.firstpos
        lastpos = node_a.lastpos + node_b.lastpos

        self.nodes.append(Node(None, firstpos, lastpos,
                               is_nullable, '|', node_a, node_b))
        return Node(None, firstpos, lastpos, is_nullable, '|', node_a, node_b)

    def EvalRegex(self):
        curr_state = 'A'
        for symbol in self.regex:

            if not symbol in self.symbols:
                return 'No pertenece a la expresion'

            try:
                curr_state = self.trans_func[curr_state][symbol]
            except:
                if curr_state in self.accepting_states and symbol in self.trans_func['A']:
                    curr_state = self.trans_func['A'][symbol]
                else:
                    return 'No'

        return 'Cadena aceptada' if curr_state in self.accepting_states else 'Cadena no aceptada'

    def GraphDFA(self):
        states = set(self.trans_func.keys())
        alphabet = set(self.symbols)

        dfa = SimpleDFA(states, alphabet, self.initial_state, self.accepting_states, self.trans_func)

        graph = dfa.trim().to_graphviz()
        graph.attr(rankdir='LR')

        source = graph.source
        WriteToFile('./salidas/DirectDFA.gv', source)
        graph.render('./salidas/DirectDFA', format='png')



class Node:
    def __init__(self, _id, firstpos=None, lastpos=None, nullable=False, value=None, c1=None, c2=None):
        self._id = _id
        self.firstpos = firstpos
        self.lastpos = lastpos
        self.followpos = list()
        self.nullable = nullable
        self.value = value
        self.c1 = c1
        self.c2 = c2

    def __repr__(self):
        return f'''
    id: {self._id}
    value: {self.value}
    firstpos: {self.firstpos}
    lastpos: {self.lastpos}
    followpos: {self.followpos}
    nullabe: {self.nullable}
    '''
