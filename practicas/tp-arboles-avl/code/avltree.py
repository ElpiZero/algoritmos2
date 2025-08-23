class AVLTree:
    root = None

class AVLNode:
    parent = None
    leftnode = None
    rightnode = None
    key = None
    value = None
    bf = None


#Insertamos un elemento en el AVL
def insert(T,element,key):
    new_node = AVLNode()
    new_node.value = element
    new_node.key = key
    
    #Caso con root vacio
    if T.root is None:
        T.root = new_node
        return key
    
    #Funcion recursiva que explora el arbol y devuelve verdadero si se pudo insertar el nodo
    def insert_node(node):
        #Verifica nodo izquierdo
        if new_node.key < node.key:
            if node.leftnode is None:
               node.leftnode = new_node
               new_node.parent = node
               return True
            else:
                return insert_node(node.leftnode)
        #Verifica nodo derecho
        elif (new_node.key > node.key):
            if node.rightnode is None:
                node.rightnode = new_node
                new_node.parent = node
                return True
            else:
                return insert_node(node.rightnode)
        else:
            return None
               
    #Llamamos a la funcion recursiva
    if insert_node(T.root):
        updateBf(T, new_node)
        return key
    else:
        return None
    

#Buscamos un elemento (.value) en un arbol dado
def search(T, element):
    #Compara el elemento ingresado con el .value de un nodo
    #Funcion recursiva
    def search_node(node, element):
        if node is None:
            return None
        if node.value == element:
            return node.key
    
        # Buscar en el subárbol izquierdo
        left_result = search_node(node.leftnode, element)
        if left_result is not None:
            return left_result
    
        # Buscar en el subárbol derecho
        return search_node(node.rightnode, element)

    return search_node(T.root,element)


#Funcion para borrar/desvincular un nodo con una key determinada 
def deleteKey(T,key):

    #Funcion que hace el reemplazo de un nuevo nodo en el lugar del nodo que queremos reemplazar
    def replace(parent, replace_node, new_child):
        if parent is None:  #Eliminamos la raiz
            T.root = new_child
        elif parent.leftnode == replace_node:
            parent.leftnode = new_child             #Cambiamos el child node
        elif parent.rightnode == replace_node:
            parent.rightnode = new_child            #Cambiamos el child node
        if new_child is not None:
            new_child.parent = parent               #Cambiamos el parent del child node

    def delete_node_key(node):
        #Caso sin child nodes
        if node.leftnode is None and node.rightnode is None:
            replace(node.parent,node,None)
        #Casos 1 childnode
        elif node.leftnode is None:
            replace(node.parent, node, node.rightnode)
        elif node.rightnode is None:
            replace(node.parent, node, node.leftnode)
        #Caso 2 childnodes
        else:
            max_node = node.rightnode
            while max_node.leftnode is not None:
                max_node = max_node.leftnode
        
            node.key = max_node.key  
            node.value = max_node.value
            delete_node_key(max_node)
            #En esta parte hacemos lo siguiente:
            #1. Ubicamos "el menor de los mayores"
            #2. Pasamos su key y value al nodo actual
            #3. Eliminamos el nodo que ocupa la posicion de "El menor de los mayores"

    #Buscamos el elemento que queremos borrar por su key
    def find_node_key(node,key):
        if node is None:
            return None
        if key < node.key:
            return find_node_key(node.leftnode, key)
        elif key > node.key:
            return find_node_key(node.rightnode, key)
        else:
            return node

    #Buscamos el elemento a borrar y si logramos borrarlo devolvemos su key
    target = find_node_key(T.root,key)
    if target is not None:
        bf_check = target.parent
        delete_node_key(target)
        updateBf(T, bf_check)
        return key
    else:
        return None
    
#Funcion para borrar/desvincular un nodo con .value == element 
def delete(T,element):
    key_to_find = search(T,element)
    if key_to_find is None:
        return None

    #Usamos la funcion deleteKey para borrar ese elemento
    return deleteKey(T,key_to_find)


#Funcion que calcula la altura de un arbol
def h(node):
    if node is None:
        return 0
    
    return 1 + max(h(node.leftnode),h(node.rightnode))
  

#Funcion que calcula el balance factor
def bf(node):
    if node is None:
        return 
    return h(node.leftnode)-h(node.rightnode)


#Funcion que realiza una rotacion a la izquierda de los nodos
def rotateLeft(T, old_root):
    new_root = old_root.rightnode

    #Asignamos el hijo izquierdo de new_root a la derecha de old_root
    #Si ese hijo != None, le asignamos a old_root como padre
    old_root.rightnode = new_root.leftnode
    if new_root.leftnode:
        new_root.leftnode.parent = old_root

    #Ponemos old_root a la izquierda de new_root
    new_root.leftnode = old_root
    new_root.parent = old_root.parent
    old_root.parent = new_root

    #Actualizamos el padre de new_root y validamos si debe ser la raiz del arbol o no
    if new_root.parent is None:
        T.root = new_root
    elif new_root.parent.leftnode == old_root:
        new_root.parent.leftnode = new_root
    else:
        new_root.parent.rightnode = new_root

    return new_root

#Funcion que realiza una rotacion a la derecha de los nodos
def rotateRight(T, old_root):
    new_root = old_root.leftnode

    #Asignamos el hijo derecho de new_root a la izquierda de old_root
    #Si ese hijo != None, le asignamos a old_root como padre
    old_root.leftnode = new_root.rightnode
    if new_root.rightnode:
        new_root.rightnode.parent = old_root

    #Ponemos old_root a la derecha de new_root
    new_root.rightnode = old_root
    new_root.parent = old_root.parent
    old_root.parent = new_root

    #Actualizamos el padre de new_root y validamos si debe ser la raiz del arbol o no
    if new_root.parent is None:
        T.root = new_root
    else:
        if new_root.parent.leftnode == old_root:
            new_root.parent.leftnode = new_root
        else:
            new_root.parent.rightnode = new_root

    return new_root

#Calcula el balance factor de cada uno de los nodos
def calculateBalance(T):

    def bf_recursive(node):
        if node is None:
            return 0
        node.bf = bf(node)
        bf_recursive(node.leftnode)
        bf_recursive(node.rightnode)

    bf_recursive(T.root)
    return

#reBalance para cada nodo
def reB_node(T, node):
        if node is None:
            return 
        if node.bf > 1:
            rotateRight(T,node)
        if node.bf < -1:
            rotateLeft(T,node)
        calculateBalance(T)

#Funcion reBalance para un arbol
def reBalance(T):
    #Actualizamos los bf del arbol y de ser necesario hacemos rotaciones    
    calculateBalance(T)
    reB_node(T, T.root)
    return

#Actualiza el bf del nodo actual, se verifica que no haya que hacer una rotacion
#finalmente llamamos al parent del nodo
#Esta funcion se va  usar principalmente cuando hagamos un delete o un insert
def updateBf(T,node):
    node.bf = bf(node)
    reB_node(T,node)
    if node.parent != None:
        updateBf(T,node.parent)
    return



A = AVLTree()
insert(A,4,4)
insert(A,2,2)
insert(A,1,1)
insert(A,1.5,1.5)
insert(A,0,0)

deleteKey(A,4)




