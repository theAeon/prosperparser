"""Sequence cleaving logic for ProsperParser"""


from pandas import DataFrame

TYPE_CHECKING = False
if TYPE_CHECKING:
    from pyfastx import Sequence

    from .cli import ProsperParser  # noqa: TC004

def search(masterlist, query):
    found_any = False
    newmasterlist = []
    for seq in masterlist:
        target = seq
        a = target.search(query)
        if a is not None:
            found_any = True
        while a is not None:
            newmasterlist.append(target[: a - 1])
            target = target[a + len(query) - 1 :]
            a = target.search(query)
        newmasterlist.append(target)
    return newmasterlist, found_any

def cleave(args: ProsperParser, results: DataFrame) -> list[str]:
    if args.fasta is not None:
        if args.sequence is not None:
            seq: Sequence = args.fasta[args.sequence]
            masterlist = []
            for query in results["seqs"].drop_duplicates().array:
                a = seq.search(query)
                while a is not None:
                    masterlist.append(seq[:a-1])
                    seq = seq[a + len(query) - 1 :]
                    a = seq.search(query)
                masterlist.append(seq)
            to_search = list(results["seqs"].drop_duplicates().array)
            while len(to_search) > 0:
                search_next = to_search.pop()
                masterlist, found_any = search(masterlist, search_next)
                if found_any is True:
                    to_search.reverse()
                    to_search.append(search_next)
                    to_search.reverse()
            for i in range(len(masterlist)):
                masterlist[i] = masterlist[i].seq
            return masterlist
        raise TypeError(args.sequence)
    raise TypeError(args.fasta)
