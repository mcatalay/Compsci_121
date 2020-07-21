'''
Polling places

YOUR NAME(s) HERE

Main file for polling place simulation
'''

import sys
import random
import queue
import click
import util


### YOUR Voter, VoterGenerator, and Precinct classes GO HERE.
#testing function
def generate_and_print(filename):
    poop = util.load_precincts(filename)
    poop1 = poop[0][0]
    poo = Voter_generator(poop1) 
    pee = []
    for i in range(0, poo.num_voters):
        poo.generate_voter()
        pee.append(poo.voter)
    return util.print_voters(pee)





# Voter class
class Voter(object):

    #innitialiser
    def __init__(self, arrival_time, voting_duration):
        self.arrival_time = arrival_time
        self.voting_duration = voting_duration
        self.start_time = None
        self.departure_time =  None

# Voter Generator Class 
class Voter_generator(object):

    #innitialise
    def __init__(self, di, num_voters):
        self.arrival_rate = di["arrival_rate"]
        self.voting_duration_rate = di["voting_duration_rate"]
        self.num_voters = num_voters
        self.time = 0
        self.turnout = 0


    def generate_voter(self):
        gap, voting_duration = util.gen_poisson_voter_parameters(self.arrival_rate, self.voting_duration_rate)
        self.time += gap
        self.turnout += 1
        return Voter(self.time, voting_duration)



#Precinct Class
class Precinct(object):
    def __init__(self, name, num_voters, hours_open, num_booths):
        self.name = name
        self.max_num_voters = num_voters
        self.hours_open = hours_open
        self.num_booths = num_booths
        self.voter_generator = None



    def __booth_avail__(self):
    	if self.__booths.full():
    		return True
    	else:
    		return False
        #if people inside priority queue is less than number of booths than return true
        #otherwise look inside the people in the priority queue
        #find person who will finish earliest
        #return that time
    

    def simulate_precinct(self):
        i_voted = []
        self.__booths = queue.PriorityQueue(self.num_booths)

        while self.voter_generator.turnout < self.max_num_voters:
            next_voter = self.voter_generator.generate_voter()
            if next_voter.arrival_time > self.hours_open*60:
                break
            if self.__booth_avail__():
                next_voter.start_time = max(self.__booths.get()[0], next_voter.arrival_time)

            else:
                next_voter.start_time = next_voter.arrival_time

            next_voter.departure_time = next_voter.start_time + next_voter.voting_duration
            self.__booths.put((next_voter.departure_time, next_voter))
            i_voted.append(next_voter)
                # start of voter is max of departure time of 1st in queue and arrival
                # time (while kicking out the first person in pq)
                                # find their start (arrival time) 
            # departure time (start time plus duration)
            # add them to the queue
            # add them to ivoted
        return i_voted




def simulate_election_day(precincts, seed=0):
    # YOUR CODE HERE.

    # in priority queue store voters. use dep  
    d = {}

    for p in precincts:
        name = p['name']
        num_voters = p['num_voters']
        hours_open = p['hours_open']
        num_booths = p['num_booths']
        voter_distribution = p['voter_distribution']
        p1 = Precinct(name, num_voters, hours_open, num_booths)
        random.seed(seed)
        p1.voter_generator = Voter_generator(voter_distribution, num_voters)
        d[p1.name] = p1.simulate_precinct()


    # REPLACE {} with a diionary mapping precint names
    # to a list of voters for that precinct
    return d


def find_avg_wait_time(precinct, num_booths, ntrials, initial_seed=0):
    # YOUR CODE HERE.
    avg_list = []
    name = precinct['name']
    num_voters = precinct['num_voters']
    hours_open = precinct['hours_open']
    p = Precinct(name, num_voters, hours_open, num_booths)
    for i in range(ntrials):
        p.voter_generator = Voter_generator(precinct["voter_distribution"], precinct["num_voters"])
        random.seed(initial_seed)
        voters = p.simulate_precinct()
        avg_wt = sum([v.start_time - v.arrival_time for v in voters]) / len(voters) #from cmd
        avg_list.append(avg_wt)
        initial_seed += 1

    avg_list.sort()
    median = avg_list[ntrials // 2]
    # REPLACE 0.0 with the waiting time this function computes
    return median


def find_number_of_booths(precinct, target_wait_time, max_num_booths, ntrials, seed=0):
    # YOUR CODE HERE
    # Replace (0,0) with a tuple containing the optimal number of booths
    # and the average waiting time for that number of booths
    for i in range(1, max_num_booths+1):
        wait_time = find_avg_wait_time(precinct, i, ntrials, seed)
        booth_num = i
        if wait_time < target_wait_time:
            break
    if wait_time > target_wait_time:
        booth_num = 0
        wait_time = None


    # Replace (0,0) with a tuple containing the optimal number of booths
    # and the average waiting time for that number of booths

    return (booth_num, wait_time)


# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg= invalid-name, len-as-condition, too-many-locals

@click.command(name="simulate")
@click.argument('precincts_file', type=click.Path(exists=True))
@click.option('--max-num-booths', type=int)
@click.option('--target-wait-time', type=float)
@click.option('--print-voters', is_flag=True)
def cmd(precincts_file, max_num_booths, target_wait_time, print_voters):
    '''
    Run the command.
    '''

    precincts, seed = util.load_precincts(precincts_file)

    if target_wait_time is None:
        voters = simulate_election_day(precincts, seed)
        print()
        if print_voters:
            for p in voters:
                print("PRECINCT '{}'".format(p))
                util.print_voters(voters[p])
                print()
        else:
            for p in precincts:
                pname = p["name"]
                if pname not in voters:
                    print("ERROR: Precinct file specified a '{}' precinct".format(pname))
                    print("       But simulate_election_day returned no such precinct")
                    print()
                    return -1
                pvoters = voters[pname]
                if len(pvoters) == 0:
                    print("Precinct '{}': No voters voted.".format(pname))
                else:
                    pl = "s" if len(pvoters) > 1 else ""
                    closing = p["hours_open"]*60.
                    last_depart = pvoters[-1].departure_time
                    avg_wt = sum([v.start_time - v.arrival_time for v in pvoters]) / len(pvoters)
                    print("PRECINCT '{}'".format(pname))
                    print("- {} voter{} voted.".format(len(pvoters), pl))
                    msg = "- Polls closed at {} and last voter departed at {:.2f}."
                    print(msg.format(closing, last_depart))
                    print("- Avg wait time: {:.2f}".format(avg_wt))
                    print()
    else:
        precinct = precincts[0]

        if max_num_booths is None:
            max_num_booths = precinct["num_voters"]

        nb, avg_wt = find_number_of_booths(precinct, target_wait_time, max_num_booths, 20, seed)

        if nb is 0:
            msg = "The target wait time ({:.2f}) is infeasible"
            msg += " in precint '{}' with {} or fewer booths"
            print(msg.format(target_wait_time, precinct["name"], max_num_booths))
        else:
            msg = "Precinct '{}' can achieve average waiting time"
            msg += " of {:.2f} with {} booths"
            print(msg.format(precinct["name"], avg_wt, nb))
    return 0


if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
