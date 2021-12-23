# Peer Evaluation Documentation

We will use peer evaluation as part of grading assignments. 
After all deliverables have been submitted, we will ask you to fill out an online form to officially evaluate your teammates. The purpose of this peer evaluation is to evaluate team citizenship, not technical capability.

You will rate each team member, including yourself. These ratings should reflect each individual’s level of participation and effort and their sense of team responsibility. The scale is as follows:

- Excellent: Consistently carried more than their fair share of the workload
- Very good: Consistently did what they were supposed to do, very well prepared and cooperative
- Satisfactory: Usually did what they were supposed to do, acceptably prepared and cooperative
- Ordinary: Often did what they were supposed to do, minimally prepared and cooperative
- Marginal: Sometimes failed to show up or complete assignments, rarely prepared
- Deficient: Often failed to show up or complete assignments, rarely prepared
- Unsatisfactory: Consistently failed to show up or complete assignments, rarely prepared
- Superficial: Practically no participation
- No show: No participation at all

You will also write brief comments to justify your ratings. Your comments will not be revealed to your teammates. Only the professor and perhaps a TA will see your comments.

The ratings you give your peers and yourself will be transformed into a numeric score for each team member. 
Each assignment is worth 13pt. The assignment grading will account for 10pt, and the peer evaluation score will account for 3pt. 
The peer evaluation score is computed on a scale of 20, where 20 equals the complete 3pt. 
The 10pt will be identical for all team members, while the 3pt given for peer evaluation will be individual. 
The ratings you submit will not be directly revealed to your team members, but some function of them will be.

## TL;DR

Just do your best to honestly assess yourself and your teammates. The rating system we are using is robust and works well in practice. It was used in CS 3110. It has also been studied academically; see the citations at the end of the document for details.

The rest of this document describes how scores will be calculated. The details are here as reassurance, rather than because you need to know them. It’s fine to stop reading here.

## Calculation of Scores

Each qualitative rating will be transformed into a quantitative rating as follows:

- Excellent: 100
- Very Good: 87.5
- Satisfactory: 75
- Ordinary: 62.5
- Marginal: 50
- Deficient: 37.5
- Unsatisfactory: 25
- Superficial: 12.5
- No Show: 0

Suppose that a team of three people submits the following ratings:

Name | Vote 1 | Vote 2 | Vote 3
-----|--------|--------|-------
David | 87.5 | 100 | 87.5
Anne | 100 | 100 | 87.5
Michael | 75 | 75 | 75

Each vote was submitted by one of the team members, providing a rating of all three team members (including themself). For example, maybe David submitted vote 2, in which he gives himself and Anne ratings of 100, but gives Michael a score of 75. But, it doesn’t matter who submitted which vote for the calculations we’re about to describe. A four-person team would, of course, have an additional row and an additional column.

The _individual rating_ for a team member is their average quantitative rating, including their own self-rating. These are the individual ratings for our example team:

Name 	| Individual Rating
--------|------------------
David 	| 91.67
Anne 	| 95.83
Michael |	75

The _team rating_ is the average of all the quantitative ratings for all team members. Our example team has nine quantitative ratings, and the average of them is 87.5, so that is the team rating.

The _individual adjustment factor_ (henceforth, factor) is an individual’s rating divided by the team rating. The factor is capped at 1.05. The teamwork score is the factor times 20, rounded to the nearest integer. For our example team, the factors and teamwork scores are as follows:

Name |	Factor |	Score
-----|---------|---------
David |	1.047 |	21
Anne |	1.050 |	21
Michael |	0.857 |	17

That teamwork score is what will be used for the Peer Evaluation component of the grade. Note that it’s possible for some team members to get a small bonus.

## How this Worked in the Past

A similar calculation was used in CS 3110 at Cornell University. It resulted in a mean factor of 1.010 and standard deviation of 0.091. So, only in rather extreme situations would anyone lose more than about 5 points from their teamwork score. We therefore recommend that, instead of trying to overanalyze or game this calculation, you simply fill out the evaluations as honestly as you can.

## Some Examples

Next, we discuss some situations that might arise and how this scoring system handles them.

**Everyone gives the same rating to everyone.** Then everyone gets a teamwork score of 20. For example:

Name  | Vote 1  | Vote 2  | Vote 3  | Individual  | Factor  | Score
------|---------|---------|---------|-------------|---------|------
David  | 75  | 75  | 75  | 75  | 1  | 20
Anne  | 75  | 75  | 75  | 75  | 1  | 20
Michael  | 75  | 75  | 75  | 75  | 1  | 20
   |    |    | Team:  | 75 	  	 | |

Note that it doesn’t matter whether everyone used 75 or 100 or 25 for their votes. As long as everyone agrees, everyone gets the score of 20.

**One person dislikes the rest of the team.** Then the other team members’ scores go down, but not by much.

Name | Vote 1 | Vote 2 | Vote 3 | Individual | Factor | Score
------|---------|---------|---------|-------------|---------|------
David | 100 | 100 | 0 | 66.67 | 0.857 | 17
Anne | 100 | 100 | 0 | 66.67 | 0.857 | 17
Michael | 100 | 100 | 100 | 100 | 1.05 | 21
  |   |   | Team: | 77.78 	  	 | |

Whoever submitted Vote 3 (probably Michael) has caused David and Anne’s scores to go down by 3 points. Out of their final grade in the entire course, this makes little difference.

**The rest of the team dislikes one person.** That person’s score goes down by about half.

Name  | Vote 1  | Vote 2  | Vote 3  | Individual  | Factor  | Score
------|---------|---------|---------|-------------|---------|------
David  | 100  | 100  | 100  | 100  | 1.05  | 21
Anne  | 100  | 100  | 100  | 100  | 1.05  | 21
Michael  | 0  | 0  | 100  | 33.33  | 0.429  | 9
   |    |    | Team:  | 77.78 	  	  | |

It looks like David and Anne don’t like Michael. He loses 11 points. This might be enough to impact his final letter grade, but no more than that. This is an extreme situation, because it makes Michael’s factor go down so low. In such cases, the professor will read (i) the written comments provided by the other team members and (ii) the activity on the GitHub repository to see whether they provide justification for lowering Michael’s score. If the professor thinks the other team members have been too critical, then the professor could raise Michael’s factor.

**The dislike is mutual.** Then the outcome doesn’t change by much.

Name | Vote 1 | Vote 2 | Vote 3 | Individual | Factor | Score
------|---------|---------|---------|-------------|---------|------
David | 100 | 100 | 0 | 66.67 | 1.05 | 21
Anne | 100 | 100 | 0 | 66.67 | 1.05 | 21
Michael | 0 | 0 | 100 | 33.33 | 0.6 | 12
|  |   | Team: | 55.56 	  	 | |

This time Michael dislikes David and Anne, too. Their score remain unchanged; his goes up by a little.

**Team members fail to provide ratings.** If a team member fails to vote, that person’s column will be filled automatically. A zero will imputed to any team member who didn’t vote (including themself), and a 25 to those who did. For example, suppose that Michael failed to vote. Then his vote (#3 below) would be filled in with a 25 for Anne and David and a 0 for himself:

Name | Vote 1 | Vote 2 | Vote 3 | Individual | Factor | Score
------|---------|---------|---------|-------------|---------|------
David | 100 | 100 | 25 | 75 | 1.038 | 21
Anne | 100 | 100 | 25 | 75 | 1.038 | 21
Michael | 100 | 100 | 0 | 66.67 | 0.923 | 18
  |   |   | Team: | 72.22 	  	 | |

This results in about a 10% deduction for Michael.

## Acknowledgments

This evaluation scheme was cloned (with slightly modification) from [CS 3110 at Cornell](https://www.cs.cornell.edu/courses/cs3110/2020sp/proj/peer_eval.html). 
The core of this rating scheme has been examined and found to be highly useful and infrequently problematic in three academic publications:

- R.W. Brown. Autorating: Getting Individual Marks from Team Marks and Enhancing Teamwork. IEEE Frontiers in Education Conference, 1995.
- D.B. Kaufman, R.M. Felder, H.Fuller. Accounting for Individual Effort in Cooperative Learning Teams. J. Engr. Education 89(2): 133-140, 2000.
- B. Oakley, R.M. Felder, R. Brent, I. Elhajj. Turning Student Groups into Effective Teams. J. Student Centered Learning 2(1): 9-34, 2004.

