"""CSV parsing logic for ProsperousPlus"""

import pandas as pd


def parse_csv(args):
    results = pd.read_csv(args.input)
    results = results[results["prediction"] == 1]
    if args.threshold:
        results = results[results["pro"] >= args.threshold]
    if args.protease:
        results = results[results["protease"].isin(args.protease)]
    if args.sequence:
        results = results[results["sequence_id"] == args.sequence]
    results = results.sort_values("pro", ascending = False)
    if args.top:
        results_group = results.groupby("sequence_id")
        results = results_group.head(args.top).sort_values("sequence_id")
    else:
        results = results.sort_values("sequence_id")
    if args.output:
        results.to_csv(args.output)
    print(results)  # noqa: T201
