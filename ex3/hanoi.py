import sys


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file

    # props
    domain_file.write("Propositions:\n")
    for disk in disks:
        for peg in pegs:
            domain_file.write(disk + peg + " " + "not_" + disk + peg + " ")
    domain_file.write("\n")

    # actions
    domain_file.write("Actions:\n")
    for disk_index, disk in enumerate(disks):
        for source_peg in pegs:
            for dest_peg in pegs:
                if source_peg != dest_peg:
                    # name
                    domain_file.write("Name: MOVE_" + disk + source_peg + dest_peg + "\n")

                    # pre
                    domain_file.write("pre: " + disk + source_peg + " ") # disk must be on source peg
                    # smaller disk can't be on source peg
                    for smaller_disk in range(disk_index):  # smaller disk can't be on dest peg
                        domain_file.write("not_d_" + str(smaller_disk) + source_peg + " ")
                    # domain_file.write("\n")

                    for smaller_disk in range(disk_index):  # smaller disk can't be on dest peg
                        domain_file.write("not_d_" + str(smaller_disk) + dest_peg + " ")
                    domain_file.write("\n")

                    # add
                    domain_file.write("add: ")
                    domain_file.write("not_" + disk + source_peg + " ")
                    domain_file.write(disk + dest_peg + "\n")

                    # delete
                    domain_file.write("delete: ")
                    domain_file.write(disk + source_peg + " ")
                    domain_file.write("not_" + disk + dest_peg + "\n")


    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file

    problem_file.write("Initial state: ")
    for disk in disks[::-1]:
        problem_file.write(disk + pegs[0] + " ")
        for peg in pegs[1:]:
            problem_file.write("not_"+disk + peg + " ")
    problem_file.write("\n")

    problem_file.write("Goal state: ")
    for disk in disks[::-1]:
        problem_file.write(disk + pegs[-1] + " ")
        # for peg in pegs[len(pegs) - 2::-1]:
        #     problem_file.write("not_" + disk + peg + " ")

    problem_file.write("\n")



    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
