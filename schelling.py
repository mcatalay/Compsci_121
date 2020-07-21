'''
Schelling Model of Housing Segregation

Program for simulating of a variant of Schelling's model of
housing segregation.  This program takes five parameters:

    filename -- name of a file containing a sample city grid

    R - The radius of the neighborhood: home at Location (i, j) is in
        the neighborhood of the home at Location (k,l)
        if k-R <= i <= k+R and l-R <= j <= l+R

    M threshold - minimum acceptable threshold for ratio of the number
                of similar neighbors to the number of occupied homes
                in a neighborhood for maroon homeowners.

    B threshold - minimum acceptable threshold for ratio of the number
                of similar neighbors to the number of occupied homes
                in a neighborhood for blue homeowners.

    max_steps - the maximum number of passes to make over the city
                during a simulation.

Sample:
  python3 schelling.py --grid_file=tests/a18-sample-grid.txt --r=1 --m_threshold=0.44 --b_threshold=0.70 --max_steps=2
'''

import os
import sys
import click
import utility


def is_satisfied(grid, R, location, M_threshold, B_threshold):
    '''
    Determine whether or not the homeowner at a specific location is satisfied
    using a neighborhood of radius R and specified M and B thresholds.

    Inputs:
        grid: the grid
        R: radius for the neighborhood
        location: a grid location
        M_threshold: lower bound for similarity score for maroon homeowners
        B_threshold: lower bound for similarity score for blue homeowners

    Returns: Boolean
    '''

    assert utility.is_grid(grid), ("The grid argument has the wrong type.  "
                                   "It should be a list of lists of strings "
                                   "with the same number of rows and columns")

    # We recommend adding an assertion to check that the location does
    # not contain an open (unoccupied) home.

    # YOUR CODE HERE
    S = 0
    H = 0
    for i in range(max(location[0]-R,0), min(location[0]+R+1, len(grid))):
        for j in range(max(location[1]-R, 0), min(location[1]+R+1, len(grid))):
            if grid[i][j] == grid[location[0]][location[1]]:
                S +=1
            if grid[i][j] != "O":
                H +=1
    sim_score = S / H

    if grid[location[0]][location[1]] == "M":
        if sim_score >= M_threshold:
            return True
    elif grid[location[0]][location[1]] == "B":
        if sim_score >= B_threshold:
            return True
    # Replace False with correct return value
    return False



# PUT YOUR AUXILIARY FUNCTIONS HERE
def distance_to(poo, poo1):
    '''
    measures distance from one locationo to another on the grid.
    inputs:
        poo: the first location
        poo1: the second location
    returns: a numerical distance in terms of a float
    '''
    distance = ((poo1[0] - poo[0])**2 + (poo1[1] - poo[1])**2)**0.5
    return distance


def dir_neighbor(grid, R, location):
    '''
    counts the number of neighbours inside the radius
    inputs:
        grid:the grid
        R: radius for the neighbourhood
        location: a location inthe grid
    returns: the number of direct neighbours
    '''
    direct_neighbor = 0
    for i in range(max(location[0]-R,0), min(location[0]+R+1, len(grid))):
        for j in range(max(location[1]-R, 0), min(location[1]+R+1, len(grid))):
            if grid[i][j] != "O":
                direct_neighbor += 1
    return direct_neighbor

def swap(grid, org_loc, new_loc):
        '''
        swaps the values at a location with the value at anothers' location.
        inputs:
            grid: the grid
            org_loc: the first location
            new_loc: the second location
        returns: a grid
        '''
        spot1 = grid[new_loc[0]][new_loc[1]]
        spot2 = grid[org_loc[0]][org_loc[1]]

        grid[new_loc[0]][new_loc[1]] = spot2
        grid[org_loc[0]][org_loc[1]] = spot1  

        return grid

def evaluate_open_list(grid, R, location, opens, M_threshold, B_threshold):
    '''
    takes the open list and iterates down it using auxillary functions to find 
    best spot to move to. 
    inputs:
        grid: the grid
        R: the radius
        location: a spot in grid
        opens: list of open locations
        M_threshold: the point that m is no longer satisfied
        b_threshold: the point that b is no longer satisfied 
    returns: the location that passes each tiebreaker, the ideal for swapping. 
    '''
    satisfieds = []
    for i in opens:
        swap(grid, location, i)
        if is_satisfied(grid, R, i, M_threshold, B_threshold) == True:
            satisfieds.append(i)
        swap(grid, location, i)

    if len(satisfieds) == 0:
        bestie = location
    else:
        bestie = satisfieds[0]

    for i in satisfieds:
        if distance_to(location, i) < distance_to(location, bestie):
            bestie= i 
        elif distance_to(location, i) == distance_to(location, bestie):
            if dir_neighbor(grid, R, i) >= dir_neighbor(grid, R, bestie):
                bestie = i
    return bestie


def sim_one(grid, R, opens, M_threshold, B_threshold):
    counts = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if grid[i][j] != "O" and is_satisfied(grid, R, (i,j), M_threshold, B_threshold) == False:
                swap_pos = evaluate_open_list(grid, R, (i,j), opens, M_threshold, B_threshold)
                if swap_pos != (i,j):
                    swap(grid, (i,j), swap_pos)
                    counts += 1
                    opens.remove(swap_pos)
                    opens.append((i,j))
    return counts


# DO NOT REMOVE THE COMMENT BELOW
#pylint: disable-msg=too-many-arguments
def do_simulation(grid, R, M_threshold, B_threshold, max_steps, opens):
    '''
    Do a full simulation.

    Inputs:
        grid: (list of lists of strings) the grid
        R: (int) radius for the neighborhood
        M_threshold: (float) satisfaction threshold for maroon homeowners
        B_threshold: (float) satisfaction threshold for blue homeowners
        max_steps: (int) maximum number of steps to do
        opens: (list of tuples) a list of open locations

    Returns:
        The total number of relocations completed.
    '''

    assert utility.is_grid(grid), ("The grid argument has the wrong type.  "
                                   "It should be a list of lists of strings "
                                   "with the same number of rows and columns")

    # YOUR CODE HERE

    steps = 0
    counts = 0
    while steps < max_steps:
        test = counts
        counts += sim_one(grid, R, opens, M_threshold, B_threshold)
        steps += 1
        print(counts)
        if test == counts:
            print("broke because no change")
            break


    # REPLACE -1 with an appropriate return value
    return counts


@click.command(name="schelling")
@click.option('--grid_file', type=click.Path(exists=True))
@click.option('--r', type=int, default=1, help="neighborhood radius")
@click.option('--m_threshold', type=float, default=0.44, help="M threshold")
@click.option('--b_threshold', type=float, default=0.70, help="B threshold")
@click.option('--max_steps', type=int, default=1)
def run(grid_file, r, m_threshold, b_threshold, max_steps):
    '''
    Put it all together: do the simulation and process the results.
    '''

    if grid_file is None:
        print("No parameters specified...just loading the code")
        return

    grid = utility.read_grid(grid_file)

    if len(grid) < 20:
        print("Initial state of city:")
        for row in grid:
            print(row)
        print()

    opens = utility.find_opens(grid)
    num_relocations = do_simulation(grid, r, m_threshold, b_threshold,
                                    max_steps, opens)
    print("Number of relocations done: " + str(num_relocations))

    if len(grid) < 20:
        print()
        print("Final state of the city:")
        for row in grid:
            print(row)

if __name__ == "__main__":
    run() # pylint: disable=no-value-for-parameter


On Fri, 19 Oct 2018 at 11:45 Mufitcan Atalay <mcatalay97@gmail.com> wrote:

def M_sim_score(grid, R, location):
    S = 1
    H = 1
    for i in range(max(location[0]-R,0), min(location[0]+R+1, len(grid))):
        for j in range(max(location[1]-R, 0), min(location[1]+R+1, len(grid))):
            if grid[i][j] == "M":
                S +=1
            if grid[i][j] != "O":
                H +=1
    sim_score = S / H
    return sim_score


def B_sim_score(grid, R, location, comp):
    S = 1
    H = 1
    for i in range(max(location[0]-R,0), min(location[0]+R+1, len(grid))):
        for j in range(max(location[1]-R, 0), min(location[1]+R+1, len(grid))):
            if grid[i][j] == "B":
                S +=1
            if grid[i][j] != "O":
                H +=1
    if distance_to(location, comp) > R * (2)**0.5:            
        sim_score = S / H
    else:
        sim_score = ((S-1)/H) 
    return sim_score


def sim_one(grid, R, location, M_threshold, B_threshold):
        open_loc = []
        pos_loc = []
        t_sim_score = []
        for i in range(0, len(grid)):
                for j in range(0, len(grid)):
                        if grid[i][j] == "O":
                            open_loc.append((i,j))

        for i in open_loc:
            if grid[location[0]][location[1]] == "M":
                threshold == M_threshold
                t_sim_score.append(M_sim_score(grid, R, i, location))
            if grid[location[0]][location[1]] == "B":
                threshold = B_threshold
                t_sim_score.append(B_sim_score(grid, R, i, location))
                
        #         for m in t_sim_score:
        #             if m >= threshold:
        #                 pos_loc.append(i)
        #                 print(pos_loc)
        #                 if len(pos_loc) == 1:
        #                     switch_to = pos_loc[0]
        #                     swap(grid, location, switch_to)
        #                     open_loc.remove(switch_to)
        #                 else:
        #                     min_dist = min(distance(loc,j))
        #                     pos_loc = [j for j in pos_loc if j != min_dist]
        #                     if len(pos_loc) == 1:
        #                         switch_to = pos_loc[0]
        #                         swap(grid, location, switch_to)
        #                         open_loc.remove(switch_to)
        #                     else:
        #                         max_nbr = max(dir_neighbor(grid,R,k))
        #                         pos_loc = [k for k in posloc if dir_neighbor(grid,R,k) != max_nbr]
        #                         if pos_loc == 1:
        #                             switch_to = pos_loc[0]
        #                             swap(grid, location, switch_to)
        #                             open_loc.remove(switch_to)
        #                         else:
        #                             switch_to = pos_loc[len(pos_loc)]
        #                             swap(grid, location, switch_to)
        #                             open_loc.remove(switch_to)
        # open_loc.append(location)
        return open_loc, t_sim_scoreＨ⤣Ｈ⤣Ｈ⤣Ｈ⤣Ｈ⠢Ｇ⠢Ｇ✡Ｆ✡Ｆ┠Ｄ┠Ｄ⼬Ｏ⼬Ｏ㬷＼㬷＼㬷＼㬷＼㬷＼㬷＼㬷＼㬷＼㬷＼㬷＼㠵Ｙ㠵Ｙ