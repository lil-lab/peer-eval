from collections import defaultdict
import pandas as pd
import yaml, argparse, logging
from typing import Set, Dict, List, Tuple
import numpy as np
from yaml import Loader

parser: argparse.ArgumentParser = argparse.ArgumentParser(
    description='Process peer evaluation responses to grades.')
parser.add_argument(
    'metadata',
    help=
    'Gradescope assignment metadata YML file with grouping information. Generate this file by downloading the assignment ZIP file from Gradescope.'
)
parser.add_argument('survey', help='Google Forms survey CSV output.')
parser.add_argument(
    'outputtemplate',
    help=
    'Grades export from Canvas to use as template for the output. Generate this file by exporting the current grades from Canvas.'
)
parser.add_argument('assignment_id', type=int, help='Assignment ID (integer).')
parser.add_argument('output',
                    help='Output CSV file to be imported directly to Canvas.')

args = parser.parse_args()

logging.basicConfig(filename=args.output + '.log',
                    level=logging.DEBUG,
                    filemode='w')

RATINGS: Dict[str, float] = {
    'Excellent': 100,
    'Very good': 87.5,
    'Satisfactory': 75,
    'Ordinary': 62.5,
    'Marginal': 50,
    'Deficient': 37.5,
    'Unsatisfactory': 25,
    'Superficial': 12.5,
    'No show': 0
}

# The score to give when an evaluation is missing.
# All missing evaluation of others get 50.
# If any evaluation is missing, self gets 25.
DEFAULT_PEER_SCORE = 50
DEFAULT_SELF_SCORE = 25

# The points allocated for peer evaluation.
MAX_POINTS = 3

# Get groups from Gradescope meta data.
groups: List[Set[str]] = []
with open(args.metadata) as f:
    metadata = yaml.load(f, Loader=Loader)

for group in metadata.values():
    groups.append(
        set([d[':email'].split('@')[0] for d in group[':submitters']]))

# Read peer eval survey CSV.
with open(args.survey) as f:
    survey = pd.read_csv(f)

STUDENT_NETID = 'Your NetID'
STUDENT_NAME = 'Your Name'
SELF_EVAL = 'Rate Yourself'

P1_NETID = 'Team Member 1: NetID'
P1_EVAL = 'Team Member 1: Rating'

P2_NETID = 'Team Member 2: NetID'
P2_EVAL = 'Team Member 2: Rating'

P3_NETID = 'Team Member 3: NetID'
P3_EVAL = 'Team Member 3: Rating'

P4_NETID = 'Team Member 4: NetID'
P4_EVAL = 'Team Member 4: Rating'

COMMENTS_COL = 'Comments'

NO_NETID_VALUE = 'none'

# Extract evaluation tuples from the spreadsheet.
# Each tuple is (evaluating student NetID, peer NetID, numerical rating)


def rating_to_number(text_rating: str) -> float:
    return RATINGS[text_rating.split(':')[0]]


def is_netid_given(field_value) -> bool:
    return field_value != NO_NETID_VALUE


ratings: Dict[Tuple[str, str], float] = dict()
comments: Dict[str, str] = dict()
student_names: Dict[str, str] = dict()
for index, row in survey.iterrows():
    # Skip the headers row.
    student_id = row[STUDENT_NETID]
    # Get student's name.
    student_names[student_id] = row[STUDENT_NAME]
    # Get student's comments.
    if row[COMMENTS_COL] != '':
        comments[student_id] = row[COMMENTS_COL]
    # Self evaluation.
    ratings[(student_id.lower(),
             student_id.lower())] = rating_to_number(row[SELF_EVAL])
    # Partner 1 evaluation.
    p1_netid = row[P1_NETID]
    if is_netid_given(p1_netid):
        ratings[(student_id.lower(),
                 p1_netid.lower())] = rating_to_number(row[P1_EVAL])
    # Partner 2 evaluation.
    p2_netid = row[P2_NETID]
    if is_netid_given(p2_netid):
        ratings[(student_id.lower(),
                 p2_netid.lower())] = rating_to_number(row[P2_EVAL])
    # Partner 3 evaluation.
    p3_netid = row[P3_NETID]
    if is_netid_given(p3_netid):
        ratings[(student_id.lower(),
                 p3_netid.lower())] = rating_to_number(row[P3_EVAL])
    # Partner 4 evaluation.
    p4_netid = row[P4_NETID]
    if is_netid_given(p4_netid):
        ratings[(student_id.lower(),
                 p4_netid.lower())] = rating_to_number(row[P4_EVAL])

# For each group, compute the score for each student.

teamwork_score: Dict[str, float] = dict()

DEFAULT_BAD_SCORE: int = 0
DEFAULT_GOOD_SCORE: int = 25

# Set of all the students who submitted any feedback.
responded: Set[str] = set(map(lambda x: x[0], ratings.keys()))
logging.debug(f"{len(responded)} students submitted feedback")

for group in groups:
    logging.debug(f"========= {group}")

    # Collect the scores for all group members.
    student_scores: Dict[str, List[float]] = defaultdict(list)
    all_scores: List[float] = list()
    for student in group:
        if student in student_names:
            logging.debug(f"{student} -> {student_names[student]}")
        else:
            logging.debug(f"{student} -> missing name, student didn't submit")
        if student in comments:
            logging.debug(f"[comments] {student}: {comments[student]}")
        missing_eval: bool = False
        for peer in group:
            pair = (student, peer)
            if student == peer and (not student in responded):
                # Self eval for students who skipped the evaluation completely, so  self-eval score as someone who didn't submit properly.
                student_scores[student].append(DEFAULT_BAD_SCORE)
                all_scores.append(DEFAULT_BAD_SCORE)
                logging.debug(
                    f"{student} didn't submit evaluation at all -- self eval is {DEFAULT_BAD_SCORE}"
                )
                if pair in ratings:
                    logging.debug(
                        f"Ignoring self-eval of {ratings[pair]} for {student}")
                    del ratings[pair]
            elif pair in ratings:
                # We have a reported evaluation for this pair, so use it.
                eval_score = ratings.pop(pair)
                logging.debug(f"{pair} -> {eval_score}")
                student_scores[peer].append(eval_score)
                all_scores.append(eval_score)
            elif not peer in responded:
                # We are missing an evaluation pair, and the peer has omissions, so they get teh default bad score.
                logging.debug(
                    f"{pair} -> {DEFAULT_BAD_SCORE} (because peer has omissions)"
                )
                student_scores[peer].append(DEFAULT_BAD_SCORE)
                all_scores.append(DEFAULT_BAD_SCORE)
            else:
                # We are missing an evaluation pair, but peer has reported well, without omissions, so using default good score.
                logging.debug(
                    f"{pair} -> {DEFAULT_GOOD_SCORE} (because peer has no omissions)"
                )
                student_scores[peer].append(DEFAULT_GOOD_SCORE)
                all_scores.append(DEFAULT_GOOD_SCORE)

    logging.debug(student_scores)
    logging.debug(all_scores)

    # The individual rating for a team member is their average quantitative rating, including their own self-rating.
    individual_ratings: Dict[str, float] = dict()
    for student, scores in student_scores.items():
        individual_ratings[student] = sum(scores) / len(scores)
    logging.debug(f"Individual ratings: {individual_ratings}")

    # The team rating is the average of all the quantitative ratings for all team members.
    team_rating = sum(all_scores) / len(all_scores)
    logging.debug(f"Team rating: {team_rating}")

    # The individual adjustment factor (henceforth, factor) is an individual’s rating divided by the team rating. The factor is capped at 1.05.
    factor: Dict[float, float] = dict()
    for student, rating in individual_ratings.items():
        factor[student] = np.min([rating / team_rating, 1.05])
    logging.debug(f"Individual factor: {factor}")

    # The teamwork score is the factor times MAX_POINTS.
    for student, factor in factor.items():
        teamwork_score[student] = factor * MAX_POINTS
        logging.debug(f"{student} teamwork score: {factor * MAX_POINTS}")

# Create a CSV to upload to Canvas.

# Open template CSV (e.g., from grades export).
with open(args.outputtemplate) as f:
    grades_df = pd.read_csv(f)

# Remove all columns except these we need.
grades_df.drop(grades_df.columns.difference(
    ['Student', 'ID', 'SIS User ID', 'SIS Login ID', 'Section']),
               1,
               inplace=True)

# Create a table from the current teamwork data.
teamwork_df = pd.DataFrame(
    teamwork_score.items(),
    columns=['SIS Login ID', f"Assignment {args.assignment_id} Teamwork"])
logging.info(teamwork_df)

# Output warning for all pairs that are not used.
for key, value in ratings.items():
    logging.warning(f"Warning: evaluation pair not used: {key} -> {value}")

# Merge the tables.
merged = grades_df.merge(teamwork_df, how='left', on='SIS Login ID')

with open(args.output, 'w') as f:
    merged.to_csv(f, index=False)
