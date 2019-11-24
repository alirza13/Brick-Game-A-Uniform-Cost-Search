# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 17:57:35 2018

@author: Alirza Guliyev
"""

import time


graph = [ ['O', 'O', 'O', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
         ['O', 'O', 'O', 'O', 'O', 'G', 'X', 'X', 'X', 'X'],
         ['O', 'O', 'O', 'S', 'O', 'O', 'O', 'O', 'O', 'X'],
         ['X', 'O', 'O', 'S', 'O', 'O', 'O', 'O', 'O', 'O'],
         ['X', 'X', 'X', 'X', 'X', 'O', 'O', 'O', 'O', 'O'],
         ['X', 'X', 'X', 'X', 'X', 'X', 'O', 'O', 'O', 'X']
        ] 


class Brick:   # a brick class with x list , y list and shape attributes
    
    def __init__ (self, children, x = [2,3], y = [3,3],  gStep = 0, parent = None , state = None, fValue = 0):
        self.x = x;
        self.y = y;
        self.parent = parent
        self.children = []
        self.graph = graph;
        self.gStep = gStep
        self.state = state
        
        
    def isHorizontal (self):
        if len(self.x) == 1:
            return False
        else: 
            return True
        
# ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR         
class AStar:
          def __init__ (self, graph,start,goal):
            self.graph = graph
            self.start = start
            self.goal = goal
          
          def goalState (self,brick):
            if  brick.isHorizontal() == False and graph [brick.x[0]] [brick.y[0]] == 'G':
                return True
            else:
                return False
            
          def getHeuristic (self,brick):             # Manhattan distance as a heuristic function
            if brick.isHorizontal() == False:
                h = abs(self.goal[0] - brick.x[0]) + abs(self.goal[1] - brick.y[0])
                return h
            else:
                h1 = abs(self.goal[0] - brick.x[0]) + abs(self.goal[1] - brick.y[0])
                h2 = abs(self.goal[0] - brick.x[1]) + abs(self.goal[1] - brick.y[1])
                if h1 < h2:
                    return h1
                else:
                    return h2
                
          def getPath (self,brick):
            if brick == None:
                return
            print ('solution is ',brick.x,brick.y)
            self.getPath(brick.parent)
            
          def inClosed (self,brick,mset):
            if len(mset) == 0:
                return False
            for n in mset:
                if brick.x == n.x and brick.y == n.y:
                    return True
            return False
                
          def inQueue (self, brick,queue):
            if len(queue) == 0:
                return False
            for m in queue:
                if m[1].x == brick.x and m[1].y == brick.y:
                    return True
            return False
                
          def inQueueLessThanF (self, brick, queue):
            if len(queue) == 0:
                return False
            for m in queue:
                if m[1].x == brick.x and m[1].y == brick.y and m[1].fValue > brick.fValue:
                    m[1].gStep = brick.gStep
                    m[1].state = 'S'
                    m[1].parent = brick.parent
                    m[1].fValue = brick.fValue
                    print('Inside inQueueLessThanF')
                    
          def inClosedLessThanF (self, brick, closed, queue):
              if len(queue) == 0:
                return False
              if len(closed) == 0:
                return False
              for n in closed:
                  if brick.x == n.x and brick.y == n.y and n.fValue > brick.fValue:
                      closed.remove(n)
                      print('Inside inClosedLessThanF')
                      #queue.append([brick.fValue,brick])                    
                      for m in queue:
                          if  m[1].x == brick.x and m[1].y == brick.y:
                              m[1].gStep = brick.gStep
                              m[1].state = 'S'
                              m[1].parent = brick.parent
                              m[1].fValue = brick.fValue
                              print('Inside inClosedLessThanF')
                              
             
          def astar(self, graph, start):
                visited = set()
                c = 0
                queue = []
                queue.append([0,start])
                              
                while len(queue) > 0:
                    #print ('Queue', queue)
                    cost,node = queue.pop(0)               
                    if self.goalState(node):
                        print (self.getPath(node))
                        return
                    if c > 0:
                        print('Node coordinates:',node.x,node.y, 'Node gstep:', node.gStep, 'Node f value:', node.fValue )
                    self.successor(node)
                    c = c + 1
                    for n in node.children:
                      h = self.getHeuristic(n)
                      n.fValue = h + n.gStep
                      print ('N coordinates',n.x,n.y, 'N gstep:', n.gStep, 'Node f value:', n.fValue)  
                      if self.inClosed(n,visited) == False or self.inQueue(n,queue) == False: 
                          queue.append([n.fValue,n])
                          queue.sort(key=lambda x: x[0])
                      elif self.inQueueLessThanF(n,queue):  
                          i = 0                             # empty statement
                      elif self.inClosedLessThanF(n,visited,queue):
                          i = 1
                    visited.add(node)
            
          def successor (self,brick):         # Checking successor if it is visitable or not according to horizontiality and verticaliality 
            if brick.isHorizontal():
                if brick.y[0] == brick.y[1]:    # looking down
                    #print ('horizontal')
                    if (brick.y[0] + 1 < len(graph[0])) and (graph[brick.x[0]][brick.y[0] + 1] == 'O' or graph[brick.x[0]][brick.y[0] + 1] ==  'G')  and  (graph[brick.x[1]][brick.y[1] + 1] == 'O' or graph[brick.x[1]][brick.y[1] + 1] == 'G') :    # check right child
                        brickRight = Brick ([],[brick.x[0],brick.x[1]],  [brick.y[0] + 1, brick.y[1] + 1],brick.gStep + 1, brick, 'S')                        
                        brick.children.append(brickRight)
                    if (brick.y[0] - 1 >= 0) and (graph[brick.x[0]][brick.y[0] - 1] == 'O' or graph[brick.x[0]][brick.y[0] - 1] == 'G')  and  (graph[brick.x[1]][brick.y[1] - 1] == 'O' or graph[brick.x[1]][brick.y[1] - 1] == 'G') :    # check left child
                        brickLeft = Brick ([],[brick.x[0],brick.x[1]],  [brick.y[0] - 1, brick.y[1] - 1],brick.gStep + 1, brick, 'S')                       
                        brick.children.append(brickLeft)
                    if (brick.x[0] - 1 >= 0) and (graph[brick.x[0] - 1][brick.y[0]] == 'O' or graph[brick.x[0] - 1][brick.y[0]] == 'G') :          # check upper child
                        brickUp = Brick ([],[brick.x[0] - 1],[brick.y[0]],brick.gStep + 1, brick, 'S')                      
                        brick.children.append(brickUp)
                    if (brick.x[1] + 1 < len(graph)) and (graph[brick.x[1] + 1][brick.y[0]] == 'O' or graph[brick.x[1] + 1][brick.y[0]] == 'G'):  # check lower child
                        brickLow = Brick ([],[brick.x[1] + 1],[brick.y[0]],brick.gStep + 1, brick, 'S')                        
                        brick.children.append(brickLow)
                else:   # looking right or left
                    if (brick.x[0] - 1 >= 0) and (graph[brick.x[0] - 1][brick.y[0]] == 'O' or graph[brick.x[0] - 1][brick.y[0]] == 'G')  and (graph[brick.x[1] - 1][brick.y[1]] == 'O' or graph[brick.x[1] - 1][brick.y[1]] == 'G'):    # check up child
                        brickUp = Brick ([],[brick.x[0] - 1,brick.x[1] - 1],  [brick.y[0], brick.y[1]],brick.gStep + 1, brick, 'S')                     
                        brick.children.append(brickUp)
                    if (brick.x[0] + 1 < len(graph) ) and (graph[brick.x[0] + 1][brick.y[0]] == 'O' or graph[brick.x[0] + 1][brick.y[0]] == 'G')  and  (graph[brick.x[1] + 1][brick.y[1]] == 'O' or graph[brick.x[1] + 1][brick.y[1]] == 'G' ) :    # check down child
                        brickDown = Brick ([],[brick.x[0] + 1,brick.x[1] + 1],  [brick.y[0], brick.y[1]],brick.gStep + 1, brick, 'S')
                        brick.children.append(brickDown)
                    if (brick.y[1] + 1 < len(graph[0]))  and (graph[brick.x[1]][brick.y[1] + 1] == 'O' or graph[brick.x[1]][brick.y[1] + 1] == 'G'):   # checking right child
                        brickRight = Brick ([],[brick.x[1]],  [brick.y[1] + 1],brick.gStep + 1, brick, 'S')
                        brick.children.append(brickRight)
                    if (brick.y[0] - 1 >= 0)  and (graph[brick.x[0]][brick.y[0] - 1] == 'O' or graph[brick.x[0]][brick.y[0] - 1] == 'G'):   # checking left child
                        brickLeft = Brick ([],[brick.x[0]],  [brick.y[0] - 1],brick.gStep + 1, brick, 'S')
                        brick.children.append(brickLeft)
            else:
                #print ('vertical')    # vertical shape
                if (brick.y[0] + 1 < len(graph[0]) and brick.y[0] + 2 < len(graph[0])) and (graph[brick.x[0]][brick.y[0] + 1] == 'O' or graph[brick.x[0]][brick.y[0] + 1] == 'G')  and (graph[brick.x[0]][brick.y[0] + 2] == 'O' or graph[brick.x[0]][brick.y[0] + 2] == 'G'):    # checking right child 2 cells
                    brickRight = Brick ([],[brick.x[0],brick.x[0]],  [brick.y[0] + 1, brick.y[0] + 2],brick.gStep + 1, brick, 'S')  
                    brick.children.append(brickRight)
                if (brick.y[0] - 1 >= 0 and brick.y[0] - 2 >= 0) and (graph[brick.x[0]][brick.y[0] - 1] == 'O' or graph[brick.x[0]][brick.y[0] - 1] == 'G')  and (graph[brick.x[0]][brick.y[0] - 2] == 'O' or graph[brick.x[0]][brick.y[0] - 2] == 'G') :      # checking left child
                    brickLeft = Brick ([],[brick.x[0],brick.x[0]],  [brick.y[0] - 2, brick.y[0] - 1],brick.gStep + 1, brick, 'S')
                    brick.children.append(brickLeft)
                if (brick.x[0] - 1 >= 0 and brick.x[0] - 2 >= 0) and (graph[brick.x[0] - 1][brick.y[0]] == 'O' or graph[brick.x[0] - 1][brick.y[0]] == 'G') and  (graph[brick.x[0] - 2][brick.y[0]] == 'O' or graph[brick.x[0] - 2][brick.y[0]] == 'G'):          # checking upper child                                                      
                    brickUp = Brick ([],[brick.x[0] - 2,brick.x[0] - 1],  [brick.y[0] , brick.y[0]],brick.gStep + 1, brick, 'S')
                    brick.children.append(brickUp)
                if (brick.x[0] + 1 < len(graph) and brick.x[0] + 2 < len(graph) ) and (graph[brick.x[0] + 1][brick.y[0]] == 'O' or graph[brick.x[0] + 1][brick.y[0]] == 'G') and  (graph[brick.x[0] + 2][brick.y[0]] == 'O' or graph[brick.x[0] + 2][brick.y[0]] == 'G'):          # checking lower child
                    brickDown = Brick ([],[brick.x[0] + 1,brick.x[0] + 2],  [brick.y[0] , brick.y[0]],brick.gStep + 1, brick, 'S')
                    brick.children.append(brickDown) 
                    
      # ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR 
      # ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR 
      # ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR 
      # ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR ASTAR 
            
 
     # UCS ALGORITHM   UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM
     # UCS ALGORITHM   UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM     
     # UCS ALGORITHM   UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM 
     # UCS ALGORITHM   UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM UCS ALGORITHM 
class UCS:
        def __init__ (self, graph,start,goal):
            self.graph = graph
            self.start = start
            self.goal = goal
            
            
        def successor (self,brick):         # Checking successor if it is visitable or not according to horizontiality and verticaliality 
            if brick.isHorizontal():
                if brick.y[0] == brick.y[1]:    # looking down
                    #print ('horizontal')
                    if (brick.y[0] + 1 < len(graph[0]) ) and (graph[brick.x[0]][brick.y[0] + 1] == 'O' or graph[brick.x[0]][brick.y[0] + 1] ==  'G')  and  (graph[brick.x[1]][brick.y[1] + 1] == 'O' or graph[brick.x[1]][brick.y[1] + 1] == 'G') :    # check right child
                        brickRight = Brick ([],[brick.x[0],brick.x[1]],  [brick.y[0] + 1, brick.y[1] + 1],brick.gStep + 1, brick, 'S')                        
                        brick.children.append(brickRight)
                    if (brick.y[0] - 1 >= 0) and (graph[brick.x[0]][brick.y[0] - 1] == 'O' or graph[brick.x[0]][brick.y[0] - 1] == 'G')  and  (graph[brick.x[1]][brick.y[1] - 1] == 'O' or graph[brick.x[1]][brick.y[1] - 1] == 'G') :    # check left child
                        brickLeft = Brick ([],[brick.x[0],brick.x[1]],  [brick.y[0] - 1, brick.y[1] - 1],brick.gStep + 1, brick, 'S')                       
                        brick.children.append(brickLeft)
                    if (brick.x[0] - 1 >= 0) and (graph[brick.x[0] - 1][brick.y[0]] == 'O' or graph[brick.x[0] - 1][brick.y[0]] == 'G') :          # check upper child
                        brickUp = Brick ([],[brick.x[0] - 1],[brick.y[0]],brick.gStep + 1, brick, 'S')                      
                        brick.children.append(brickUp)
                    if (brick.x[1] + 1 < len(graph)) and (graph[brick.x[1] + 1][brick.y[0]] == 'O' or graph[brick.x[1] + 1][brick.y[0]] == 'G'):  # check lower child
                        brickLow = Brick ([],[brick.x[1] + 1],[brick.y[0]],brick.gStep + 1, brick, 'S')                        
                        brick.children.append(brickLow)
                else:   # looking right or left
                    if (brick.x[0] - 1 >= 0) and (graph[brick.x[0] - 1][brick.y[0]] == 'O' or graph[brick.x[0] - 1][brick.y[0]] == 'G')  and (graph[brick.x[1] - 1][brick.y[1]] == 'O' or graph[brick.x[1] - 1][brick.y[1]] == 'G'):    # check up child
                        brickUp = Brick ([],[brick.x[0] - 1,brick.x[1] - 1],  [brick.y[0], brick.y[1]],brick.gStep + 1, brick, 'S')                     
                        brick.children.append(brickUp)
                    if (brick.x[0] + 1 < len(graph) ) and (graph[brick.x[0] + 1][brick.y[0]] == 'O' or graph[brick.x[0] + 1][brick.y[0]] == 'G')  and  (graph[brick.x[1] + 1][brick.y[1]] == 'O' or graph[brick.x[1] + 1][brick.y[1]] == 'G' ) :    # check down child
                        brickDown = Brick ([],[brick.x[0] + 1,brick.x[1] + 1],  [brick.y[0], brick.y[1]],brick.gStep + 1, brick, 'S')
                        brick.children.append(brickDown)
                    if (brick.y[1] + 1 < len(graph[0]))  and (graph[brick.x[1]][brick.y[1] + 1] == 'O' or graph[brick.x[1]][brick.y[1] + 1] == 'G'):   # checking right child
                        brickRight = Brick ([],[brick.x[1]],  [brick.y[1] + 1],brick.gStep + 1, brick, 'S')
                        brick.children.append(brickRight)
                    if (brick.y[0] - 1 >= 0)  and (graph[brick.x[0]][brick.y[0] - 1] == 'O' or graph[brick.x[0]][brick.y[0] - 1] == 'G'):   # checking left child
                        brickLeft = Brick ([],[brick.x[0]],  [brick.y[0] - 1],brick.gStep + 1, brick, 'S')
                        brick.children.append(brickLeft)
            else:
                #print ('vertical')    # vertical shape
                if (brick.y[0] + 1 < len(graph[0]) and brick.y[0] + 2 < len(graph[0])) and (graph[brick.x[0]][brick.y[0] + 1] == 'O' or graph[brick.x[0]][brick.y[0] + 1] == 'G')  and (graph[brick.x[0]][brick.y[0] + 2] == 'O' or graph[brick.x[0]][brick.y[0] + 2] == 'G'):    # checking right child 2 cells
                    brickRight = Brick ([],[brick.x[0],brick.x[0]],  [brick.y[0] + 1, brick.y[0] + 2],brick.gStep + 1, brick, 'S')  
                    brick.children.append(brickRight)
                if (brick.y[0] - 1 >= 0 and brick.y[0] - 2 >= 0) and (graph[brick.x[0]][brick.y[0] - 1] == 'O' or graph[brick.x[0]][brick.y[0] - 1] == 'G')  and (graph[brick.x[0]][brick.y[0] - 2] == 'O' or graph[brick.x[0]][brick.y[0] - 2] == 'G') :      # checking left child
                    brickLeft = Brick ([],[brick.x[0],brick.x[0]],  [brick.y[0] - 2, brick.y[0] - 1],brick.gStep + 1, brick, 'S')
                    brick.children.append(brickLeft)
                if (brick.x[0] - 1 >= 0 and brick.x[0] - 2 >= 0) and (graph[brick.x[0] - 1][brick.y[0]] == 'O' or graph[brick.x[0] - 1][brick.y[0]] == 'G') and  (graph[brick.x[0] - 2][brick.y[0]] == 'O' or graph[brick.x[0] - 2][brick.y[0]] == 'G'):          # checking upper child                                                      
                    brickUp = Brick ([],[brick.x[0] - 2,brick.x[0] - 1],  [brick.y[0] , brick.y[0]],brick.gStep + 1, brick, 'S')
                    brick.children.append(brickUp)
                if (brick.x[0] + 1 < len(graph) and brick.x[0] + 2 < len(graph)) and (graph[brick.x[0] + 1][brick.y[0]] == 'O' or graph[brick.x[0] + 1][brick.y[0]] == 'G') and  (graph[brick.x[0] + 2][brick.y[0]] == 'O' or graph[brick.x[0] + 2][brick.y[0]] == 'G'):          # checking lower child
                    brickDown = Brick ([],[brick.x[0] + 1,brick.x[0] + 2],  [brick.y[0] , brick.y[0]],brick.gStep + 1, brick, 'S')
                    brick.children.append(brickDown)
                    
        def goalState (self,brick):
            if  brick.isHorizontal() == False and graph [brick.x[0]] [brick.y[0]] == 'G':
                return True
            else:
                return False
                  
        def getPath (self,brick):
            if brick == None:
                return
            print ('solution is ',brick.x,brick.y)
            self.getPath(brick.parent)
        
        def inClosed (self,brick,mset):
            if len(mset) == 0:
                return False
            
            for n in mset:
                if brick.x == n.x and brick.y == n.y:
                    return True
            return False
                
        def inQueue (self, brick,queue):
            if len(queue) == 0:
                return False
            for m in queue:
                if m[1].x == brick.x and m[1].y == brick.y:
                    return True
            return False
                
        def inQueueLessThanG (self, brick, queue):
            if len(queue) == 0:
                return False
            for m in queue:
                if m[1].x == brick.x and m[1].y == brick.y and m[1].gStep > brick.gStep:
                    m[1].gStep = brick.gStep
                    m[1].state = 'S'
                    m[1].parent = brick.parent
                    print('Inside inQueueLessThanG')
                    
                    
        def ucs(self, graph, start):
                visited = set() 
                queue = []
                queue.append([0,start])

                while len(queue) > 0:
                    #print ('Queue', queue)
                    cost,node = queue.pop(0)               
                    if self.goalState(node):
                        print (self.getPath(node))
                        return
                    print('Node coordinates:',node.x,node.y, 'Node gstep:', node.gStep)
                    self.successor(node)
                    
                    for n in node.children:
                      print ('N coordinates',n.x,n.y, 'N gstep:', n.gStep)  
                      if self.inClosed(n,visited) == False or self.inQueue(n,queue) == False: 
                          queue.append([n.gStep,n])
                          queue.sort(key=lambda x: x[0])
                      elif self.inQueueLessThanG(n,queue):  
                          i = 0                             # empty statement
                    visited.add(node)
                          
                   
                               
# test  test test test test test test  test test                       


brick = Brick ([],[2,3], [3,3], 0)
ucs = UCS(graph, brick, [4,7])

start = time.clock()
ucs.ucs(graph,brick)
print (time.clock() - start)


brick1 = Brick ([],[2,3],  [3,3], 0,None,None,0)
astar = AStar(graph,brick1,[1,5])

start = time.clock()
astar.astar(graph,brick1)
print (time.clock() - start)



