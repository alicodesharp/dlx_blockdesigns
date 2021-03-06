from functools import reduce
import pyncomb
import dlx


class DesignDLX(dlx.DLX):
    def __init__(self, t, v, k):
        self.t = t
        self.v = v
        self.k = k

        # Populate the columns variable.
        columns = list(pyncomb.ksubsetlex.all(v, t))
        # print(columns)
        # Now create the rows, one for each k-set.
        rows = [[pyncomb.ksubsetlex.rank(v, T) for T in pyncomb.ksubsetlex.all(
            pyncomb.combfuncs.createLookup(S), t)] for S in pyncomb.ksubsetlex.all(v, k)]
        #print(rows)
        #print(len(rows))
        # Add a field to each column to indicate that it is primary.
        dlx.DLX.__init__(self, [(c, dlx.DLX.PRIMARY) for c in columns])
        self.rowsByLexOrder = self.appendRows(rows)

    def printSolution(self, solution):
        return [list(set(reduce(lambda x, y: x + y, self.getRowList(i), []))) for i in solution]


def solutions_list(design):
    (t, v, k) = (design.t, design.v, design.k)
    design_list = list(design.solve())
    new_list = []
    for d in design_list:
        new_list.append(design.printSolution(d))
    print(f"---DESIGN ({v}, {k}, {1}) DONE ---".center(50, "-"))
    print("Number of designs found: %d" % len(design_list))
    r = (v - 1) / (k - 1)
    b = (v * r) / k
    print(f'Design parameters(v,b,r,k,lambda):\nv:{v}, b:{b}, r:{r}, k:{k}, lambda:{1}')
    return new_list


design_731 = DesignDLX(2,7,3)

sol_list_731 = solutions_list(design_731)